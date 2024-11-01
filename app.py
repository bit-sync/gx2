from flask import Flask, render_template, send_from_directory, request, session, redirect
from pdb_sqlite import PdbSQLite
from config import config
app = Flask(__name__)
db = PdbSQLite("gx2.db")
app.secret_key = config['secrets-app_secret_key'] 
# Create db schema
db.create_table('games', {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'path': 'TEXT',
    'img_path': 'TEXT',
    'name': 'TEXT',
    'name_short': 'TEXT',
    'runcount': 'INTEGER'

})

@app.route('/player')
def player():
    game_n = request.args.get('name', default=None, type=str)
    game = None
    if game_n:
        game = db.select('games', query={'name_short': game_n})
        print(game_n)
        print(game)
        if game:
            db.update('games', {'runcount': game[0]['runcount'] + 1}, {'id': game[0]['id']})  # Increment the runcount by 1
        return render_template('player.html', game=game[0])
    else:
        return 'No game name provided in the query parameters.'
    
@app.route('/')
def index():
    games = db.select('games')

    # Sort the dictionary by value in descending order
    sorted_data = sorted(games, key=lambda x: x["runcount"], reverse=True)
    return render_template('base.html', games=sorted_data)
    
@app.route('/admin/login_form/', methods=['POST', "GET"])
def admin_login_form():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == config['pin']:
            session['pin'] = config['pin']
        return redirect("/admin/")
    return render_template('login.html')
@app.route('/admin/logout/')
def admin_logout():
    session.pop('pin', None)
    return render_template('login.html')
@app.route('/admin/', methods=["GET", "POST"])
def admin_index():
    if 'pin' not in session or session["pin"] != config["pin"]:
        return redirect("/admin/login_form/")

    return render_template('admin.html')
@app.route('/admin/add-game-form/', methods=['POST'])
def add_game_form():
    if request.method == 'POST':
        game_path = request.form.get('gp')
        game_img_path = request.form.get('gip')
        game_name = request.form.get('gn')
        game_name_short = request.form.get('gns')
        db.insert('games', {
            'path': game_path,
            'img_path': game_img_path,
            'name': game_name,
            'name_short': game_name_short,
            'runcount': 0  # Initialize runcount to 0
        })
        return 'Game added successfully'
    return redirect('/admin/')
@app.route('/admin/clear_runcount')
def clear_runcount():
    games = db.select('games')
    for game in games:
        db.update('games', {'runcount': 0}, {'id': game['id']})
    return 'Runcount cleared successfully'
# Static file routes
@app.route('/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)