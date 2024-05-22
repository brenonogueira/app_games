import sys
from flask import Flask, flash, render_template, request, redirect, session, url_for

from models.game import Game
from models.user import User

app = Flask(__name__)
app.secret_key = 'helloworld'

game1 =  Game('Counter-Strike 2', 'FPS', 'PC')
game2 =  Game('GTA V', 'Adveture', 'PS5')
game3 =  Game('Red Dead Redemption 2', 'Adveture', 'PC')
gamesList = [game1, game2, game3]

user1 = User('Breno', 'brenitchow', 'admin')
user2 = User('Isabella', 'bella', 'love')

users = { user1.nickname: user1, user2.nickname: user2 }

@app.route('/')
def index():
    return render_template('list.html', title='games', games=gamesList)

@app.route('/add-game')
def addGame():
    if 'loggedUser' not in session or session['loggedUser'] == None:
        return redirect(url_for('login', next=url_for('addGame')))
    return render_template('add_game.html', title='Add new game')

@app.post('/create-game')
def createGame():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    
    newGame = Game(name, category, console)
    
    gamesList.append(newGame)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    
    if next == None:
        next = '/'
    
    return render_template('login.html', next=next)

@app.route('/auth', methods=['POST'])
def auth():
    
    username = request.form.get('username')
    password = request.form.get('password')
 
    if username in users:
        user = users[username]
        if password == user.password:
            session['loggedUser'] = user.nickname
            flash(f'{user.nickname} logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid password!', 'error')
            return redirect(url_for('login'))
    else:
        flash('User not found!', 'error')
        return redirect(url_for('login'))
    

        
    
@app.route('/logout')
def logout():
    session['loggedUser'] = None
    flash('logout successfully')
    return redirect(url_for('login'))

app.run(debug=True)