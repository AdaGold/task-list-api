# Wave 5: Creating a Second Model

## Goal

Our task list API should be able to work with an entity called `Goal`.
- `Goal`s are entities that describe a task a user wants to complete.
- They contain a title to name the goal.

For this wave, we want to be able to create, read, update, and delete different `Goal`s. We will create RESTful routes for these different operations.

## Writing Tests

This wave requires more test writing. The tests you need to write are scaffolded in the `test_wave_05.py` file. 
- As with incomplete tests in other waves, you should comment out the `Exception` when implementing a test.
- These tests are currently skipped with `@pytest.mark.skip(reason="test to be completed by student")` and the function body has `pass` in it. 
  - Once you implement these tests you should remove the `skip` decorator and the `pass`.

For the tests you write, use the requirements in this document to guide your test writing. 
- You can model your tests off of the Wave 1 tests for Tasks.
- Pay attention to the exact shape of the expected JSON. Double-check nested data structures and the names of the keys for any misspellings.
- Some tests use a [fixture](https://docs.pytest.org/en/6.2.x/fixture.html) named `one_goal` that is defined in `tests/conftest.py`. This fixture saves a specific goal to the test database.


# Requirements

## Goal Model

There should be a `Goal` model that lives in `app/models/goal.py`.

Goals should contain these attributes. **The tests require the title column to be named exactly** as `title`.

- `id`: a primary key for each goal
- `title`: text to name the goal

### Tips

- Don't forget to run:
  - `flask db migrate` every time there's a change in models, in order to generate migrations
  - `flask db upgrade` to run all generated migrations
- Similar to the Task model, we should add a class method to the Goal model that initializes a new instance from a dictionary, and use this method in relevant routes. 
  - If all of our models have this method, we could create a route helper method that initializes a new model instance from a dictionary, and use it in any route that creates a new model instance.
- Also like the Task model, notice that routes that return a JSON response are sending a dictionary representation of the goal that was fetched or created. 
  - Creating a model helper method to return this dictionary, which we can then use to help build these route responses, will improve the consistency of our endpoints.
- Further, we should remember that retrieving a model by its ID is a common operation. If it has not been done yet, we should create a route helper method that can retrieve a model by its ID, and use it for relevant routes. 
  - This method would be very similar in functionality to retrieving a Task model by its ID, so rather than making an entirely new route helper method, we could generalize any similar function to also work with a Goal (or any other model).

## CRUD for Goals

The following are required routes for wave 5. Feel free to implement the routes in any order within this wave.

### Create a Goal: Valid Goal

As a client, I want to be able to make a `POST` request to `/goals` with the following HTTP request body

```json
{
  "title": "My New Goal"
}
```

and get this response:

`201 CREATED`

```json
{
  "id": 1,
  "title": "My New Goal"
}
```

so that I know I successfully created a goal that is saved in the database.

### Get Goals: Getting Saved Goals

As a client, I want to be able to make a `GET` request to `/goals` when there is at least one saved goal and get this response:

`200 OK`

```json
[
  {
    "id": 1,
    "title": "Example Goal Title 1"
  },
  {
    "id": 2,
    "title": "Example Goal Title 2"
  }
]
```

### Get Goals: No Saved Goals

As a client, I want to be able to make a `GET` request to `/goals` when there are zero saved goals and get this response:

`200 OK`

```json
[]
```

### Get One Goal: One Saved Goal

As a client, I want to be able to make a `GET` request to `/goals/1` when there is at least one saved goal and get this response:

`200 OK`

```json
{
  "id": 1,
  "title": "Build a habit of going outside daily"
}
```

### Update Goal

As a client, I want to be able to make a `PUT` request to `/goals/1` when there is at least one saved goal with this request body:

```json
{
  "title": "Updated Goal Title"
}
```

and get this response:

`204 No Content`

The response should have a mimetype of "application/json" to keep our API response type consistent.

### Delete Goal: Deleting a Goal

As a client, I want to be able to make a `DELETE` request to `/goals/1` when there is at least one saved goal and get this response:

`204 No Content`

The response should have a mimetype of "application/json" to keep our API response type consistent.

### No matching Goal: Get, Update, and Delete

As a client, if I make any of the following requests:

  * `GET` `/goals/<goal_id>`
  * `UPDATE` `/goals/<goal_id>`
  * `DELETE` `/goals/<goal_id>`

and there is no existing goal with `goal_id`

The response code should be `404`.

You may choose the response body.

Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.

By using a helper method to retrieve a model by its ID, we could ensure that the response for a non-existing model is consistent across all these routes.

### Create a Goal: Invalid Goal With Missing Title

As a client, I want to be able to make a `POST` request to `/goals` with the following HTTP request body

```json
{}
```

and get this response:

`400 Bad Request`

```json
{
  "details": "Invalid data"
}
```

so that I know I did not create a Goal that is saved in the database.
