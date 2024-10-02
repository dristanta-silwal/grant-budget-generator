from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Allows dict-like access to rows
    return conn

# Home Page route with search functionality
@app.route("/", methods=['GET'])
def home():
    query = request.args.get('query')  # Get the search query from the form
    con = get_db_connection()

    if query:
        cur = con.cursor()
        # Search for names that match the query
        cur.execute("SELECT rowid, * FROM researchers WHERE name LIKE ?", ('%' + query + '%',))
        rows = cur.fetchall()
    else:
        # If no query, display all records
        cur = con.cursor()
        cur.execute("SELECT rowid, * FROM researchers")
        rows = cur.fetchall()

    con.close()

    return render_template("home.html", rows=rows, query=query)

# Route to form used to add a new researcher to the database
@app.route("/enternew")
def enternew():
    return render_template("researcher.html")

# Route to add a new record (INSERT) researcher data to the database
@app.route("/addrec", methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO researchers (name, addr, city, zip) VALUES (?,?,?,?)", (nm, addr, city, zip))

                con.commit()
                msg = "Researcher successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route to SELECT all researchers and display in a table
@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM researchers")
    rows = cur.fetchall()
    con.close()
    return render_template("list.html", rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM researchers WHERE rowid = ?", (id,))
            rows = cur.fetchall()
        except:
            id = None
        finally:
            con.close()
            return render_template("edit.html", rows=rows)

# Route used to execute the UPDATE statement on a specific researcher in the database
@app.route("/editrec", methods=['POST', 'GET'])
def editrec():
    if request.method == 'POST':
        try:
            rowid = request.form['rowid']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE researchers SET name=?, addr=?, city=?, zip=? WHERE rowid=?", (nm, addr, city, zip, rowid))

                con.commit()
                msg = "Researcher record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route used to DELETE a specific researcher from the database    
@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM researchers WHERE rowid=?", (rowid,))

                con.commit()
                msg = "Researcher record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route to search for a researcher by name in the database (no JavaScript, just form-based search)
@app.route('/search_researcher', methods=['GET'])
def search_researcher():
    query = request.args.get('query')  # Get the search query from the form
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    # Search for names that match the query
    cur.execute("SELECT rowid, * FROM researchers WHERE name LIKE ?", ('%' + query + '%',))
    rows = cur.fetchall()
    con.close()
    return render_template("home.html", rows=rows, query=query)

if __name__ == '__main__':
    app.run(debug=True)
