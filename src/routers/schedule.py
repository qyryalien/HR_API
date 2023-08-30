from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from src import models, schemas, oauth2
from src.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/', response_model=List[schemas.ScheduleBaseSchema])
def get_all_schedules(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    try:
        schedules = db.query(models.Schedule).filter(models.Schedule.created_by_id == user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return [schedule for schedule in schedules]


@router.post('/create_schedule', status_code=status.HTTP_201_CREATED)
def create_schedule(payload: schemas.ScheduleBaseSchema, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    try:
        payload.created_by_id = user_id
        schedule = models.Schedule(**payload.dict())
        db.add(schedule)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Schedule was created successfully"
    }


@router.put('/{schedule_id}', status_code=status.HTTP_200_OK)
def update_schedule(schedule_id: int, payload: schemas.ScheduleUpdateSchema, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    try:
        schedule = db.query(models.Schedule).filter(models.Schedule.created_by_id == user_id,
                                                    models.Schedule.id == schedule_id)
        updated_schedule = schedule.first()
        if not updated_schedule:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Schedule doesn't exist")
        schedule.update(payload.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Schedule was updated successfully"
    }


@router.delete('/{schedule_id}', status_code=status.HTTP_200_OK)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db),
                    user_id: str = Depends(oauth2.require_user)):
    try:
        schedule = db.query(models.Schedule).filter(models.Schedule.created_by_id == user_id,
                                                    models.Schedule.id == schedule_id).first()
        updated_schedule = schedule
        if not updated_schedule:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Schedule doesn't exist")
        db.delete(schedule)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Schedule was deleted successfully"
    }

# TO DO
# Sorting by data
