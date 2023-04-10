import requests
import colorama
import os
from colorama import Fore, Style

colorama.init()

# Check if players.txt file exists, and prompt user to add names if it doesn't
if not os.path.exists('players.txt'):
    with open('players.txt', 'w') as f:
        print("players.txt file created. Please add player names to the file and re-run the program.")
        input("Press ENTER to exit...")
        exit()

players = [line.strip() for line in open('players.txt')]

def to_roman(num):
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = ""
    for i in range(len(values)):
        while num >= values[i]:
            result += symbols[i]
            num -= values[i]
    return result

for player in players:
    url = f'https://pitpanda.rocks/api/players/{player}'
    response = requests.get(url).json()
    if 'data' in response:
        desc = response['data']['inventories']['generalStats'][6]['desc'][0]
        prestige = to_roman(int(desc.split('§a')[1].split('§')[0]))
        status = response['data']['online']
        xp = response['data']['xpProgress']['description'].replace(' XP', '')
        gold = response['data']['goldProgress']['description'].replace(' GOLD', '')
        hourly_xp = response['data']['inventories']['generalStats'][2]['desc'][1].replace('§7', '').replace('§b', '')
        if status:
            print(f"[{prestige}] {player} {Fore.GREEN}online {Fore.BLUE}XP: {xp} {Fore.YELLOW}GOLD: {gold} {Fore.LIGHTBLUE_EX} {hourly_xp}{Style.RESET_ALL}")
        else:
            print(f"[{prestige}] {player} {Fore.RED}offline{Style.RESET_ALL}")
    else:
        status = response.get('status', 'unknown')
        print(f"{Fore.RED}Error accessing URL '{url}' (HTTP {status}) {Style.RESET_ALL}")

input("Press ENTER to exit...")