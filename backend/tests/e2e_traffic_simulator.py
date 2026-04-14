import asyncio
import random
import string
from dataclasses import dataclass
from typing import List, Optional

import httpx


BASE_URL = "http://127.0.0.1:8000"


def random_string(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"user_{random_string()}@example.com"


def random_phone() -> str:
    return f"+1{random.randint(2000000000, 9999999999)}"


def random_name() -> str:
    first = random.choice(["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"])
    last = random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"])
    return f"{first} {last}"


def random_message() -> str:
    topics = [
        "I need help with my account login",
        "How do I upgrade my subscription?",
        "The billing page is not loading correctly",
        "Can you explain the pricing plans?",
        "I found a bug in the dashboard",
        "Request for a new feature",
        "Need assistance with API integration",
        "Question about the mobile app",
    ]
    return random.choice(topics)


@dataclass
class TestPayload:
    channel: str
    payload: dict
    customer_identifier: str  # email or phone


async def send_request(client: httpx.AsyncClient, payload: TestPayload) -> tuple[bool, int]:
    url = f"{BASE_URL}/api/v1/webhooks/{payload.channel}"
    try:
        response = await client.post(url, json=payload.payload, timeout=30.0)
        return response.status_code == 201, response.status_code
    except Exception as e:
        return False, 0


async def run_traffic_simulation():
    payloads: List[TestPayload] = []
    
    # Shared identifiers for cross-channel testing
    shared_email = random_email()
    shared_phone = random_phone()
    
    # 10 Web Form requests
    for i in range(10):
        # Make 1st web form use shared email (for Gmail matching)
        # Make 2nd web form use shared phone (for WhatsApp matching)
        if i == 0:
            email = shared_email
            phone = ""
        elif i == 1:
            email = random_email()
            phone = shared_phone
        else:
            email = random_email()
            phone = random.choice([random_phone(), ""])
        
        payloads.append(TestPayload(
            channel="web-form",
            payload={
                "name": random_name(),
                "email": email,
                "phone": phone if phone else None,
                "category": random.choice(["General", "Bug Report", "Feature Request", "Billing"]),
                "priority": random.choice(["low", "medium", "high", "urgent"]),
                "message": random_message()
            },
            customer_identifier=email
        ))
    
    # 5 Gmail requests - first one uses shared email for cross-channel test
    for i in range(5):
        if i == 0:
            sender_email = shared_email
        else:
            sender_email = random_email()
        
        payloads.append(TestPayload(
            channel="gmail",
            payload={
                "sender_email": sender_email,
                "subject": f"Support Request {random_string(4).upper()}",
                "body": random_message()
            },
            customer_identifier=sender_email
        ))
    
    # 5 WhatsApp requests - first one uses shared phone for cross-channel test
    for i in range(5):
        if i == 0:
            phone_number = shared_phone
        else:
            phone_number = random_phone()
        
        payloads.append(TestPayload(
            channel="whatsapp",
            payload={
                "phone_number": phone_number,
                "message": random_message(),
                "name": random_name()
            },
            customer_identifier=phone_number
        ))
    
    # Randomize order
    random.shuffle(payloads)
    
    print(f"\n{'='*60}")
    print(f"E2E TRAFFIC SIMULATOR - Omnichannel Load Test")
    print(f"{'='*60}")
    print(f"Total Requests: {len(payloads)}")
    print(f"  - Web Form: 10")
    print(f"  - Gmail: 5")
    print(f"  - WhatsApp: 5")
    print(f"Cross-Channel Test:")
    print(f"  - Shared Email (web-form <-> gmail): {shared_email}")
    print(f"  - Shared Phone (web-form <-> whatsapp): {shared_phone}")
    print(f"{'='*60}\n")
    
    results = {"success": 0, "failed": 0, "by_channel": {}}
    
    async with httpx.AsyncClient() as client:
        # Send all requests concurrently
        tasks = [send_request(client, p) for p in payloads]
        responses = await asyncio.gather(*tasks)
        
        for payload, (success, status) in zip(payloads, responses):
            channel = payload.channel
            if channel not in results["by_channel"]:
                results["by_channel"][channel] = {"success": 0, "failed": 0}
            
            if success:
                results["success"] += 1
                results["by_channel"][channel]["success"] += 1
            else:
                results["failed"] += 1
                results["by_channel"][channel]["failed"] += 1
    
    # Print summary
    print(f"{'='*60}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total: {results['success'] + results['failed']}")
    print(f"  Succeeded (201 Created): {results['success']}")
    print(f"  Failed: {results['failed']}")
    print(f"\nBy Channel:")
    for channel, counts in results["by_channel"].items():
        total = counts["success"] + counts["failed"]
        print(f"  {channel}: {counts['success']}/{total} succeeded")
    print(f"{'='*60}\n")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_traffic_simulation())