# -*- coding: utf-8 -*-
"""
Aplicación Web para el Sistema de Autolavado

Este script utiliza Flask para crear una interfaz web simple y amigable
para el sistema de gestión de autolavado.
"""

import uuid
from flask import Flask, render_template, request

app = Flask(__name__)

# --- Módulo A: Base de Datos de Clientes (Simulada) ---
base_de_datos_clientes = {
    "B-2024-XYZ": {
        "nombre_cliente": "Ana García",
        "tipo_vehiculo": "SUV",
        "telefono": "+1-202-555-0182"
    },
    "C-2023-ABC": {
        "nombre_cliente": "Carlos Mendoza",
        "tipo_vehiculo": "Sedán",
        "telefono": "+1-202-555-0149"
    },
    "D-2022-JKL": {
        "nombre_cliente": "Diana Rojas",
        "tipo_vehiculo": "Camioneta",
        "telefono": "+1-202-555-0123"
    }
}

# --- Módulo B: Matriz de Precios ---
matriz_precios = {
    "Sedán": {
        "Lavado Básico": 20.00,
        "Lavado Completo": 30.00,
        "Cera": 15.00,
        "Limpieza Interior": 25.00
    },
    "SUV": {
        "Lavado Básico": 25.00,
        "Lavado Completo": 35.00,
        "Cera": 20.00,
        "Limpieza Interior": 30.00
    },
    "Camioneta": {
        "Lavado Básico": 30.00,
        "Lavado Completo": 45.00,
        "Cera": 25.00,
        "Limpieza Interior": 35.00,
        "Limpieza de Caja": 15.00
    }
}

def get_all_services():
    """Obtiene una lista de todos los servicios únicos disponibles."""
    all_services = set()
    for vehicle in matriz_precios.values():
        all_services.update(vehicle.keys())
    return sorted(list(all_services))

def generar_orden_logica(patente, servicios_solicitados):
    """
    Lógica de negocio para generar una orden.
    Devuelve un diccionario con el resultado o un mensaje de error.
    """
    info_cliente = base_de_datos_clientes.get(patente.upper())
    if not info_cliente:
        return {"error": f"Cliente con patente '{patente}' no encontrado."}

    tipo_vehiculo = info_cliente["tipo_vehiculo"]

    if tipo_vehiculo not in matriz_precios:
        return {"error": f"El tipo de vehículo '{tipo_vehiculo}' no tiene precios definidos."}

    total_orden = 0.0
    servicios_confirmados = []
    servicios_no_disponibles = []

    for servicio in servicios_solicitados:
        precio_servicio = matriz_precios[tipo_vehiculo].get(servicio)
        if precio_servicio:
            total_orden += precio_servicio
            servicios_confirmados.append({"servicio": servicio, "precio": f"${precio_servicio:.2f}"})
        else:
            servicios_no_disponibles.append(servicio)

    orden_final = {
        "id_orden": str(uuid.uuid4().hex[:8].upper()),
        "estado": "En Espera",
        "cliente": {
            "nombre": info_cliente["nombre_cliente"],
            "patente": patente.upper(),
            "vehiculo": tipo_vehiculo
        },
        "servicios_confirmados": servicios_confirmados,
        "servicios_no_disponibles": servicios_no_disponibles,
        "total_a_pagar": f"${total_orden:.2f}"
    }

    return {"orden": orden_final}

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal que muestra el formulario y el resultado de la orden.
    """
    all_services = get_all_services()
    resultado = None

    if request.method == 'POST':
        patente = request.form.get('patente')
        servicios_solicitados = request.form.getlist('servicios')

        if not patente:
            resultado = {"error": "Por favor, ingrese una patente."}
        elif not servicios_solicitados:
             resultado = {"error": "Por favor, seleccione al menos un servicio."}
        else:
            resultado = generar_orden_logica(patente, servicios_solicitados)

    return render_template('index.html', all_services=all_services, resultado=resultado)

if __name__ == '__main__':
    # El host '0.0.0.0' hace que la app sea accesible desde otros dispositivos en la misma red.
    app.run(host='0.0.0.0', port=5000, debug=True)