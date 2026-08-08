import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "laboratorio.db"


datos_iniciales = [
    (
        "Glucosa",
        70,
        100,
        "Hipoglucemia: ingesta de hidratos de absorción rápida y valoración clínica.",
        "Hiperglucemia: posible diabetes, estrés metabólico u otra alteración endocrina.",
        "La glucosa es la principal fuente de energía y debe interpretarse según ayuno y contexto clínico.",
    ),
    (
        "Colesterol",
        0,
        200,
        "Nivel bajo: habitualmente no preocupante, valorar contexto nutricional y clínico.",
        "Hipercolesterolemia: posible aumento del riesgo cardiovascular.",
        "El colesterol es un lípido necesario, pero valores elevados requieren valoración del perfil lipídico.",
    ),
    (
        "Hemoglobina",
        13.5,
        17.5,
        "Anemia: posible déficit de hierro, sangrado, inflamación u otra causa hematológica.",
        "Poliglobulia: aumento de glóbulos rojos; valorar hidratación, hipoxia y otras causas.",
        "Proteína de los hematíes responsable del transporte de oxígeno.",
    ),
]


def crear_tabla(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS parametros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            min_ref REAL NOT NULL,
            max_ref REAL NOT NULL,
            mensaje_bajo TEXT NOT NULL,
            mensaje_alto TEXT NOT NULL,
            explicacion TEXT NOT NULL
        )
        """
    )


def insertar_o_actualizar_datos(cursor):
    for nombre, min_ref, max_ref, mensaje_bajo, mensaje_alto, explicacion in datos_iniciales:
        cursor.execute(
            """
            UPDATE parametros
            SET min_ref = ?,
                max_ref = ?,
                mensaje_bajo = ?,
                mensaje_alto = ?,
                explicacion = ?
            WHERE lower(nombre) = lower(?)
            """,
            (min_ref, max_ref, mensaje_bajo, mensaje_alto, explicacion, nombre),
        )

        if cursor.rowcount == 0:
            cursor.execute(
                """
                INSERT INTO parametros (nombre, min_ref, max_ref, mensaje_bajo, mensaje_alto, explicacion)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (nombre, min_ref, max_ref, mensaje_bajo, mensaje_alto, explicacion),
            )


def main():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        crear_tabla(cursor)
        insertar_o_actualizar_datos(cursor)

    print("Base de datos creada o actualizada correctamente.")


if __name__ == "__main__":
    main()
