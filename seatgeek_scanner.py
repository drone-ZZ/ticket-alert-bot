import time
import requests
from datetime import datetime
try:
    from private_config import DISCORD_WEBHOOK_URL
except ImportError:
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"



# STEP 1: Mock Event + Ticket Data
sample_data = {
    "events": [
        {
            "id": 123456,
            "title": "Dead & Company at the Sphere",
            "datetime_local": "2025-04-18T19:30:00",
        },
        {
            "id": 789012,
            "title": "Dead & Company at the Sphere",
            "datetime_local": "2025-04-19T19:30:00",
        }
    ]
}

sample_listings = {
    123456: [
        {"price": {"amount": "120.00"}, "section": "100", "row": "D", "url": "https://example.com/ticket1"},
        {"price": {"amount": "160.00"}, "section": "200", "row": "F", "url": "https://example.com/ticket2"},
        {"price": {"amount": "140.00"}, "section": "TEST", "row": "Z", "url": "https://example.com/ticket999"}
    ],
    789012: [
        {"price": {"amount": "280.00"}, "section": "102", "row": "B", "url": "https://example.com/ticket3"},
        {"price": {"amount": "320.00"}, "section": "300", "row": "M", "url": "https://example.com/ticket4"}
    ]
}

# STEP 2: Discord Alert Function
def send_discord_alert(ticket_info, webhook_url):
    data = {
        "content": f"""🔥 **New Ticket Found!**
🎟️ {ticket_info['title']} – {ticket_info['date']}
💵 ${ticket_info['price']} – Section {ticket_info['section']}, Row {ticket_info['row']}
🔗 {ticket_info['url']}
"""
    }
    response = requests.post(webhook_url, json=data)
    print(f"Discord Response: {response.status_code} - {response.text}")
    if response.status_code == 204:
        print("✅ Discord alert sent!")
    else:
        print("❌ Failed to send Discord alert.")

# STEP 3: Smart Scanner Loop
def smart_ticket_loop(mock_data, mock_listings, webhook_url, delay=60):
    seen_tickets = set()
    print("🎯 Starting loop. Scanning for new qualifying tickets...\n")

    while True:
        found_new = False

        for event in mock_data["events"]:
            event_id = event["id"]
            title = event["title"]
            date = event["datetime_local"]

            if not (date.startswith("2025-04-18") or date.startswith("2025-04-19")):
                continue

            tickets = mock_listings.get(event_id, [])
            for ticket in tickets:
                price = float(ticket["price"]["amount"])
                section = ticket["section"]
                row = ticket["row"]
                url = ticket["url"]

                max_price = 150 if date.startswith("2025-04-18") else 300

                if price <= max_price and url not in seen_tickets:
                    seen_tickets.add(url)
                    found_new = True

                    print(f"🧪 Found new ticket: ${price} in Section {section}, Row {row}")

                    ticket_info = {
                        "title": title,
                        "date": datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime("%A, %B %d, %Y @ %#I:%M %p"),
                        "price": price,
                        "section": section,
                        "row": row,
                        "url": url
                    }

                    print("📢 Sending alert now...")
                    send_discord_alert(ticket_info, webhook_url)

        if not found_new:
            print("🕒 No new qualifying tickets found. Checking again soon...\n")

        time.sleep(delay)
        print("🔄 Scanning again...\n")

# STEP 4: Start the Scanner (replace with your webhook url up top
smart_ticket_loop(sample_data, sample_listings, DISCORD_WEBHOOK_URL, delay=60)
