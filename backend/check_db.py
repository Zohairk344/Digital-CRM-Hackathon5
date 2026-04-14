import asyncio
from sqlalchemy import text
from app.db.database import engine

async def check_linking():
    async with engine.begin() as conn:
        print("\n=== 🧑‍🤝‍🧑 CUSTOMERS TABLE ===")
        customers = await conn.execute(text("SELECT id, email, phone FROM customer"))
        for c in customers:
            print(f"Customer ID: {c.id}\n -> Email: {c.email}\n -> Phone: {c.phone}\n")

        print("=== 🎫 TICKETS TABLE ===")
        tickets = await conn.execute(text("SELECT id, customer_id, channel_origin FROM ticket"))
        for t in tickets:
            print(f"Ticket ID: {t.id}\n -> Belongs to Customer: {t.customer_id}\n -> Channel: {t.channel_origin}\n")
        print("========================\n")

if __name__ == "__main__":
    asyncio.run(check_linking())
