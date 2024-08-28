import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Teddy360
from app.main import fetch_data
from app.models import Teddy360


@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_api_response():
    return [
        {"userId": 1, "id": 1, "title": "delectus aut autem", "completed": False},
        {
            "userId": 1,
            "id": 2,
            "title": "quis ut nam facilis et officia qui",
            "completed": True,
        },
        {"userId": 2, "id": 3, "title": "fugiat veniam minus", "completed": False},
        {"userId": 2, "id": 4, "title": "", "completed": None},
        {
            "userId": 3,
            "id": 5,
            "title": "laboriosam mollitia et enim quasi adipisci quia provident illum",
            "completed": True,
        },
    ]


@patch("requests.get")
def test_fetch_data(mock_get, mock_api_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_api_response

    data = fetch_data()

    assert data[0]["title"] == "delectus aut autem"
    assert data[1]["completed"] is True
    assert data[2]["userId"] == 2


@patch("app.main.fetch_data")
def test_store_data(mock_fetch_data, mock_api_response, session):
    mock_fetch_data.return_value = mock_api_response

    data = mock_fetch_data()

    for item in data:
        if item["completed"]:
            teddy_item = Teddy360(
                id=item["id"],
                userId=item["userId"],
                title=item["title"],
                completed=item["completed"],
            )
            session.merge(teddy_item)

    session.commit()

    stored_data = session.query(Teddy360).all()
    print(stored_data)
    assert len(stored_data) == 2
    assert all(item.title and item.completed is not None for item in stored_data)
