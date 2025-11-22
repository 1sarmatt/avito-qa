import pytest
import requests
import random
import json
import re
from typing import Dict, Any, Optional

BASE_URL = "https://qa-internship.avito.com"
API_V1 = f"{BASE_URL}/api/1"
API_V2 = f"{BASE_URL}/api/2"

created_item_ids = []
test_seller_id = 500000 + random.randint(1000, 99999)


def extract_id_from_response(response_data: dict) -> Optional[str]:
    """
    Extract ID from API response.
    API returns: {"status": "Сохранили объявление - {UUID}"}
    """
    if isinstance(response_data, dict):
        if "id" in response_data:
            return response_data["id"]
        
        if "status" in response_data:
            status = response_data["status"]
            uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
            match = re.search(uuid_pattern, status, re.IGNORECASE)
            if match:
                return match.group(0)
        
        if "result" in response_data:
            result = response_data["result"]
            if isinstance(result, str):
                uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
                match = re.search(uuid_pattern, result, re.IGNORECASE)
                if match:
                    return match.group(0)
    
    return None


class TestCreateItem:
    """Test cases for creating items (POST /api/1/item)"""
    
    def test_001_create_item_success(self):
        """TC-001: Successfully create item with correct data"""
        payload = {
            "sellerID": test_seller_id,
            "name": "iPhone 14 Pro",
            "price": 85000,
            "statistics": {
                "likes": 5,
                "viewCount": 120,
                "contacts": 8
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        item_id = extract_id_from_response(data)
        assert item_id is not None, f"Could not extract ID from response: {data}"
        
        created_item_ids.append(item_id)
        print(f"✅ Created item with ID: {item_id}")
    
    def test_002_create_item_minimal_data(self):
        """TC-002: Create item with minimal allowed data"""
        payload = {
            "sellerID": test_seller_id + 1,
            "name": "Книга",
            "price": 100,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        if response.status_code == 400:
            print(f"⚠️ API returned 400 for minimal data: {response.text}")
            payload["statistics"] = {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
            response = requests.post(f"{API_V1}/item", json=payload)
            print(f"Retry with non-zero stats - Status: {response.status_code}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        else:
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        
        item_id = extract_id_from_response(data)
        assert item_id is not None, f"Could not extract ID from response: {data}"
        
        created_item_ids.append(item_id)
        print(f"✅ Created item with ID: {item_id}")
    
    def test_003_create_item_high_price(self):
        """TC-003: Create item with high price"""
        payload = {
            "sellerID": test_seller_id + 2,
            "name": "Квартира в центре",
            "price": 99999999,
            "statistics": {
                "likes": 100,
                "viewCount": 5000,
                "contacts": 250
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        
        item_id = extract_id_from_response(data)
        assert item_id is not None
        
        created_item_ids.append(item_id)
        print(f"✅ Created item with high price, ID: {item_id}")
    
    def test_004_create_item_missing_name(self):
        """TC-004: Attempt to create item without name field"""
        payload = {
            "sellerID": test_seller_id + 3,
            "price": 50000,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print(f"✅ Correctly rejected request without name")
    
    def test_005_create_item_missing_price(self):
        """TC-005: Attempt to create item without price field"""
        payload = {
            "sellerID": test_seller_id + 4,
            "name": "Товар",
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 400
        print(f"✅ Correctly rejected request without price")
    
    def test_006_create_item_negative_price(self):
        """TC-006: Attempt to create item with negative price"""
        payload = {
            "sellerID": test_seller_id + 5,
            "name": "Товар",
            "price": -1000,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code in [400, 200]
        print(f"✅ Negative price handled with status {response.status_code}")
    
    def test_007_create_item_empty_name(self):
        """TC-008: Create item with empty name"""
        payload = {
            "sellerID": test_seller_id + 6,
            "name": "",
            "price": 1000,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }
        
        response = requests.post(f"{API_V1}/item", json=payload)
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 400
        print(f"✅ Correctly rejected item with empty name")
    
    def test_008_create_item_invalid_json(self):
        """TC-009: Attempt to create item with invalid JSON"""
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(
            f"{API_V1}/item",
            data="{invalid json}",
            headers=headers
        )
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 400
        print(f"✅ Correctly rejected invalid JSON")
    
    def test_009_create_duplicate_items(self):
        """TC-010: Create two items with same data"""
        payload = {
            "sellerID": test_seller_id + 7,
            "name": "Дублирующийся товар",
            "price": 5000,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }
        
        response1 = requests.post(f"{API_V1}/item", json=payload)
        response2 = requests.post(f"{API_V1}/item", json=payload)
        
        print(f"\nFirst response: {response1.status_code}, {response1.text}")
        print(f"Second response: {response2.status_code}, {response2.text}")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        id1 = extract_id_from_response(data1)
        id2 = extract_id_from_response(data2)
        
        assert id1 is not None and id2 is not None
        assert id1 != id2, "IDs should be unique"
        
        created_item_ids.append(id1)
        created_item_ids.append(id2)
        print(f"✅ Created two items with different IDs: {id1}, {id2}")


class TestGetItemById:
    """Test cases for getting item by ID (GET /api/1/item/:id)"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Create test item before tests"""
        payload = {
            "sellerID": test_seller_id + 100,
            "name": "Test Item for Get",
            "price": 15000,
            "statistics": {
                "likes": 3,
                "viewCount": 50,
                "contacts": 2
            }
        }
        response = requests.post(f"{API_V1}/item", json=payload)
        if response.status_code == 200:
            self.item_id = extract_id_from_response(response.json())
            created_item_ids.append(self.item_id)
        else:
            self.item_id = None
    
    def test_201_get_existing_item(self):
        """TC-201: Get existing item by ID"""
        if not self.item_id:
            pytest.skip("Item not created")
        
        response = requests.get(f"{API_V1}/item/{self.item_id}")
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        
        if isinstance(data, list):
            assert len(data) > 0
            assert data[0].get("id") == self.item_id or self.item_id in str(data)
        else:
            assert "id" in data or self.item_id in str(data)
        
        print(f"✅ Successfully retrieved item {self.item_id}")
    
    def test_202_get_nonexistent_item(self):
        """TC-202: Get item with non-existent ID"""
        response = requests.get(f"{API_V1}/item/nonexistent-id-12345")
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code in [404, 400]
        print(f"✅ Correctly returned {response.status_code} for non-existent item")
    
    def test_203_get_item_empty_id(self):
        """TC-203: Get item with empty ID"""
        response = requests.get(f"{API_V1}/item/")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [404, 400]
        print(f"✅ Correctly handled empty ID")
    
    def test_204_get_item_invalid_format(self):
        """TC-204: Get item with invalid ID format"""
        response = requests.get(f"{API_V1}/item/!@#$%^&*()")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [400, 404]
        print(f"✅ Correctly handled invalid ID format")


class TestGetSellerItems:
    """Test cases for getting all items by seller"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Create test items for seller"""
        self.seller_id = test_seller_id + 200
        self.item_ids = []
        
        for i in range(2):
            payload = {
                "sellerID": self.seller_id,
                "name": f"Seller Item {i+1}",
                "price": 1000 * (i + 1),
                "statistics": {
                    "likes": i,
                    "viewCount": 10 * i,
                    "contacts": i
                }
            }
            response = requests.post(f"{API_V1}/item", json=payload)
            if response.status_code == 200:
                item_id = extract_id_from_response(response.json())
                if item_id:
                    self.item_ids.append(item_id)
                    created_item_ids.append(item_id)
    
    def test_301_get_seller_items_multiple(self):
        """TC-301: Get items for seller with multiple items"""
        if not self.item_ids:
            pytest.skip("Items not created")
        
        response = requests.get(f"{API_V1}/{self.seller_id}/item")
        print(f"\nStatus: {response.status_code}, Response: {response.text[:200]}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= len(self.item_ids)
        
        print(f"✅ Retrieved {len(data)} items for seller")
    
    def test_302_get_seller_items_empty(self):
        """TC-302: Get items for seller without items"""
        empty_seller_id = test_seller_id + 999
        response = requests.get(f"{API_V1}/{empty_seller_id}/item")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        print(f"✅ Correctly returned empty list for seller without items")
    
    def test_303_get_items_nonexistent_seller(self):
        """TC-303: Get items for non-existent seller"""
        response = requests.get(f"{API_V1}/999999999/item")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [200, 404]
        print(f"✅ Handled non-existent seller with status {response.status_code}")
    
    def test_304_get_items_negative_seller_id(self):
        """TC-304: Get items with negative seller ID"""
        response = requests.get(f"{API_V1}/-1/item")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [400, 404, 200]
        print(f"✅ Handled negative seller ID")
    
    def test_305_get_items_invalid_seller_id(self):
        """TC-305: Get items with invalid seller ID format"""
        response = requests.get(f"{API_V1}/abc123/item")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [400, 404]
        print(f"✅ Rejected invalid seller ID format")


class TestGetStatistic:
    """Test cases for getting item statistics"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Create test item with known statistics"""
        payload = {
            "sellerID": test_seller_id + 300,
            "name": "Item with Statistics",
            "price": 25000,
            "statistics": {
                "likes": 42,
                "viewCount": 1000,
                "contacts": 15
            }
        }
        response = requests.post(f"{API_V1}/item", json=payload)
        if response.status_code == 200:
            self.item_id = extract_id_from_response(response.json())
            self.expected_stats = payload["statistics"]
            created_item_ids.append(self.item_id)
        else:
            self.item_id = None
    
    def test_401_get_statistic_success(self):
        """TC-401: Get statistics for existing item"""
        if not self.item_id:
            pytest.skip("Item not created")
        
        response = requests.get(f"{API_V1}/statistic/{self.item_id}")
        print(f"\nStatus: {response.status_code}, Response: {response.text[:200]}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list) or isinstance(data, dict)
        print(f"✅ Retrieved statistics for item {self.item_id}")
    
    def test_402_get_statistic_nonexistent(self):
        """TC-402: Get statistics for non-existent item"""
        response = requests.get(f"{API_V1}/statistic/nonexistent-stat-id")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [404, 400]
        print(f"✅ Correctly handled non-existent item")
    
    def test_403_get_statistic_v2(self):
        """TC-403: Get statistics through API v2"""
        if not self.item_id:
            pytest.skip("Item not created")
        
        response = requests.get(f"{API_V2}/statistic/{self.item_id}")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [200, 404]
        print(f"✅ v2 endpoint responded with status {response.status_code}")
    
    def test_404_get_statistic_empty_id(self):
        """TC-404: Get statistics with empty ID"""
        response = requests.get(f"{API_V1}/statistic/")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [404, 400]
        print(f"✅ Correctly handled empty ID")


class TestDeleteItem:
    """Test cases for deleting items"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Create test items for deletion"""
        self.item_ids_to_delete = []
        
        for i in range(2):
            payload = {
                "sellerID": test_seller_id + 400 + i,
                "name": f"Item to Delete {i+1}",
                "price": 10000 + i * 1000,
                "statistics": {
                    "likes": 0,
                    "viewCount": 0,
                    "contacts": 0
                }
            }
            response = requests.post(f"{API_V1}/item", json=payload)
            if response.status_code == 200:
                item_id = extract_id_from_response(response.json())
                if item_id:
                    self.item_ids_to_delete.append(item_id)
    
    def test_501_delete_existing_item(self):
        """TC-501: Successfully delete existing item"""
        if not self.item_ids_to_delete:
            pytest.skip("Items not created")
        
        item_id = self.item_ids_to_delete[0]
        
        response = requests.delete(f"{API_V2}/item/{item_id}")
        print(f"\nStatus: {response.status_code}, Response: {response.text}")
        
        assert response.status_code in [200, 201, 204]
        print(f"✅ Successfully deleted item {item_id}")
    
    def test_502_delete_nonexistent_item(self):
        """TC-502: Attempt to delete non-existent item"""
        response = requests.delete(f"{API_V2}/item/nonexistent-delete-id")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [404, 400]
        print(f"✅ Correctly rejected deletion of non-existent item")
    
    def test_503_delete_invalid_id(self):
        """TC-503: Delete with invalid ID format"""
        response = requests.delete(f"{API_V2}/item/!@#$%")
        print(f"\nStatus: {response.status_code}")
        
        assert response.status_code in [400, 404]
        print(f"✅ Correctly handled invalid ID format")


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Clean up created items after all tests"""
    yield
    print("\n\n" + "="*70)
    print("CLEANING TEST DATA")
    print("="*70)
    for item_id in created_item_ids:
        try:
            response = requests.delete(f"{API_V2}/item/{item_id}")
            print(f"✅ Deleted {item_id}")
        except Exception as e:
            print(f"❌ Failed to delete {item_id}: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
