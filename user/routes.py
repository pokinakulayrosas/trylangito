from flask import Flask
from nugits import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
    
    return User().signup()