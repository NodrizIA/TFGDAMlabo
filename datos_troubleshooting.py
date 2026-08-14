"""
Árbol de decisión para el asistente técnico del laboratorio.

Cada nodo representa una pregunta o una conclusión. Las opciones apuntan al
identificador del siguiente nodo, lo que permite ampliar el protocolo sin tocar
las rutas de Flask.
"""

arbol_decision = {
    "inicio": {
        "titulo": "Clasificación inicial",
        "texto": "¿Qué tipo de incidencia has detectado en el laboratorio?",
        "opciones": [
            {"respuesta": "Problema con una muestra de Hematología", "siguiente_paso": "hematologia"},
            {"respuesta": "Fallo en control de calidad (QC)", "siguiente_paso": "qc_fallo"},
            {"respuesta": "Fallo en un equipo o analizador", "siguiente_paso": "equipo"},
            {"respuesta": "Problema con una muestra de Bioquímica", "siguiente_paso": "bioquimica"},
            {"respuesta": "Problema con una muestra de Coagulacion", "siguiente_paso": "coagulacion"},
            {"respuesta": "Valores de referencia, avisos y criticos", "siguiente_paso": "valores_referencia"},
            {"respuesta": "Microbiologia y tinciones", "siguiente_paso": "microbiologia_tinciones"},
        ],
    },
    "valores_referencia": {
        "titulo": "Valores de referencia, avisos y criticos",
        "texto": "Selecciona el area que quieres consultar.",
        "opciones": [
            {"respuesta": "hematologia valores", "siguiente_paso": "hematologia valores"},
            {"respuesta": "bioquimica valores", "siguiente_paso": "bioquimica valores"},
            {"respuesta": "gases valores", "siguiente_paso": "gases valores"},
            {"respuesta": "orina valores", "siguiente_paso": "orina valores"},
            {"respuesta": "coagulacion valores", "siguiente_paso": "coagulacion valores"},
        ],
    },
    "hematologia valores": {
        "titulo": "hematologia valores",
        "texto": "Apartado de valores de referencia, avisos y criticos de Hematologia.",
        "criticidad": "media",
        "permite_imagenes": True,
        "conclusion": True,
    },
    "bioquimica valores": {
        "titulo": "bioquimica valores",
        "texto": "Apartado de valores de referencia, avisos y criticos de Bioquimica.",
        "criticidad": "media",
        "permite_imagenes": True,
        "conclusion": True,
    },
    "gases valores": {
        "titulo": "gases valores",
        "texto": "Apartado de valores de referencia, avisos y criticos de Gases.",
        "criticidad": "media",
        "permite_imagenes": True,
        "conclusion": True,
    },
    "orina valores": {
        "titulo": "orina valores",
        "texto": "Apartado de valores de referencia, avisos y criticos de Orina.",
        "criticidad": "media",
        "permite_imagenes": True,
        "conclusion": True,
    },
    "coagulacion valores": {
        "titulo": "coagulacion valores",
        "texto": "Apartado de valores de referencia, avisos y criticos de Coagulacion.",
        "criticidad": "media",
        "permite_imagenes": True,
        "conclusion": True,
    },
    "microbiologia_tinciones": {
        "titulo": "Microbiologia y tinciones",
        "texto": "Apartado de Microbiologia y tinciones.",
        "criticidad": "media",
        "permite_imagenes": True,
        "conclusion": True,
    },
    "qc_fallo": {
        "titulo": "Control de calidad",
        "texto": "¿Qué regla de Westgard se ha violado?",
        "opciones": [
            {"respuesta": "Regla 1-2s: aviso", "siguiente_paso": "solucion_12s"},
            {"respuesta": "Regla 1-3s: error aleatorio", "siguiente_paso": "solucion_13s"},
            {"respuesta": "Regla 2-2s: error sistemático", "siguiente_paso": "solucion_22s"},
            {"respuesta": "Regla R-4s: error aleatorio", "siguiente_paso": "solucion_r4s"},
        ],
    },
    "equipo": {
        "titulo": "Equipo o analizador",
        "texto": "¿El equipo muestra algún código de error en pantalla?",
        "opciones": [
            {"respuesta": "Sí, hay un código numérico", "siguiente_paso": "solucion_manual"},
            {"respuesta": "No arranca o hace ruido anómalo", "siguiente_paso": "solucion_reiniciar"},
            {"respuesta": "Aspiración o pipeteo irregular", "siguiente_paso": "solucion_aspiracion"},
        ],
    },
    "bioquimica": {
        "titulo": "Muestra de Bioquímica",
        "texto": "¿Cómo se observa visualmente el suero o plasma?",
        "opciones": [
            {"respuesta": "Rojizo: sospecha de hemólisis", "siguiente_paso": "solucion_hemolisis"},
            {"respuesta": "Turbio o lechoso: sospecha de lipemia", "siguiente_paso": "solucion_lipemia"},
            {"respuesta": "Con grumos o filamentos: fibrina", "siguiente_paso": "solucion_fibrina"},
            {"respuesta": "Ictérico: color amarillo intenso", "siguiente_paso": "solucion_ictericia"},
        ],
    },
    "hematologia": {
        "titulo": "Muestra de Hematología",
        "texto": "¿Cuál es el problema detectado en la muestra?",
        "opciones": [
            {"respuesta": "Muestra coagulada", "siguiente_paso": "hema_coagulada"},
            {"respuesta": "Volumen insuficiente", "siguiente_paso": "hema_volumen"},
            {"respuesta": "Valores críticos o incoherentes", "siguiente_paso": "valores_hematologia"},
        ],
    },
        "coagulacion": {
            "titulo": "Muestra de Coagulación",
            "texto": "¿Cuál es el problema detectado en la muestra?",
            "opciones": [
                {"respuesta": "coagulacion coagulada", "siguiente_paso": "coagula_coagulada"},
                {"respuesta": "Mal enrasada", "siguiente_paso": "Fallo_enrasado"},
                {"respuesta": "No coagula", "siguiente_paso": "no_coagula"},
            ],
             },
    "coagula_coagulada": {
        "titulo": "Muestra coagulada",
        "texto": (
            "Rechazar la muestra y solicitar una nueva extracción en tubo citrato. "
            "Verificar que los tiempos de aptt y cefalina coincidan con la actividad a veces el analizador si hace los calculos pero estos son bajos y hay que verificar el rango."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "Fallo_enrasado": {
        "titulo": "Mal enrasada",
        "texto": (
            "Rechazar la muestra y solicitar una nueva extracción en tubo citrato si la extraccion es dificil usar un tubo pediatrico." 
            "verificar que el tubo esta enrasado sin un trasvase de tubo EDTA a citrato cuando esto se hace la cefalina es alta"),
        "criticidad": "alta",
        "conclusion": True,
    },
    "no_coagula": {
        "titulo": "No coagula",
        "texto": (
            "repetir la muestra por otro analizador si la muestra indica un INR ALTO la persona no coagula y estara pasado de medicacion si la muestra da una cefalina alta es probable que exista una contaminacion por Heparina u otro anticoagulante"
            "Verificar que no exista contaminacion por EDTA."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },

            
    "hema_coagulada": {
        "titulo": "Muestra coagulada",
        "texto": (
            "Rechazar la muestra y solicitar una nueva extracción en tubo EDTA. "
            "Verificar que el tubo se mezcle por inversión inmediatamente tras la extracción."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "hema_volumen": {
        "titulo": "Volumen insuficiente",
        "texto": (
            "Comprobar el volumen mínimo requerido por el analizador y solicitar nueva muestra "
            "si no se garantiza la proporción correcta de sangre y anticoagulante."
        ),
        "criticidad": "media",
        "conclusion": True,
    },
    "valores_hematologia": {
        "titulo": "Valores críticos",
        "texto": (
            "Revisar alarmas del analizador, inspeccionar el frotis si procede y repetir la medición. "
            "Si el resultado se confirma, seguir el circuito de comunicación de valores críticos."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "solucion_12s": {
        "titulo": "Regla 1-2s",
        "texto": (
            "Tratarlo como aviso. Revisar tendencia, lote de control y calibración reciente. "
            "Si es un punto aislado, puede aceptarse la serie manteniendo vigilancia."
        ),
        "criticidad": "baja",
        "conclusion": True,
    },
    "solucion_13s": {
        "titulo": "Regla 1-3s",
        "texto": (
            "No validar resultados de pacientes. Repetir el control y comprobar reactivo, calibrador "
            "y mantenimiento del equipo antes de liberar la serie."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "solucion_22s": {
        "titulo": "Regla 2-2s",
        "texto": (
            "Sospecha de error sistemático. Revisar calibración, estabilidad del reactivo, lote del QC "
            "y condiciones de almacenamiento. No validar muestras hasta resolverlo."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "solucion_r4s": {
        "titulo": "Regla R-4s",
        "texto": (
            "Sospecha de error aleatorio. Revisar pipeteo, burbujas, obstrucciones, volumen de muestra "
            "y estado del sistema hidráulico."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "solucion_manual": {
        "titulo": "Código de error",
        "texto": (
            "Registrar el código, consultar el manual del fabricante y aplicar el procedimiento indicado. "
            "Si el error persiste, escalar a soporte técnico con hora, módulo afectado y acciones realizadas."
        ),
        "criticidad": "media",
        "conclusion": True,
    },
    "solucion_reiniciar": {
        "titulo": "Equipo sin arranque correcto",
        "texto": (
            "Apagar el equipo, esperar al menos 30 segundos y reiniciar. Revisar alimentación, red, "
            "temperatura y ruidos anómalos. Si persiste, detener el uso y avisar a soporte."
        ),
        "criticidad": "media",
        "conclusion": True,
    },
    "solucion_aspiracion": {
        "titulo": "Aspiración irregular",
        "texto": (
            "Comprobar sondas, nivel de reactivos, presencia de coágulos o burbujas y realizar limpieza "
            "del circuito según el mantenimiento del fabricante."
        ),
        "criticidad": "media",
        "conclusion": True,
    },
    "solucion_hemolisis": {
        "titulo": "Hemólisis",
        "texto": (
            "Valorar el índice de hemólisis y los analitos afectados. No informar resultados comprometidos "
            "y solicitar nueva muestra si la interferencia invalida la determinación."
        ),
        "criticidad": "alta",
        "conclusion": True,
    },
    "solucion_lipemia": {
        "titulo": "Lipemia",
        "texto": (
            "Si el procedimiento lo permite, ultracentrifugar o aplicar dilución validada. Registrar la "
            "interferencia y tener en cuenta el factor de dilución en la interpretación."
        ),
        "criticidad": "media",
        "conclusion": True,
    },
    "solucion_fibrina": {
        "titulo": "Fibrina",
        "texto": (
            "Recentrifugar la muestra o retirar cuidadosamente el suero limpio evitando arrastrar fibrina. "
            "Si existe riesgo de obstrucción o resultado no fiable, solicitar nueva muestra."
        ),
        "criticidad": "media",
        "conclusion": True,
    },
    "solucion_ictericia": {
        "titulo": "Ictericia",
        "texto": (
            "Revisar el índice ictérico y las posibles interferencias por bilirrubina. Informar la "
            "limitación analítica cuando el método o el equipo lo indiquen."
        ),
        "criticidad": "baja",
        "conclusion": True,
    },
}


def obtener_paso(id_paso):
    return arbol_decision.get(id_paso, arbol_decision["inicio"])


def validar_arbol_decision():
    errores = []

    for id_paso, paso in arbol_decision.items():
        if paso.get("conclusion"):
            continue

        opciones = paso.get("opciones", [])
        if not opciones:
            errores.append(f"El paso '{id_paso}' no tiene opciones ni conclusión.")

        for opcion in opciones:
            siguiente = opcion.get("siguiente_paso")
            if siguiente not in arbol_decision:
                errores.append(f"El paso '{id_paso}' apunta a un nodo inexistente: '{siguiente}'.")

    if errores:
        raise ValueError("Errores en el árbol de decisión:\n" + "\n".join(errores))

    return True
