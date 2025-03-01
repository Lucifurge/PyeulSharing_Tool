import requests
import time
import threading
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear_screen():
    os.system('clear')  # For Termux

def display_banner(title):
    console.print(Panel(
        """
█████ █   █ ████ █   █  █       █████ █   █     █    ████  ████   █████  
█    █ █  █ █    █   █  █       █     █████    █ █   █   █ █      █      
█████   █   ██   █   █  █        ██   █   █   █   █  ███   ██      ███   
█      █    ███   ███   ████   ████   █   █  █     █ █  █  ████  █████  
        """,
        title=f"[green]●[yellow] {title} [/]",
        width=65,
        style="bold bright_white",
    ))

def load_cookies():
    clear_screen()
    display_banner("PASTE MULTIPLE TOKENS")
    
    console.print("[yellow]Paste your access tokens (one per line) and press Enter when done:[/yellow]")
    tokens_input = []
    while True:
        line = input().strip()
        if not line:
            break
        tokens_input.append(line)
    
    cookies = [token for token in tokens_input if token.startswith("EAAAA")]
    
    if not cookies:
        console.print("[red]No valid tokens found! Please enter valid access tokens.")
        time.sleep(2)
        return None
    
    return cookies

def share_post(cookie, share_url, share_count):
    url = "https://graph.facebook.com/me/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "link": share_url,
        "privacy": '{"value":"SELF"}',
        "no_story": "true",
        "published": "false",
        "access_token": cookie
    }

    success_count = 0  # Initialize counter

    for i in range(1, share_count * 2 + 1):  # Double share feature
        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            post_id = response_data.get("id", None)

            if post_id:
                success_count += 1  # Increment count on success
                console.print(f"[bold cyan]({success_count}/{share_count * 2})[/bold cyan] [green]Post shared with account: {cookie[:10]}... ✔")
                console.print(f"[cyan]Post ID: {post_id}")
            else:
                console.print(f"[red]({i}/{share_count * 2}) Failed to share post for account {cookie[:10]}: {response_data}")

        except requests.exceptions.RequestException as e:
            console.print(f"[red]({i}/{share_count * 2}) Failed to share post for account {cookie[:10]}: {e}")

        time.sleep(0.5)  # Small delay for processing

    console.print(f"\n[bold cyan]Total successful shares for account {cookie[:10]}: {success_count}[/bold cyan]\n")

def spam_share_multiple():
    clear_screen()
    display_banner("MULTI-COOKIE SPAM SHARE")
    
    cookies = load_cookies()
    if not cookies:
        return
    
    share_url = input("Enter your post link: ").strip()
    try:
        share_count = int(input("Enter Share Count per account: ").strip())
        if share_count <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]Invalid number! Enter a positive integer.")
        time.sleep(2)
        return
    
    threads = []
    for cookie in cookies:
        thread = threading.Thread(target=share_post, args=(cookie, share_url, share_count))
        thread.start()
        threads.append(thread)
        time.sleep(0.25)
    
    for thread in threads:
        thread.join()
    
    console.print("[green]Finished sharing posts from all accounts.")
    input("\n[bold yellow]Press Enter to return to the main menu...[/bold yellow]")

def spam_share_single():
    clear_screen()
    display_banner("SINGLE TOKEN SHARE")
    
    token = input("Enter your Facebook access token: ").strip()
    if not token.startswith("EAAAA"):
        console.print("[red]Invalid token format!")
        time.sleep(2)
        return
    
    share_url = input("Enter your post link: ").strip()
    try:
        share_count = int(input("Enter Share Count: ").strip())
        if share_count <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]Invalid number! Enter a positive integer.")
        time.sleep(2)
        return
    
    share_post(token, share_url, share_count)
    console.print("[green]Finished sharing post.")
    input("\n[bold yellow]Press Enter to return to the main menu...[/bold yellow]")

def main_menu():
    while True:
        clear_screen()
        display_banner("FACEBOOK TOOL")
        console.print(Panel(
            """
[green]1. Multi-Cookie Spam Share
[green]2. Single Token Share
[green]3. Exit
            """,
            width=65,
            style="bold bright_white",
        ))
        choice = input("Select an option: ").strip()

        if choice == "1":
            spam_share_multiple()
        elif choice == "2":
            spam_share_single()
        elif choice == "3":
            console.print("[red]Exiting... Goodbye!")
            break
        else:
            console.print("[red]Invalid choice! Try again.")
            time.sleep(2)

if __name__ == '__main__':
    main_menu()
