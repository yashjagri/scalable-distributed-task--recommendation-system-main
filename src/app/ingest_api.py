import asyncio
import json
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

#FastAPI is the web framework, HTTPExcpetion is how you return error responses, Request gives you acsess to request headers
#Kafka producer sends messages to kafka and kafka error is the exception type to catch when kafka fails

from . import config, schemas

app = FastAPI(title = 'Event Ingest API') #creates the FASTAPI application instance

@app.on_event("startup") #one time startup function
async def startup_event():
    app.state.producer = None
    app.state.producer_ready = False
    #defensive programming, offering an attribute to kafka even if the connection fails
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            client_id=config.KAFKA_CLIENT_ID,
            acks="all",
        )
        await producer.start()
        # use async and await calls when you are calling something external to the system
        #in this case its just the FastAPI endpoints we are calling
        app.state.producer = producer
        app.state.producer_ready = True
    except Exception:
        pass

#this function, when started, created a kafka producer and connects to kafka
#acks = all means that kafka wont confirm receipt until all brokers have the message

@app.on_event("shutdown")
async def shutdown_event():
    producer = getattr(app.state, "producer", None)
    if producer:
        await producer.flush()
        await producer.stop()

# this runs when the server is stopping

@app.post("/events", response_model=schemas.EventOut, status_code=202) #/events registers this function to handle POST /events. EventOut shape is used here to validate the shape of incoming requests
async def ingest_event(event_in: schemas.EventIn, request: Request):
    producer = getattr(app.state, "producer", None)
    if producer is None or not getattr(app.state, "producer_ready", False):
        raise HTTPException(status_code=503, detail="Producer not ready")

    event_id_str = str(event_in.event_id) if event_in.event_id else str(uuid4())
    ingest_ts = datetime.utcnow().isoformat() + "Z"

    enriched = {
        "event_id": event_id_str,
        "user_id": event_in.user_id,
        "item_id": event_in.item_id,
        "event_type": event_in.event_type.value,
        "metadata": event_in.metadata or {},
        "ingest_ts": ingest_ts,
    }
    message_bytes = json.dumps(enriched).encode("utf-8")
# this converts dicts to bytes since kafka only accpts bytes
    key_bytes = event_id_str.encode("utf-8")
# this code builds the enriched dict from the validated EventIn feilds plust the server-added ingest_ts

    for attempt in range(1, config.PRODUCER_MAX_RETRIES + 1):
        try:
            await producer.send_and_wait(
                config.KAFKA_TOPIC,
                value=message_bytes,
                key=key_bytes,
                timeout=config.PRODUCER_OPERATION_TIMEOUT_SECONDS,
            )
            return JSONResponse(status_code=202, content={"event_id": event_id_str, "status": "accepted"})
        except (KafkaError, asyncio.TimeoutError):
            if attempt == config.PRODUCER_MAX_RETRIES:
                break
            await asyncio.sleep(config.PRODUCER_RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1)))

    raise HTTPException(status_code=503, detail="Failed to publish event")

# ^ this is the actual endpoint, checks if the producedr is ready, generates an event id if there isnt one, builds enriched dict
# then searlizes to JSON bytes and publishes to kafka