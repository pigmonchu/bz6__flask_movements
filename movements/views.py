from movements import app
from movements.forms import MovementForm
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from datetime import date

DBFILE = app.config['DBFILE']

def consulta(query, params=()):
    '''
        'SELECT * FROM TABLA' -> [(),(), (),]
        'SELECT * FROM TABLA VACIA ' -> []
        'INSERT ...' -> []
        'UPDATE ...' -> []
        'DELETE ...' -> []
    '''

    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()
    print(filas)

    conn.close()


    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

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

    form = MovementForm()
    
    if request.method == 'POST':
        # iNSERT INTO movimientos (cantidad, concepto, fecha) VALUES (1500, "Paga extra", "2020-12-16" )

        if form.validate():
            consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ? ,? );', 
                    (
                        form.cantidad.data,
                        form.concepto.data,
                        form.fecha.data
                    )
            )

            return redirect(url_for('listaIngresos'))
        else:
            return render_template("alta.html", form=form)
            

    return render_template("alta.html", form=form)



@app.route("/modifica/<id>", methods=['GET', 'POST'])
def modificaIngreso(id):
    
    if request.method == 'GET':

        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id = ?', (id,))[0] 
        registro['fecha'] = date.fromisoformat(registro['fecha'])
        form = MovementForm(data=registro)

        return render_template("modifica.html", form=form, id=id)


    else:
        form = MovementForm()
        if form.validate():
            consulta('UPDATE movimientos SET fecha = ?, concepto= ?, cantidad = ? WHERE id = ?',
                    (request.form.get('fecha'),
                    request.form.get('concepto'),
                    float(request.form.get('cantidad')),
                    id
                    )
            )

            return redirect(url_for("listaIngresos"))
        else:
            return render_template("modifica.html", form=form, id=id)


