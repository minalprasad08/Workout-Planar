from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        exercises TEXT NOT NULL
                    )''')
    conn.commit()

    # Insert sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM workouts")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO workouts (name, exercises) VALUES ('Full Body Workout', 'Push-ups, Squats, Planks')")
        cursor.execute("INSERT INTO workouts (name, exercises) VALUES ('Cardio Session', 'Running, Jump Rope')")
        conn.commit()

    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts")
    workouts = cursor.fetchall()
    conn.close()
    return render_template('base.html', workouts=workouts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        exercises = request.form['exercises']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workouts (name, exercises) VALUES (?, ?)", (name, exercises))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts WHERE id = ?", (id,))
    workout = cursor.fetchone()
    conn.close()
    
    if request.method == 'POST':
        name = request.form['name']
        exercises = request.form['exercises']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE workouts SET name = ?, exercises = ? WHERE id = ?", (name, exercises, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('edit.html', workout=workout)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM workouts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
