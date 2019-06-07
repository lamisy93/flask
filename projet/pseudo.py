#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, flash, session
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/', methods=['GET', 'POST'])
def accueil():
    session.modified = True
    if request.method == 'POST':
        if request.form['pseudo'] and request.form['check']:
            if request.form['check'] == 'mensuelle':
                session.permanent = True
            session['pseudo'] = request.form['pseudo']
            return "Vous avez envoyé le pseudo : {pseudo}".format(pseudo=request.form['pseudo'])
            flash(u'Votre pseudo a bien été envoyé !', 'succes')
    return render_template('pseudo_form.html', titre='Coucou')


@app.route('/pseudo', methods=['GET', 'POST'])
def pseudo():
    if 'pseudo' in session:
        return "C'est un plaisir de se revoir, {pseudo} !".format(pseudo=session['pseudo'])


@app.route('/salut', methods=['GET', 'POST'])
def salut():
    return render_template('pseudo.html', pseudo=session['pseudo'], titre='Coucou')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('logout.html', titre='Deconnexion')


if __name__ == '__main__':
    app.run(debug=True)
