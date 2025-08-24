# IMPORTS
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import text
from db import engine  # Import the engine from our db.py

# Load environment variables from .env file
load_dotenv()

# APP INITIALIZATION
app = Flask(__name__)

# MIDDLEWARE
CORS(app)

# Helper function to convert SQLAlchemy Row to a dictionary
def row_to_dict(row):
    return dict(row._mapping)

# ROUTE DEFINITIONS
@app.route('/healthtest', methods=['GET'])
def health_check():
    return jsonify({"message": "Task API is running!"})

@app.route('/', methods=['GET'])
def home():
    html_content = "<html><head><title>Task API</title></head><body><h1>Task API</h1><p>This is the home page of the Task API.</p></body></html>"
    return html_content, 200, {'Content-Type': 'text/html'}

# GET ALL TASKS
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tasks ORDER BY created_at DESC"))
        tasks = [row_to_dict(row) for row in result]
        return jsonify(tasks)

# CREATE TASK
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    with engine.connect() as conn:
        try:
            query = text(
                "INSERT INTO tasks (title, description, completed) VALUES (:title, :description, :completed) RETURNING id, title, description, completed, created_at"
            )
            result = conn.execute(
                query,
                {
                    "title": data['title'],
                    "description": data.get('description', ''),
                    "completed": data.get('completed', False)
                }
            )
            new_task = result.fetchone()
            conn.commit()
            return jsonify(row_to_dict(new_task)), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500

# UPDATE TASK
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    
    with engine.connect() as conn:
        try:
            # First, check if the task exists
            find_query = text("SELECT * FROM tasks WHERE id = :id")
            result = conn.execute(find_query, {"id": task_id})
            task = result.fetchone()

            if not task:
                return jsonify({"error": "Task not found"}), 404
            
            # Get current values
            current_task = row_to_dict(task)
            
            # Prepare the update query
            update_fields = []
            params = {"id": task_id}
            
            if 'title' in data:
                update_fields.append("title = :title")
                params['title'] = data['title']
            
            if 'description' in data:
                update_fields.append("description = :description")
                params['description'] = data['description']

            if 'completed' in data:
                update_fields.append("completed = :completed")
                params['completed'] = data['completed']
            
            if not update_fields:
                return jsonify(current_task) # No changes, return current task

            query = text(
                f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = :id RETURNING id, title, description, completed, created_at"
            )
            
            result = conn.execute(query, params)
            updated_task = result.fetchone()
            conn.commit()

            return jsonify(row_to_dict(updated_task))
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500

# DELETE TASK
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with engine.connect() as conn:
        try:
            query = text("DELETE FROM tasks WHERE id = :id RETURNING id")
            result = conn.execute(query, {"id": task_id})
            
            if result.rowcount == 0:
                return jsonify({"error": "Task not found"}), 404
            
            conn.commit()
            return jsonify({"message": "Task deleted"})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500

# SERVER STARTUP
if __name__ == '__main__':
    # The create_table function could be called here on startup,
    # but it's often better to manage schema with migration tools.
    # For this example, we'll assume the table is created manually or via `python db.py`.
    app.run(host='0.0.0.0', port=5500, debug=False)