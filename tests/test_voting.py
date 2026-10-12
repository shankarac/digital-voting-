from datetime import timedelta

from app.config import get_settings
from tests.conftest import auth_header, register_user


def _proposal(client, token, **overrides):
    payload = {
        "title": "Plant street trees",
        "description": "Fund forty trees on Main Street.",
        "deadline": "2030-01-05T12:00:00Z",
    }
    payload.update(overrides)
    response = client.post("/proposals/", json=payload, headers=auth_header(token))
    assert response.status_code == 201, response.text
    return response.json()


def test_challenge_rules_vote_once_revoke_then_close(client, clock):
    creator_token, _ = register_user(
        client,
        email="creator@example.com",
        display_name="Creator",
    )
    voter_token, voter = register_user(
        client,
        email="user1@example.com",
        display_name="User1",
    )
    other_token, _ = register_user(
        client,
        email="user2@example.com",
        display_name="User2",
    )
    proposal = _proposal(client, creator_token)
    proposal_id = proposal["id"]

    first = client.post(
        f"/proposals/{proposal_id}/vote",
        json={"vote": "yes"},
        headers=auth_header(voter_token),
    )
    assert first.status_code == 201, first.text
    assert first.json()["vote"] == "yes"
    assert first.json()["voter_name"] == voter["display_name"]
    vote_id = first.json()["id"]

    duplicate = client.post(
        f"/proposals/{proposal_id}/vote",
        json={"vote": "no"},
        headers=auth_header(voter_token),
    )
    assert duplicate.status_code == 409
    assert "already voted" in duplicate.json()["detail"].lower()

    revoked = client.delete(f"/votes/{vote_id}", headers=auth_header(voter_token))
    assert revoked.status_code == 204
    assert revoked.content == b""

    changed = client.post(
        f"/proposals/{proposal_id}/vote",
        json={"vote": "no"},
        headers=auth_header(voter_token),
    )
    assert changed.status_code == 201, changed.text
    new_vote_id = changed.json()["id"]

    closed = client.patch(
        f"/proposals/{proposal_id}/close",
        headers={"X-Admin-Key": get_settings().admin_key},
    )
    assert closed.status_code == 200, closed.text
    assert closed.json()["status"] == "closed"
    assert closed.json()["no_count"] == 1

    rejected_vote = client.post(
        f"/proposals/{proposal_id}/vote",
        json={"vote": "yes"},
        headers=auth_header(other_token),
    )
    assert rejected_vote.status_code == 409
    assert "closed" in rejected_vote.json()["detail"].lower()

    rejected_revoke = client.delete(
        f"/votes/{new_vote_id}",
        headers=auth_header(voter_token),
    )
    assert rejected_revoke.status_code == 409
    assert "closed" in rejected_revoke.json()["detail"].lower()

    fetched = client.get(f"/proposals/{proposal_id}")
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "closed"
    assert fetched.json()["total_votes"] == 1


def test_expiry_rejects_new_votes_and_revokes(client, clock):
    creator_token, _ = register_user(client, email="c1@example.com", display_name="Creator One")
    voter_token, _ = register_user(client, email="v1@example.com", display_name="User1")
    other_token, _ = register_user(client, email="v2@example.com", display_name="User2")
    proposal = _proposal(client, creator_token, deadline="2030-01-03T12:00:00Z")
    proposal_id = proposal["id"]
    voted = client.post(
        f"/proposals/{proposal_id}/vote",
        json={"vote": "yes"},
        headers=auth_header(voter_token),
    )
    assert voted.status_code == 201, voted.text
    vote_id = voted.json()["id"]

    clock["now"] = clock["now"] + timedelta(days=3)

    late_vote = client.post(
        f"/proposals/{proposal_id}/vote",
        json={"vote": "no"},
        headers=auth_header(other_token),
    )
    assert late_vote.status_code == 409
    assert "expired" in late_vote.json()["detail"].lower()

    late_revoke = client.delete(f"/votes/{vote_id}", headers=auth_header(voter_token))
    assert late_revoke.status_code == 409
    assert "expired" in late_revoke.json()["detail"].lower()


