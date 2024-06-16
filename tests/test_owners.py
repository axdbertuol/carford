def test_add_owner(client, jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post("/main/owners", json={"name": "New Owner"}, headers=headers)
    assert response.status_code == 201


def test_update_owner(client, jwt_token, create_owner):
    owner_id = create_owner
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.put(
        f"/main/owners/{owner_id}", json={"name": "Updated Owner"}, headers=headers
    )
    assert response.status_code == 200


def test_get_all_owners(client, jwt_token, create_owner):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/main/owners", headers=headers)
    assert response.status_code == 200
    assert len(response.json) > 0


def test_delete_owner(client, jwt_token, create_owner):
    owner_id = create_owner
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.delete(f"/main/owners/{owner_id}", headers=headers)
    assert response.status_code == 200
