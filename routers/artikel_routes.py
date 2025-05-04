from fastapi import APIRouter, HTTPException
from typing import List
from db.database import database, artikel
from models.artikel import Artikel, ArtikelUpdate, ArtikelCreate
from datetime import datetime

router = APIRouter()

# Artikel erstellen

@router.post("/artikel", response_model=ArtikelCreate)
async def add_artikel(new_artikel: ArtikelCreate):
    query = artikel.insert().values(
        headline=new_artikel.headline,
        shorttext=new_artikel.shorttext,
        longtext=new_artikel.longtext,
        created_at=datetime.utcnow()
    )

    await database.execute(query)

    return new_artikel

# Alle Artikel abrufen
@router.get("/artikel", response_model=List[Artikel])
async def artikel_abruf(skip: int = 0, limit: int = 100):
    query = artikel.select().offset(skip).limit(limit)
    rows = await database.fetch_all(query)

    return [Artikel(**dict(row)) for row in rows]

# Einzelne Artikel abrufen
@router.get("/artikel/{id}", response_model=Artikel)
async def einzelner_artikel_abruf(abruf_id: int):
    query = artikel.select().where(artikel.c.id == abruf_id)
    abgerufener_artikel = await database.fetch_one(query)

    if not abgerufener_artikel:
        raise HTTPException(status_code=404, detail="Kein Artikel mit der Such-ID gefunden")
 
    return Artikel(**dict(abgerufener_artikel))

# Artikel aktualisieren
@router.put("/artikel/{id}", response_model=Artikel)
async def austausch_artikel(id: int, artikel_neu: Artikel):
    
    # Artikel suchen
    query = artikel.select().where(artikel.c.id == id)
    betroffener_artikel = await database.fetch_one(query)

    # Falls nicht gefunden
    if not betroffener_artikel:
        raise HTTPException(status_code=404, detail="Kein Artikel unter der ID gefunden")
    
    # Artikel austauschen
    query = artikel.update().where(artikel.c.id == id).values(
        shorttext = artikel_neu.shorttext,
        longtext = artikel_neu.longtext,
        headline = artikel_neu.headline
    )
    await database.execute(query)

    return artikel_neu

# Artikel teilweise aktualisieren
@router.patch("/artikel/{id}", response_model=Artikel)
async def patch_artikel(id: int, artikel_neu: ArtikelUpdate):
    
    # Artikel suchen
    query = artikel.select().where(artikel.c.id == id)
    betroffener_artikel = await database.fetch_one(query)

    # Falls nicht gefunden
    if not betroffener_artikel:
        raise HTTPException(status_code=404, detail="Kein Artikel unter der ID gefunden")
    
    # Update Daten dicten
    daten = artikel_neu.dict(exclude_unset=True)
    
    # Artikel austauschen
    update_query = artikel.update().where(artikel.c.id == id).values(**daten)
    await database.execute(update_query)

    # Artikel zurückgeben
    return_query = artikel.select().where(artikel.c.id == id)
    aktualisierter_artikel = await database.fetch_one(return_query)
    
    return Artikel(**dict(aktualisierter_artikel))

# Artikel löschen
@router.delete("/artikel/{id}", response_model=Artikel)
async def delete_artikel(id: int):

    #Treffer suchen
    query = artikel.select().where(artikel.c.id == id)
    betroffener_artikel = await database.fetch_one(query)

    if not betroffener_artikel:
        raise HTTPException(status_code=404, detail=("Artikel mit gesuchter ID nicht gefunden"))

    delete_query = artikel.delete().where(artikel.c.id == id)
    await database.execute(delete_query)

    return Artikel(**dict(betroffener_artikel))