# DubsSampath
A lightweight full-stack sample workflow tracker for research labs

## Backend Setup (FastAPI)

1. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Use Scripts\activate on Windows
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the development server:

    ```bash
    uvicorn app.main:app --reload
    ```

4. Create a `.env` file in `/backend/` based on `.env.example`.


## Frontend Setup (React)

1. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the development server:

    ```bash
    npm start
    ```

4. Open http://localhost:3000 in your browser. You should the the React app running with the message: _Edit `src/App.js` and save to reload._

5. Add this import to `src/index.js` to include Boostrap styles globally:

    ```bash
    import 'bootstrap/dist/css/bootstrap.min.css';
    ```