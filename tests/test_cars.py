def test_add_car(client, jwt_token, create_owner):
    owner_id = create_owner
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post(
        "/main/cars",
        json={"owner_id": owner_id, "color": "blue", "model": "sedan"},
        headers=headers,
    )
    assert response.status_code == 201


def test_update_car(client, jwt_token, create_owner, create_car):
    owner_id = create_owner
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.post(
        "/main/cars",
        json={"owner_id": owner_id, "color": "blue", "model": "sedan"},
        headers=headers,
    )
    car_id = response.json["id"]
    response = client.put(
        f"/main/cars/{car_id}",
        json={"owner_id": owner_id, "color": "yellow", "model": "hatch"},
        headers=headers,
    )
    assert response.status_code == 200


def test_get_all_cars(client, jwt_token, create_owner):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.get("/main/cars", headers=headers)
    assert response.status_code == 200
    assert len(response.json) > 0


def test_delete_car(client, jwt_token, create_car):
    car_id = create_car
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = client.delete(
        f"/main/cars/{car_id}",
        headers=headers,
    )
    assert response.status_code == 200
