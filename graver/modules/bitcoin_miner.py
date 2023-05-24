import json
import random
import string
import time
import threading
import requests
from termcolor import colored
from urllib.parse import urlparse
import datetime
import os



WORDS_FILE_PATH = "words.txt"  # This path might vary based on your OS
SETTINGS_FILE_PATH = "settings.json"
def get_btc_usd():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    price_usd = response.json()['bpi']['USD']['rate_float']
    return price_usd
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def run():
    # Load settings
    with open(SETTINGS_FILE_PATH, 'r') as file:
        settings = json.load(file)

    # Check if webhook is set
    if 'discord_webhook' not in settings or not is_valid_url(settings['discord_webhook']):
        while True:
            webhook = input(colored('[?] Webhook url: ', 'white'))
            if is_valid_url(webhook):
                settings['discord_webhook'] = webhook
                break
            else:
                print(colored("Invalid URL. Please enter a valid URL.", 'red'))


    # Ask user for number of threads
    num_threads = int(input(colored('[?] Number of threads: ', 'white')))

    # Load words
    with open(WORDS_FILE_PATH, 'r') as file:
        words = file.read().splitlines()

    # Start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=generate_addresses, args=(words, settings['discord_webhook']))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    input(colored("\nPress Enter to return to the main menu.\n", 'white'))

def generate_addresses(words, webhook):
    # Generate 5 addresses
    start_time = time.time()
    for i in range(5):
        # Generate random address
        address = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(24, 32)))

        # Generate 20 random words
        random_words = ' '.join(random.choices(words, k=20))

        # Print address and words
        print(colored(f'[INVALID] {address} {random_words}', 'red'))

        # Sleep for a bit to simulate spamming
        time.sleep(0.1)

        # Print line breaks
        print('\n' * 1)

    # Generate a valid address and words
    valid_address = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(24, 32)))
    valid_words = ' '.join(random.choices(words, k=20))

    # Print valid address and words with a [VALID] label
    print(colored(f'[VALID] {valid_address} {valid_words}', 'green'))

    # Send webhook message
    time_taken = time.time() - start_time
    btc = random.uniform(0.001, 0.01)
    btc_usd = btc * get_btc_usd()
    date ="" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SETTINGS_FILE_PATH, 'r') as file:
        settings = json.load(file)
    data = {
        "embeds": [{
            "title": "",
            "fields": [
                {
                    "name": "Bitcoin address",
                    "value": valid_address,
                    "inline": True
                },
                {
                    "name": "Transfered to",
                    "value": settings['bitcoin_address'],
                    "inline": True
                },
                
                {
                    "name": "2FA",
                    "value": "Yes",
                    "inline": True
                },
                {
                    "name": "Current BTC",
                    "value": f"{btc:.3f} BTC ~ {btc_usd:.2f} USD",
                    "inline": True
                },
                {
                    "name": "Generated at",
                    "value": date,
                    "inline": True
                },
                {
                    "name": "Network Fees",
                    "value": f"{random.uniform(0.0001, 0.001):.4f} BTC",
                    "inline": True
                },
                {
                    "name": "Word list",
                    "value": f"```\n{valid_words}\n```",
                    "inline": False
                }
            ],
            "footer": {
            "text": f"Hit achieved in {time_taken:.2f} seconds | made by reverse®"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/emojis/1105165797598449684.webp?size=512&quality=lossless"
        }
        }]
    }
    requests.post(webhook, json=data)
