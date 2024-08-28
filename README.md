# Teddy Challenge Documentation

![Python App Workflow](https://github.com/zembruzkill/teddy_challenge/actions/workflows/python-app.yml/badge.svg)

## Overview

This application is designed to fetch data from an external API, store the relevant data in a PostgreSQL database, and provide automated testing, linting, and formatting via GitHub Actions. The data is stored using SQLAlchemy, and the database migrations are managed using Alembic.

## Decision-Making Rationale

During the development of this application, several key decisions were made to ensure its robustness, maintainability, and ease of use:

1. **Use of Alembic for Migrations**:

   Alembic was chosen as the migration tool due to its seamless integration with SQLAlchemy, the ORM used in the project. Alembic allows for efficient management of database schema changes, ensuring that the database remains consistent and in sync with the application's models as they evolve over time.

2. **Pipenv for Dependency Management**:

   Pipenv was selected to manage the Python dependencies because it provides a reliable way to maintain a virtual environment and lock files (`Pipfile` and `Pipfile.lock`). This ensures that the application runs consistently across different environments and prevents "dependency hell."

3. **Docker for Database Management**:

   Docker was chosen to manage the PostgreSQL database environment. Using Docker ensures that the database setup is consistent and reproducible, avoiding discrepancies between different developers' environments. Docker Compose further simplifies the process of starting and stopping the database during development.

4. **GitHub Actions for CI/CD**:

   GitHub Actions was implemented for continuous integration and continuous deployment (CI/CD). This automation ensures that every push or pull request triggers automated tests, linting, and formatting checks, thus maintaining code quality and preventing potential issues from being merged into the main branch.

## Setup

### Prerequisites

- **Python 3.12+**: Ensure you have Python installed.
- **Pipenv**: Used for managing the virtual environment and dependencies.
- **Docker**: Used for running the PostgreSQL database.
- **Git**: For version control.
- **Make**: Used for running automation scripts.

### Clone the Repository

```bash
git clone https://github.com/zembruzkill/teddy_challenge.git
cd teddy_challenge
```

### Environment Setup

1. **Create a `.env` file** in the root directory of the project and add the following environment variables:

```
HOST=YOUR_DATABASE_HOST        # Database host name
DB_PORT=YOUR_DATABASE_PORT        # Database port
DB_USER=YOUR_DATABASE_USER     # Database username
DB_PASSWORD=YOUR_DATABASE_PASSWORD  # Database user's password
DB_NAME=YOUR_DATABASE_NAME     # Name of the database to be used
```

1. **Set Up Virtual Environment**:

   Use Pipenv to create and activate a virtual environment:

   ```bash
   pipenv install --dev
   pipenv shell
   ```

   or using make:

   ```bash
   make setup_venv
   ```

### Database Setup

1. **Start PostgreSQL with Docker**:

   Use Docker Compose to start the PostgreSQL database:

   ```bash
   docker-compose up -d
   ```

   or using make:

   ```bash
   make setup_db
   ```

2. **Apply Database Migrations**:

   Run Alembic to apply the database migrations:

   ```bash
   pipenv run alembic upgrade head
   ```

   or using make:

   ```bash
   make migrate
   ```

### Complete Setup in One Command

To set up the virtual environment, start the database, and apply migrations in one step:

```bash
make setup_all
```

## Running the Application

To run the application, execute the following command:

```bash
pipenv run python3 -m app.main
```

or if you are inside the virtual env simply run:

```bash
python3 -m app/main.py
```

or using make:

```bash
make run
```

This command will fetch data from the API and store it in the PostgreSQL database.

## Testing and Linting

### Running Tests

The application includes automated tests to ensure functionality. To run the tests:

```bash
pipenv run pytest
```

or using make

```bash
make test
```

💡 **The application includes tests that cover various layers of the system:**

- **Creation and Persistence Tests**: Verify that instances of the `Teddy360` model are correctly created and stored in the database. These tests use an in-memory SQLite database to ensure the ORM (SQLAlchemy) behaves as expected.
- **API Mocking**: Tests simulate API responses to verify that the data is correctly processed and stored. The API responses are mocked using `unittest.mock.patch`, ensuring that the tests do not rely on actual external calls.
- **Database Integration Tests**: Ensure that the data returned by the API is correctly filtered and stored in the database. These tests validate that only completed items are saved, ensuring data integrity.

### Linting and Formatting

Linting is done using Flake8, and formatting is done using Black. Both can be run as follows:

```bash
pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pipenv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

pipenv run black .
```

or using make

```bash
make lint
make format
```

## Makefile

The Makefile provides a convenient way to automate common tasks. Below are all available commands:

```makefile
.PHONY: all test lint format run deploy setup_db migrate clean

# Default target
all: format lint test

setup_all: setup_venv setup_db migrate

# Create a virtual environment
setup_venv:
	@echo "Setting up virtual environment..."
	pipenv install --dev

# Run Docker Compose to start the database
setup_db:
	@echo "Starting database with Docker Compose..."
	docker-compose up -d

# Perform migrations
migrate:
	@echo "Running migrations..."
	pipenv run alembic upgrade head

# Run linters
lint:
	@echo "Running linters..."
	pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	pipenv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run tests
test:
	@echo "Running tests..."
	pipenv run pytest

# Format code
format:
	@echo "Formatting code..."
	pipenv run black .

# Start the environment (example command)
run:
	@echo "Starting the environment..."
	pipenv run python -m app.main

# Clean up
clean:
	@echo "Stopping and removing Docker containers..."
	docker-compose down

```

## GitHub Actions CI

The project includes a GitHub Actions configuration file (`.github/workflows/python-app.yml`) to automate testing, linting, and formatting on each push or pull request to the `main` branch.

## Logging

The application uses Python's built-in logging module to provide detailed information about the data processing steps. Logs include information about the start and completion of data storage, any errors encountered, and the closing of database sessions.

## FAQ

### What should I do if the database connection fails?

Ensure that the Docker container is running, and that the environment variables in the `.env` file match your local setup. Use `docker-compose logs` to check for any errors.

### How do I add new database migrations?

1. Modify your SQLAlchemy models as needed.
2. Generate a new migration script with:

   ```bash
   pipenv run alembic revision --autogenerate -m "Migration description"
   ```

3. Apply the migration with:

   ```bash
   pipenv run alembic upgrade head
   ```

   or using make:

   ```bash
   make migrate
   ```
