from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # Looks for templates/index.html

@app.route('/get_words', methods=['POST'])
def get_words():
    data = request.get_json()
    color_string = data.get('colors', '')
    if len(color_string) != 30:
        return jsonify({"Response":400,"Message": "Color string must be 30 characters","Solution":[]})

    # Generate or look up the words based on the color string
    words = main(color_string)
    return words

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
    # serve(app, host='0.0.0.0', port=8080,_quiet=False)
