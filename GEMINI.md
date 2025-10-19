# GEMINI.md - Formazing Project

## Project Overview

This project, "Formazing," is a Flask-based web application designed to streamline the management of training sessions. It uses Notion as a database to store training information, and it automates the process of creating Teams meetings, sending email and Telegram notifications, and collecting feedback.

The application is designed with a clear separation of concerns, with services for Notion, Microsoft Graph (Teams and email), and Telegram. The frontend is built with Jinja2 templates, following an atomic design structure.

**Key Technologies:**

*   **Backend:** Python, Flask
*   **Database:** Notion
*   **Communication:** Microsoft Graph API (Teams, Email), Telegram Bot API
*   **Frontend:** Jinja2, HTML, CSS
*   **Dependencies:** See `requirements.txt` for a full list.

## Building and Running

### 1. Prerequisites

*   Python 3.x
*   `pip` for package management

### 2. Installation

1.  **Clone the repository.**
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

1.  Create a `.env` file in the root directory of the project.
2.  Add the following environment variables to the `.env` file, filling in the values for your specific setup:

    ```
    FLASK_SECRET_KEY='a-strong-secret-key'
    FLASK_BASIC_AUTH_USERNAME='your-username'
    FLASK_BASIC_AUTH_PASSWORD='your-password'

    TELEGRAM_BOT_TOKEN='your-telegram-bot-token'

    NOTION_TOKEN='your-notion-integration-token'
    NOTION_DATABASE_ID='your-notion-database-id'

    MICROSOFT_CLIENT_ID='your-azure-app-client-id'
    MICROSOFT_CLIENT_SECRET='your-azure-app-client-secret'
    MICROSOFT_TENANT_ID='your-azure-tenant-id'
    MICROSOFT_USER_EMAIL='your-email@example.com'
    ```

### 4. Running the Application

To start the Flask development server, run the following command in a terminal:

```bash
python run.py
```

The application will be available at `http://localhost:5000`.

### 5. Running the Telegram Bot

To run the Telegram bot, open a **second terminal** and run the following command:

```bash
python run_bot.py
```

This will start a separate process to handle Telegram bot commands.

## Development Conventions

*   **Code Style:** The project follows the PEP 8 style guide for Python code.
*   **Modularity:** The application is structured into modules and services to promote separation of concerns and reusability.
*   **Atomic Design:** The frontend templates are organized using the atomic design methodology, with atoms, molecules, organisms, and pages.
*   **Configuration:** All configuration is managed through the `config.py` file and environment variables.
*   **Error Handling:** The application includes specific error handling for services like Notion and TrainingService.
*  **Logging:** The application uses Python's built-in logging module for logging important events and errors.
*   **Documentation:** The codebase is documented with docstrings and comments to explain complex logic and workflows. Do not reduce documentation quality and quantity. Do not touch docstrings or comments.

## Testing

The project includes a comprehensive test suite using `pytest`.

### Running Tests

To run the tests, use the following command:

```bash
pytest
```

This will run all tests except those marked as `real_telegram`, which send actual messages.

To run a specific test or group of tests, you can use `pytest` with the `-k` flag or markers defined in `pytest.ini`. For example, to run only the Notion tests, you can use:

```bash
pytest -m notion
```

### Quick Test Scripts

The project provides `quick_test.bat` (for Windows) and `quick_test.sh` (for macOS/Linux) scripts for running common test scenarios. Here are some of the most useful commands:

*   `quick_test.bat unit` or `./quick_test.sh unit`: Runs all unit tests.
*   `quick_test.bat notion` or `./quick_test.sh notion`: Runs tests for the Notion service.
*   `quick_test.bat config` or `./quick_test.sh config`: Verifies the connections to Notion and Telegram.
*   `quick_test.bat workflow` or `./quick_test.sh workflow`: Runs a full, safe simulation of the training creation workflow.
*   `quick_test.bat all` or `./quick_test.sh all`: Runs a comprehensive pre-commit suite of tests.

For a full list of available commands, run `quick_test.bat` or `./quick_test.sh` with no arguments.

### Test Structure

The tests are organized into the following directories:

*   `tests/unit`: Unit tests for individual components.
*   `tests/integration`: Integration tests for multiple components.
*   `tests/e2e`: End-to-end tests that simulate user workflows.
*   `tests/fixtures`: Pytest fixtures for setting up test data and resources.
*   `tests/mocks`: Mock objects for external services.
