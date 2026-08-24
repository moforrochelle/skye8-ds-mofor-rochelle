# SKYE8 Health No-Show Prediction

This project analyses healthcare appointment attendance patterns and focuses on predicting healthcare appointment no-shows

## Project Goals

* Load and validate healthcare appointment data
* Build a PostgreSQL database with appropriate keys and constraints
* Answer operational questions using SQL
* Analyse appointment attendance and no-show patterns
* Build and compare classification models
* Select a prediction threshold using operational costs
* Test the loading, feature-building, and threshold functions

## Development Setup

Create and activate a Python virtual environment before installing the project dependencies.

Install the required packages with:

```
pip install -r requirements.txt
```

The project uses PostgreSQL installed locally through Postgres.app during development.

Database connection details are supplied through environment variables and are not stored in the repository.

To run the automated tests:

```
python -m pytest
```

## Security and Data Handling

Raw project data is stored in `data/` and excluded from version control.

Database credentials and connection details must never be hard-coded in source code or committed to the repository. They are supplied through environment variables.

The `.env` file, raw data, virtual environment, and other local files are excluded through `.gitignore`.

## Project Structure

```
data/              Raw project data, excluded from version control
src/               Reusable Python source code
sql/               PostgreSQL schema and analytical queries
notebooks/         Jupyter notebooks for analysis and modelling
tests/             Automated tests
reports/           Project documentation and findings
README.md          Project documentation
requirements.txt   Python dependencies
.gitignore         Files excluded from version control
```

## Database

The project uses PostgreSQL for the database stage.

The database schema is defined in `sql/schema.sql`. The SQL exercises and analytical queries are stored in `sql/exercises.sql` and `sql/analytics.sql`.

The data-loading pipeline handles inconsistent date formats, distances containing units, different boolean representations, and duplicated identifiers. The load process is designed to be idempotent.

## Classification

Four classifiers were evaluated for appointment no-show prediction:

* Logistic Regression
* Decision Tree
* K-Nearest Neighbours
* Naive Bayes

Because no-shows are the minority class, model performance was evaluated using accuracy, precision, recall, F1 score, and Precision-Recall AUC rather than relying on accuracy alone.

Logistic Regression achieved the highest PR-AUC among the models tested and was selected for threshold optimisation. Precision-Recall was given particular emphasis because it provides a more informative view of classifier performance when the positive class is imbalanced (Saito & Rehmsmeier, 2015).

Probability calibration was also evaluated using Platt scaling, following the probability-calibration methods discussed by Niculescu-Mizil and Caruana (2005).

The modelling table was reduced from **35.1 MB to 11.9 MB**, representing a **66.09% reduction** in memory usage and exceeding the required 50% reduction.

**Recommended threshold: 0.11, implying approximately 59 reminder calls per week under the project's cost assumptions.**

Detailed classification results, threshold calculations, and calibration findings are available in `reports/classification_findings.md`.

## References

* Saito, T. & Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets*. PLOS ONE, 10(3), e0118432. https://doi.org/10.1371/journal.pone.0118432
* Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting Good Probabilities With Supervised Learning*. Proceedings of the 22nd International Conference on Machine Learning, 625–632.
* PostgreSQL Global Development Group. *PostgreSQL Documentation*. https://www.postgresql.org/docs/current/
