from fastapi import APIRouter, HTTPException
from typing import List
from db.database import database, artikel
from models.artikel import Artikel, ArtikelUpdate

router = APIRouter()

# Artikel erstellen

@router.post("/artikel", response_model=Artikel)
async def add_artikel(new_artikel: Artikel):
    query = artikel.insert().values(
        headline=new_artikel.headline,
        shorttext=new_artikel.shorttext,
        longtext=new_artikel.longtext
    )

    await database.execute(query)
    return new_artikel

# Alle Artikel abrufen
@router.get("/artikel", response_model=List[Artikel])
async def artikel_abruf():
    query = artikel.select()
    return await database.fetch_all(query)

# Einzelne Artikel abrufen
@router.get("/artikel/{id}", response_model=Artikel)
async def einzelner_artikel_abruf(abruf_id: int):
    query = artikel.select().where(artikel.c.id == abruf_id)
    abgerufener_artikel = database.fetch_one(query)

    if not abgerufener_artikel:
        raise HTTPException(status_code=404, detail="Kein Artikel mit der Such-ID gefunden")
    else:
        return abgerufener_artikel