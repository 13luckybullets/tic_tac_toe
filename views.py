from app import app
from flask import render_template, request, redirect, url_for, flash, g
from engine import *
from models import *


DATA = {"x": "x", "o": "o", "moves": 0}
FIELD = []
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

    if move == 0:
        field = getattr(g, 'field', None)
    else:
        field = FIELD

    data = DATA

    if data['moves'] % 2 == 0:
        data['player'] = "пан 'X' "
    else:
        data['player'] = "пан '0' "


    field = update_field(field, int(move), int(line), int(point))
    log = GameLog(parent=pk, move=int(data['moves']), line=int(line), point=int(point))
    db.session.add(log)

    if check_winner(field):
        set_null()
        flash(f"Переможець {data['player']}, на {data['moves']} ході")

    data['moves'] = int(move) + 1
    db.session.commit()
    return render_template('game.html', field=field, data=DATA, pk=pk)


@app.route("/history/")
def history():
    games = Game.query.order_by(Game.date.desc())
    page_num = request.args.get('page_num')

    if page_num and page_num.isdigit:
        page_num = int(page_num)
    else:
        page_num = 1

    pages = games.paginate(page=page_num, per_page=10)

    return render_template("history.html", games=games, pages=pages)


@app.route("/review/<pk>/")
def draw_map(pk):
    view_game = Game.query.filter(Game.id == pk).first()
    global FIELD
    FIELD = get_field(view_game.field_size)
    return render_template("review.html", game=view_game, data=DATA, field=FIELD)


@app.route("/review/<pk>/next_move")
def review(pk):

    data = DATA
    log = GameLog.query.filter(GameLog.parent == pk)
    view_game = Game.query.filter(Game.id == pk).first()
    log_list = [{'move': i.move, "point": i.point, "line": i.line} for i in log]

    if data['moves'] % 2 == 0:
        data['player'] = "пан 'X' "
    else:
        data['player'] = "пан '0' "

    try:
        data['chord'] = f"{log_list[data['moves']]['line']+1}:{log_list[data['moves']]['point']+1}"
        global FIELD
        FIELD = update_field(FIELD, log_list[data['moves']]['move'], log_list[data['moves']]['line'],
                             log_list[data['moves']]['point'])

        if check_winner(FIELD):
            flash(f"Переможець {data['player']}, на {data['moves']} ході")
            set_null()

    except IndexError:
        flash(f"Гра була не закінчена")
        set_null()
    data['moves'] += 1

    return render_template("review.html", log=log, game=view_game, data=data, field=FIELD)


@app.route("/refresh/")
def refresh():
    set_null()
    return redirect(url_for('page', field=FIELD))


@app.before_request
def before_request():
    g.field = get_field(NUM)


def set_null():
    global NUM, DATA
    NUM = 0
    DATA = {"empty": '.', 'x': 'x', 'o': 'o', "moves": 0}



