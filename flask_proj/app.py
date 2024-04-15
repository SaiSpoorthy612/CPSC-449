from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dolly#55'
app.config['MYSQL_DB'] = 'my_db'

mysql = MySQL(app)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        try:
            
            CID = request.form['CID']
            FirstName = request.form['FirstName']
            LastName = request.form['LastName']
            Address = request.form['Address']
            City = request.form['City']
            State = request.form['State']
            Zip = request.form['Zip']
            email = request.form['email']

           
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO contacts (CID, FirstName, LastName, Address, City, State, Zip, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (CID, FirstName, LastName, Address, City, State, Zip, email))

            mysql.connection.commit()
            cur.close()
            message = "Contact has been added successfully."

            return render_template('index.html', message=message)
            return redirect(url_for('index'))
        except Exception as e:
            
            return make_response(jsonify({'error': str(e)}), 400)


@app.route('/delete_contact', methods=['DELETE'])
def delete_contact():
    
    del_first_name = request.form['delFirstName']
    del_last_name = request.form['delLastName']
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM contacts WHERE FirstName=%s AND LastName=%s", (del_first_name, del_last_name))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Contact deleted successfully'})
        delmessage = "Contact has been deleted successfully."
        return render_template('index.html', message=delmessage)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/view_contacts')
def view_contacts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts")
        contacts = cur.fetchall()
        cur.close()
        return render_template('view_contacts.html', contacts=contacts)
    except Exception as e:
        
        return render_template('error.html', error=str(e))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_contact/<int:CID>', methods=['PUT'])
@app.route('/update_contact', methods=['PUT'])
def update_contact():
    if request.method == 'PUT':
        try:
            CID = request.form['CID']
            new_FirstName = request.form['FirstName']
            new_LastName = request.form['LastName']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE contacts 
                SET FirstName=%s, LastName=%s
                WHERE CID=%s
            """, (new_FirstName, new_LastName, CID))
            
            mysql.connection.commit()
            cur.close()
            
            return jsonify({'message': 'First Name and Last Name updated successfully'})
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)



if __name__ == '__main__':
    app.run(debug=True)
