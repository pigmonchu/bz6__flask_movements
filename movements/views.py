from movements import app
from flask import render_template, request
import csv

@app.route('/')
def listaIngresos():
    fIngresos = open("movements/data/basededatos.csv", "r")
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)

    print(ingresos)

    total = 0
    for ingreso in ingresos:
        total += float(ingreso[2])

    return render_template("movementsList.html",datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        errores = valida(request.form)
        if len(errores)>0:
            return render_template("alta.html", errores=errores, datos=request.form)

        <graba_datos>

        redirect('/')
    
    render_template("alta.html")

def valida(f):
    result = {}
    if f.get('fecha') <no es fecha>:
        result['fecha'] = 'La fecha no es valida'
    
    if f.get("cantidad") no es numero o <= 0:
        result['cantidad'] = "Cantidad debe ser numérica mayor que cero"

    return result