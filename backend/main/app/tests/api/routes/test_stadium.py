import pytest
from fastapi.testclient import TestClient
import uuid


class TestStadiumCRUD:
    """Test Create, Read, Update, Delete operations for stadiums"""
    
    def test_create_stadium(self, client: TestClient):
        """Test creating a new stadium"""
        data = {"name": "New Stadium", "address": "456 New St"}
        response = client.post("/api/stadiums", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == data["name"]
        assert content["address"] == data["address"]
        assert "id" in content
        
        client.delete(f"/api/stadiums/{content['id']}")
    
    def test_create_stadium_without_address(self, client: TestClient):
        """Test creating a stadium without an address"""
        data = {"name": "Stadium No Address"}
        response = client.post("/api/stadiums", json=data)
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == data["name"]
        assert content["address"] is None
        
        client.delete(f"/api/stadiums/{content['id']}")
    
    def test_list_stadiums(self, client: TestClient, test_stadium):
        """Test listing all stadiums"""
        response = client.get("/api/stadiums")
        
        assert response.status_code == 200
        stadiums = response.json()
        assert isinstance(stadiums, list)
        assert len(stadiums) >= 1
        
        stadium_ids = [s["id"] for s in stadiums]
        assert test_stadium["id"] in stadium_ids
    
    def test_list_stadiums_with_pagination(self, client: TestClient, test_stadium):
        """Test listing stadiums with skip and limit"""
        response = client.get("/api/stadiums?skip=0&limit=10")
        
        assert response.status_code == 200
        stadiums = response.json()
        assert isinstance(stadiums, list)
        assert len(stadiums) <= 10
    
    def test_get_stadium(self, client: TestClient, test_stadium):
        """Test getting a specific stadium"""
        response = client.get(f"/api/stadiums/{test_stadium['id']}")
        
        assert response.status_code == 200
        content = response.json()
        assert content["id"] == test_stadium["id"]
        assert content["name"] == test_stadium["name"]
    
    def test_get_stadium_not_found(self, client: TestClient):
        """Test getting a non-existent stadium"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/stadiums/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_stadium_name(self, client: TestClient, test_stadium):
        """Test updating a stadium's name"""
        response = client.put(
            f"/api/stadiums/{test_stadium['id']}",
            params={"name": "Updated Stadium"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "Updated Stadium"
        assert content["address"] == test_stadium["address"]
    
    def test_update_stadium_address(self, client: TestClient, test_stadium):
        """Test updating a stadium's address"""
        response = client.put(
            f"/api/stadiums/{test_stadium['id']}",
            params={"address": "999 New Address"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["address"] == "999 New Address"
        assert content["name"] == test_stadium["name"]
    
    def test_update_stadium_both_fields(self, client: TestClient, test_stadium):
        """Test updating both name and address"""
        response = client.put(
            f"/api/stadiums/{test_stadium['id']}",
            params={"name": "New Name", "address": "New Address"}
        )
        
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "New Name"
        assert content["address"] == "New Address"
    
    def test_update_stadium_not_found(self, client: TestClient):
        """Test updating a non-existent stadium"""
        fake_id = str(uuid.uuid4())
        response = client.put(
            f"/api/stadiums/{fake_id}",
            params={"name": "New Name"}
        )
        
        assert response.status_code == 404
    
    def test_delete_stadium(self, client: TestClient):
        """Test deleting a stadium"""
        
        data = {"name": "To Delete", "address": "Delete St"}
        create_response = client.post("/api/stadiums", json=data)
        stadium_id = create_response.json()["id"]
        
        response = client.delete(f"/api/stadiums/{stadium_id}")
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()
        
        get_response = client.get(f"/api/stadiums/{stadium_id}")
        assert get_response.status_code == 404
    
    def test_delete_stadium_not_found(self, client: TestClient):
        """Test deleting a non-existent stadium"""
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/stadiums/{fake_id}")
        
        assert response.status_code == 404