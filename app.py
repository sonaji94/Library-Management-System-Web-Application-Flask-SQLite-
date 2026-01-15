from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("library.db")

# Create table
conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    status TEXT
)
""")
conn.commit()
conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        bid = request.form["id"]
        title = request.form["title"]
        author = request.form["author"]

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO books VALUES (?, ?, ?, ?)",
                (bid, title, author, "Available")
            )
            conn.commit()
        except:
            pass
        conn.close()
        return redirect("/books")

    return render_template("add.html")

@app.route("/books")
def books():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    data = cur.fetchall()
    conn.close()
    return render_template("books.html", books=data)

@app.route("/issue/<bid>")
def issue_book(bid):
    conn = get_db()
    conn.execute(
        "UPDATE books SET status='Issued' WHERE id=?",
        (bid,)
    )
    conn.commit()
    conn.close()
    return redirect("/books")

@app.route("/return/<bid>")
def return_book(bid):
    conn = get_db()
    conn.execute(
        "UPDATE books SET status='Available' WHERE id=?",
        (bid,)
    )
    conn.commit()
    conn.close()
    return redirect("/books")

if __name__ == "__main__":
    app.run(debug=True)
