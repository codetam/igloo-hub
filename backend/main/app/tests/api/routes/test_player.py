import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import uuid


@pytest.fixture
def test_player(client: TestClient, session: Session):
    """Fixture that creates a test player and cleans up after the test"""
    
    data = {"name": "TestName", "nickname": "TestNickname"}
    response = client.post("/api/players", json=data)
    assert response.status_code == 200
    player = response.json()
    
    yield player
    
    client.delete(f"/api/players/{player['id']}")


class TestPlayerCRUD:
    """Test Create, Read, Update, Delete operations for players"""
    
    def test_create_player(self, client: TestClient):
        """Test creating a new player"""
        data = {"name": "NewPlayer", "nickname": "NP"}
        response = client.post("/api/players", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == data["name"]
        assert content["nickname"] == data["nickname"]
        assert "id" in content
        assert "profile" in content
        
        client.delete(f"/api/players/{content['id']}")
    
    def test_create_player_without_nickname(self, client: TestClient):
        """Test creating a player without a nickname"""
        data = {"name": "NoNickname"}
        response = client.post("/api/players", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == data["name"]
        assert content["nickname"] is None
        
        client.delete(f"/api/players/{content['id']}")
    
    def test_list_players(self, client: TestClient, test_player):
        """Test listing all players"""
        response = client.get("/api/players")
        
        assert response.status_code == 200
        players = response.json()
        assert isinstance(players, list)
        assert len(players) >= 1
        # Check our test player is in the list
        player_ids = [p["id"] for p in players]
        assert test_player["id"] in player_ids
    
    def test_list_players_with_pagination(self, client: TestClient, test_player):
        """Test listing players with skip and limit"""
        response = client.get("/api/players?skip=0&limit=10")
        
        assert response.status_code == 200
        players = response.json()
        assert isinstance(players, list)
        assert len(players) <= 10
    
    def test_get_player(self, client: TestClient, test_player):
        """Test getting a specific player"""
        response = client.get(f"/api/players/{test_player['id']}")
        
        assert response.status_code == 200
        content = response.json()
        assert content["id"] == test_player["id"]
        assert "stats" in content or "profile" in content
    
    def test_get_player_not_found(self, client: TestClient):
        """Test getting a non-existent player"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/players/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_player_name(self, client: TestClient, test_player):
        """Test updating a player's name"""
        response = client.put(
            f"/api/players/{test_player['id']}",
            params={"name": "UpdatedName"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "UpdatedName"
    
    def test_update_player_nickname(self, client: TestClient, test_player):
        """Test updating a player's nickname"""
        response = client.put(
            f"/api/players/{test_player['id']}",
            params={"nickname": "UpdatedNick"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["nickname"] == "UpdatedNick"
    
    def test_update_player_both_fields(self, client: TestClient, test_player):
        """Test updating both name and nickname"""
        response = client.put(
            f"/api/players/{test_player['id']}",
            params={"name": "NewName", "nickname": "NewNick"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "NewName"
        assert content["nickname"] == "NewNick"
    
    def test_update_player_not_found(self, client: TestClient):
        """Test updating a non-existent player"""
        fake_id = str(uuid.uuid4())
        response = client.put(
            f"/api/players/{fake_id}",
            params={"name": "NewName"}
        )
        
        assert response.status_code == 404
    
    def test_delete_player(self, client: TestClient):
        """Test deleting a player"""
        
        data = {"name": "ToDelete", "nickname": "TD"}
        create_response = client.post("/api/players", json=data)
        player_id = create_response.json()["id"]
        
        response = client.delete(f"/api/players/{player_id}")
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()
        
        get_response = client.get(f"/api/players/{player_id}")
        assert get_response.status_code == 404
    
    def test_delete_player_not_found(self, client: TestClient):
        """Test deleting a non-existent player"""
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/players/{fake_id}")
        
        assert response.status_code == 404
    
    def test_search_players_by_name(self, client: TestClient, test_player):
        """Test searching players by name"""
        
        response = client.get(
            "/api/players/search/by-name",
            params={"name": "Test"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content[0]["name"] == "TestName"
        assert content[0]["nickname"] == "TestNickname"
        
    
    def test_get_player_games_empty(self, client: TestClient, test_player):
        """Test getting games for a player with no games"""
        response = client.get(f"/api/players/{test_player['id']}/games")
        
        assert response.status_code == 200
        games = response.json()
        assert isinstance(games, list)
        assert len(games) == 0
    
    def test_get_player_games_not_found(self, client: TestClient):
        """Test getting games for a non-existent player"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/players/{fake_id}/games")
        
        assert response.status_code == 404