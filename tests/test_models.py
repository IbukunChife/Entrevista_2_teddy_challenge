import pytest
from app.models import Teddy360
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Teddy360


@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="module")
def session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


def test_create_teddy360(session):
    new_entry = Teddy360(id=1, userId=1, title="delectus aut autem", completed=True)
    session.add(new_entry)
    session.commit()

    entry = session.query(Teddy360).filter_by(id=1).first()
    assert entry is not None
    assert entry.userId == 1
    assert entry.title == "delectus aut autem"
    assert entry.completed is True
