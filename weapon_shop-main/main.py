from flask import Flask, flash, session, render_template, redirect, url_for, request
import sqlite3
from data import init_db, init_db_info
import os

app = Flask(__name__)
app.secret_key = "Nigaron31"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

init_db()
init_db_info()
db_name = 'quiz'
def open_db():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close_db():
    cursor.close()
    conn.close()

def get_quizzes():
    open_db()
    query = 'SELECT name FROM quiz ORDER BY id'
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()
    return result


@app.route("/")
def index():
    if "user" in session:
        username = session['user'] 
        conn = sqlite3.connect("info.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM info WHERE owner_name = ?", (username,))
        items = cursor.fetchall() 
        conn.close()

        return render_template('main.html', items=items, username=username) 
    else:
        return redirect('/login')
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            session['user'] = username
            flash("Login successful", "success")
            return redirect('/')
        else:
            flash("Invalid username or password", "error")
            return redirect('/login')
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash('Registration successful', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('User with this username already exists', 'error')
            return redirect('/register')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("/")

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        owner_name = session['user']
        name = request.form.get('name')
        item_type = request.form.get('type')  
        price = request.form.get('price')
        image = request.files.get('image')
        image_path = None
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            image_path = os.path.normpath(image_path).replace('\\', '/')
        conn = sqlite3.connect("info.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO info (owner_name, name, type, price, image_path)
                VALUES (?, ?, ?, ?, ?)
            """, (owner_name, name, item_type, price, image_path))
            conn.commit()
            conn.close()
            flash("Item added successfully.", "success")
            return redirect(url_for("add"))
        except sqlite3.Error as e:
            flash(f"Database error: {e}", "error")
            conn.rollback()
        finally:
            conn.close()
    return render_template('add.html',username=  session['user'] )


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        q_list = get_quizzes()
        return render_template('quiz.html', quizzes=q_list)
    

@app.route("/delete/<int:item_id>", methods=["POST"]) 
def delete_item(item_id): 
    if "user" not in session: 
        return redirect('/login') 
 
    username = session['user'] 
    conn = sqlite3.connect("info.db") 
    cursor = conn.cursor() 
 
    cursor.execute("DELETE FROM info WHERE id = ? AND owner_name = ?", (item_id, username)) 
    conn.commit() 
    conn.close() 
 
    return redirect("/")
if __name__ == '__main__':
    app.run()