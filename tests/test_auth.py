import pytest

from tests.conftest import client


def test_create_user_pass_do_not_match():
    response = client.post("api/auth/register", json={
        "name": "flex",
        "email": "flex@gmail.com",
        "photo": "string",
        "password": "flex@123",
        "passwordConfirm": "flex@124",
        "role": "user",
        "verified": False
    })

    assert response.status_code == 400


def test_create_user():
    response = client.post("api/auth/register", json={
        "name": "flex",
        "email": "flex@gmail.com",
        "photo": "string",
        "password": "flex@123",
        "passwordConfirm": "flex@123",
        "role": "user",
        "verified": False
    })

    assert response.status_code == 201


def test_create_user_existing():
    response = client.post("api/auth/register", json={
        "name": "flex",
        "email": "flex@gmail.com",
        "photo": "string",
        "password": "flex@123",
        "passwordConfirm": "flex@123",
        "role": "user",
        "verified": False
    })

    assert response.status_code == 409


def test_verify_email_token_invalid():
    response = client.get("api/auth/verify_email/qwerty")

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid code or user doesn't exist"}


def test_login_user_not_verified():
    response = client.post("api/auth/login", json={
        "email": "flex@gmail.com",
        "password": "flex@123"
    })

    assert response.status_code == 401


def test_verify_email_token():
    response = client.get("api/auth/verify_email/dadadadada")

    assert response.status_code == 200


def test_verify_email_token_verified_once():
    response = client.get("api/auth/verify_email/qyry")

    assert response.status_code == 403
    assert response.json() == {"detail": "Email can only be verified once"}


def test_login_user_doesnt_exist():
    response = client.post("api/auth/login", json={
        "email": "adadadad@gmail.com",
        "password": "flex@123"
    })

    assert response.status_code == 400


def test_login_user_password_error():
    response = client.post("api/auth/login", json={
        "email": "flex@gmail.com",
        "password": "1231312313"
    })

    assert response.status_code == 400


def test_logout_before_login():
    response = client.get("api/auth/logout")

    assert response.status_code == 401


def test_login():
    response = client.post("api/auth/login", json={
        "email": "flex@gmail.com",
        "password": "flex@123"
    })

    assert response.status_code == 200


def test_refresh_token():
    response = client.get("api/auth/refresh")

    assert response.status_code == 200


def test_logout():
    response = client.get("api/auth/logout")

    assert response.status_code == 200
