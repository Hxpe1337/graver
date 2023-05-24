import json
import stdiomask
from termcolor import colored

def run():
    # Load settings
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {}

    # Get Discord webhook
    if 'discord_webhook' in settings:
        print(colored(f"Current Discord Webhook: {settings['discord_webhook']}", 'white'))
    else:
        settings['discord_webhook'] = stdiomask.getpass(prompt=colored('[?] Enter Discord Webhook URL: ', 'white'), mask='*')

    # Get Bitcoin address
    if 'bitcoin_address' in settings:
        print(colored(f"Current Bitcoin Address: {settings['bitcoin_address']}", 'white'))
    else:
        settings['bitcoin_address'] = stdiomask.getpass(prompt=colored('[?] Enter Bitcoin Address: ', 'white'), mask='*')

    # Save settings
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

    print(colored("\nSettings saved successfully.\n", 'white'))
    input(colored("\nPress Enter to return to the main menu.\n", 'white'))
