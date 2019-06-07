#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from datetime import date
app = Flask(__name__)

@app.route('/')
def accueil():
    mots = ["bonjour", "à", "toi,", "visiteur."]
    d = date.today().isoformat()
    return render_template('accueil.html', titre="Bienvenue !", mots=mots, la_date=d, nombre=2)


def est_impair(n):
    if n % 2 == 1:
        return True
    return False
app.jinja_env.tests['impair'] = est_impair

if __name__ == '__main__':
    app.run(debug=True)


