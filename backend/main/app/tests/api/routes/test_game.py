import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import uuid


class TestGameCRUD:
    """Test Create, Read, Update, Delete operations for games"""
    
    def test_create_game(self, client: TestClient, test_stadium):
        """Test creating a new game"""
        data = {
            "stadium_id": test_stadium["id"],
            "date": datetime.now().isoformat()
        }
        response = client.post("/api/games", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert content["stadium"]["id"] == data["stadium_id"]
        assert content["date"] == data["date"]
        assert "id" in content
        assert "home_team" in content
        assert "away_team" in content
        
        client.delete(f"/api/games/{content['id']}")
    
    def test_create_game_future_date(self, client: TestClient, test_stadium):
        """Test creating a game with a future date"""
        future_date = datetime.now() + timedelta(days=7)
        data = {
            "stadium_id": test_stadium["id"],
            "date": future_date.isoformat()
        }
        response = client.post("/api/games", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert content["date"] == future_date.isoformat()
        
        client.delete(f"/api/games/{content['id']}")
    
    def test_list_games(self, client: TestClient, test_game):
        """Test listing all games"""
        response = client.get("/api/games")
        
        assert response.status_code == 200
        games = response.json()
        assert isinstance(games, list)
        assert len(games) >= 1
        
        game_ids = [g["id"] for g in games]
        assert test_game["id"] in game_ids
    
    def test_list_games_with_pagination(self, client: TestClient, test_game):
        """Test listing games with skip and limit"""
        response = client.get("/api/games?skip=0&limit=5")
        
        assert response.status_code == 200
        games = response.json()
        assert isinstance(games, list)
        assert len(games) <= 5
    
    def test_get_game(self, client: TestClient, test_game):
        """Test getting a specific game"""
        response = client.get(f"/api/games/{test_game['id']}")
        
        assert response.status_code == 200
        content = response.json()
        assert content["id"] == test_game["id"]
        assert content["stadium"]["id"] == test_game["stadium"]["id"]
    
    def test_get_game_not_found(self, client: TestClient):
        """Test getting a non-existent game"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/games/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_delete_game(self, client: TestClient, test_stadium):
        """Test deleting a game"""
        
        data = {
            "stadium_id": test_stadium["id"],
            "date": datetime.now().isoformat()
        }
        create_response = client.post("/api/games", json=data)
        game_id = create_response.json()["id"]
        
        response = client.delete(f"/api/games/{game_id}")
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()
        
        get_response = client.get(f"/api/games/{game_id}")
        assert get_response.status_code == 404
    
    def test_delete_game_not_found(self, client: TestClient):
        """Test deleting a non-existent game"""
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/games/{fake_id}")
        
        assert response.status_code == 404


class TestGameLifecycle:
    """Test game start/end lifecycle"""
    
    def test_start_game(self, client: TestClient, test_game):
        """Test starting a game"""
        response = client.put(f"/api/games/{test_game['id']}/start")
        
        assert response.status_code == 200
        content = response.json()
        assert content["started_at"] is not None
        assert content["ended_at"] is None
    
    def test_start_game_twice(self, client: TestClient, test_game):
        """Test that starting a game twice fails"""
        client.put(f"/api/games/{test_game['id']}/start")
        
        response = client.put(f"/api/games/{test_game['id']}/start")
        
        assert response.status_code == 400
        assert "already started" in response.json()["detail"].lower()
    
    def test_start_game_not_found(self, client: TestClient):
        """Test starting a non-existent game"""
        fake_id = str(uuid.uuid4())
        response = client.put(f"/api/games/{fake_id}/start")
        
        assert response.status_code == 404
    
    def test_end_game(self, client: TestClient, test_game):
        """Test ending a game"""
        client.put(f"/api/games/{test_game['id']}/start")
        
        response = client.put(f"/api/games/{test_game['id']}/end")
        
        assert response.status_code == 200
        content = response.json()
        assert content["started_at"] is not None
        assert content["ended_at"] is not None
    
    def test_end_game_not_started(self, client: TestClient, test_game):
        """Test that ending a game that hasn't started fails"""
        response = client.put(f"/api/games/{test_game['id']}/end")
        
        assert response.status_code == 400
        assert "not started" in response.json()["detail"].lower()
    
    def test_end_game_twice(self, client: TestClient, test_game):
        """Test that ending a game twice fails"""
        client.put(f"/api/games/{test_game['id']}/start")
        client.put(f"/api/games/{test_game['id']}/end")
        
        # Try to end again
        response = client.put(f"/api/games/{test_game['id']}/end")
        
        assert response.status_code == 400
        assert "already ended" in response.json()["detail"].lower()
    
    def test_end_game_not_found(self, client: TestClient):
        """Test ending a non-existent game"""
        fake_id = str(uuid.uuid4())
        response = client.put(f"/api/games/{fake_id}/end")
        
        assert response.status_code == 404


class TestGamePlayers:
    """Test adding players to games"""
    
    def test_add_player_to_game(self, client: TestClient, test_game, test_player):
        """Test adding a player to a game"""
        data = {
            "player_id": test_player["id"],
            "team_id": test_game["home_team"]["id"]
        }
        response = client.post(f"/api/games/{test_game['id']}/players", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert "added" in content["message"].lower()
        assert test_player["name"] in content["message"]
    
    def test_add_player_to_game_invalid_game(self, client: TestClient, test_player):
        """Test adding a player to a non-existent game"""
        fake_game_id = str(uuid.uuid4())
        fake_team_id = str(uuid.uuid4())
        data = {
            "player_id": test_player["id"],
            "team_id": fake_team_id
        }
        response = client.post(f"/api/games/{fake_game_id}/players", json=data)
        
        assert response.status_code == 404
    
    def test_add_player_to_game_invalid_player(self, client: TestClient, test_game):
        """Test adding a non-existent player to a game"""
        fake_player_id = str(uuid.uuid4())
        data = {
            "player_id": fake_player_id,
            "team_id": test_game["home_team"]["id"]
        }
        response = client.post(f"/api/games/{test_game['id']}/players", json=data)
        
        assert response.status_code == 404


class TestGameGoals:
    """Test recording goals in games"""
    
    def test_add_goal(self, client: TestClient, test_game, test_player):
        """Test recording a goal"""
        # First add player to game
        gameplayer_data = {
            "player_id": test_player["id"],
            "team_id": test_game["home_team"]["id"]
        }
        client.post(f"/api/games/{test_game['id']}/players", json=gameplayer_data)
        
        # Record a goal
        goal_minute = (datetime.fromisoformat(test_game["date"]) + timedelta(minutes=15)).isoformat()
        goal_data = {
            "team_id": test_game["home_team"]["id"],
            "scorer_id": test_player["id"],
            "minute": goal_minute
        }
        response = client.post(f"/api/games/{test_game['id']}/goals", json=goal_data)
        
        assert response.status_code == 200
        content = response.json()
        assert "goal recorded" in content["message"].lower()
    
    def test_add_goal_with_assister(self, client: TestClient, test_game, multiple_players):
        """Test recording a goal with an assist"""
        scorer = multiple_players[0]
        assister = multiple_players[1]
        
        # Add both players to game
        for player in [scorer, assister]:
            gameplayer_data = {
                "player_id": player["id"],
                "team_id": test_game["home_team"]["id"]
            }
            client.post(f"/api/games/{test_game['id']}/players", json=gameplayer_data)
        
        # Record a goal with assist
        goal_minute = (datetime.fromisoformat(test_game["date"]) + timedelta(minutes=30)).isoformat()
        goal_data = {
            "team_id": test_game["home_team"]["id"],
            "scorer_id": scorer["id"],
            "assister_id": assister["id"],
            "minute": goal_minute
        }
        response = client.post(f"/api/games/{test_game['id']}/goals", json=goal_data)
        
        assert response.status_code == 200
    
    def test_add_goal_invalid_game(self, client: TestClient, test_player):
        """Test recording a goal for a non-existent game"""
        fake_game_id = str(uuid.uuid4())
        fake_team_id = str(uuid.uuid4())
        goal_data = {
            "team_id": fake_team_id,
            "scorer_id": test_player["id"]
        }
        response = client.post(f"/api/games/{fake_game_id}/goals", json=goal_data)
        
        assert response.status_code == 404
    
    def test_add_goal_invalid_player(self, client: TestClient, test_game):
        """Test recording a goal for a non-existent player"""
        fake_player_id = str(uuid.uuid4())
        goal_minute = (datetime.fromisoformat(test_game["date"]) + timedelta(minutes=30)).isoformat()
        goal_data = {
            "team_id": test_game["home_team"]["id"],
            "scorer_id": fake_player_id,
            "minute": goal_minute
        }
        response = client.post(f"/api/games/{test_game['id']}/goals", json=goal_data)
        
        assert response.status_code == 404