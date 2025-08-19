# IMPORTS - Similar to require() in Node.js
from flask import Flask, request, jsonify  # Like: const express = require('express')
from flask_cors import CORS                # Like: const cors = require('cors')
import os                                  # Like: const os = require('os') or process.env
from datetime import datetime              # Like: const { DateTime } = require('luxon') or new Date()

# APP INITIALIZATION - Like: const app = express()
app = Flask(__name__)

# MIDDLEWARE - Like: app.use(cors())
CORS(app)

# GLOBAL VARIABLES - Like declaring variables outside routes in Express
# In Express you might do: let tasks = []; let taskIdCounter = 1;
tasks = []
task_id_counter = 1

# ROUTE DEFINITIONS - Similar to app.get(), app.post(), etc. in Express
# Express equivalent: app.get('/', (req, res) => { res.json({message: "Task API is running!"}) })
@app.route('/healthtest', methods=['GET'])
def health_check():
    return jsonify({"message": "Task API is running!"})

@app.route('/', methods=['GET'])
def home():
    html_content = """
    <html>
    <head>
        <title>Task API</title>
    </head>
    <body>
        <h1>Task API</h1>
        <p>This is the home page of the Task API.</p>
    </body>
    </html>
    """
    return html_content, 200, {'Content-Type': 'text/html'}

# GET ALL TASKS - Express: app.get('/api/tasks', (req, res) => { res.json(tasks) })
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)  # Like: res.json(tasks)

# CREATE TASK - Express: app.post('/api/tasks', (req, res) => { ... })
@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter  # Python needs this to modify global vars (Express doesn't need this)
    
    # GET REQUEST BODY - Like: const data = req.body in Express
    data = request.get_json()
    
    # VALIDATION - Same concept as Express validation
    # Express: if (!data || !data.title) { return res.status(400).json({error: "Title required"}) }
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400  # Status code after comma
    
    # CREATE OBJECT - Same as JavaScript object creation
    # Express: const task = { id: taskIdCounter++, title: data.title, ... }
    task = {
        "id": task_id_counter,
        "title": data['title'],                           # Like: data.title
        "description": data.get('description', ''),       # Like: data.description || ''
        "completed": False,                               # Python uses False, JS uses false
        "created_at": datetime.now().isoformat()          # Like: new Date().toISOString()
    }
    
    # ADD TO ARRAY - Like: tasks.push(task)
    tasks.append(task)
    task_id_counter += 1  # Like: taskIdCounter++
    
    # RETURN RESPONSE - Like: res.status(201).json(task)
    return jsonify(task), 201  # 201 status code for created

# UPDATE TASK - Express: app.put('/api/tasks/:taskId', (req, res) => { ... })
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])  # <int:task_id> = req.params.taskId
def update_task(task_id):  # Function receives the URL parameter
    data = request.get_json()  # Like: const data = req.body
    
    # FIND TASK - Python's way of: tasks.find(t => t.id === taskId)
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    # ERROR HANDLING - Like: if (!task) return res.status(404).json({error: "Not found"})
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    # UPDATE FIELDS - Like: task.title = data.title || task.title
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['completed'] = data.get('completed', task['completed'])
    
    return jsonify(task)  # Like: res.json(task)

# DELETE TASK - Express: app.delete('/api/tasks/:taskId', (req, res) => { ... })
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks  # Need this to reassign the global tasks array
    
    # FILTER OUT TASK - Like: tasks = tasks.filter(t => t.id !== taskId)
    tasks = [t for t in tasks if t['id'] != task_id]  # Python list comprehension
    
    return jsonify({"message": "Task deleted"})  # Like: res.json({message: "Task deleted"})

# SERVER STARTUP - Like: app.listen(PORT, () => console.log(`Server running on ${PORT}`))
if __name__ == '__main__':  # Python's way of "only run if this file is executed directly"
    port = int(os.environ.get('PORT', 5500))  # Like: process.env.PORT || 5000
    app.run(host='0.0.0.0', port=port, debug=False)  # Like: app.listen(port, '0.0.0.0')