from app import app
from flask import render_template, request, redirect, url_for, flash, session
from engine import *
from models import *


# creating main page,
# say "Hi!" and accept the argument that enter by user
@app.route("/")
def page():
    num = request.args.get("num")
    if num:

        # take argument 'num', ones that input user
        # and creating game field
        field = get_field(int(num))

        # add new game to database
        new_game = Game(field_size=int(num))
        db.session.add(new_game)
        db.session.commit()

        # add game data to session
        session[f'game_{new_game.id}_field'] = field
        session[f'game_{new_game.id}_data'] = {"x": "x", "o": "o", "moves": 0}

        # let's go! :)
        return render_template("game.html", field=field, data=session.get(f'game_{new_game.id}_data'),
                               pk=new_game.id, num=num)
    return render_template('first_page.html')


# game part..
@app.route("/game<pk>/<move>/<line>:<point>")
def game(pk, move, line, point):

    # get work data from session
    data = session[f'game_{pk}_data']
    field = session[f'game_{pk}_field']

    # check player by argument 'move'
    if data['moves'] % 2 == 0:
        data['player'] = "пан 'X'"
    else:
        data['player'] = "пан '0'"

    # updating field by player move
    field = update_field(field, int(move), int(line), int(point))
    log = GameLog(parent=pk, move=int(data['moves']), line=int(line), point=int(point))

    # add changes to session
    db.session.add(log)

    # check winner on that point
    # if winner - congratulations and clear our work data
    if check_winner(field):
        db.session.commit()
        flash(f"Переможець {data['player']}, на {data['moves']+1} ході")

    # if not winner update session arguments, to change player and field
    session[f'game_{pk}_data']['moves'] += 1
    session[f'game_{pk}_field'] = field

    # add changes to table GameLog in database
    db.session.commit()

    return render_template('game.html', field=field, data=session.get(f'game_{pk}_data'), pk=pk)


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

    # take game data from database
    view_game = Game.query.filter(Game.id == pk).first()
    field = get_field(view_game.field_size)

    # add data to session
    session[f'{pk}_field'] = field
    session[f'{pk}_data'] = {"x": "x", "o": "o", "moves": 0}

    return render_template("review.html", game=view_game, data=session.get(f'{pk}_data'), field=field)


# review tha game
@app.route("/review/<pk>/next_move")
def review(pk):

    # get wor data from session
    data = session[f'{pk}_data']
    field = session[f'{pk}_field']

    # most of steps looks like steps in the game view
    # taking log record from database with using game id
    log = GameLog.query.filter(GameLog.parent == pk)
    view_game = Game.query.filter(Game.id == pk).first()
    log_list = [{'move': i.move, "point": i.point, "line": i.line} for i in log]

    # check player
    if data['moves'] % 2 == 0:
        data['player'] = "пан 'X'"
    else:
        data['player'] = "пан '0'"

    # updating game field till victory :)
    try:
        data['chord'] = f"{log_list[data['moves']]['line']+1}:{log_list[data['moves']]['point']+1}"

        field = update_field(field, log_list[data['moves']]['move'], log_list[data['moves']]['line'],
                             log_list[data['moves']]['point'])
        if check_winner(field):
            flash(f"Переможець {data['player']}, на {data['moves']+1} ході")

    # in case that game was not played, or finished incorrect - catch exception
    except IndexError:
        flash(f"Гра була не закінчена")

    # update session and move on
    session[f'{pk}_data']['moves'] += 1
    session[f'{pk}_field'] = field

    return render_template("review.html", log=log, game=view_game, data=data, field=field)


# cleaned our work data and go to first page
@app.route("/refresh/")
def refresh():
    return redirect(url_for('page'))



