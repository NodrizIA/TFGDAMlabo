import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "laboratorio.db"

# Estructura: (Nombre, Min_Hombre, Max_Hombre, Min_Mujer, Max_Mujer, Unidades, Msj_Bajo, Msj_Alto, Explicacion)
datos_iniciales = [
    (
        "Glucosa", 
        70.0, 100.0, 70.0, 100.0, "mg/dL",
        "Hipoglucemia: ingesta de hidratos de absorción rápida y valoración clínica.",
        "Hiperglucemia: posible diabetes, estrés metabólico u otra alteración endocrina.",
        "La glucosa es la principal fuente de energía y debe interpretarse según ayuno y contexto clínico."
    ),
    (
        "Colesterol Total", 
        0.0, 200.0, 0.0, 200.0, "mg/dL",
        "Nivel bajo: habitualmente no preocupante, valorar contexto nutricional.",
        "Hipercolesterolemia: posible aumento del riesgo cardiovascular.",
        "El colesterol es un lípido necesario, pero valores elevados requieren valoración del perfil lipídico."
    ),
    (
        "Hemoglobina", 
        13.5, 17.5, 12.0, 15.5, "g/dL",
        "Anemia: posible déficit de hierro, sangrado, inflamación u otra causa hematológica.",
        "Poliglobulia: aumento de glóbulos rojos; valorar hidratación, hipoxia y otras causas.",
        "Proteína de los hematíes responsable del transporte de oxígeno."
    ),
    (
        "Creatinina", 
        0.7, 1.3, 0.6, 1.1, "mg/dL",
        "Valores bajos: posible disminución de masa muscular o desnutrición.",
        "Valores altos: posible alteración de la función renal.",
        "Producto de desecho muscular. Es el indicador principal para evaluar cómo filtran los riñones."
    ),
    (
        "Ácido Úrico", 
        3.4, 7.0, 2.4, 6.0, "mg/dL",
        "Hipouricemia: poco frecuente, revisar dieta o medicación.",
        "Hiperuricemia: aumento del riesgo de gota o cálculos renales.",
        "Producto final del metabolismo de las purinas, eliminado principalmente por la orina."
    ),
    (
        "Triglicéridos", 
        0.0, 150.0, 0.0, 150.0, "mg/dL",
        "Nivel bajo: habitualmente no preocupante, valorar contexto nutricional.",
        "Hipertrigliceridemia: posible riesgo cardiovascular y pancreatitis.",
        "Los triglicéridos son un tipo de grasa en la sangre; niveles altos requieren cambios en dieta y estilo de vida."
    ),
    (
        "GOT (AST)", 
        10.0, 40.0, 10.0, 40.0, "U/L",
        "Valores bajos: generalmente no clínicamente relevantes.",
        "Elevación: posible daño hepático o muscular; valorar contexto clínico.",
        "Enzima presente en hígado y músculo; su elevación puede indicar lesión tisular."
    ),
    (
        "GPT (ALT)", 
        7.0, 56.0, 7.0, 56.0, "U/L",
        "Valores bajos: generalmente no clínicamente relevantes.",
        "Elevación: posible daño hepático; valorar contexto clínico.",
        "Enzima principalmente hepática; su elevación suele indicar lesión del hígado."
    ),
    (
        "LDH", 
        100.0, 250.0, 100.0, 250.0, "U/L",
        "Valores bajos: generalmente no clínicamente relevantes.",
        "Elevación: posible daño tisular; valorar contexto clínico.",
        "Enzima presente en músculo, hígado y otros tejidos; su elevación puede indicar lesión tisular."
    ),
    (
        "Albumina", 
        3.4, 5.4, 3.4, 5.4, "g/dL",
        "Hipoalbuminemia: posible malnutrición, enfermedad hepática (cirrosis) o síndrome nefrótico.",
        "Hiperalbuminemia: generalmente indica deshidratación aguda.",
        "Es la proteína más abundante en el plasma sanguíneo, fundamental para mantener la presión oncótica."
    ),
    (
        "CPK (Creatina Quinasa)", 
        55.0, 170.0, 30.0, 135.0, "U/L",
        "Valores bajos: habitualmente sin significación clínica (poca masa muscular o vida muy sedentaria).",
        "Elevación: posible daño muscular (rabdomiólisis), infarto agudo de miocardio o ejercicio muy intenso.",
        "Enzima presente en el corazón, cerebro y músculo esquelético. Sus niveles cambian drásticamente por sexo y masa muscular."
    ),
    (
        "Troponina I", 
        0.0, 0.04, 0.0, 0.04, "ng/mL",
        "Valor normal. No se detecta daño miocárdico agudo.",
        "Nivel elevado: ¡ALERTA! Indicador altamente específico de daño miocárdico (Infarto de miocardio).",
        "Proteína del músculo cardíaco. En condiciones normales no debe estar en la sangre o sus niveles deben ser indetectables."
    ),
    (
        "TSH (Tirotropina)", 
        0.4, 4.0, 0.4, 4.0, "mUI/L",
        "Posible hipertiroidismo. La glándula tiroides está hiperactiva, frenando la producción de TSH.",
        "Posible hipotiroidismo. La glándula tiroides no produce suficiente hormona, elevando la TSH.",
        "Hormona producida por la hipófisis en el cerebro que actúa como el 'termostato' de la glándula tiroides."
    ),
    (
        "T3 Libre", 
        2.0, 4.4, 2.0, 4.4, "pg/mL",
        "Hipotiroidismo o síndrome del enfermo eutiroideo (enfermedad grave no tiroidea).",
        "Hipertiroidismo (ej. Enfermedad de Graves) o inflamación tiroidea aguda.",
        "Es la hormona tiroidea biológicamente activa que regula directamente el metabolismo de las células."
    ),
    (
        "T4 Libre", 
        0.9, 1.7, 0.9, 1.7, "ng/dL",
        "Hipotiroidismo primario (falla tiroidea) o secundario (falla hipofisaria).",
        "Hipertiroidismo. Acelera el metabolismo (pérdida de peso, taquicardia, ansiedad).",
        "Hormona principal producida por la tiroides. Sirve como reserva y se convierte en T3 en los tejidos."
    )
]


