from datetime import date

class Ingreso():
    def __init__(self, fecha, concepto, valor):
        self.fecha = date(int(fecha[:4]), int(fecha[5:7]), int(fecha[9:]))
        self.concepto = concepto
        self.valor = float(valor)