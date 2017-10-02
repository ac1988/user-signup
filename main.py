from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('signup_form.html')

@app.route("/", methods=['POST'])
def validate_input():
    username = request.form['username']
    password = request.form['password']
    password_verification = request.form['password_verification']
    email = request.form['email']

    username_error = ''
    password_error = ''
    password_verification_error = ''
    email_error = ''

    if (not username) or (username.strip() == ""):
        username_error = "That's not a valid username!"
    else:
        if len(username) < 3 or len(username) > 20:
            username_error = "That's not a valid username!"
        else:
            if " " in username:
                username_error = "That's not a valid username!"

    if (not password) or (password.strip() == ""):
        password_error = "That's not a valid password!"
    else:
        if len(password) < 3 or len(username) > 20:
            password_error = "That's not a valid password!"
        else:
            if " " in password:
                password_error = "That's not a valid password!"

    if (not password_verification) or (password_verification.strip() == ""):
        password_verification_error = "The passwords don't match!"
    else:
        if not password == password_verification:
            password_verification_error = "The passwords don't match!"
    
    if len(email) > 1 and len(email) < 3 or len(email) > 20:
        email_error = "That's not a valid email!"
    else:
        if len(email) > 0:
            if " " in email:
                email_error = "That's not a valid email!"
            else:
                at_count = 0
                period_count = 0
                for char in email: 
                    if char == "@":
                        at_count += 1
                        if at_count > 1:
                            email_error = "That's not a valid email!" 
                    else:
                        if char == ".":
                            period_count += 1
                            if period_count > 1:
                                email_error = "That's not a valid email!"
                    
                if at_count < 1 or period_count < 1:
                    email_error = "That's not a valid email!"       
        
    if not username_error and not password_error and not password_verification_error and not email_error:
        valid_username = username
        return redirect('/welcome-page?valid_username={0}'.format(valid_username))
    else:
        return render_template('signup_form.html', username_error=username_error, 
        password_error=password_error, 
        password_verification_error=password_verification_error, email_error=email_error, 
        username=username, email=email)

@app.route("/welcome-page", methods=['POST', 'GET'])
def valid_input():
    valid_username = request.args.get('valid_username')
    return '<h1>Welcome, {0}!<h1>'.format(valid_username)   

app.run()