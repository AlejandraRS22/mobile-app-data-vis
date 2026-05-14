# Session 12 - Mobile Field Report App

This Streamlit app simulates a mobile scientific field-reporting workflow.

## Features

- Researcher name, discovery title, and observation notes
- GPS location capture with coordinates
- Map display of the observation location
- Photo evidence using camera input or image upload
- PDF report generation
- Required-field validation and graceful error handling
- Custom Streamlit theme using `.streamlit/config.toml`

## How to run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files to upload to GitHub

```text
mobile-app-data-vis/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

## Deployment

Deploy the repository on Streamlit Cloud and set `app.py` as the main file.
