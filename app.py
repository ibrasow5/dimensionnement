import math
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculer', methods=['POST'])
def calculer():
    data = request.get_json()
    Pt = data.get('Pt')
    d = data.get('d')
    f = data.get('f')
    Le = data.get('Le')
    Gt = data.get('Gt')
    Gr = data.get('Gr')

    Lp = 20 * (math.log10(d) + math.log10(f)) + 32.44
    Pr = Pt + Gt + Gr - Lp - Le

    return jsonify({'Pr': Pr})

if __name__ == '__main__':
    app.run(debug=True)
