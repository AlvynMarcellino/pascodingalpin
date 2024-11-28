from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Koneksi ke database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nilai_siswa"
)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aksi_login', methods=["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("SELECT * FROM user WHERE username = %s AND password = md5(%s)")
    data = (request.form['username'], request.form['password'],)
    cursor.execute(query, data)
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template("salah.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/dashboard')
def dashboard():
    if session.get("user"):
        return render_template("dashboard.html")
    else:
        return redirect(url_for("home"))

@app.route('/tambah', methods=["POST", "GET"])
def tambah():
    if session.get("user"):
        if request.method == "POST":
            cursor = mydb.cursor()
            nama = request.form["nama"]
            mata_pelajaran = request.form["mata_pelajaran"]
            nilai = request.form["nilai"]

            query = ("INSERT INTO nilai VALUES (%s, %s, %s, %s)")
            data = ("", nama, mata_pelajaran, nilai)

            cursor.execute(query, data)
            mydb.commit()
            cursor.close()
            return redirect("/tampil")
        return render_template("tambah.html")
    else:
        return redirect(url_for("home"))

@app.route('/tampil')
def tampil():
    if session.get("user"):
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM nilai")
        data = cursor.fetchall()
        return render_template('tampil.html', data=data)
    else:
        return redirect(url_for("home"))

@app.route('/hapus/<id>')
def hapus(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = ("DELETE FROM nilai WHERE id = %s")
        data = (id,)
        cursor.execute(query, data)
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))

@app.route('/update/<id>', methods=["POST", "GET"])
def update(id):
    if session.get("user"):
        cursor = mydb.cursor()
        if request.method == "POST":
            nama = request.form["nama"]
            mata_pelajaran = request.form["mata_pelajaran"]
            nilai = request.form["nilai"]

            query = ("UPDATE nilai SET nama = %s, mata_pelajaran = %s, nilai = %s WHERE id = %s")
            data = (nama, mata_pelajaran, nilai, id)

            cursor.execute(query, data)
            mydb.commit()
            cursor.close()
            return redirect('/tampil')
        else:
            query = ("SELECT * FROM nilai WHERE id = %s")
            data = (id,)
            cursor.execute(query, data)
            value = cursor.fetchone()
            return render_template('update.html', value=value)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
