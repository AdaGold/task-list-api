import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task
import pytest

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_incomplete_task(client, one_task):
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert Task.query.get(1).completed_at


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_on_complete_task(client, completed_task):
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
    assert Task.query.get(1).completed_at == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_completed_task(client, completed_task):
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert Task.query.get(1).completed_at


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_on_incomplete_task(client, one_task):
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
    assert Task.query.get(1).completed_at == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_missing_task(client):
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    assert response.status_code == 404
    assert not "task" in response_body
    assert response_body == {"message": f"Invalid request: Task 1 not found"}
    

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_missing_task(client):
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    assert response.status_code == 404
    assert not "task" in response_body
    assert response_body == {"message": f"Invalid request: Task 1 not found"}