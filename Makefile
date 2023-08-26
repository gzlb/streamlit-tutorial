# Use tabs for indentation in a Makefile

# Commands for managing the Docker container
.PHONY: build-docker run-docker stop-docker

# Build the Docker container
build-docker:
	docker build -t streamlit-crypto-app .

# Run the Docker container
run-docker:
	docker run -d -p 8501:8501 --name crypto-app streamlit-crypto-app

# Stop the Docker container
stop-docker:
	docker stop crypto-app
	docker rm crypto-app

# Commands for managing the virtual environment with Poetry
.PHONY: install-dev run-app

# Install development dependencies using Poetry
install-dev:
	poetry install --no-root

# Run the Streamlit app using Poetry
run-app:
	streamlit run main.py

