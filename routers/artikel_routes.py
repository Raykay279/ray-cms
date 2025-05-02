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

    # Hole die ID des neuen Artikels
    neue_id = await database.execute(query)

    # Hole den Artikel inkl. ID aus der DB
    get_query = artikel.select().where(artikel.c.id==neue_id)
    created_article = await database.fetch_one(get_query)

    print(created_article)
    print(Artikel(**dict(created_article)))

    return Artikel(**dict(created_article))

# Alle Artikel abrufen
@router.get("/artikel", response_model=List[Artikel])
async def artikel_abruf():
    query = artikel.select()
    rows = await database.fetch_all(query)

    for row in rows:
        print(dict(row))  # 👈 Debug-Ausgabe ins Terminal

    return [Artikel(**dict(row)) for row in rows]

# Einzelne Artikel abrufen
@router.get("/artikel/{id}", response_model=Artikel)
async def einzelner_artikel_abruf(abruf_id: int):
    query = artikel.select().where(artikel.c.id == abruf_id)
    abgerufener_artikel = await database.fetch_one(query)

    if not abgerufener_artikel:
        raise HTTPException(status_code=404, detail="Kein Artikel mit der Such-ID gefunden")
 
    return Artikel(**dict(abgerufener_artikel))