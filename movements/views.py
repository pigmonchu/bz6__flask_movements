from movements import app
from flask import render_template
import csv
from movements.entities import Ingreso

@app.route('/')
def listaIngresos():
    fIngresos = open("movements/data/basededatos.csv", "r")
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos = list(map(lambda item: Ingreso(item[0], item[1], item[2]), csvReader))

    print(ingresos)

    return render_template("movementsList.html",datos=ingresos)

@app.route('/creaalta')
def nuevoIngreso():
    return 'Ya el miercoles si eso te enseño el formulario'

