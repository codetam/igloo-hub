import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.api.deps import get_db
from datetime import datetime


@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with the test database"""
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_player(client: TestClient):
    """Fixture that creates a test player and cleans up after the test"""
    data = {"name": "TestPlayer", "nickname": "TP"}
    response = client.post("/api/players", json=data)
    assert response.status_code == 200
    player = response.json()
    
    yield player
    
    client.delete(f"/api/players/{player['id']}")


@pytest.fixture
def test_stadium(client: TestClient):
    """Fixture that creates a test stadium and cleans up after the test"""
    data = {"name": "Test Stadium", "address": "123 Test St"}
    response = client.post("/api/stadiums", json=data)
    assert response.status_code == 200
    stadium = response.json()
    
    yield stadium
    
    client.delete(f"/api/stadiums/{stadium['id']}")


@pytest.fixture
def test_game(client: TestClient, test_stadium):
    """Fixture that creates a test game and cleans up after the test"""
    data = {
        "stadium_id": test_stadium["id"],
        "date": datetime.now().isoformat()
    }
    response = client.post("/api/games", json=data)
    assert response.status_code == 200
    game = response.json()
    
    yield game
    
    client.delete(f"/api/games/{game['id']}")


@pytest.fixture
def multiple_players(client: TestClient):
    """Create multiple test players"""
    players = []
    for i in range(3):
        data = {"name": f"Player{i}", "nickname": f"P{i}"}
        response = client.post("/api/players", json=data)
        assert response.status_code == 200
        players.append(response.json())
    
    yield players
    
    for player in players:
        client.delete(f"/api/players/{player['id']}")