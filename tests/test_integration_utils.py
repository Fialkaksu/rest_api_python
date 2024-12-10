# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import MagicMock, AsyncMock
# from sqlalchemy.exc import SQLAlchemyError


# def test_healthchecker_success(client, monkeypatch):
#     # Mock get_db
#     async def mock_get_db():
#         mock_session = MagicMock()
#         mock_session.execute = AsyncMock(
#             return_value=MagicMock(scalar_one_or_none=AsyncMock(return_value=1))
#         )
#         yield mock_session

#     monkeypatch.setattr("src.database.db.get_db", mock_get_db)

#     # healthchecker
#     response = client.get("/api/healthchecker")

#     # Assertions
#     assert response.status_code == 200
#     assert response.json() == {"message": "Welcome to FastAPI!"}


import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from main import app  # Імпортуємо ваш FastAPI додаток
from unittest.mock import AsyncMock
from sqlalchemy.exc import SQLAlchemyError
from src.database.db import get_db


@pytest.fixture
def mock_db_session():
    """Фікстура для мокінгу підключення до бази даних"""
    mock_session = AsyncMock(spec=AsyncSession)
    yield mock_session


@pytest.fixture
def client(mock_db_session):
    """Фікстура для TestClient з мокнутим підключенням до бази"""
    app.dependency_overrides[get_db] = lambda: mock_db_session
    return TestClient(app)


@pytest.mark.asyncio
async def test_healthchecker_success(client, mock_db_session):
    """Тестуємо успішний сценарій, коли база даних підключена коректно"""
    # Мокаємо виконання SQL-запиту
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = 1

    response = client.get("/api/healthchecker")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}


@pytest.mark.asyncio
async def test_healthchecker_database_error(client, mock_db_session):
    """Тестуємо випадок, коли виникає помилка при підключенні до бази даних"""
    mock_db_session.execute.side_effect = SQLAlchemyError("Database error")

    response = client.get("/api/healthchecker")

    assert response.status_code == 500
    assert response.json() == {"detail": "Error connecting to the database"}


# @pytest.mark.asyncio
# async def test_healthchecker_no_result(client, mock_db_session):
#     """Тестуємо випадок, коли запит до бази не повертає результат"""
#     # Мокаємо, що execute поверне об'єкт, у якого scalar_one_or_none верне None
#     mock_result = AsyncMock()
#     mock_result.scalar_one_or_none.return_value = None
#     mock_db_session.execute.return_value = mock_result

#     response = client.get("/api/healthchecker")

#     # Перевіряємо, що повернувся 500 статус код
#     assert response.status_code == 500
#     assert response.json() == {"detail": "Database is not configured correctly"}
