import sqlite3

# Connect to the database (creates database.db if it doesn't exist)
con = sqlite3.connect('database.db')

# Create the researchers table if it doesn't exist
con.execute('''CREATE TABLE IF NOT EXISTS researchers
               (name TEXT, addr TEXT, city TEXT, zip TEXT)''')

# Insert some sample data
con.execute("INSERT INTO researchers (name, addr, city, zip) VALUES ('John Doe', '123 Elm St', 'Springfield', '11111')")
con.execute("INSERT INTO researchers (name, addr, city, zip) VALUES ('Jane Smith', '456 Oak St', 'Rivertown', '22222')")
con.commit()

con.close()
