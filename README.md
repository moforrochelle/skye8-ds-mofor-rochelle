# SKYE8 Health No-Show Prediction

This project analyses healthcare appointment attendance patterns and focuses on predicting healthcare appointment no-shows

## Project Goals

- Load and validate healthcare data
- Build a PostgreSQL database
- Analyse appointment attendance
- Build classification models
- Choose a prediction threshold using real-world costs

## Development Setup

Create and activate a Python virtual environment before installing the project dependencies.

Install the required packages with:

    pip install -r requirements.txt

Project data is stored outside version control, and database credentials must be supplied through environment variables.

## Security and Data Handling

Raw project data must remain outside version control.

Database credentials and connection details must never be hard-coded in source code or committed to the repository. They must be supplied through environment variables.

The `.env` file is excluded from Git through `.gitignore`.

## Project Structure

text
data/          Project data, excluded from version control
src/           Reusable Python source code
sql/           PostgreSQL schema and query scripts
notebooks/     Jupyter notebooks for analysis and modelling
tests/         Automated tests
reports/       Project documentation and reports
README.md      Project documentation
requirements.txt  Python dependencies
.gitignore     Files excluded from version control



## Database

This project uses PostgreSQL installed and running locally through Postgres.app during development.

Database connection details are provided through environment variables and are not stored in the repository.