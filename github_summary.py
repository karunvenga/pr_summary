import requests
import argparse
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

def main(args):
    # Set up the basic email properties
    email = EmailMessage()
    email['From'] = args.sender
    email['To'] = args.receiver
    email['Subject'] = 'GitHub Pull Requests Weekly Summary'

    # Define target repository and API URL
    owner = args.owner
    repo = args.repo
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'

    # Set up date range for filtering pull requests
    now = datetime.now()
    last_week = (now - timedelta(days=7)).replace(tzinfo=timezone.utc)

    # Retrieve pull requests
    response = requests.get(url, params={'state': 'all'})
    pull_requests = response.json()

    # Filter pull requests by date
    filtered_pull_requests = [
        pr for pr in pull_requests if datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')) >= last_week
    ]

    # Organize pull requests by state
    opened = [pr for pr in filtered_pull_requests if pr['state'] == 'open']
    closed = [pr for pr in filtered_pull_requests if pr['state'] == 'closed']
    merged = [pr for pr in closed if pr['merged_at'] is not None]

    # Prepare email body
    email_body = f'GitHub Pull Requests Weekly Summary for {owner}/{repo}\n\n'
    email_body += f'From {last_week.strftime("%Y-%m-%d")} to {now.strftime("%Y-%m-%d")}\n\n'
    email_body += f'Opened PRs: {len(opened)}\n'
    email_body += f'Closed PRs: {len(closed)}\n'
    email_body += f'Merged PRs: {len(merged)}\n\n'

    email_body += 'Details:\n\n'

    for pr in filtered_pull_requests:
        email_body += f"Title: {pr['title']}\n"
        email_body += f"URL: {pr['html_url']}\n"
        email_body += f"State: {pr['state']}\n"
        email_body += f"Created At: {pr['created_at']}\n"
        email_body += f"Updated At: {pr['updated_at']}\n"
        email_body += f"Closed At: {pr['closed_at']}\n"
        email_body += f"Merged At: {pr['merged_at']}\n"
        email_body += f"Author: {pr['user']['login']}\n\n"

    email.set_content(email_body)

    # Print email details
    print(f"From: {email['From']}\nTo: {email['To']}\nSubject: {email['Subject']}\n\n{email.get_content()}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a GitHub Pull Requests Weekly Summary.')
    parser.add_argument('--owner', required=True, help='GitHub repository owner')
    parser.add_argument('--repo', required=True, help='GitHub repository name')
    parser.add_argument('--sender', required=True, help='Email sender address')
    parser.add_argument('--receiver', required=True, help='Email receiver address')
    
    args = parser.parse_args()
    main(args)

