Ticket Alert Bot
A Python-based automation script that helps you track and grab tickets for Dead & Company events (or any event) through SeatGeek. The bot scans for new tickets in your desired price range and sends you alerts through Discord when a match is found.

Goals
Monitor ticket listings for Dead & Company events.

Track price changes and availability for tickets under specific conditions.

Send instant notifications to a Discord channel when a new ticket that matches your criteria is found.

Features
Monitors tickets for Dead & Company at the Sphere (April 18 & 19, 2025).

Price filter to alert only for tickets under $150 (April 18) and under $300 (April 19).

Discord webhook alerts with event details, section, row, and price.

Continuously checks for new tickets and avoids duplicate alerts.

How it Works
Discord Webhook: A Discord webhook is used to send the alert to your chosen channel.

Mock Event Data: The script currently uses mock event data to simulate ticket scanning. To track real tickets, you will need to integrate the SeatGeek API (instructions below).

Smart Loop: The script runs in a loop, continuously checking for new tickets that fit your specified criteria and sending alerts as soon as one is found.

Requirements
Python 3.x

requests library for API calls

Install via pip:
pip install requests

Setup
Clone the repository to your local machine.

Create a private_config.py file to store your Discord Webhook URL:

python
Copy
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-url"
API Key: Currently, the script uses mock data for testing. To get real-time data, you will need to obtain a SeatGeek API key from SeatGeek’s Developer Portal. Once you have the API key, you can integrate it into the script.

Run the script:

bash
Copy
python ticket_scanner.py
Future Features
Integration with SeatGeek API to get real-time data.

Support for more events and flexible ticket filters (e.g., by section, number of tickets).

Option to email alerts in addition to Discord notifications.
