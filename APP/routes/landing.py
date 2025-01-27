from . import app

@app.route('/landing')
def landing():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('landing.html')