def crear_tabla(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS parametros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            min_ref_m REAL NOT NULL,
            max_ref_m REAL NOT NULL,
            min_ref_f REAL NOT NULL,
            max_ref_f REAL NOT NULL,
            unidades TEXT NOT NULL,
            mensaje_bajo TEXT NOT NULL,
            mensaje_alto TEXT NOT NULL,
            explicacion TEXT NOT NULL
        )
        """
    )

def insertar_o_actualizar_datos(cursor):
    for nombre, min_m, max_m, min_f, max_f, uni, msg_bajo, msg_alto, exp in datos_iniciales:
        cursor.execute(
            """
            UPDATE parametros
            SET min_ref_m = ?,
                max_ref_m = ?,
                min_ref_f = ?,
                max_ref_f = ?,
                unidades = ?,
                mensaje_bajo = ?,
                mensaje_alto = ?,
                explicacion = ?
            WHERE lower(nombre) = lower(?)
            """,
            (min_m, max_m, min_f, max_f, uni, msg_bajo, msg_alto, exp, nombre),
        )

        if cursor.rowcount == 0:
            cursor.execute(
                """
                INSERT INTO parametros (nombre, min_ref_m, max_ref_m, min_ref_f, max_ref_f, unidades, mensaje_bajo, mensaje_alto, explicacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (nombre, min_m, max_m, min_f, max_f, uni, msg_bajo, msg_alto, exp),
            )

def main():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        crear_tabla(cursor)
        insertar_o_actualizar_datos(cursor)

    print("Base de datos creada o actualizada correctamente con rangos por sexo.")

if __name__ == "__main__":
    main()
