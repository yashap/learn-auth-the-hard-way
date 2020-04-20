from flask import render_template


def get():
    return render_template('index.html')
