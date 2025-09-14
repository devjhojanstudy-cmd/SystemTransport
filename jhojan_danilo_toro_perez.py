#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulación de cálculo de tarifas de pasaje.
- Variables y nombres en inglés.
- Comentarios explicativos en español.
- Estructura: funciones + clases (objetos).
- No se usan librerías externas.
"""

# Constante: tarifa por kilómetro (pesos)
BASE_RATE_PER_KM = 500.0


class Passenger:
    """
    Clase que representa a un pasajero y calcula su tarifa final.
    - name: str
    - age: int
    - distance_km: float
    """

    def __init__(self, name: str, age: int, distance_km: float) -> None:
        self.name = name
        self.age = age
        self.distance_km = distance_km
        self.final_fare = 0.0  # se calculará más adelante

    def compute_fare(self, base_rate_per_km: float = BASE_RATE_PER_KM) -> float:
        """
        Calcula la tarifa final según las reglas:
          - tarifa base = base_rate_per_km * distance_km
          - si age < 12 => 50% descuento
          - si age > 60 => 30% descuento
          - en otro caso => tarifa completa
        Devuelve la tarifa final (float) y la guarda en self.final_fare.
        """
        base_fare = base_rate_per_km * self.distance_km

        if self.age < 12:
            # Menores de 12 años: 50% de descuento
            self.final_fare = base_fare * 0.5
        elif self.age > 60:
            # Mayores de 60 años: 30% de descuento
            self.final_fare = base_fare * 0.7
        else:
            # Resto de pasajeros: tarifa completa
            self.final_fare = base_fare

        return self.final_fare


class TransportFareCalculator:
    """
    Clase para manejar el proceso de múltiples pasajeros:
      - almacenar pasajeros
      - procesar cálculos
      - generar resumen y total recaudado
    """

    def __init__(self, base_rate_per_km: float = BASE_RATE_PER_KM) -> None:
        self.base_rate_per_km = base_rate_per_km
        self.passengers: list[Passenger] = []

    def add_passenger(self, passenger: Passenger) -> None:
        """Agregar un objeto Passenger a la lista interna."""
        self.passengers.append(passenger)

    def process_all(self) -> None:
        """Calcular la tarifa final para todos los pasajeros almacenados."""
        for passenger in self.passengers:
            passenger.compute_fare(self.base_rate_per_km)

    def total_collected(self) -> float:
        """Retornar la suma de las tarifas finales de todos los pasajeros."""
        return sum(p.final_fare for p in self.passengers)

    def print_summary(self) -> None:
        """Imprimir en consola un resumen ordenado con los datos requeridos."""
        print("\n" + "=" * 50)
        print("SUMMARY OF FARES".center(50))
        print("=" * 50)
        if not self.passengers:
            print("No passengers processed.")
            return

        # Encabezado
        print(f"{'Name':<20} {'Age':>5} {'Distance(km)':>14} {'Fare (pesos)':>15}")
        print("-" * 50)

        # Filas por pasajero
        for p in self.passengers:
            # formateo de tarifa sin decimales y con separadores de miles
            fare_str = f"{p.final_fare:,.0f}"
            print(f"{p.name:<20} {p.age:>5} {p.distance_km:>14.2f} {fare_str:>15}")

        print("-" * 50)
        total_str = f"{self.total_collected():,.0f}"
        print(f"{'Total collected:':<39} {total_str:>11} pesos")
        print("=" * 50 + "\n")


# -----------------------
# Funciones auxiliares para entrada validada
# -----------------------
def get_non_empty_string(prompt: str) -> str:
    """Pide una cadena no vacía al usuario."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("El valor no puede estar vacío. Intente de nuevo.")


def get_positive_int(prompt: str) -> int:
    """Pide un entero positivo (>= 0) al usuario."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value >= 0:
                return value
            print("Ingrese un número entero no negativo.")
        except ValueError:
            print("Entrada inválida. Ingrese un número entero válido.")


def get_non_negative_float(prompt: str) -> float:
    """Pide un número float no negativo al usuario."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value >= 0.0:
                return value
            print("Ingrese un valor numérico no negativo.")
        except ValueError:
            print("Entrada inválida. Ingrese un número válido (ej: 12.5).")


# -----------------------
# Función principal
# -----------------------
def main() -> None:
    """
    Flujo principal del programa:
      1. Pedir N pasajeros.
      2. Para cada pasajero pedir nombre, edad y distancia.
      3. Crear objetos Passenger y agregarlos al TransportFareCalculator.
      4. Procesar todos, mostrar resumen y total recaudado.
    """
    print("=" * 60)
    print("TRANSPORT FARE SIMULATOR".center(60))
    print("=" * 60)

    # Número de pasajeros a procesar
    num_passengers = get_positive_int("Ingrese la cantidad de pasajeros a procesar (N): ")

    if num_passengers == 0:
        print("\nNo hay pasajeros para procesar. Fin del programa.")
        return

    # Crear calculadora
    calculator = TransportFareCalculator()

    # Entrada de datos para cada pasajero
    for i in range(1, num_passengers + 1):
        print(f"\n--- Passenger {i} ---")
        name = get_non_empty_string("Name: ")
        age = get_positive_int("Age (years): ")
        distance_km = get_non_negative_float("Distance to travel (km): ")

        passenger = Passenger(name=name, age=age, distance_km=distance_km)
        calculator.add_passenger(passenger)

    # Calcular tarifas y mostrar resumen
    calculator.process_all()
    calculator.print_summary()


# Punto de entrada
if __name__ == "__main__":
    main()

