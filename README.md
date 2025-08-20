# Next.js & Flask Full-Stack Template

This project serves as a minimal template for building full-stack applications using Next.js for the frontend, Python with Flask for the backend and PostgresSQL for the database. It provides a basic setup for a task management application, allowing you to quickly get started with your own features.

## ✨ Features

- **Frontend**: Built with [Next.js](https://nextjs.org/), a popular React framework for building server-side rendered and static websites.
- **Backend**: A simple and lightweight RESTful API built with [Flask](https://flask.palletsprojects.com/), a micro web framework for Python.
- **CORS Enabled**: The Flask backend is configured with `Flask-CORS` to allow cross-origin requests from the frontend.
- **Database**: PostgreSQL with SQLAlchemy Core for database management.

- **RESTful API**: The backend exposes a set of RESTful endpoints for managing tasks (Create, Read, Update, Delete).

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Node.js](https://nodejs.org/) (v18.x or later recommended)
- [Python](https://www.python.org/downloads/) (v3.8 or later recommended)
- `pip` (Python package installer)
- `venv` (for creating virtual environments)

### Backend Setup (Flask)

1.  **Navigate to the server directory:**
    ```bash
    cd server
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The backend server will start on `http://127.0.0.1:5500`.

### Frontend Setup (Next.js)

1.  **Navigate to the frontend directory:**
    ```bash
    cd task-app-frontend
    ```

2.  **Install the required npm packages:**
    ```bash
    npm install
    ```

3.  **Run the Next.js development server:**
    ```bash
    npm run dev
    ```
    The frontend development server will start on `http://localhost:3000`.

## 📂 Project Structure

```
.
├── server/
│   ├── app.py              # Main Flask application file
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Python virtual environment
└── task-app-frontend/
    ├── src/
    │   └── app/
    │       ├── page.tsx    # Main page for the Next.js app
    │       └── layout.tsx  # Layout for the Next.js app
    ├── next.config.ts      # Next.js configuration
    └── package.json        # Node.js dependencies
```

## 📝 API Endpoints

The Flask backend provides the following API endpoints for managing tasks:

| Method | Endpoint             | Description                |
| ------ | -------------------- | -------------------------- |
| `GET`    | `/api/tasks`         | Get all tasks              |
| `POST`   | `/api/tasks`         | Create a new task          |
| `PUT`    | `/api/tasks/<id>`    | Update an existing task    |
| `DELETE` | `/api/tasks/<id>`    | Delete a task              |
| `GET`    | `/healthtest`        | Health check for the API   |

### Create Task Request Body Example

```json
{
    "title": "My New Task",
    "description": "This is a description for my new task."
}
```

## 🤝 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.