from app import app
from flask import render_template, request, redirect, url_for, flash, g
from engine import *
from models import *

# Creating global variables for comfortable using
DATA = {"x": "x", "o": "o", "moves": 0}
FIELD = []
NUM = 0


# creating main page,
# say "Hi!" and accept the argument that enter by user
@app.route("/")
def page():
    num = request.args.get("num")
    if num:

        # take argument 'num', ones that input user
        # and creating game field

        global NUM
        NUM = int(num)
        global FIELD
        FIELD = get_field(NUM)
        field = FIELD

        # add new game to database
        new_game = Game(field_size=NUM)
        db.session.add(new_game)
        db.session.commit()

        # let's go! :)
        return render_template("game.html", field=field, data=DATA, pk=new_game.id, num=num)
    return render_template('first_page.html')


# game part..
@app.route("/game<pk>/<move>/<line>:<point>")
def game(pk, move, line, point):

    # create game field if not created, or used already created field
    if move == 0:
        field = getattr(g, 'field', None)
    else:
        field = FIELD

    data = DATA

    # check player by argument 'move'
    if data['moves'] % 2 == 0:
        data['player'] = "пан 'X' "
    else:
        data['player'] = "пан '0' "

    # updating field by player move
    field = update_field(field, int(move), int(line), int(point))
    log = GameLog(parent=pk, move=int(data['moves']), line=int(line), point=int(point))

    # add changes to session
    db.session.add(log)

    # check winner on that point
    # if winner - congratulations and clear our work data
    if check_winner(field):
        set_null()
        flash(f"Переможець {data['player']}, на {data['moves']} ході")

    # if not winner update argument 'move', to change player
    data['moves'] = int(move) + 1

    # add changes to table GameLog in database
    db.session.commit()
    return render_template('game.html', field=field, data=DATA, pk=pk)


# creating a page with games that was played
@app.route("/history/")
def history():

    # taking games from database
    games = Game.query.order_by(Game.date.desc())

    # paginate page
    page_num = request.args.get('page_num')

    if page_num and page_num.isdigit:
        page_num = int(page_num)
    else:
        page_num = 1

    pages = games.paginate(page=page_num, per_page=10)

    return render_template("history.html", games=games, pages=pages)


# drawing map to review game
@app.route("/review/<pk>/")
def draw_map(pk):
    view_game = Game.query.filter(Game.id == pk).first()
    global FIELD
    FIELD = get_field(view_game.field_size)
    return render_template("review.html", game=view_game, data=DATA, field=FIELD)


# review tha game
@app.route("/review/<pk>/next_move")
def review(pk):

    # most of steps looks like steps in the game view
    # taking log record from database with using game id
    data = DATA
    log = GameLog.query.filter(GameLog.parent == pk)
    view_game = Game.query.filter(Game.id == pk).first()
    log_list = [{'move': i.move, "point": i.point, "line": i.line} for i in log]

    # check player
    if data['moves'] % 2 == 0:
        data['player'] = "пан 'X' "
    else:
        data['player'] = "пан '0' "

    # updating game field till victory :)
    try:
        data['chord'] = f"{log_list[data['moves']]['line']+1}:{log_list[data['moves']]['point']+1}"
        global FIELD
        FIELD = update_field(FIELD, log_list[data['moves']]['move'], log_list[data['moves']]['line'],
                             log_list[data['moves']]['point'])

        if check_winner(FIELD):
            flash(f"Переможець {data['player']}, на {data['moves']} ході")
            set_null()

    # in case that game was not played, or finished incorrect - catch exception
    except IndexError:
        flash(f"Гра була не закінчена")
        set_null()
    data['moves'] += 1

    return render_template("review.html", log=log, game=view_game, data=data, field=FIELD)

# cleaned our work data and go to first page
@app.route("/refresh/")
def refresh():
    set_null()
    return redirect(url_for('page', field=FIELD))


# function that provides work of flask.g variables
@app.before_request
def before_request():
    g.field = get_field(NUM)


# function that cleaning up our work data
def set_null():
    global NUM, DATA
    NUM = 0
    DATA = {"empty": '.', 'x': 'x', 'o': 'o', "moves": 0}



