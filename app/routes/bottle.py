from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/bottles", tags=["Bottles"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Bottle])
async def get_bottles(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    """
    Retrieve bottle log data.

    Parameters
    ----------
    db : Session, optional
        database engine, by default Depends(get_db)
    current_user : int, optional
        logged in user, by default Depends(oauth2.get_current_user)
    limit : int, optional
        query parameter to limit records, by default 10
    offset : int, optional
        query parameter to skip records, by default 0
    search : Optional[str], optional
        search by brand type, by default ""

    Returns
    -------
    dict
        bottle log records from db.
    """
    bottles = (
        db.query(models.Bottle)
        .filter(models.Bottle.parent_id == current_user.id)
        .filter(models.Bottle.brand.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return bottles


@router.get(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Bottle,
)
async def get_bottle(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    bottle = db.query(models.Bottle).filter(models.Bottle.id == id).first()

    if not bottle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"bottle with id {id} not found",
        )

    if bottle.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform requested action",
        )

    return bottle


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Bottle)
async def create_bottle(
    bottle: schemas.BottleCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_bottle = models.Bottle(parent_id=current_user.id, **bottle.dict())
    db.add(new_bottle)
    db.commit()
    db.refresh(new_bottle)
    return new_bottle


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Bottle)
async def edit_bottle(
    id: int,
    updated_bottle: schemas.BottleCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    bottle_query = db.query(models.Bottle).filter(models.Bottle.id == id)

    bottle = bottle_query.first()

    if bottle == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"entry with id: {id} does not exist",
        )

    if bottle.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform requested action",
        )

    bottle_query.update(updated_bottle.dict(), synchronize_session=False)

    db.commit()

    return bottle_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bottle(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    bottle_query = db.query(models.Bottle).filter(models.Bottle.id == id)

    bottle = bottle_query.first()

    if bottle == None:
        raise HTTPException(
            statsu_code=status.HTTP_404_NOT_FOUND,
            detail=f"bottle with id {id} not found",
        )

    if bottle.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform requested action",
        )

    bottle_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
