# Patient Search Tool

A simple Flask web application that allows users to search for patients using the [HAPI FHIR R4 public server](https://hapi.fhir.org/baseR4).

## Features

- **Patient Search**: Search for patients by name.
- **Data Display**: Shows Patient ID, Name, Gender, and Birth Date.
- **Fail-safe Mode**: Automatically falls back to mock data if the FHIR server is offline or unreachable.
- **Responsive Design**: Built with Bootstrap 5 for a clean, mobile-friendly interface.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- `pip` (Python package installer)

## Installation

1.  Clone or download this repository.
2.  Navigate to the project directory:
    ```bash
    cd health-informatics-fhir
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Start the Flask application:
    ```bash
    python app.py
    ```
2.  Open your web browser and go to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
3.  Enter a name (e.g., "Smith") in the search bar and click **Search**.

## Project Structure

- `app.py`: Main Python Flask application containing backend logic and FHIR integration.
- `templates/`: HTML templates for the application.
    - `base.html`: Base layout template with Bootstrap.
    - `index.html`: Main interface for search and results.
- `requirements.txt`: List of Python dependencies.

## APIs Used

- **HAPI FHIR R4**: `https://hapi.fhir.org/baseR4/Patient`

## License

This project is open source.
