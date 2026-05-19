from flask import Flask, # FLASH, redirect, render_template, request, session, abort

app= Flask(__name__)

def hello():
    print("Hello, World!")