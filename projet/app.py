    #/usr/bin/env python
# -*- coding:utf-8 -*-

from io import StringIO
import os

from flask import (
    Flask, request, redirect, url_for, make_response, render_template, flash, session
)
from werkzeug import secure_filename
from PIL import Image
app = Flask(__name__)
app.secret_key = 'super secret key'


# @app.route('/')
# def racine():
#     return "Le chemin de 'racine' est : " + request.path


# @app.route('/')
# def index():
#     pseudo_visiteur = request.cookies.get('pseudo') # on récupère le cookie 'pseudo'
#     if pseudo_visiteur is not None:
#         return "C'est un plaisir de se revoir, {pseudo} !".format(pseudo=pseudo_visiteur)
#     else:
#         reponse = make_response("Bonjour, c'est votre première visite ?")
#         reponse.set_cookie('pseudo', 'Luc', max_age=3600*24*30)
#         reponse.set_cookie('pseudo', '', max_age=-1)
#         return reponse

@app.route('/')
def index():
    session.permanent = True
    session.modified = True
    if 'pseudo' in session:
        return "C'est un plaisir de se revoir, {pseudo} !".format(pseudo=session['pseudo'])
    else:
        session['pseudo'] = 'Luc'
        return "Bonjour, c'est votre première visite ?"


@app.route('/accueil')
def accueillir():
    return 'Bienvenue !'


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash(u'Votre message a bien été envoyé !', 'succes')
        return "Vous avez envoyé le message : {msg}".format(msg=request.form.get('msg', 'valeur par défaut'))
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'


@app.route('/uploads', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        fichier = request.files['mon_fichier']
        nom_fichier = fichier.filename
        fileName, fileExtension = os.path.splitext(nom_fichier)
        if fileExtension in ('.csv', '.pdf', 'jpg', 'svg', 'png', 'xlxs'):
            nom_fichier = secure_filename(nom_fichier)
            fichier.save('./uploads/' + nom_fichier)
    return '<form enctype="multipart/form-data" action="" method="post"><input type="file" name="mon_fichier" /><input type="submit" value="Envoyer" /></form>'


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         if donnees_envoyees_correctes:
#             flash(u'Votre message a bien été envoyé !', 'succes')
#             traiter_donnees()
#         else:
#             flash(u'Erreur dans les données envoyées.', 'erreur')
#     return render_template('contact.html')


@app.route('/discussion')
@app.route('/discussion/page/<int:num_page>')
def mon_chat(num_page = 1):
    premier_msg = 1 + 50 * (num_page - 1)
    dernier_msg = premier_msg + 50
    return 'affichage des messages {} à {}'.format(premier_msg, dernier_msg)


@app.route('/afficher')
@app.route('/afficher/mon_nom_est_<nom>_et_mon_prenom_<prenom>')
def afficher(nom=None, prenom=None):
    if nom is None or prenom is None:
        return "Entrez votre nom et votre prénom comme il le faut dans l'url"
    return "Vous vous appelez {} {} !".format(prenom, nom)


@app.route('/image')
def genere_image():
    mon_image = StringIO()
    Image.new("RGB", (300,300), "#92C41D").save(mon_image, 'BMP')
    reponse = make_response(mon_image.getvalue())
    reponse.mimetype = "image/bmp"  # à la place de "text/html"
    return reponse


@app.route('/404')
def page_non_trouvee():
    return "Cette page devrait vous avoir renvoyé une erreur 404", 404


@app.errorhandler(404)
def ma_page_404(error):
    return "Ma jolie page 404", 404


# @app.errorhandler(401)
# @app.errorhandler(404)
# @app.errorhandler(500)
# def ma_page_erreur(error):
#     return "Ma jolie page {}".format(error.code), error.code


utilisateur_non_identifie = True


@app.route('/profil')
def profil():
    if utilisateur_non_identifie:
        return redirect(url_for('page_de_login'))
    return "Vous êtes bien identifié, voici la page demandée : ..."

@app.route('/login')
def page_de_login():
    pass


@app.route('/profil/<pseudo>')
def afficher_profil(pseudo):
    if utilisateur_non_identifie:
        return redirect(url_for('afficher_profil', pseudo="Luc1664"))
    return "Vous êtes bien identifié, voici la page demandée : ..."


if __name__ == '__main__':
    app.debug = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # la session dure une heure
    app.run()

