# -*- coding: utf-8 -*-
"""
Módulo de Simulación de un Sistema de Autolavado

Este script simula un flujo de trabajo completo para un autolavado, integrando:
1.  **Base de Datos de Clientes y Vehículos**: Para identificar a los clientes por su patente.
2.  **Matriz de Precios Dinámica**: Para calcular costos basados en el tipo de vehículo y los servicios.
3.  **Generación de Órdenes de Trabajo**: Para crear un ticket final con todos los detalles.

Este prototipo demuestra la lógica central que podría ser la base para una aplicación real.
"""

import uuid

# --- Módulo A: Base de Datos de Clientes (Simulada) ---
# En un sistema real, esto sería una base de datos (SQL, NoSQL, etc.).
# Usamos la patente como clave única para un acceso rápido ("Patente Primero").
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
# Define los precios de cada servicio según el tipo de vehículo.
# Es flexible y fácil de expandir sin cambiar la lógica de cálculo.
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
        "Limpieza de Caja": 15.00  # Servicio exclusivo
    }
}

# --- Módulo C: Generación y Cálculo de Órdenes ---

def generar_orden_de_trabajo(patente, servicios_solicitados):
    """
    Función principal que integra la búsqueda de cliente, cálculo de costos y generación de orden.

    Args:
        patente (str): La patente del vehículo del cliente.
        servicios_solicitados (list): Lista de nombres de los servicios requeridos.

    Returns:
        dict: Un diccionario representando la orden de trabajo final, o None si el cliente no se encuentra.
    """
    print(f"--- Iniciando Nueva Orden para la Patente: {patente} ---")

    # 1. Búsqueda del Cliente ("Patente Primero")
    info_cliente = base_de_datos_clientes.get(patente)
    if not info_cliente:
        print(f"Error: Cliente con patente '{patente}' no encontrado.")
        return None

    tipo_vehiculo = info_cliente["tipo_vehiculo"]
    print(f"Cliente encontrado: {info_cliente['nombre_cliente']} ({tipo_vehiculo})")

    # 2. Cálculo del Total de la Orden
    total_orden = 0.0
    servicios_confirmados = []

    if tipo_vehiculo not in matriz_precios:
        print(f"Error: El tipo de vehículo '{tipo_vehiculo}' no tiene una lista de precios definida.")
        return None

    print("\nDetalle de la Orden:")
    for servicio in servicios_solicitados:
        precio_servicio = matriz_precios[tipo_vehiculo].get(servicio)
        if precio_servicio:
            total_orden += precio_servicio
            servicios_confirmados.append({"servicio": servicio, "precio": precio_servicio})
            print(f"  - Servicio: '{servicio}', Precio: ${precio_servicio:.2f}")
        else:
            print(f"  - Advertencia: El servicio '{servicio}' no está disponible para '{tipo_vehiculo}'.")

    # 3. Generación del Ticket de Orden Final
    orden_final = {
        "id_orden": str(uuid.uuid4()),  # Genera un ID único para la orden
        "estado": "En Espera",
        "cliente": {
            "nombre": info_cliente["nombre_cliente"],
            "patente": patente,
            "vehiculo": tipo_vehiculo
        },
        "servicios": servicios_confirmados,
        "total_a_pagar": f"${total_orden:.2f}"
    }

    print("\n" + "="*50)
    print("      ORDEN DE TRABAJO GENERADA CORRECTAMENTE")
    print("="*50)
    print(f"ID de Orden: {orden_final['id_orden']}")
    print(f"Estado: {orden_final['estado']}")
    print(f"Cliente: {orden_final['cliente']['nombre']} - Patente: {orden_final['cliente']['patente']}")
    print(f"Total a Pagar: {orden_final['total_a_pagar']}")
    print("="*50 + "\n")

    return orden_final

# --- EJEMPLOS DE USO ---

if __name__ == "__main__":
    # Caso 1: Cliente conocido (SUV) solicita servicios válidos.
    print("### Ejemplo 1: SUV con Lavado Completo y Cera ###")
    servicios_suv = ["Lavado Completo", "Cera"]
    generar_orden_de_trabajo("B-2024-XYZ", servicios_suv)

    # Caso 2: Cliente conocido (Sedán) solicita un servicio que no existe.
    print("### Ejemplo 2: Sedán con Lavado Básico y un servicio no válido ###")
    servicios_sedan = ["Lavado Básico", "Pulido de Faros"]
    generar_orden_de_trabajo("C-2023-ABC", servicios_sedan)

    # Caso 3: Camioneta solicita un servicio exclusivo de su tipo.
    print("### Ejemplo 3: Camioneta con Limpieza de Caja ###")
    servicios_camioneta = ["Lavado Básico", "Limpieza de Caja"]
    generar_orden_de_trabajo("D-2022-JKL", servicios_camioneta)

    # Caso 4: Se intenta generar una orden para una patente no registrada.
    print("### Ejemplo 4: Patente no existente ###")
    servicios_fantasma = ["Lavado Básico"]
    generar_orden_de_trabajo("X-2025-XXX", servicios_fantasma)