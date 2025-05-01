from fastapi import APIRouter, HTTPException
from typing import List
from db.database import database, artikel
from models.artikel import Artikel, ArtikelUpdate

router = APIRouter()

# Artikel erstellen

@router.post("/artikel", response_model=Artikel)
async def add_artikel(new_artikel: Artikel):
    query = artikel.insert(new_artikel).values(
        headline=new_artikel.headline,
        shorttext=new_artikel.shorttext,
        longtext=new_artikel.longtext
    )

    await database.execute(query)
    return new_artikel

# Artikel abrufen
@router.get("/artikel", response_model=List[Artikel])
async def artikel_abruf():
    query = artikel.select()
    return await database.fetch_all(query)