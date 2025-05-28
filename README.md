# DubsSampath
A lightweight full-stack sample workflow tracker for research labs

## Backend Setup (FastAPI)

1. Create a virtual environment:

    'python3 -m venv venv'
    'source venv/bin/activate  # Use Scripts\activate on Windows'

2. Install dependencies:

    'pip install -r requirements.txt'

3. Run the development server:

    'uvicorn app.main:app --reload'

4. Create a .env file in /backend/ based on .env.example.