# Wave 6: Establishing a One-to-Many Relationship

## Goal

Our users want to associate tasks and goals. Specifically, our users want to designate that there are many tasks that serve one goal.

This wave focuses on creating a one-to-many relationship between goals and tasks, where a goal has-many tasks, and a task belongs to one goal.

When we have many tasks and many goals, users will want to conveniently gather all of the tasks associated with one goal. Our API should serve this information with a new route, `/goals/<goal_id>/tasks`.

## Requirements

First, we should update our models so that the relationship is saved in our database.

Secondly, we should create our new route, `/goals/<goal_id>/tasks`, so that our API gives back the right information.

### Tips

- Use lesson materials and independent research to review how to set up a one-to-many relationship in Flask.
- Remember to run `flask db migrate` and `flask db upgrade` whenever there is a change to the model.
- Pay attention to the exact shape of the expected JSON. Double-check nested data structures and the names of the keys for any mispellings.
- Use the tests in `tests/test_wave_06.py` to guide your implementation.
- Some tests use a fixture named `one_task_belongs_to_one_goal` that is defined in `tests/conftest.py`. This fixture saves a task and a goal to the test database, and uses SQLAlchemy to associate the goal and task together.

### Updates to the Goal Model

The Goal model should have a _relationship_ with the model Task.

After reviewing the strategy for creating a one-to-many relationship, it is up to you if you would like to add convenience attributes for accessing the `Goal` model from it's related `Task`s and vice versa, accessing the list of associated `Task`s from a `Goal` model.

### Updates to the Task Model

The Task model should belong to one `Goal`.

After reviewing the strategy for creating a one-to-many relationship, in the Task model, we recommend:

- Setting the foreign key to `goal`'s primary key column
- Using `Optional` syntax to make the attribute nullable

Remember to run `flask db migrate` and `flask db upgrade` whenever there is a change to the model.

### Sending a List of Task IDs to a Goal

Given:

- a goal that has the ID `1`
- three tasks with the IDs `1`, `2`, and `3`

When I send a `POST` request to `/goals/1/tasks` with this request body:

```json
{
  "task_ids": [1, 2, 3]
}
```

Then the three `Task`s belong to the `Goal` and it gets updated in the database, and we get back a `200 OK` with the following response body:

```json
{
  "id": 1,
  "task_ids": [1, 2, 3]
}
```

### Getting Tasks of One Goal

Given a goal that has:

- An id `333`
- A `title` attribute with the value `"Build a habit of going outside daily"`

and a task that has:

- An id `999`
- A `title` attribute with the value `"Go on my daily walk 🏞"`
- A `description` attribute with the value `"Notice something new every day"`
- A `completed_at` attribute with a `null` value
- It belongs to the Goal with ID 333

when I send a `GET` request to `/goals/333/tasks`,

then I get this response:

`200 OK`

```json
{
  "id": 333,
  "title": "Build a habit of going outside daily",
  "tasks": [
    {
      "id": 999,
      "goal_id": 333,
      "title": "Go on my daily walk 🏞",
      "description": "Notice something new every day",
      "is_complete": false
    }
  ]
}
```

### Getting Tasks of One Goal: No Matching Tasks

Given a goal that has:

- An id `333`
- A `title` attribute with the value `"Build a habit of going outside daily"`

and no tasks that belong to this goal,

when I send a `GET` request to `/goals/333/tasks`,

then I get this response:

`200 OK`

```json
{
  "id": 333,
  "title": "Build a habit of going outside daily",
  "tasks": []
}
```

### Getting Tasks of One Goal: No Matching Goal

Given that no goals exist,

when I send a `GET` request to `/goals/1/tasks`,

then I get this response:

`404 Not Found`

You may choose the response body.

 Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.
