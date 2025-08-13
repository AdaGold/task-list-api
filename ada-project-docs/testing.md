## Tests

We will need to complete part – or all – of some of the tests for this project. If a test is incomplete, it will raise an `Exception`. You should comment out the `Exception` when implementing the test. 

You may wish to review details about how to run tests [here](https://github.com/AdaGold/viewing-party#details-about-how-to-run-tests).

Recall that it is always a good idea to search the file for any `# @pytest.mark.skip` decorators you may have missed before moving to the next wave.

### Code Coverage

Code coverage is a term used to describe how much application code is executed when a particular test suite is run. It is a good practice to check our code coverage in order to understand how much of our code is exercised by tests vs how much is still untested. A test suite with a high percentage of coverage is likely to be tested more thoroughly and have fewer bugs. A code coverage tool can partner with our testing suite to give us a report illustrating the coverage of our tests.

Review the [code coverage exercise](https://github.com/adaGold/code-coverage-exercise) on how to use `pytest-cov` to generate a code coverage report. We will need to change the directory where the application code is located from `student` to `app`.

`pytest --cov=app --cov-report html --cov-report term`

There is not a specific code coverage percentage required for this project. Creating a code coverage report allows us to continue practicing the skill of reading the code coverage report and using it as part of our development workflow.