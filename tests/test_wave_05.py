from app.models.goal import Goal
import pytest

@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_to_dict():
    #Arrange
    new_goal = Goal(id=1, title="Seize the Day!")
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] == "Seize the Day!"

@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_to_dict_no_id():
    #Arrange
    new_goal = Goal(title="Seize the Day!")
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] is None
    assert goal_dict["title"] == "Seize the Day!"

@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_to_dict_no_title():
    #Arrange
    new_goal = Goal(id=1)
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] is None



@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_from_dict():
    #Arrange
    goal_dict =  {
        "title": "Seize the Day!",
    }

    #Act
    goal_obj =  Goal.from_dict(goal_dict)

    #Assert
    assert goal_obj.title == "Seize the Day!"

@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_from_dict_no_title():
    #Arrange
    goal_dict =  {
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        Goal.from_dict(goal_dict)


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


@pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    pass
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    raise Exception("Complete test")
    # Assert
    # ---- Complete Test ----
    # assertion 1 goes here
    # assertion 2 goes here
    # ---- Complete Test ----


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }


@pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    raise Exception("Complete test")
    # Act
    # ---- Complete Act Here ----

    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    # assertion 2 goes here
    # assertion 3 goes here
    # ---- Complete Assertions Here ----


@pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    raise Exception("Complete test")
    # Act
    # ---- Complete Act Here ----

    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    # assertion 2 goes here
    # ---- Complete Assertions Here ----


@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")

    # Assert
    assert response.status_code == 204

    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404

    response_body = response.get_json()
    assert "message" in response_body

    raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


@pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    raise Exception("Complete test")

    # Act
    # ---- Complete Act Here ----

    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    # assertion 2 goes here
    # ---- Complete Assertions Here ----


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
