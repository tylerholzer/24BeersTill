from flask import Flask, Response, redirect, request, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
from helpers.sqlite import SqliteDB

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_veiw = "login"
bcrypt = Bcrypt(app)

# User login stuff
class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        db = SqliteDB()
        pw_hash = db.get_pw_hash(request.form['email'])
        db.disconnect()
        if bcrypt.check_password_hash(pw_hash, request.form['password']):
            login_user(User(request.form['email']))
            return redirect(request.args.get('next'))
        else:
            return abort(401)
    else:
        return Response('''
            <form action="" method="post">
                <p>Email:<input type=text name=email>
                <p>Password:<input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

@app.errorhandler(401)
def login_failed(e):
    return Response('<p>Login failed</p>')

@app.route("/")
def home():
    return Response('''
        <a href="/scary">scary place</a>
        <form action="/create/user" method="post">
            <p>Email:<input type=text name=email>
            <p>Password:<input type=password name=password>
            <p>First Name:<input type=text name=first>
            <p>Last Name:<input type=text name=last>
            <p><input type=submit value=Create>
        </form>
    ''')

@app.route("/create/user", methods=['POST'])
def create_user():
    db = SqliteDB()
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    db.create_user(request.form['email'],pw_hash,request.form['first'],request.form['last'])
    db.disconnect()
    return Response('<a href="/scary">scary place</a>')

@app.route("/scary")
@login_required
def scary():
    return Response("Hello!")

if __name__ == "__main__":
        app.run()
