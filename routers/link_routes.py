from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List
from db.database import link, database
from models.link import Link, LinkUpdate, LinkCreate
from auth.security import get_current_user

router = APIRouter()

# Link anlegen
@router.post("/links", response_model=Link)
async def link_anlage(neuer_link: LinkCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nicht berechtigt")

    query = link.insert().values(
        url=neuer_link.url,
        clicktext=neuer_link.clicktext,
        created_at=datetime.utcnow()
    )

    neue_id = await database.execute(query)
    result_query = link.select().where(link.c.id == neue_id)
    erstellter_link = await database.fetch_one(result_query)

    return Link(**dict(erstellter_link))

# Links abrufen
@router.get("/links", response_model=List[Link])
async def links_abrufen(skip: int = 0, limit: int = 100):
    query = link.select().offset(skip).limit(limit)
    rows = await database.fetch_all(query)
    return [Link(**dict(row)) for row in rows]

# Einzelner Link
@router.get("/links/{id}", response_model=Link)
async def einzelner_link(id: int):
    query = link.select().where(link.c.id == id)
    gefundener_link = await database.fetch_one(query)

    if not gefundener_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link nicht gefunden")

    return Link(**dict(gefundener_link))

# Link aktualisieren
@router.put("/links/{id}", response_model=Link)
async def link_aktualisieren(id: int, neuer_link: LinkCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nicht berechtigt")

    query = link.select().where(link.c.id == id)
    vorhandener_link = await database.fetch_one(query)

    if not vorhandener_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link nicht gefunden")

    update_query = link.update().where(link.c.id == id).values(
        url=neuer_link.url,
        clicktext=neuer_link.clicktext,
        created_at=datetime.utcnow()
    )
    await database.execute(update_query)

    result_query = link.select().where(link.c.id == id)
    aktualisierter_link = await database.fetch_one(result_query)

    return Link(**dict(aktualisierter_link))

# Link patchen
@router.patch("/links/{id}", response_model=Link)
async def link_patchen(id: int, link_patch: LinkUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nicht berechtigt")

    query = link.select().where(link.c.id == id)
    vorhandener_link = await database.fetch_one(query)

    if not vorhandener_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link nicht gefunden")

    daten = link_patch.dict(exclude_unset=True)
    update_query = link.update().where(link.c.id == id).values(**daten)
    await database.execute(update_query)

    result_query = link.select().where(link.c.id == id)
    aktualisierter_link = await database.fetch_one(result_query)

    return Link(**dict(aktualisierter_link))

# Link löschen
@router.delete("/links/{id}", response_model=Link)
async def link_loeschen(id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nicht berechtigt")

    query = link.select().where(link.c.id == id)
    vorhandener_link = await database.fetch_one(query)

    if not vorhandener_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link nicht gefunden")

    delete_query = link.delete().where(link.c.id == id)
    await database.execute(delete_query)

    return Link(**dict(vorhandener_link))
