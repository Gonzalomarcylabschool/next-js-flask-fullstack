'use client';

import { useState, useEffect } from 'react';

// Define the Task type
interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
}

const API_URL = 'http://127.0.0.1:5500/api/tasks';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  // Fetch tasks from the API
  const fetchTasks = async () => {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error(error);
    }
  };

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  // Handle form submission to create a new task
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title) {
      alert('Title is required');
      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        throw new Error('Failed to create task');
      }

      // Clear form and refetch tasks
      setTitle('');
      setDescription('');
      fetchTasks();
    } catch (error) {
      console.error(error);
    }
  };

  // Handle task deletion
  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete task');
      }
      
      // Refetch tasks
      fetchTasks();
    } catch (error) {
      console.error(error);
    }
  };

  // Handle toggling task completion status
  const toggleComplete = async (task: Task) => {
    try {
      const response = await fetch(`${API_URL}/${task.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !task.completed }),
      });

      if (!response.ok) {
        throw new Error('Failed to update task');
      }

      // Refetch tasks
      fetchTasks();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-white shadow">
        <div className="max-w-4xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">Task Management App</h1>
        </div>
      </header>
      <main className="max-w-4xl mx-auto py-6">
        <div className="px-4">
          {/* New Task Form */}
          <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow mb-8">
            <h2 className="text-2xl font-bold mb-4">Create a New Task</h2>
            <div className="mb-4">
              <label htmlFor="title" className="block text-gray-700 font-bold mb-2">Title</label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter task title"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="description" className="block text-gray-700 font-bold mb-2">Description</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter task description"
              />
            </div>
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              Add Task
            </button>
          </form>

          {/* Task List */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold mb-4">Tasks</h2>
            <ul>
              {tasks.length > 0 ? (
                tasks.map((task) => (
                  <li key={task.id} className={`flex items-center justify-between p-4 mb-2 rounded-lg ${task.completed ? 'bg-green-100' : 'bg-yellow-100'}`}>
                    <div className="flex-1">
                      <h3 className={`text-lg font-bold ${task.completed ? 'line-through text-gray-500' : ''}`}>{task.title}</h3>
                      <p className={`text-gray-600 ${task.completed ? 'line-through' : ''}`}>{task.description}</p>
                    </div>
                    <div className="flex items-center">
                      <button
                        onClick={() => toggleComplete(task)}
                        className={`mr-2 font-bold py-1 px-3 rounded ${task.completed ? 'bg-yellow-500 hover:bg-yellow-700 text-white' : 'bg-green-500 hover:bg-green-700 text-white'}`}
                      >
                        {task.completed ? 'Undo' : 'Complete'}
                      </button>
                      <button
                        onClick={() => handleDelete(task.id)}
                        className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded"
                      >
                        Delete
                      </button>
                    </div>
                  </li>
                ))
              ) : (
                <p>No tasks yet. Add one above!</p>
              )}
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
