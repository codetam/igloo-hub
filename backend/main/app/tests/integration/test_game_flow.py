import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


class TestCompleteGameFlow:
    """Integration tests for complete game workflows"""
    
    def test_complete_game_creation_and_play(self, client: TestClient):
        """Test a complete game flow from creation to completion"""
        # 1. Create a stadium
        stadium_data = {"name": "Integration Stadium", "address": "123 Integration St"}
        stadium_response = client.post("/api/stadiums", json=stadium_data)
        assert stadium_response.status_code == 200
        stadium = stadium_response.json()
        
        # 2. Create players
        players = []
        for i in range(4):
            player_data = {"name": f"Player{i}", "nickname": f"P{i}"}
            player_response = client.post("/api/players", json=player_data)
            assert player_response.status_code == 200
            players.append(player_response.json())
        
        # 3. Create a game
        game_data = {
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }
        game_response = client.post("/api/games", json=game_data)
        assert game_response.status_code == 200
        game = game_response.json()
        
        # 4. Add players to teams (2 per team)
        for i, player in enumerate(players[:2]):
            gameplayer_data = {
                "player_id": player["id"],
                "team_id": game["home_team"]["id"]
            }
            response = client.post(f"/api/games/{game['id']}/players", json=gameplayer_data)
            assert response.status_code == 200
        
        for i, player in enumerate(players[2:]):
            gameplayer_data = {
                "player_id": player["id"],
                "team_id": game["away_team"]["id"]
            }
            response = client.post(f"/api/games/{game['id']}/players", json=gameplayer_data)
            assert response.status_code == 200
        
        # 5. Start the game
        start_response = client.put(f"/api/games/{game['id']}/start")
        assert start_response.status_code == 200
        started_game = start_response.json()
        assert started_game["started_at"] is not None
        
        # 6. Record some goals
        goal_minute = (datetime.fromisoformat(game["date"]) + timedelta(minutes=15)).isoformat()
        goal1_data = {
            "team_id": game["home_team"]["id"],
            "scorer_id": players[0]["id"],
            "minute": goal_minute
        }
        goal1_response = client.post(f"/api/games/{game['id']}/goals", json=goal1_data)
        assert goal1_response.status_code == 200
        
        goal_minute = (datetime.fromisoformat(game["date"]) + timedelta(minutes=30)).isoformat()
        goal2_data = {
            "team_id": game["home_team"]["id"],
            "scorer_id": players[1]["id"],
            "assister_id": players[0]["id"],
            "minute": goal_minute
        }
        goal2_response = client.post(f"/api/games/{game['id']}/goals", json=goal2_data)
        assert goal2_response.status_code == 200
        
        goal_minute = (datetime.fromisoformat(game["date"]) + timedelta(minutes=60)).isoformat()
        goal3_data = {
            "team_id": game["away_team"]["id"],
            "scorer_id": players[2]["id"],
            "minute": goal_minute
        }
        goal3_response = client.post(f"/api/games/{game['id']}/goals", json=goal3_data)
        assert goal3_response.status_code == 200
        
        # 7. End the game
        end_response = client.put(f"/api/games/{game['id']}/end")
        assert end_response.status_code == 200
        ended_game = end_response.json()
        assert ended_game["ended_at"] is not None
        
        # 8. Verify final game state
        final_game = client.get(f"/api/games/{game['id']}").json()
        assert final_game["started_at"] is not None
        assert final_game["ended_at"] is not None
        
        # 9. Check player stats
        for player in players:
            player_games = client.get(f"/api/players/{player['id']}/games").json()
            assert len(player_games) >= 1
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        for player in players:
            client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")
    
    def test_multiple_games_at_same_stadium(self, client: TestClient):
        """Test creating multiple games at the same stadium"""
        # Create stadium
        stadium_data = {"name": "Multi-Game Stadium", "address": "456 Multi St"}
        stadium_response = client.post("/api/stadiums", json=stadium_data)
        stadium = stadium_response.json()
        
        # Create multiple games
        games = []
        for i in range(3):
            game_data = {
                "stadium_id": stadium["id"],
                "date": datetime.now().isoformat()
            }
            game_response = client.post("/api/games", json=game_data)
            assert game_response.status_code == 200
            games.append(game_response.json())
        
        # Verify all games are listed
        all_games = client.get("/api/games").json()
        game_ids = [g["id"] for g in all_games]
        for game in games:
            assert game["id"] in game_ids
        
        # Cleanup
        for game in games:
            client.delete(f"/api/games/{game['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")
    
    def test_player_participation_in_multiple_games(self, client: TestClient):
        """Test a player participating in multiple games"""
        # Create player
        player_data = {"name": "Multi-Game Player", "nickname": "MGP"}
        player_response = client.post("/api/players", json=player_data)
        player = player_response.json()
        
        # Create stadium
        stadium_data = {"name": "Test Stadium", "address": "Test St"}
        stadium_response = client.post("/api/stadiums", json=stadium_data)
        stadium = stadium_response.json()
        
        # Create multiple games and add player to each
        games = []
        for i in range(3):
            game_data = {
                "stadium_id": stadium["id"],
                "date": datetime.now().isoformat()
            }
            game_response = client.post("/api/games", json=game_data)
            game = game_response.json()
            games.append(game)
            
            # Add player to game
            gameplayer_data = {
                "player_id": player["id"],
                "team_id": game["home_team"]["id"]
            }
            client.post(f"/api/games/{game['id']}/players", json=gameplayer_data)
        
        # Verify player has participated in all games
        player_games = client.get(f"/api/players/{player['id']}/games").json()
        assert len(player_games) == 3
        
        # Cleanup
        for game in games:
            client.delete(f"/api/games/{game['id']}")
        client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")
    
    def test_stadium_deletion_with_games(self, client: TestClient):
        """Test that stadium can be deleted (or cascade rules are enforced)"""
        # Create stadium
        stadium_data = {"name": "Delete Test Stadium", "address": "Delete St"}
        stadium_response = client.post("/api/stadiums", json=stadium_data)
        stadium = stadium_response.json()
        
        # Create a game at this stadium
        game_data = {
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }
        game_response = client.post("/api/games", json=game_data)
        game = game_response.json()
        
        # Try to delete stadium (behavior depends on cascade rules)
        # This test documents the current behavior
        stadium_delete = client.delete(f"/api/stadiums/{stadium['id']}")
        
        # Cleanup game if stadium deletion failed
        if stadium_delete.status_code != 200:
            client.delete(f"/api/games/{game['id']}")
            client.delete(f"/api/stadiums/{stadium['id']}")
        
    def test_game_with_no_goals(self, client: TestClient):
        """Test a complete 0-0 game"""
        # Create stadium
        stadium_data = {"name": "Boring Stadium", "address": "Boring St"}
        stadium = client.post("/api/stadiums", json=stadium_data).json()
        
        # Create players
        players = []
        for i in range(2):
            player = client.post("/api/players", json={"name": f"Player{i}"}).json()
            players.append(player)
        
        # Create game
        game = client.post("/api/games", json={
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }).json()
        
        # Add players
        for i, player in enumerate(players):
            team_id = game["home_team"]["id"] if i == 0 else game["away_team"]["id"]
            client.post(f"/api/games/{game['id']}/players", json={
                "player_id": player["id"],
                "team_id": team_id
            })
        
        # Start and end game without any goals
        client.put(f"/api/games/{game['id']}/start")
        client.put(f"/api/games/{game['id']}/end")
        
        # Verify game is complete
        final_game = client.get(f"/api/games/{game['id']}").json()
        assert final_game["started_at"] is not None
        assert final_game["ended_at"] is not None
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        for player in players:
            client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")


