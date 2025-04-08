# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import smtplib
from email.message import EmailMessage

# === Auto-disable after event ===
end_date = datetime(2025, 4, 21)
if datetime.now() > end_date:
    print("🛑 Scanner stopped: show has passed.")
    exit(0)


try:
    from private_config import (
        DISCORD_WEBHOOK_URL,
        SEATGEEK_CLIENT_ID,
        SEATGEEK_CLIENT_SECRET,
        EMAIL_ADDRESS,
        EMAIL_PASSWORD,
        EMAIL_RECIPIENT
    )
except ImportError:
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
    SEATGEEK_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
    SEATGEEK_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
    EMAIL_ADDRESS = "your_email@example.com"
    EMAIL_PASSWORD = "your_password"
    EMAIL_RECIPIENT = "recipient_email@example.com"


# STEP 1: Fetch events from SeatGeek
def fetch_seatgeek_events():
    url = "https://api.seatgeek.com/2/events"
    params = {
        "client_id": SEATGEEK_CLIENT_ID,
        "client_secret": SEATGEEK_CLIENT_SECRET,
        "performers.slug": "dead-company",
        "venue.slug": "sphere-las-vegas",
        "datetime_local.gte": "2025-04-18T00:00:00",
        "datetime_local.lte": "2025-04-19T23:59:59",
        "per_page": 100
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching SeatGeek data: {response.status_code} - {response.text}")
        return []

    return response.json().get("events", [])


# STEP 2: Send Discord Alert
def send_discord_alert(ticket_info, webhook_url):
    data = {
        "content": f"""🔥 **New Ticket Found!**\n🎟️ {ticket_info['title']} – {ticket_info['date']}\n💵 ${ticket_info['price']} (Lowest Listed)\n🔗 {ticket_info['url']}\n"""
    }
    response = requests.post(webhook_url, json=data)
    print(f"Discord Response: {response.status_code} - {response.text}")
    if response.status_code == 204:
        print("✅ Discord alert sent!")
    else:
        print("❌ Failed to send Discord alert.")


# STEP 3: Send Email Alert
def send_email_alert(ticket_info):
    msg = EmailMessage()
    msg['Subject'] = f"New Ticket Alert: {ticket_info['title']}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_RECIPIENT
    msg.set_content(f"""
New Ticket Found!

Event: {ticket_info['title']}
Date: {ticket_info['date']}
Price: ${ticket_info['price']}
Link: {ticket_info['url']}
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✉️ Email alert sent!")
    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")


# STEP 4: One-time Ticket Scan
def single_ticket_scan(webhook_url):
    seen_event_urls = set()
    emailed_event_urls = set()
    print("🎯 Running single scan for qualifying tickets...\n")

    events = fetch_seatgeek_events()

    for event in events:
        event_id = event["id"]
        title = event["title"]
        date = event["datetime_local"]
        url = event["url"]
        stats = event.get("stats", {})
        price = stats.get("lowest_price")

        if not price:
            continue

        if not (date.startswith("2025-04-18") or date.startswith("2025-04-19")):
            continue

        max_price = 150 if date.startswith("2025-04-18") else 300

        if price <= max_price and url not in seen_event_urls:
            seen_event_urls.add(url)

            print(f"🧪 Found new ticket: ${price} for {title}")

            ticket_info = {
                "title": title,
                "date": datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime("%A, %B %d, %Y @ %#I:%M %p"),
                "price": price,
                "url": url,
            }

            print("📢 Sending Discord alert...")
            send_discord_alert(ticket_info, webhook_url)

            if url not in emailed_event_urls:
                print("📧 Sending email alert...")
                send_email_alert(ticket_info)
                emailed_event_urls.add(url)

    print("🔚 Scan complete.")


# STEP 5: Run One-Time Scan
single_ticket_scan(DISCORD_WEBHOOK_URL)
