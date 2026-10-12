# Advanced Python Calculator
A professional command-line calculator built with Python using modular design, object-oriented programming (OOP), error handling, design patterns, pandas,input validation, logging, automated testing, and GitHub Actions.

## Features

- **Arithmetic operations:** Addition, subtraction, multiplication, division, power, and root.
- **Interactive REPL:** Perform calculations and manage the application through a command-line interface.
- **Input validation:** Handles invalid inputs and provides helpful error messages.
- **Error handling:** Uses appropriate exception handling to prevent common errors from crashing the application.
- **Design patterns:** Uses Strategy, Factory, Observer, Memento, and Facade patterns to keep the code organized and maintainable.
- **Calculation history:** Stores calculation records in a pandas DataFrame.
- **CSV storage:** Saves and loads calculation history from a CSV file.
- **Undo and redo:** Supports undoing and redoing previous calculations.
- **Logging:** Records application events, calculations, and errors in a log file.
- **Configuration:** Uses environment variables and a `.env` file to manage application settings.
- **Automated testing:** Uses pytest to test application functionality.
- **Continuous integration:** Uses GitHub Actions to run automated tests.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- pandas
- pytest
- pytest-cov
- python-dotenv
- Git and GitHub
- GitHub Actions

## Project Structure

```text
python-calculator-AOOP_1/
├── app/
│   ├── __init__.py
│   ├── calculator_repl.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger_config.py
│   └── operations.py
├── tests/
│   ├── __init__.py
│   ├── test_calculations.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   ├── test_logger_config.py
│   ├── test_operations.py
│   └── test_calculator_repl.py
├── .github/
│   └── workflows/
│       └── python-app.yml
├── .env
├── .gitignore
├── README.md
├── main.py
└── requirements.txt


```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd python-calculator-AOOP_1
```

Replace the repository URL with your GitHub repository URL.

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

`.env` for configuration settings.

Example configuration:

```env
CALCULATOR_HISTORY_FILE=calculator_history.csv
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_LOG_FILE=calculator.log
```

Keep `.env` out of version control if it contains local or sensitive configuration.

## Running the Calculator

Start the interactive calculator from the project root:

```bash
python -m app.calculator_repl
```
OR
```bash
python main.py
```
The calculator provides commands for performing calculations and managing the application.

| Command | Description |
|---|---|
| `help` | Displays available commands and instructions |
| `history` | Displays previous calculations |
| `undo` | Reverts the last supported action |
| `redo` | Restores an undone action |
| `save` | Saves calculation history |
| `load` | Loads saved calculation history |
| `clear` | Clears the displayed terminal output |
| `exit` | Exits the application |

The calculator also supports arithmetic operations such as addition, subtraction, multiplication, division, power, and root. Follow the prompts or help instructions displayed by your version of the application.

## Calculation History and Persistence

The calculator uses pandas to manage calculation history in a structured format.

- Calculation records can be saved to a CSV file.
- Saved history can be loaded in a later session.
- Automatic saving can be controlled through the application configuration.
- Undo and redo functionality helps manage supported changes.

The history filename and related settings can be configured through environment variables.

## Logging

The application uses Python's built-in `logging` module to help monitor activity and troubleshoot problems.

Logs can record events such as:

- Application startup and shutdown
- Commands entered by the user
- Successful calculations
- Input validation and calculation errors
- Problems encountered while saving or loading history

Log messages are written to the configured log file, such as `calculator.log`.

Logging helps developers understand what happened during a session without relying entirely on terminal print statements.

## Running Tests

Run the complete test suite from the project root:

```bash
pytest
```
OR

```bash
python -m pytest -v
```

Run a specific test module:

```bash
python -m pytest tests/test_calculations.py -v
```

Run tests with code coverage:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing
```

The coverage report shows which parts of the application are tested and identifies lines that still need test coverage.

## Continuous Integration

The project uses GitHub Actions to run automated tests when changes are pushed to GitHub or pull requests are created.

This helps identify problems early and keeps the application reliable as new features are added.

The workflow configuration is located at:

```text
.github/workflows/tests.yml
```

Check the workflow's configured coverage threshold to ensure it matches the assignment requirement of 100%.

## Design Patterns

This project applies several design patterns to improve code organization and maintainability.

| Pattern | Purpose |
|---|---|
| Strategy | Separates individual arithmetic operations into independent implementations |
| Factory | Creates or selects the appropriate operation |
| Observer | Allows interested components to respond to calculation events |
| Memento | Supports saving and restoring application state for undo and redo |
| Facade | Provides a simpler interface to the underlying calculator components |

These patterns help separate responsibilities, reduce dependencies between components, and make the application easier to test and extend.

## Error Handling

The calculator validates user input and handles common errors, including:

- Invalid commands or operation names
- Non-numeric input where numbers are required
- Division by zero
- Invalid mathematical operations, such as unsupported roots
- File errors while saving or loading history

It uses appropriate exception handling and input checks to provide meaningful feedback instead of allowing expected errors to terminate the application unexpectedly.

## Future Improvements

Possible improvements include:

- Adding more mathematical operations
- Improving the command-line interface
- Adding more unit and integration tests
- Maintaining complete line and branch coverage
- Improving log rotation and log formatting
- Adding automated code quality checks

## Learning Outcomes

This project provided practical experience with:

- Building a modular Python application
- Applying OOP concepts and design patterns
- Using abstract classes, inheritance, and polymorphism where appropriate
- Separating application logic into modules and packages
- Validating user input and handling exceptions
- Implementing calculation history and state management
- Adding logging for debugging and monitoring
- Writing automated tests with pytest
- Measuring code coverage
- Using GitHub Actions for continuous integration

## License

This project was created for learning and educational purposes.