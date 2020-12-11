from movements import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3

DBFILE = 'movements/data/DBFLASK.db'

def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    
    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []
    filas = c.fetchall()

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    conn.commit()
    conn.close()

    if len(listaDeDiccionarios) == 1:
        return listaDeDiccionarios[0]
    elif len(listaDeDiccionarios) == 0:
        return None
    else:
        return listaDeDiccionarios

@app.route('/')
def listaIngresos():

    ingresos = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos;')

    total = 0
    for ingreso in ingresos:
        total += float(ingreso['cantidad'])


    return render_template("movementsList.html",datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        # iNSERT INTO movimientos (cantidad, concepto, fecha) VALUES (1500, "Paga extra", "2020-12-16" )

        consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ? ,? );', 
                 (
                    float(request.form.get('cantidad')),
                    request.form.get('concepto'),
                    request.form.get('fecha')
                 )
        )

        return redirect(url_for('listaIngresos'))
        


    return render_template("alta.html")


@app.route("/modifica/<id>", methods=['GET', 'POST'])
def modificaIngreso(id):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    if request.method == 'GET':

        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id = ?', (id,))

        return render_template("modifica.html", registro=registro)
    else:
        consulta('UPDATE movimientos SET fecha = ?, concepto= ?, cantidad = ? WHERE id = ?',
                  (request.form.get('fecha'),
                   request.form.get('concepto'),
                   float(request.form.get('cantidad')),
                   id
                  )
        )

        return redirect(url_for("listaIngresos"))
 


