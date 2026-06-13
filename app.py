from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage
todos = []
next_id = 1

# FLAW 1: Tidak ada validasi input — title boleh kosong atau None
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    global next_id
  todo = {
    'id': next_id,
    'title': data['title'],
    'done': False,
    'created_at': datetime.now().isoformat()    # ← diubah jadi string format ISO 8601
}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

# FLAW 3: Logika update salah — selalu set done=True, tidak bisa set ke False
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body tidak boleh kosong'}), 400

    for todo in todos:
        if todo['id'] == todo_id:
            # Update hanya field yang dikirim, sisanya tetap
            if 'done' in data:
                todo['done'] = data['done']     # ← ambil dari request, bisa True atau False
            if 'title' in data and data['title'].strip():
                todo['title'] = data['title'].strip()
            return jsonify(todo)

    return jsonify({'error': 'Todo tidak ditemukan'}), 404

# FLAW 4: Endpoint delete tidak mengembalikan response yang benar
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            todos.pop(i)
            return jsonify({'message': f'Todo {todo_id} berhasil dihapus'}), 200  # ← ada response + status code

    return jsonify({'error': 'Todo tidak ditemukan'}), 404   # ← handle kalau id tidak ada                   # Harusnya return response + status code 204

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

if __name__ == '__main__':
    app.run(debug=True)
