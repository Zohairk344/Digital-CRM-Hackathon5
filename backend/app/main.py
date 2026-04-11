import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.webhooks import web_form
from app.core.kafka_producer import kafka_producer
from app.core.outbox_relay import run_outbox_relay

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start Kafka Producer
    await kafka_producer.start()
    
    # Startup: Start Outbox Relay background task
    relay_task = asyncio.create_task(run_outbox_relay())
    
    yield
    
    # Shutdown: Cancel Outbox Relay task
    relay_task.cancel()
    try:
        await relay_task
    except asyncio.CancelledError:
        pass
    
    # Shutdown: Stop Kafka Producer
    await kafka_producer.stop()

app = FastAPI(
    title="Digital Success Employee API",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(web_form.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Digital Success Employee API"}
