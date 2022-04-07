# Wave 5: Creating a Second Model

## Goal

Our task list API should be able to work with an entity called `Goal`.

Goals are entities that describe a task a user wants to complete.

They contain a title to name the goal.

Our goal for this wave is to be able to create, read, update, and delete different goals.

## Writing Tests

This wave requires you to complete **four** tests.

- The tests you need to write are scaffolded in the `test_wave_05.py` file.
  - These tests are currently skipped with `@pytest.mark.skip(reason="test to be completed by student")` and the function body has `pass` in it. Once you implement these tests you should remove the `skip` decorator and the `pass`.
- For the tests you write, use the requirements in this document to guide your test writing.
  - Pay attention to the exact shape of the expected JSON. Double-check nested data structures and the names of the keys for any mispellings.
- You can model your tests off of the Wave 01 tests for Tasks.
- Some tests use a [fixture](https://docs.pytest.org/en/6.2.x/fixture.html) named `one_goal` that is defined in `tests/conftest.py`. This fixture saves a specific goal to the test database.

## Code Coverage

Code coverage is a term used to describe how much application code is executed when a particular test suite is run. It is a good practice to check our code coverage in order to understand how much of our code is exercised by tests vs how much is still untested. A test suite with a high percentage of coverage is likely to be tested more thoroughly and have fewer bugs. A code coverage tool can partner with our testing suite to give us a report illustrating the coverage of our tests.

Given that Ada provided all tests cases in this project, we should anticipate high code coverage.

Review the [code coverage exercise](https://github.com/adaGold/code-coverage-exercise) on how to use `pytest-cov` to generate a code coverage report. We will need to change the directory where the application code is located from `student` to `app`.

`pytest --cov=app --cov-report html --cov-report term`

**We should have greater than 95% code coverage in our model and route files.**

# Requirements

## Goal Model

There should be a `Goal` model that lives in `app/models/goal.py`.

Goals should contain these attributes. Feel free to change the name of the `goal_id` column if you would like. **The tests require the title column to be named exactly** as `title`.

- `goal_id`: a primary key for each goal
- `title`: text to name the goal

### Tips

- Don't forget to run:
  - `flask db migrate` every time there's a change in models, in order to generate migrations
  - `flask db upgrade` to run all generated migrations

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
  "goal": {
    "id": 1,
    "title": "My New Goal"
  }
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

_This feature requires you to write a test._

### Get One Goal: One Saved Goal

As a client, I want to be able to make a `GET` request to `/goals/1` when there is at least one saved goal and get this response:

`200 OK`

```json
{
  "goal": {
    "id": 1,
    "title": "Build a habit of going outside daily"
  }
}
```

_This feature requires you to write a test._

### Get One Goal: No Matching Goal

As a client, I want to be able to make a `GET` request to `/goals/1` when there are no matching goals and get this response:

`404 Not Found`

No response body.

_This feature requires you to write a test._

### Update Goal

As a client, I want to be able to make a `PUT` request to `/goals/1` when there is at least one saved goal with this request body:

```json
{
  "title": "Updated Goal Title"
}
```

and get this response:

`200 OK`

```json
{
  "goal": {
    "id": 1,
    "title": "Updated Goal Title"
  }
}
```

### Update Goal: No Matching Goal

As a client, I want to be able to make a `PUT` request to `/goals/1` when there are no matching goals with this request body:

```json
{
  "title": "Updated Goal Title"
}
```

and get this response:

`404 Not Found`

No response body

### Delete Goal: Deleting a Goal

As a client, I want to be able to make a `DELETE` request to `/goals/1` when there is at least one saved goal and get this response:

`200 OK`

```json
{
  "details": "Goal 1 \"Build a habit of going outside daily\" successfully deleted"
}
```

### Delete Goal: No Matching Goal

As a client, I want to be able to make a `DELETE` request to `/goals/1` when there are no matching goals and get this response:

`404 Not Found`

No response body.

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
