from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select, func, extract

from src import models, schemas, oauth2
from src.database import get_db
from sqlalchemy.orm import Session, joinedload

router = APIRouter()


@router.get('/', response_model=List[schemas.CandidateShortSchema])
def get_all_candidates(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    candidates = db.query(
        models.Candidate.id,
        models.Position.title.label("position_title"),
        models.Candidate.status,
        models.Candidate.name,
        models.Candidate.career_site,
        models.Candidate.date_applied,
        models.Candidate.created_by_id
    ).join(models.Candidate.position).filter(models.Candidate.created_by_id == user_id).all()

    result = []
    for candidate in candidates:
        candidate_dict = candidate._asdict()
        result.append(candidate_dict)

    return [candidate for candidate in result]


@router.post('/create_candidate', status_code=status.HTTP_201_CREATED)
def create_candidate(payload: schemas.CandidateCreateSchema, db: Session = Depends(get_db),
                     user_id: str = Depends(oauth2.require_user)):
    try:
        payload.created_by_id = user_id
        candidate = models.Candidate(**payload.dict())
        db.add(candidate)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Candidate was created successfully"
    }


@router.get('/{candidate_id}', response_model=schemas.CandidateFullSchema)
def get_candidate(candidate_id: int, db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    candidate = db.query(
        models.Candidate.id,
        models.Candidate.phone_number,
        models.Candidate.linkedin_link,
        models.Position.title.label("position_title"),
        models.Candidate.status,
        models.Candidate.name,
        models.Candidate.email,
        models.Candidate.github_link,
        models.Candidate.career_site,
        models.Candidate.date_applied,
        models.Candidate.created_by_id
    ).join(models.Candidate.position).filter(models.Candidate.created_by_id == user_id,
                                             models.Candidate.id == candidate_id).first()

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Candidate doesn't exist")

    return candidate


@router.put('/{candidate_id}', status_code=status.HTTP_200_OK)
def update_candidate(candidate_id: int, payload: schemas.CandidateUpdateSchema, db: Session = Depends(get_db),
                     user_id: str = Depends(oauth2.require_user)):
    try:
        candidate = db.query(models.Candidate).filter(models.Candidate.created_by_id == user_id,
                                                      models.Candidate.id == candidate_id)
        updated_candidate = candidate.first()
        if not updated_candidate:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Candidate doesn't exist")
        candidate.update(payload.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Candidate was updated successfully"
    }


@router.patch('/{candidate_id}', status_code=status.HTTP_200_OK)
def update_status_candidate(candidate_id: int, payload: schemas.CandidateUpdateStatusSchema,
                            db: Session = Depends(get_db),
                            user_id: str = Depends(oauth2.require_user)):
    try:
        candidate = db.query(models.Candidate).filter(models.Candidate.created_by_id == user_id,
                                                      models.Candidate.id == candidate_id)
        updated_candidate = candidate.first()
        if not updated_candidate:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Candidate doesn't exist")
        candidate.update(payload.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Candidate status was updated successfully"
    }


@router.get('/today_status/', response_model=List[schemas.CandidateTodaySchema])
def get_all_today_status_candidates(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    today = func.current_date()
    candidates = db.query(
        models.Candidate.id,
        models.Position.title.label("position_title"),
        models.Candidate.name,
        models.Candidate.created_by_id,
        models.Candidate.status
    ).join(models.Candidate.position).filter(models.Candidate.created_by_id == user_id,
                                             models.Candidate.date_applied == today,
                                             models.Candidate.status == "Offer").all()

    result = []
    for candidate in candidates:
        candidate_dict = candidate._asdict()
        result.append(candidate_dict)

    return [candidate for candidate in result]


@router.get('/today_count/')
def get_all_today_count_candidates(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    today = func.current_date()
    count = db.query(func.count(models.Candidate.id)).filter(models.Candidate.created_by_id == user_id,
                                                             models.Candidate.date_applied == today).scalar()

    return {
        "count": count
    }


@router.delete('/{candidate_id}', status_code=status.HTTP_200_OK)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db),
                     user_id: str = Depends(oauth2.require_user)):
    try:
        candidate = db.query(models.Candidate).filter(models.Candidate.created_by_id == user_id,
                                                      models.Candidate.id == candidate_id).first()
        updated_candidate = candidate
        if not updated_candidate:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Candidate doesn't exist")
        db.delete(candidate)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {
        "status": "success",
        "message": "Candidate was deleted successfully"
    }


@router.get('/statistic/', status_code=status.HTTP_200_OK)
def statistic_candidate(method: str, data_start: date, data_end: date, db: Session = Depends(get_db),
                        user_id: str = Depends(oauth2.require_user)):
    total_count = db.query(func.count(models.Candidate.id)).filter(models.Candidate.created_by_id == user_id).scalar()

    offers_count = db.query(func.count(models.Candidate.id)).filter(
        models.Candidate.created_by_id == user_id,
        models.Candidate.status == 'offer',
        models.Candidate.date_applied >= data_start,
        models.Candidate.date_applied <= data_end
    ).scalar()
    offers_percent = (offers_count / total_count) * 100 if total_count else 0

    rejected_count = db.query(func.count(models.Candidate.id)).filter(
        models.Candidate.created_by_id == user_id,
        models.Candidate.status == 'rejected',
        models.Candidate.date_applied >= data_start,
        models.Candidate.date_applied <= data_end
    ).scalar()
    rejected_percent = (rejected_count / total_count) * 100 if total_count else 0

    review_count = db.query(func.count(models.Candidate.id)).filter(
        models.Candidate.created_by_id == user_id,
        models.Candidate.status == 'review',
        models.Candidate.date_applied >= data_start,
        models.Candidate.date_applied <= data_end
    ).scalar()
    review_percent = (review_count / total_count) * 100 if total_count else 0
    offers_percent = round(offers_percent, 2)
    rejected_percent = round(rejected_percent, 2)
    review_percent = round(review_percent, 2)

    return {
        "offers_count": offers_count,
        "offers_percent": offers_percent,
        "rejected_count": rejected_count,
        "rejected_percent": rejected_percent,
        "review_count": review_count,
        "review_percent": review_percent,
    }

# TO DO
