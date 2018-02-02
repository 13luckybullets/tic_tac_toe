from flask import Flask, render_template, request, redirect
from engine import *

app = Flask(__name__, static_url_path='/static')


DATA = {'field': get_field(), "chord": "0", "empty": '.', 'x': 'x', 'o': 'o', "moves": 1}


@app.route("/game/<move>/<line>:<point>")
def game(move, line, point):
    data = DATA
    data['moves'] = int(move) + 1
    data['chord'] = f"{line}:{point}"
    data['field'] = update_field(data['field'], int(move), int(line), int(point))
    if check_winner(data['field']):
        return render_template('move.html')
    return render_template('base.html', data=data)


@app.route("/")
def page():
    data = {'field': get_field(), "chord": "0", "empty": '.', 'x': 'x', 'o': 'o', "moves": 1}
    return render_template('base.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)