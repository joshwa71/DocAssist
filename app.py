from flask import Flask, request, jsonify, render_template
from backend.core import run_llm # Replace with the name of your existing script file

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    technology = data.get('technology', 'pytorch')
    user_query = data['query']
    response = run_llm(user_query, technology)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
