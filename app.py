from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app=Flask(__name__)
app.config['SECRET_KEY']='hongan'
app.permanent_session_lifetime=timedelta(seconds=30)

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        user_name=request.form['name']
        session.permanent=True
        if user_name:
            session['user']=user_name
            flash('Login Successful!', 'info')
            return render_template('user.html', user=user_name)
    if 'user' in session:
        name=session['user']
        flash('Login Successful!', 'info')
        return render_template('user.html')

    return render_template('login.html')

@app.route('/user')
def hello_user():
    if 'user' in session:
        name=session['user']
        return render_template('user.html')
    else:
        flash("You haven't logged in!", "info")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash('Logout', 'info')
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)