from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# create a connection to the database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="bharath13",
    database="student"
)

# create a cursor to execute SQL queries
cursor = db.cursor()

# create a table to store the data
cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(255), branch VARCHAR(255), Scholar_no VARCHAR(255), Addresss TEXT, Email VARCHAR(255), Joined_date DATE)")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['student_name']
    branch = request.form['branch']
    Scholar_no = request.form['Scholar_no']
    Addresss = request.form['Addresss']
    Email = request.form['Email']
    Joined_date = request.form['Joined_date']
    query = "INSERT INTO students (student_name, branch, Scholar_no, Addresss, Email, Joined_date) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (student_name, branch, Scholar_no, Addresss, Email, Joined_date)
    cursor.execute(query, values)
    db.commit()
    return redirect(url_for('display'))

@app.route('/display')
def display():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('display.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    query = "DELETE FROM students WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    db.commit()
    return redirect(url_for('display'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    data = cursor.fetchone()
    if request.method == 'POST':
        student_name = request.form['student_name']
        branch = request.form['branch']
        Scholar_no = request.form['Scholar_no']
        Addresss = request.form['Addresss']
        Email = request.form['Email']
        Joined_date = request.form['Joined_date']
        query = "UPDATE students SET student_name = %s, branch = %s, Scholar_no = %s, Addresss = %s, Email = %s, Joined_date = %s WHERE id = %s"
        values = (student_name, branch, Scholar_no, Addresss, Email, Joined_date, id)
        cursor.execute(query, values)
        db.commit()
        return redirect(url_for('display'))
    else:
        return render_template('update.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
