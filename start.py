from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index(task="Python"):
    return render_template('task.html', task=task)


app.run(debug=True, port=8000, host='0.0.0.0')