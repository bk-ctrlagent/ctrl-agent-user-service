import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from services.user_service import UserService
from models.User import User

# Fixtures
@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def mock_user():
    return User(
        id=1,
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

# Test verify_password
def test_verify_password():
    password = "test_password"
    hashed_password = UserService.get_password_hash(password)
    assert UserService.verify_password(password, hashed_password) is True
    assert UserService.verify_password("wrong_password", hashed_password) is False

# Test create_access_token
def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = UserService.create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

    # Test with custom expiration
    custom_expire = timedelta(minutes=30)
    token = UserService.create_access_token(data, expires_delta=custom_expire)
    assert isinstance(token, str)
    assert len(token) > 0

# Test create_user
def test_create_user_success(mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    result = UserService.create_user(mock_db, "Test User", "test@example.com", "password123")
    
    assert isinstance(result, User)
    assert result.name == "Test User"
    assert result.email == "test@example.com"
    assert result.password != "password123"  # Password should be hashed
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_create_user_email_exists(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    with pytest.raises(HTTPException) as exc_info:
        UserService.create_user(mock_db, "Test User", "test@example.com", "password123")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email already registered"

# Test authenticate_user
def test_authenticate_user_success(mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    with patch.object(UserService, 'verify_password', return_value=True):
        result = UserService.authenticate_user(mock_db, "test@example.com", "password123")
        assert result == mock_user

def test_authenticate_user_invalid_credentials(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        UserService.authenticate_user(mock_db, "test@example.com", "wrong_password")
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect email or password"

# Test get_user_by_id
def test_get_user_by_id_success(mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    result = UserService.get_user_by_id(mock_db, 1)
    assert result == mock_user

def test_get_user_by_id_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        UserService.get_user_by_id(mock_db, 1)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

# Test update_user
def test_update_user_success(mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    result = UserService.update_user(mock_db, 1, "Updated Name", "updated@example.com", "newpassword")
    
    assert result.name == "Updated Name"
    assert result.email == "updated@example.com"
    assert result.password != "newpassword"  # Password should be hashed
    mock_db.commit.assert_called_once()

# Test delete_user
def test_delete_user_success(mock_db, mock_user):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    
    result = UserService.delete_user(mock_db, 1)
    
    assert result is True
    mock_db.delete.assert_called_once_with(mock_user)
    mock_db.commit.assert_called_once()

# Test get_users
def test_get_users(mock_db, mock_user):
    mock_users = [mock_user]
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_users
    
    result = UserService.get_users(mock_db, skip=0, limit=10)
    
    assert result == mock_users
    mock_db.query.return_value.offset.assert_called_once_with(0)
    mock_db.query.return_value.offset.return_value.limit.assert_called_once_with(10) 