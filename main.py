from flask import Flask, flash, session, render_template, redirect, url_for, request
import sqlite3
from data import init_db, init_db
import os
app = Flask(__name__)
app.secret_key = "Nigaron31"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

init_db()

@app.route("/")

def index():
    if "user" in session:
        return render_template('main.html')
    else:
        flash("sadfgtyu")
        return redirect('/login')
@app.route("/login", methods = ["POST", "GET"] )
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password))
        user_data = cursor.fetchone()
        print(user_data)
        conn.close()
        if user_data:
            session['user'] = username
            flash("Вхід успішний", "success",)
            return redirect('/')
        else:
             flash("Неправильний логін або пароль", "error")
             return redirect('/login')
    else:
         return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT  INTO users(username, password) VALUES (?,?)",(username, password))
            conn.commit()
            conn.close
            flash('Реєстрація успішна', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Користувач із таким іменем вже існує', 'error')
            return redirect('/register')
    return render_template('register.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("/")
@app.route('/add', methods = ["post","get"])
def app1():
    if request.method == "POST":
        owner_name = session['user']
        name = request.form("nama")
        price = request.form("price")
        image = request.form("image")
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            path = os.path.normpath(image_path).replace('\\','/')
        conn = sqlite3.connect("info.db")
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO into.db(owner_name,name,price,image_path)
                       VALUES (?,?,?,?,?)""", (owner_name,name,price,image_path))

        try:
            cursor.execute("""INSERT INTO table (name,type,price,image) (name,type,price,image)) VALUES(?,?,?,?) """, (name,type,price,image))
            conn.commit()
            conn.close
        except KeyError as e:
            flash(f"Помилка: Відсутнє поле {e}", "error")
        except sqlite3.Error as e:
            flash(f"Помилка бази даних: {e}", "error")
        except Exception as e:
            flash(f"Сталася помилка: {e}", "error")
        return redirect(url_for("/add"))
    return render_template('add.html')
app.run()