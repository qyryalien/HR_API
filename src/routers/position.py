from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from src import models, schemas, oauth2
from src.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/', response_model=List[schemas.PositionBaseSchema])
def get_all_positions(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    try:
        positions = db.query(models.Position).filter(models.Position.created_by_id == user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return [position for position in positions]


@router.post('/create_position', status_code=status.HTTP_201_CREATED)
def create_position(payload: schemas.PositionFullSchema, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    try:
        payload.created_by_id = user_id
        position = models.Position(**payload.dict())
        db.add(position)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Position was created successfully"
    }


@router.get('/{position_id}', response_model=schemas.PositionResponse)
def get_position(position_id: int, db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    position = db.query(models.Position).filter(models.Position.created_by_id == user_id,
                                                models.Position.id == position_id).first()
    if position is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Position doesn't exist")
    return position


@router.get('/short_positions/', response_model=List[schemas.PositionShortVariantsSchema])
def get_all_short_positions(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    try:
        positions = db.query(models.Position).filter(models.Position.created_by_id == user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return [position for position in positions]


@router.put('/{position_id}', status_code=status.HTTP_200_OK)
def update_position(position_id: int, payload: schemas.PositionFullSchema, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    try:
        position = db.query(models.Position).filter(models.Position.created_by_id == user_id,
                                                    models.Position.id == position_id)
        updated_position = position.first()
        if not updated_position:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Position doesn't exist")
        position.update(payload.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Position was updated successfully"
    }


@router.delete('/{position_id}', status_code=status.HTTP_200_OK)
def delete_position(position_id: int, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    try:
        position = db.query(models.Position).filter(models.Position.created_by_id == user_id,
                                                    models.Position.id == position_id).first()
        updated_position = position
        if not updated_position:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Position doesn't exist")
        db.delete(position)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Position was deleted successfully"
    }

# TO DO
