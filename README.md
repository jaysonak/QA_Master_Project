# QA Master Project: Multi-Framework CI/CD Pipeline

A professional-grade QA Automation project showcasing a synchronized testing ecosystem using **Selenium**, **Playwright**, and **GitHub Actions**.

## 🚀 Overview
This project validates a custom Flask-based Fintech application. It demonstrates the ability to handle complex automation challenges including:
- **Synchronization**: Using Explicit Waits to handle asynchronous UI updates.
- **Cross-Framework Testing**: Combining Selenium's industry-standard POM with Playwright's speed.
- **Continuous Integration**: A fully automated pipeline that triggers on every code push.

## 🛠️ Tech Stack
- **Web App**: Python Flask, SQLAlchemy (SQLite).
- **Automation**: Selenium WebDriver (Python), Playwright.
- **Infrastructure**: GitHub Actions (Ubuntu-latest), GitHub Desktop.
- **Design Pattern**: Page Object Model (POM).

## 🧪 Testing Categories
### Regression Suite (Selenium)
- `test_successful_login`: Validates core authentication path.
- `test_invalid_login`: Ensures robust error handling for failed auth.
- `test_currency_transfer`: Validates complex UI interactions and state changes.

### Data Integrity Suite (Playwright)
- `test_database_integrity`: Directly queries the backend to ensure UI actions reflect correctly in the database.

## 🤖 CI/CD Integration
The project uses a custom GitHub Actions workflow (`main.yml`) to:
1. Spin up a headless Linux environment.
2. Initialize a background Flask server.
3. Execute the full test suite in **Headless Mode** with optimized window-sizing for cloud consistency.

## ⚙️ Setup & Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize Playwright: `playwright install`
4. Run tests locally: `python -m pytest tests/ -v`