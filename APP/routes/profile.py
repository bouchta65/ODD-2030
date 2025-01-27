from flask import render_template
from APP import app

@app.route('/profile')
def profile():
    return render_template('profile.html')
