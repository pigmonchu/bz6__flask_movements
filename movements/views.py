from movements import app
from flask import render_template

import random

@app.route('/')
def listaMovimientos():
    texto= 'Hola'
    return render_template("movementsList.html",variable=texto )

@app.route('/dado')
def tiradado():
    return render_template('dado.html', tirada=random.randrange(1,7))