from app import app
from flask import render_template, request, redirect, url_for, flash
from flask import g
from engine import *

FIELD = []
DATA = {"empty": '.', 'x': 'x', 'o': 'o', "moves": 0, "player": '.'}
NUM = 0


@app.route("/")
def page():
    num = request.args.get("num")
    if num:
        global NUM
        NUM = int(num)
        global FIELD
        FIELD = get_field(NUM)
        field = FIELD
        return render_template("game.html", field=field, data=DATA)
    return render_template('first_page.html')


@app.route("/game/<move>/<line>:<point>")
def game(move, line, point):
    if move == 0:
        field = getattr(g, 'field', None)
    else:
        field = FIELD
    data = DATA
    data['moves'] = int(move) + 1

    if data['moves'] % 2 == 0:
        data['player'] = "пан '0' "
    else:
        data['player'] = "пан 'X' "

    data['chord'] = f"{line}:{point}"
    field = update_field(field, int(move), int(line), int(point))
    if check_winner(field):
        flash(f"Переможець {data['player']}, на {data['moves']} ході")
    return render_template('game.html', field=field, data=DATA)


@app.route("/history/")
def history():
    return render_template("history.html")


@app.route("/refresh/")
def refresh():
    global NUM, DATA
    NUM = 0
    field = g.field
    DATA = {"empty": '.', 'x': 'x', 'o': 'o', "moves": 0}
    return redirect(url_for('page', field=field))


@app.before_request
def before_request():
    g.field = get_field(NUM)






    # data = {"field": get_field(int(num)), "num": int(num),
    #         "chord": "0", "empty": '.', 'x': 'x', 'o': 'o', "moves": 1}

    #
    # num = request.args.get("num")
    # if num:
    #     data = Game(field_num=num, field=get_field(int(num)))
    #     db.session.add(data)
    #     db.session.commit()
    #
    #     return render_template('game.html', data=data)
    # return render_template('first_page.html')

