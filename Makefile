.PHONY: format check-format lint test install-dev install-hooks

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Install pre-commit hooks
install-hooks:
	pre-commit install

# Format code with Black
format:
	black .

# Check code formatting without making changes
check-format:
	black --check --diff .

# Run linting
lint:
	flake8 .

# Run tests
test:
	python -m pytest

# Run all quality checks
check: check-format lint test

# Setup development environment
setup: install-dev install-hooks
	@echo "Development environment setup complete!"
	@echo "Run 'make check' to verify everything is working."