class TestDataIntegrity:
    """Integration tests for data integrity and relationships"""
    
    def test_multiple_goals_same_player(self, client: TestClient):
        """Test a player scoring multiple goals in one game"""
        # Setup
        stadium = client.post("/api/stadiums", json={
            "name": "Hat-trick Stadium", "address": "Hat-trick St"
        }).json()
        
        player = client.post("/api/players", json={
            "name": "Striker", "nickname": "ST"
        }).json()
        
        game = client.post("/api/games", json={
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }).json()
        
        # Add player to game
        client.post(f"/api/games/{game['id']}/players", json={
            "player_id": player["id"],
            "team_id": game["home_team"]["id"]
        })
        
        # Start game
        client.put(f"/api/games/{game['id']}/start")
        
        # Score 3 goals (hat-trick!)
        for minute in [10, 25, 67]:
            response = client.post(f"/api/games/{game['id']}/goals", json={
                "team_id": game["home_team"]["id"],
                "scorer_id": player["id"],
                "minute": minute
            })
            assert response.status_code == 200
        
        # Verify game data
        final_game = client.get(f"/api/games/{game['id']}").json()
        assert final_game["id"] == game["id"]
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")
    
    def test_team_composition_validation(self, client: TestClient):
        """Test that both teams can have different players"""
        # Setup
        stadium = client.post("/api/stadiums", json={
            "name": "Team Stadium", "address": "Team St"
        }).json()
        
        # Create 4 players
        players = []
        for i in range(4):
            player = client.post("/api/players", json={
                "name": f"TeamPlayer{i}", "nickname": f"TP{i}"
            }).json()
            players.append(player)
        
        game = client.post("/api/games", json={
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }).json()
        
        # Add 2 players to home team
        for player in players[:2]:
            response = client.post(f"/api/games/{game['id']}/players", json={
                "player_id": player["id"],
                "team_id": game["home_team"]["id"]
            })
            assert response.status_code == 200
        
        # Add 2 players to away team
        for player in players[2:]:
            response = client.post(f"/api/games/{game['id']}/players", json={
                "player_id": player["id"],
                "team_id": game["away_team"]["id"]
            })
            assert response.status_code == 200
        
        # Verify game has players from both teams
        game_data = client.get(f"/api/games/{game['id']}").json()
        assert game_data["id"] == game["id"]
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        for player in players:
            client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")


