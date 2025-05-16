🛠️ Mulesoft to AWS: Complex API Migration
This project automates the migration of 160 complex API definitions from a Mulesoft source system to a simulated AWS destination. 
Each API record includes HTTP method details, authentication metadata, webhooks, pagination, and error-handling structures. During migration, a unique migration_id is attached to each record for traceability.
The project ensures high data reliability through backup creation, retry logic for failures, and detailed per-record logging. After migration, the data is validated using a separate testing script that confirms record count, field integrity, and ID match.
A color-coded HTML report is then generated using Selenium or Pytest to visually represent the success or failure of the migration.

📁 Project Structure
Mulesoft/ – Original and backup API files
AWS/ – Destination for migrated APIs
Migration.py – Handles migration with retries and logging
Testing.py – Validates migration success
migration_log.json – Full execution details
migration_selenium_test_report.html – Visual test report
README.md – Project documentation

🚀 How to Run
Run Migration.py to migrate data
Run Testing.py to verify the migration
Open migration_selenium_test_report.html to view the report

✅ Features
Adds migration_id to each API record
Retries failed migrations up to 3 times
Tracks and logs duration, errors, and status per record
Creates a JSON log and a visual HTML test report
Supports validation with both Selenium and Pytest

📦 Requirements
Python 3.8+
selenium
pytest
pytest-html

Install all dependencies using:

bash
pip install -r requirements.txt

🙌 Author
Developed by venkyvenkatesh10 to simulate and automate the end-to-end migration and validation of complex API data from legacy systems to cloud infrastructure.
