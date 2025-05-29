from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from datetime import datetime
import csv
import io

app = Flask(__name__)
DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Viktigt för att kunna använda row["column_name"]
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    search = request.args.get("search", "").strip()

    conn = get_db_connection()
    if search:
        sql = """
            SELECT * FROM transactions
            WHERE title LIKE ? OR category LIKE ?
            ORDER BY date DESC
        """
        params = (f"%{search}%", f"%{search}%")
        rows = conn.execute(sql, params).fetchall()
    else:
        rows = conn.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()

    transactions = []
    for row in rows:
        transactions.append({
            "id": row["id"],
            "title": row["title"],
            "amount": float(row["amount"]),
            "category": row["category"],
            "date": datetime.strptime(row["date"], "%Y-%m-%d"),
            "type": row["type"]
        })

    # Beräkna totalsaldon
    balance = 0.0
    total_income = 0.0
    total_expense = 0.0
    for t in transactions:
        if t["type"] == "income":
            total_income += t["amount"]
            balance += t["amount"]
        else:  # expense
            total_expense += t["amount"]
            balance -= t["amount"]

    conn.close()
    return render_template(
        "index.html",
        transactions=transactions,
        balance=balance,
        total_income=total_income,
        total_expense=total_expense
    )

@app.route("/add", methods=["POST"])
def add_transaction():
    title = request.form["title"].strip()
    amount_str = request.form["amount"].strip()
    category = request.form["category"].strip()
    date_str = request.form["date"].strip()
    t_type = request.form["type"].strip()

    # Validering och konvertering
    try:
        amount = float(amount_str)
    except ValueError:
        return "Felaktigt belopp", 400

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Felaktigt datumformat", 400

    if t_type not in ("income", "expense"):
        return "Felaktig typ", 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO transactions (title, amount, category, date, type) VALUES (?, ?, ?, ?, ?)",
        (title, amount, category, date_str, t_type)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete_transaction(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/export")
def export_csv():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(["ID", "Titel", "Belopp", "Kategori", "Datum", "Typ"])

    for row in rows:
        writer.writerow([
            row["id"],
            row["title"],
            row["amount"],
            row["category"],
            row["date"],
            row["type"]
        ])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="transactions.csv"
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)