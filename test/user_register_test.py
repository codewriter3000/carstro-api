from ..main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_registration():
    response = client.post('/user/create', json={
        'username': 'test_user',
        'password': 'P@ssword123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 201

def test_username_exists():
    client.post('/user/create', json={
        'username': 'test_user1',
        'password': 'P@ssword123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    response = client.post('/user/create', json={
        'username': 'test_user1',
        'password': 'P@ssword123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already exists'}

def test_failed_password():
    response = client.post('/user/create', json={
        'username': 'test_user2',
        'password': 'P@sswor',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == 'Password must be at least 8 characters'

    response = client.post('/user/create', json={
        'username': 'test_user2',
        'password': 'Password123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == 'Password must contain at least 1 special character'

    response = client.post('/user/create', json={
        'username': 'test_user2',
        'password': 'P@ssword',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == 'Password must contain at least 1 number'

    response = client.post('/user/create', json={
        'username': 'test_user2',
        'password': 'p@ssword123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == 'Password must contain at least 1 capital letter'

    response = client.post('/user/create', json={
        'username': 'test_user2',
        'password': 'P@SSWORD123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == 'Password must contain at least 1 lowercase letter'

def test_username_length():
    response = client.post('/user/create', json={
        'username': 'tes',
        'password': 'P@ssword123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username must be between 3 and 20 characters'}

    response = client.post('/user/create', json={
        'username': 'testtesttesttesttesttest',
        'password': 'P@ssword123',
        'first_name': 'Test',
        'last_name': 'User',
    })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username must be between 3 and 20 characters'}
