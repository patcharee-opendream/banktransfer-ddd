from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table, select
from databases import Database
from sqlalchemy.sql import text

DATABASE_URL = (
    "postgresql://taejai_donation:taejai_donation@localhost:5432/taejai_donation"
)
engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
metadata = MetaData()


# Reflect the donation table
donation = Table("donations", metadata, autoload_with=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/donations/")
async def read_donations():
    query = select([donation])
    result = await database.fetch_all(query)
    return result
