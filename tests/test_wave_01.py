from app.models.task import Task
from app.db import db
import pytest

@pytest.mark.skip(reason="No way to test this feature yet")
def test_task_to_dict():
    #Arrange
    new_task = Task(id = 1, title="Make My Bed", 
                    description="Start the day off right!", 
                    completed_at=None)
    
    #Act
    task_dict = new_task.to_dict()

    #Assert
    assert len(task_dict) == 4
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Make My Bed"
    assert task_dict["description"] == "Start the day off right!"
    assert task_dict["is_complete"] == False

@pytest.mark.skip(reason="No way to test this feature yet")
def test_task_to_dict_missing_id():
    #Arrange
    new_task = Task(title="Make My Bed", 
                    description="Start the day off right!", 
                    completed_at=None)
    
    #Act
    task_dict = new_task.to_dict()

    #Assert
    assert len(task_dict) == 4
    assert task_dict["id"] is None
    assert task_dict["title"] == "Make My Bed"
    assert task_dict["description"] == "Start the day off right!"
    assert task_dict["is_complete"] == False

@pytest.mark.skip(reason="No way to test this feature yet")
def test_task_to_dict_missing_title():
    #Arrange
    new_task = Task(id = 1,
                    description="Start the day off right!", 
                    completed_at=None)
    
    #Act
    task_dict = new_task.to_dict()

    #Assert
    assert len(task_dict) == 4
    assert task_dict["id"] == 1
    assert task_dict["title"] is None
    assert task_dict["description"] == "Start the day off right!"
    assert task_dict["is_complete"] == False

@pytest.mark.skip(reason="No way to test this feature yet")
def test_task_from_dict():
    #Arrange
    task_dict =  {
        "title": "Make My Bed",
        "description": "Start the day off right!",
        "is_complete": False
    }

    #Act
    task_obj =  Task.from_dict(task_dict)

    #Assert
    assert task_obj.title == "Make My Bed"
    assert task_obj.description == "Start the day off right!"
    assert task_obj.completed_at is None

@pytest.mark.skip(reason="No way to test this feature yet")
def test_task_from_dict_no_title():
    #Arrange
    task_dict =  {
        "description": "Start the day off right!",
        "is_complete": False
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        Task.from_dict(task_dict)

@pytest.mark.skip(reason="No way to test this feature yet")
def test_task_from_dict_no_description():
    #Arrange
    task_dict =  {
        "title": "Make My Bed",
        "is_complete": False
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'description'):
        Task.from_dict(task_dict)

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_no_saved_tasks(client):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_one_saved_tasks(client, one_task):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    ]


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task(client, one_task):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_not_found(client):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }
    
    query = db.select(Task).where(Task.id == 1)
    new_task = db.session.scalar(query)

    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at == None

@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })

    # Assert
    assert response.status_code == 204

    query = db.select(Task).where(Task.id == 1)
    task = db.session.scalar(query)

    assert task.title == "Updated Task Title"
    assert task.description == "Updated Test Description"
    assert task.completed_at == None



@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_not_found(client):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task(client, one_task):
    # Act
    response = client.delete("/tasks/1")

    # Assert
    assert response.status_code == 204

    query = db.select(Task).where(Task.id == 1)
    assert db.session.scalar(query) == None

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task_not_found(client):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************

    assert db.session.scalars(db.select(Task)).all() == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_title(client):
    # Act
    response = client.post("/tasks", json={
        "description": "Test Description"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert db.session.scalars(db.select(Task)).all() == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_description(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert db.session.scalars(db.select(Task)).all() == []