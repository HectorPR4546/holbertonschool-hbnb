import requests

BASE_URL = 'http://localhost:5000/api/v1/amenities/'

def test_amenity_crud():
    # Test create
    create_resp = requests.post(BASE_URL, json={'name': 'Wi-Fi'})
    print('Create:', create_resp.status_code, create_resp.json())
    
    amenity_id = create_resp.json()['id']
    
    # Test get all
    get_all_resp = requests.get(BASE_URL)
    print('Get all:', get_all_resp.status_code, get_all_resp.json())
    
    # Test get single
    get_resp = requests.get(f"{BASE_URL}{amenity_id}")
    print('Get single:', get_resp.status_code, get_resp.json())
    
    # Test update
    update_resp = requests.put(f"{BASE_URL}{amenity_id}", json={'name': 'High-Speed Wi-Fi'})
    print('Update:', update_resp.status_code, update_resp.json())

if __name__ == '__main__':
    test_amenity_crud()
