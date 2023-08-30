import hashlib
from random import randbytes

from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import datetime

from pydantic import EmailStr

from src import models, schemas, oauth2, utils
from src.database import get_db
from sqlalchemy.orm import Session

from src.email import Email
from src.schemas import UserEmailSchema

router = APIRouter()


# User profile
@router.get('/me', response_model=schemas.UserResponse)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


# User update
@router.put('/me/update')
def user_update(payload: schemas.UpdateUserSchema, db: Session = Depends(get_db),
                user_id: str = Depends(oauth2.require_user)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    updated_user = user_query.first()
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")
    user_query.update(payload.dict(exclude_unset=True), synchronize_session=False)
    user_query.update({'updated_at': datetime.now()}, synchronize_session=False)
    db.commit()
    return {
        "status": "success",
        "message": "User data was updated successfully"
    }


# Get reset password token
@router.post('/me/reset_password')
async def get_reset_password_token(user_email: UserEmailSchema, request: Request, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user_email.email)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User doesnt exist')
    try:
        # Send Verification Password
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()

        # TESTING
        # verification_code = "asasasasas"
        # TESTING

        user_query.update(
            {'verification_code': verification_code}, synchronize_session=False)
        db.commit()
        url = f"{request.url.scheme}://{request.client.host}:{request.url.port}" \
              f"/api/users/me/reset_password/{token.hex()}"
        # TESTING
        # url = f"{request.url.scheme}://{request.client.host}:{request.url.port}" \
        #       f"/api/users/me/reset_password/{verification_code}"
        # TESTING
        template = 'password_change'
        await Email(user, url, [user.email]).sendVerificationCode(template_name=template)
    except Exception as error:
        print('Error', error)
        user_query.update(
            {'verification_code': None}, synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error sending email')
    return {
        "status": "success",
        "message": "Password verification token successfully sent to your email"}


# Verify user password token
@router.get('/reset_password/{token}')
def verify_reset_password_token(token: str, db: Session = Depends(get_db)):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()
    # TESTING
    # verification_code = "asasasasas"
    # TESTING
    user_query = db.query(models.User).filter(
        models.User.verification_code == verification_code)
    db.commit()
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid code or user doesn't exist")
    user_query.update(
        {'verification_code': None}, synchronize_session=False)
    db.commit()
    return {
        "status": "success",
        "message": "User password token is valid",
        "user_id": user.id,
    }


# Change user password
@router.put('/me/change_password')
def change_password(payload: schemas.UpdateUserPasswordSchema, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == payload.user_id)
    updated_user = user_query.first()
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't exist")
    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    #  Hash the password
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    del payload.user_id
    user_query.update(payload.dict(exclude_unset=True), synchronize_session=False)
    user_query.update({'updated_at': datetime.now()}, synchronize_session=False)
    db.commit()
    return {
        "status": "success",
        "message": "User data was updated successfully"
    }
