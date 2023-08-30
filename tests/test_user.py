import pytest

from tests.conftest import client


def test_get_me_before_login():
    response = client.get("api/users/me")

    assert response.status_code == 401


def test_user_update_before_login():
    response = client.put("api/users/me/update", json={
        "name": "flex_test",
        "email": "flex@gmail.com",
        "photo": "string"
    })

    assert response.status_code == 401


def test_login():
    response = client.post("api/auth/login", json={
        "email": "flex@gmail.com",
        "password": "flex@123"
    })

    assert response.status_code == 200


def test_get_me():
    response = client.get("api/users/me")

    assert response.status_code == 200


def test_user_update():
    response = client.put("api/users/me/update", json={
        "name": "flex_test",
        "email": "flex@gmail.com",
        "photo": "string"
    })

    assert response.status_code == 200


def test_get_reset_password_token_user_doesnt_exist():
    response = client.post("api/users/me/reset_password", json={
        "email": "13223131@gmail.com"
    })

    assert response.status_code == 400


def test_verify_reset_password_token_before_get_token():
    response = client.get("api/users/reset_password/asasasasas")

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid code or user doesn't exist"}


def test_get_reset_password_token():
    response = client.post("api/users/me/reset_password", json={
        "email": "flex@gmail.com"
    })

    assert response.status_code == 200


def test_verify_reset_password_token():
    response = client.get("api/users/reset_password/asasasasas")

    assert response.status_code == 200


def test_change_password_wrong_id():
    response = client.put("api/users/me/change_password", json={
        "user_id": 321213,
        "password": "new_flex@123",
        "passwordConfirm": "new_flex@123"
    })

    assert response.status_code == 403
    assert response.json() == {"detail": "User doesn't exist"}


def test_change_password_wrong_password_validation():
    response = client.put("api/users/me/change_password", json={
        "user_id": 28,
        "password": "new_flex@123",
        "passwordConfirm": "flex@123"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords do not match"}


def test_change_password_validation_error():
    response = client.put("api/users/me/change_password", json={
        "user_id": "dasda",
        "password": "new_flex@123",
        "passwordConfirm": "new_flex@123"
    })

    assert response.status_code == 422


def test_change_password():
    response = client.put("api/users/me/change_password", json={
        "user_id": 28,
        "password": "new_flex@123",
        "passwordConfirm": "new_flex@123"
    })

    assert response.status_code == 200
