from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory task store
tasks = []
task_id_counter = 1

@app.route('/')
def home():
    return jsonify({
        "app": "Task Manager API",
        "message": "Manage your tasks easily 🚀"
    })

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    global task_id_counter
    
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": task_id_counter,
        "title": data['title'],
        "completed": False
    }

    tasks.append(task)
    task_id_counter += 1

    return jsonify(task), 201

# Mark task as completed
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks

    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"message": "Task deleted"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