def test_admin_close_is_not_overwritten_by_deadline(client, clock):
    creator_token, _ = register_user(client, email="c2@example.com", display_name="Creator Two")
    proposal = _proposal(client, creator_token, deadline="2030-01-02T12:00:00Z")
    proposal_id = proposal["id"]
    closed = client.patch(
        f"/proposals/{proposal_id}/close",
        headers={"X-Admin-Key": get_settings().admin_key},
    )
    assert closed.status_code == 200, closed.text

    clock["now"] = clock["now"] + timedelta(days=5)
    fetched = client.get(f"/proposals/{proposal_id}")
    assert fetched.json()["status"] == "closed"


def test_counts_for_several_voters_and_a_second_proposal(client, clock):
    creator_token, _ = register_user(client, email="c3@example.com", display_name="Creator Three")
    amina_token, _ = register_user(client, email="a@example.com", display_name="Amina Shah")
    leo_token, _ = register_user(client, email="l@example.com", display_name="Leo Martins")
    priya_token, _ = register_user(client, email="p@example.com", display_name="Priya Nair")
    chris_token, _ = register_user(client, email="ch@example.com", display_name="Chris Adeyemi")

    first = _proposal(client, creator_token, title="Market hours")
    second = _proposal(client, creator_token, title="Library hours")

    votes = [
        (first["id"], amina_token, "yes"),
        (first["id"], leo_token, "yes"),
        (first["id"], priya_token, "no"),
        (first["id"], chris_token, "abstain"),
        (second["id"], amina_token, "no"),
    ]
    for proposal_id, token, choice in votes:
        response = client.post(
            f"/proposals/{proposal_id}/vote",
            json={"vote": choice},
            headers=auth_header(token),
        )
        assert response.status_code == 201, response.text

    detail = client.get(f"/proposals/{first['id']}").json()
    assert detail["total_votes"] == 4


def test_omitted_deadline_is_two_days(client, clock):
    token, _ = register_user(client, email="d@example.com", display_name="Deadline User")
    response = client.post(
        "/proposals/",
        json={"title": "Notice board", "description": "Replace the cracked notice board."},
        headers=auth_header(token),
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["deadline"] == "2030-01-03T12:00:00Z"


def test_validation_auth_and_missing_records(client, clock):
    token, _ = register_user(client, email="val@example.com", display_name="Validator")
    past = client.post(
        "/proposals/",
        json={
            "title": "Too late",
            "description": "This deadline has already passed.",
            "deadline": "2029-12-31T12:00:00Z",
        },
        headers=auth_header(token),
    )
    assert past.status_code == 422

    created = _proposal(client, token)
    bad_choice = client.post(
        f"/proposals/{created['id']}/vote",
        json={"vote": "maybe"},
        headers=auth_header(token),
    )
    assert bad_choice.status_code == 422

    unauthenticated_vote = client.post(
        f"/proposals/{created['id']}/vote",
        json={"vote": "yes"},
    )
    assert unauthenticated_vote.status_code == 401

    missing_vote = client.delete("/votes/9999", headers=auth_header(token))
    assert missing_vote.status_code == 404

    no_key = client.patch(f"/proposals/{created['id']}/close")
    assert no_key.status_code == 403


def test_cannot_revoke_someone_elses_vote(client, clock):
    creator_token, _ = register_user(client, email="c4@example.com", display_name="Creator Four")
    voter_token, _ = register_user(client, email="v3@example.com", display_name="Voter A")
    other_token, _ = register_user(client, email="v4@example.com", display_name="Voter B")
    proposal = _proposal(client, creator_token)
    vote = client.post(
        f"/proposals/{proposal['id']}/vote",
        json={"vote": "yes"},
        headers=auth_header(voter_token),
    ).json()
    blocked = client.delete(f"/votes/{vote['id']}", headers=auth_header(other_token))
    assert blocked.status_code == 403


def test_openapi_lists_required_operations(client):
    spec = client.get("/openapi.json")
    assert spec.status_code == 200
    paths = spec.json()["paths"]
    assert "/auth/register" in paths
    assert "/auth/login" in paths
    operation_ids = {
        meta["operationId"]
        for methods in paths.values()
        for method, meta in methods.items()
        if method in {"get", "post", "patch", "delete"}
    }
    assert {
        "register_user",
        "login_user",
        "get_current_user",
        "create_proposal",
        "list_proposals",
        "get_proposal",
        "cast_vote",
        "close_proposal",
        "revoke_vote",
    } <= operation_ids
