from app import app
from flask import render_template, request, redirect, url_for, flash
from flask import g
from engine import *
from models import *

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
        new_game = Game(field_size=NUM)
        db.session.add(new_game)
        db.session.commit()
        return render_template("game.html", field=field, data=DATA, pk=new_game.id, num=num)
    return render_template('first_page.html')


@app.route("/game<pk>/<move>/<line>:<point>")
def game(pk, move, line, point):
    game_playing = Game.query.filter(Game.id == pk)

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
    log = GameLog(parent=pk, move=int(data['moves']), line=int(line), point=int(point))
    db.session.add(log)
    db.session.commit()

    if check_winner(field):
        game_playing.winner = data['player']
        db.session.commit()

        flash(f"Переможець {data['player']}, на {data['moves']} ході")
    return render_template('game.html', field=field, data=DATA, pk=pk)


@app.route("/history/")
def history():
    games = Game.query.all()
    return render_template("history.html", games=games)


@app.route("/review/<pk>")
def review(pk):
    data = DATA
    log = GameLog.query.filter(GameLog.parent == pk)
    view_game = Game.query.filter(Game.id == pk).first()
    field = get_field(view_game.field_size)


    return render_template("review.html", log=log, game=view_game, data=data, field=field)


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





