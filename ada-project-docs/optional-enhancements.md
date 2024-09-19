# Optional Enhancements

## Goal

Optional enhancements are meant to spark our imagination! They can give us extra ideas for how to extend this project. Optional enhancements should never compromise the project requirements, unless there are special circumstances.

## Optional Means Optional

It is more important and more valuable to do good work with the requirements, and to solidify your learning. Please do not work on optional enhancements before feeling confident in the project requirements.

## Prompts

### Edge Cases

Many waves are missing many edge case considerations. Consider different edge cases in each wave, make decisions for what should happen, and then implement it!

As inspiration, here are some beginning edge cases to consider:

What should happen if...

- when creating a task, the value of `completed_at` is a string that is not a datetime?
- when updating a task, the value of `completed_at` is a string that is not a datetime?
- when getting all tasks, and using query params, the value of `sort` is not "desc" or "asc"?

For each of these, consider what the HTTP response should be.

How would you write tests for it? How would you implement it?

Your decisions should not break the other tests.

### Model Instance Methods

We can define instance methods in our model classes.

Consider places in your code that deal with one model at a time. Is there any repeated logic or behavior?

Here are some ideas to start:

- Create an instance method in `Task` named `to_dict()`
    - Converts a `Task` instance into JSON
    - Returns a Python dictionary in the shape of the JSON our API returns in the `GET` `/tasks` route
- Create a class method in `Task` named `from_json()`
    - Converts JSON into a new instance of `Task`
    - Takes in a dictionary in the shape of the JSON our API receives in the create and update routes
    - Returns an instance of `Task` 

### Use List Comprehensions

Use list comprehensions in your route functions where applicable.

### Route Helper Methods

If you have not already refactored your route files to use helper methods, do so now!

Consider code with complex or repetitive logic, and refactor it into helper methods. Watch your route files become cleaner and more readable!

### More Query Params

Create the tests and implementation so that the user may

- filter tasks by title
- sort tasks by id
- sort goals by title
