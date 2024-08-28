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
