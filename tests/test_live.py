from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)
user_tokens = []


def _create_users():
    for i in range(8):
        response = client.post(
            "/user/create",
            json={"user_name": f"room_user_{i}", "leader_card_id": 1000},
        )
        user_tokens.append(response.json()["user_token"])


_create_users()


def _auth_header(i=0):
    token = user_tokens[i]
    return {"Authorization": f"bearer {token}"}


def test_room_1():

    room_id = 14

    response = client.post("/room/list", json={"live_id": 0})
    assert response.status_code == 200
    print("room/list response:", response.json())

    for i in range(8):
        response = client.post(
            "/room/join",
            headers=_auth_header(i),
            json={"room_id": room_id, "select_difficulty": 2},
        )
        assert response.status_code == 200
        print("room/join response:", response.json())

    response = client.post(
        "/room/wait", headers=_auth_header(), json={"room_id": room_id}
    )
    assert response.status_code == 200
    print("room/wait response:", response.json())

    # response = client.post(
    #     "/room/start", headers=_auth_header(), json={"room_id": room_id}
    # )
    # assert response.status_code == 200
    # print("room/start response:", response.json())

    for i in range(2):
        response = client.post(
            "/room/end",
            headers=_auth_header(i),
            json={
                "room_id": room_id,
                "score": 1234,
                "judge_count_list": [1111, 222, 33, 44, 5],
            },
        )
        assert response.status_code == 200
        print("room/end response:", response.json())

    # response = client.post(
    #     "/room/result",
    #     json={"room_id": room_id},
    # )
    # assert response.status_code == 200
    # print("room/end response:", response.json())
