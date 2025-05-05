from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List
from db.database import bild, database
from models.bild import Bild, BildUpdate, BildCreate
from auth.security import get_current_user


router = APIRouter()

# Bild anlegen
@router.post("/bilder", response_model=Bild)
async def bild_anlage(neues_bild: BildCreate, current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=("Nicht berechtigt"))
    
    query = bild.insert().values(
        path=neues_bild.path,
        caption=neues_bild.caption,
        created_at=datetime.utcnow()
    )

    neue_bild = await database.execute(query)

    query = bild.select().where(bild.c.id==neue_bild)
    beste_bild = await database.fetch_one(query)


    return Bild(**dict(beste_bild))

# Bilder abrufen
@router.get("/bilder", response_model=List[Bild])
async def bilder_abrufen(skip: int = 0, limit: int = 100):
    
    # DB Query
    query = bild.select().offset(skip).limit(limit)
    return await database.fetch_all(query)



# Einzelnes Bild abrufen über ID
@router.get("/bilder/{id}", response_model=Bild)
async def bild_abrufen(id: int):

    query = bild.select().where(bild.c.id==id)
    gefundenes_bild = await database.fetch_one(query)

    if not gefundenes_bild:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bild nicht gefunden")

    return Bild(**dict(gefundenes_bild))

# Bild austauschen
@router.put("/bilder/{id}", response_model=Bild)
async def bild_austausch(id: int, neues_bild: BildCreate, current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nicht berechtigt")

    # SUche nach dem Bild
    query = bild.select().where(bild.c.id==id)
    gefundenes_bild = await database.fetch_one(query)

    if not gefundenes_bild:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bild nicht gefunden")
    
    # Bildaustausch
    query = bild.update().where(bild.c.id==id).values(
        path=neues_bild.path,
        caption=neues_bild.caption,
        created_at=datetime.utcnow()
    )

    await database.execute(query)

    query = bild.select().where(bild.c.id==id)
    aktualisiertes_bild = await database.fetch_one(query)

    return Bild(**dict(aktualisiertes_bild))

# Bild patchen
@router.patch("/bilder/{id}", response_model=Bild)
async def bild_patch(id: int, neues_update: BildUpdate, current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nicht berechtigt")
    
    # suche nach bild via iD
    query = bild.select().where(bild.c.id==id)
    gefundenes_bild = await database.fetch_one(query)

    if not gefundenes_bild:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bild nicht gefunden")
    
    # bild patch
    daten = neues_update.dict(exclude_unset=True)
    update_query = bild.update().where(bild.c.id==id).values(**daten)

    await database.execute(update_query)

    result_query = bild.select().where(bild.c.id==id)
    aktualisiertes_bild = await database.fetch_one(result_query)

    return Bild(**dict(aktualisiertes_bild))

# Bild löschen
@router.delete("/bilder/{id}", response_model=Bild)
async def bild_loeschen(id: int, current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nicht berechtigt")

    query = bild.select().where(bild.c.id==id)
    gesuchtes_bild = await database.fetch_one(query)

    if not gesuchtes_bild:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bild nicht gefunden")
    
    query = bild.delete().where(bild.c.id==id)
    await database.execute(query)

    return Bild(**dict(gesuchtes_bild))