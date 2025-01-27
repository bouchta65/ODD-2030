from flask import render_template
from APP import app


@app.route('/settings')
def settings():
    return render_template('settings.html')
