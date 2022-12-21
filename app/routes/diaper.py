from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/diapers", tags=["Diapers"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Diaper])
async def get_diapers(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):

    diapers = (
        db.query(models.Diaper)
        .filter(models.Diaper.parent_id == current_user.id)
        .filter(models.Diaper.soil_type.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return diapers


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Diaper)
async def create_diaper(
    diaper: schemas.DiaperCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_diaper = models.Diaper(parent_id=current_user.id, **diaper.dict())
    db.add(new_diaper)
    db.commit()
    db.refresh(new_diaper)
    return new_diaper


@router.get(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Diaper,
)
async def get_diaper_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    diaper = db.query(models.Diaper).filter(models.Diaper.id == id).first()

    if not diaper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"diaper with id {id} not found",
        )

    if diaper.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform requested action",
        )

    return diaper


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Diaper)
async def edit_diaper(
    id: int,
    updated_diaper: schemas.DiaperCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    diaper_query = db.query(models.Diaper).filter(models.Diaper.id == id)

    diaper = diaper_query.first()

    if diaper == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"entry with id: {id} does not exist",
        )

    if diaper.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform requested action",
        )

    diaper_query.update(updated_diaper.dict(), synchronize_session=False)

    db.commit()

    return diaper_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diaper(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    diaper_query = db.query(models.Diaper).filter(models.Diaper.id == id)

    diaper = diaper_query.first()

    if diaper == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"entry with id: {id} does not exist",
        )

    if diaper.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform requested action",
        )

    diaper_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
