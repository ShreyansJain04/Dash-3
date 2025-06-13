# Dash-3

This project is a Dash web application for state-wise and district-wise customer analytics, using data from `Updated_Transprioritybase (1).xlsx`.

## Features
- State and district selection
- Customer analytics and visualizations
- Search and export functionality
- Dark theme with modern UI

## Requirements
- Python 3.8+
- See below for dependencies

## Installation
1. Clone this repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install dash dash-bootstrap-components pandas plotly openpyxl gunicorn
   ```

## Running the App (Development)
To run the app in development mode:
```bash
python district_wise.py
```

## Running with Gunicorn (Production)
For production, use Gunicorn. First, ensure your `district_wise.py` exposes the server instance:

Add this at the end of `district_wise.py` (if not already present):
```python
server = app.server
```

Then run:
```bash
gunicorn district_wise:server
```

- By default, Gunicorn will serve on port 8000. To change the port:
  ```bash
  gunicorn -b 0.0.0.0:8050 district_wise:server
  ```

## File Structure
- `district_wise.py` - Main Dash app
- `Updated_Transprioritybase (1).xlsx` - Data file

## Notes
- Make sure the Excel file is present in the project directory.
- For best performance, use Gunicorn or another WSGI server in production.

## License
MIT