from flask import Flask

app= Flask(__name__)

def hello():
    print("Hello, World!")