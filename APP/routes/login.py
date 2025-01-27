from flask import render_template, request, redirect, url_for, session
from APP import app

# Set secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Dictionary to store user credentials
users = {
    'admin@admin.com': 'admin'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
