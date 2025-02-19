"""
I created this webhook tool after noticing
many skids attempting to spread
RATs and steal information. This is a
simple webhook tool that may have
a few bugs. I havent fixed them
yet, but you can easily do so.
"""

import requests
import time
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(Fore.YELLOW + "\nPress Enter to continue...") #pops up twice dont care

def get_webhook_info(webhook_url):
    response = requests.get(webhook_url)
    if response.status_code == 200:
        webhook_data = response.json()
        return webhook_data.get("name", "Unknown"), webhook_data.get("id", "N/A")
    return "Invalid Webhook", "N/A"

def validate_webhook(webhook_url):
    clear_console()
    response = requests.get(webhook_url)
    if response.status_code == 200:
        print(Fore.GREEN + "Webhook is active and valid!")
    else:
        print(Fore.RED + "Webhook is invalid or deleted.")
    pause()

def modify_webhook(webhook_url, name=None, avatar_url=None):
    clear_console()
    data = {}
    if name:
        data["name"] = name
    if avatar_url:
        data["avatar"] = avatar_url #shit doesnt work womp womp dont care
    
    response = requests.patch(webhook_url, json=data)
    if response.status_code == 200:
        print(Fore.GREEN + "Webhook updated successfully!")
    else:
        print(Fore.RED + f"Failed to update webhook: {response.text}")
    pause()

def send_message(webhook_url, content):
    clear_console()
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(Fore.GREEN + "Message sent successfully!")
    else:
        print(Fore.RED + f"Failed to send message: {response.text}")
    pause()

def edit_message(webhook_url, message_id, new_content):
    clear_console()
    edit_url = f"{webhook_url}/messages/{message_id}"
    data = {"content": new_content}
    response = requests.patch(edit_url, json=data)
    if response.status_code == 200:
        print(Fore.GREEN + "Message edited successfully!")
    else:
        print(Fore.RED + f"Failed to edit message: {response.text}")
    pause()

def spam_messages(webhook_url, content, count, delay):
    clear_console()
    print(Fore.YELLOW + "Spamming started! Press Ctrl+C to stop.")
    try:
        for i in range(count):
            response = requests.post(webhook_url, json={"content": content})
            if response.status_code == 204:
                print(Fore.GREEN + f"Sent message {i + 1}")
            elif response.status_code == 429:
                retry_after = response.json().get("retry_after", 1)
                print(Fore.RED + f"Rate limited! Waiting {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(Fore.RED + f"Failed to send message: {response.text}")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Spamming stopped by user.")
    input(Fore.YELLOW + "\nPress Enter to return to menu...")

def delete_webhook(webhook_url):
    clear_console()
    response = requests.delete(webhook_url)
    if response.status_code == 204:
        print(Fore.GREEN + "Webhook deleted successfully!")
    else:
        print(Fore.RED + f"Failed to delete webhook: {response.text}")
    pause()

if __name__ == "__main__":
    webhook_url = input(Fore.CYAN + "Enter your Discord webhook URL: ")
    while True:
        clear_console()
        webhook_name, webhook_id = get_webhook_info(webhook_url)
        print(Fore.MAGENTA + f"Webhook Name: {webhook_name}")
        print(Fore.MAGENTA + f"Webhook ID: {webhook_id}\n")
        
        print(Fore.BLUE + "Options:")
        print(Fore.CYAN + "1. Validate Webhook")
        print(Fore.CYAN + "2. Modify Webhook (Name/PFP)")
        print(Fore.CYAN + "3. Send Message")
        print(Fore.CYAN + "4. Edit Message")
        print(Fore.CYAN + "5. Spam Messages") 
        print(Fore.CYAN + "6. Delete Webhook")
        print(Fore.CYAN + "7. Exit")
        
        choice = input(Fore.YELLOW + "Choose an option: ")
        
        if choice == "1":
            validate_webhook(webhook_url)
        elif choice == "2":
            name = input(Fore.CYAN + "Enter new webhook name (leave blank to keep current): ")
            avatar_url = input(Fore.CYAN + "Enter new avatar URL (currently broken): ") #currently broken? more like will never be fixed
            modify_webhook(webhook_url, name, avatar_url)
        elif choice == "3":
            content = input(Fore.CYAN + "Enter your message: ")
            send_message(webhook_url, content)
        elif choice == "4":
            message_id = input(Fore.CYAN + "Enter message ID to edit: ")
            new_content = input(Fore.CYAN + "Enter new message content: ")
            edit_message(webhook_url, message_id, new_content)
        elif choice == "5":
            content = input(Fore.CYAN + "Enter spam message content: ")
            count = int(input(Fore.CYAN + "Enter number of messages to send: "))
            delay = float(input(Fore.CYAN + "Enter delay between messages (seconds): ")) #if you read this: 0.2 sec to prevent ratelimit :)
            spam_messages(webhook_url, content, count, delay)
        elif choice == "6":
            confirm = input(Fore.RED + "Are you sure you want to delete the webhook? (yes/no): ") #maybe add "deathmessage"?
            if confirm.lower() == "yes":
                delete_webhook(webhook_url)
        elif choice == "7":
            print(Fore.GREEN + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid option, please try again.")
        
        pause()
