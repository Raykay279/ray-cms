from sqlalchemy import create_engine, MetaData, Column, Table, String, Integer, DateTime
from databases import Database
from datetime import datetime

# DB Pfad
DATABASE_URL = "sqlite:///./database.db"

# DB setup
database = Database(DATABASE_URL)
create_it = create_engine(DATABASE_URL)
metadata = MetaData()

# DB Tables
artikel = Table(
    "artikel",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("headline", String),
    Column("shorttext", String),
    Column("longtext", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

bild = Table(
    "bild",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("path", String),
    Column("caption", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

link = Table(
    "link",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String),
    Column("clicktext", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

usertabelle = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, index=True, unique=True),
    Column("password", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

metadata.create_all(create_it)