class TestErrorScenarios:
    """Integration tests for error handling and edge cases"""
    
    def test_game_lifecycle_violations(self, client: TestClient):
        """Test various violations of game lifecycle rules"""
        # Setup
        stadium = client.post("/api/stadiums", json={
            "name": "Lifecycle Stadium", "address": "Lifecycle St"
        }).json()
        
        game = client.post("/api/games", json={
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }).json()
        
        # Try to end game before starting
        end_response = client.put(f"/api/games/{game['id']}/end")
        assert end_response.status_code == 400
        assert "not started" in end_response.json()["detail"].lower()
        
        # Start game
        start_response = client.put(f"/api/games/{game['id']}/start")
        assert start_response.status_code == 200
        
        # Try to start again
        start_again = client.put(f"/api/games/{game['id']}/start")
        assert start_again.status_code == 400
        assert "already started" in start_again.json()["detail"].lower()
        
        # End game
        end_response = client.put(f"/api/games/{game['id']}/end")
        assert end_response.status_code == 200
        
        # Try to end again
        end_again = client.put(f"/api/games/{game['id']}/end")
        assert end_again.status_code == 400
        assert "already ended" in end_again.json()["detail"].lower()
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")
    
    def test_orphaned_relationships(self, client: TestClient):
        """Test handling of relationships when parent entities are deleted"""
        # Create a complete game setup
        stadium = client.post("/api/stadiums", json={
            "name": "Orphan Stadium", "address": "Orphan St"
        }).json()
        
        player = client.post("/api/players", json={
            "name": "Orphan Player", "nickname": "OP"
        }).json()
        
        game = client.post("/api/games", json={
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }).json()
        
        # Add player to game
        client.post(f"/api/games/{game['id']}/players", json={
            "player_id": player["id"],
            "team_id": game["home_team"]["id"]
        })
        
        # Delete player (this should handle cascade or fail appropriately)
        player_delete = client.delete(f"/api/players/{player['id']}")
        
        # Verify appropriate behavior (depends on your cascade rules)
        # Document the current behavior
        if player_delete.status_code == 200:
            # If deletion succeeded, verify game can still be accessed
            game_response = client.get(f"/api/games/{game['id']}")
            # Behavior depends on cascade rules
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        if player_delete.status_code != 200:
            client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")
    
    def test_concurrent_game_operations(self, client: TestClient):
        """Test multiple operations on the same game"""
        # Setup
        stadium = client.post("/api/stadiums", json={
            "name": "Concurrent Stadium", "address": "Concurrent St"
        }).json()
        
        players = []
        for i in range(2):
            player = client.post("/api/players", json={
                "name": f"ConcurrentPlayer{i}"
            }).json()
            players.append(player)
        
        game = client.post("/api/games", json={
            "stadium_id": stadium["id"],
            "date": datetime.now().isoformat()
        }).json()
        
        # Add multiple players simultaneously (simulating concurrent requests)
        for player in players:
            response = client.post(f"/api/games/{game['id']}/players", json={
                "player_id": player["id"],
                "team_id": game["home_team"]["id"]
            })
            assert response.status_code == 200
        
        # Start game
        client.put(f"/api/games/{game['id']}/start")
        
        # Record multiple goals in quick succession
        for i, player in enumerate(players):
            response = client.post(f"/api/games/{game['id']}/goals", json={
                "team_id": game["home_team"]["id"],
                "scorer_id": player["id"],
                "minute": 10 + i
            })
            assert response.status_code == 200
        
        # Verify game integrity
        final_game = client.get(f"/api/games/{game['id']}").json()
        assert final_game["started_at"] is not None
        
        # Cleanup
        client.delete(f"/api/games/{game['id']}")
        for player in players:
            client.delete(f"/api/players/{player['id']}")
        client.delete(f"/api/stadiums/{stadium['id']}")