from fastapi import FastAPI
from db.database import database
from routers import artikel_routes, user_routes

app = FastAPI()

# Router einbinden
app.include_router(user_routes.router)
app.include_router(artikel_routes.router)

# DB Verbinden
@app.on_event("startup")
async def startup():
    await database.connect()

# DB Verbindung kappen
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()