#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%
#
# TABLERO PARA LAS SUPERVICIONES - CONTENEDORES
#
#> Autor: Ladino Álvarez Ricardo Arturo
#> Área: CECTI

#%%%%%%%%%%%%%%%% Librerias de uso base %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import os
import pandas as pd
from PIL import Image
import streamlit as st

#%%%%%%%%%%%%%%%% Contenedores de portada %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def Contenedor_Titulo(container):
    container.markdown("""<p style="text-align: center; font-size: 36px;">
                    <b>ANÁLISIS DE RIESGOS PARA LAS SUPERVISIONES</b></p>""",unsafe_allow_html=True)
    container.markdown("""<p style="text-align: center; font-size: 16px;">
                    Coordinación de Evaluación de Comunicaciones y Tecnologías de la información.</p>""",unsafe_allow_html=True)


def Contenedor_Hacienda(container, image_path, width = 250, height = None):
    image = Image.open(image_path)
    if width and height:
        image = image.resize((width, height))
    elif width: 
        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width)
        image = image.resize((width, height))
    
    container.markdown("""<br>""", unsafe_allow_html = True)
    container.image(image)

def Contenedor_SAT(container, image_path, width = 150, height = None):
    image = Image.open(image_path)
    if width and height:
        image = image.resize((width, height))
    elif width: 
        aspect_ratio = image.height / image.width
        height = int(aspect_ratio * width)
        image = image.resize((width, height))
    
    container.markdown("""<br>""", unsafe_allow_html = True)
    container.image(image)



#%%%%%%%%%%%%%%%% Contenedores de Texto %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
#> Contenedor Menu
def CONTENEDOR_M(Tabla):
    # Extracción de datos principales
    Nombre_Unidad = Tabla.iloc[0, 1]
    Clave_Unidad = Tabla.iloc[0, 0]
    Total_Puestos = Tabla.PUESTO_NOM.nunique()
    Si_Riesgo = round((Tabla[Tabla['PTO_RIESGO'] == 'SI'].PUESTO_NOM.nunique() * 100) / Total_Puestos, 2)
    
    # Agrupación y ordenamiento de datos de riesgo
    Puestos_Riesgo = (
        Tabla[Tabla['PTO_RIESGO'] == 'SI']
        .groupby(['CVE_UNIDAD', 'UNIDAD', 'PUESTO_NOM'])['EMPLEADO']
        .nunique()
        .reset_index()
        .sort_values(by='EMPLEADO', ascending=False)
    )
    
    # Extracción de los tres principales puestos de riesgo
    Puestos_Riesgo_Top = Puestos_Riesgo.head(3)
    puestos = Puestos_Riesgo_Top['PUESTO_NOM'].tolist()
    empleados = Puestos_Riesgo_Top['EMPLEADO'].tolist()

    # Rellenar con valores "N/A" si hay menos de 3 filas
    while len(puestos) < 3:
        puestos.append("N/A")
        empleados.append(0)

    # Estilos CSS comunes
    container_style = "height: 100%; width: 100%;"
    card_style = "width: 100%; height: 100%; border: 2px solid #FFFFFF;"
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="{container_style}">
        <div class="row" style="{container_style}">
            <div class="col-12" style="{container_style}">
                <div class="card" style="{card_style}">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            La Unidad Administrativa <b>{Nombre_Unidad}</b>, identificada con la clave <b>{Clave_Unidad}</b>, cuenta con un total de <b>{Total_Puestos}</b> puestos, 
                            de los cuales un <b>{Si_Riesgo}%</b> están clasificados como de alto riesgo. Dentro de este grupo, destacan los puestos de 
                            <b>{puestos[0]}</b>, <b>{puestos[1]}</b> y <b>{puestos[2]}</b>, que agrupan a <b>{empleados[0]}</b>, <b>{empleados[1]}</b> y <b>{empleados[2]}</b> empleados, respectivamente.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)

#%%%%%%%%%%%%%%%% 
## 
#> Contenedor RIESGO PUESTO - Riesgo Puestos
def CONTENEDOR_PR(Tabla):
    # Extracción de datos principales
    Unidad = Tabla.iloc[0,12]
    Total_Puestos = Tabla.PUESTO_NOM.nunique()
    Si_Riesgo = Tabla[Tabla['PTO_RIESGO'] == 'SI'].PUESTO_NOM.nunique()
    # Agrupación y ordenamiento de datos de riesgo
    Puestos_Riesgo = (
        Tabla[Tabla['PTO_RIESGO'] == 'SI']
        .groupby(['CVE_UNIDAD', 'UNIDAD', 'PUESTO_NOM'])['EMPLEADO']
        .nunique()
        .reset_index()
        .sort_values(by='EMPLEADO', ascending=False)
    )
    # Extracción de los tres principales puestos de riesgo
    Puestos_Riesgo_Top = Puestos_Riesgo.head(3)
    puestos = Puestos_Riesgo_Top['PUESTO_NOM'].tolist()
    empleados = Puestos_Riesgo_Top['EMPLEADO'].tolist()
    
    # Rellenar con valores "N/A" si hay menos de 3 filas
    while len(puestos) < 3:
        puestos.append("N/A")
        empleados.append(0)
        
    # Estilos CSS comunes
    container_style = "height: 100%; width: 100%;"
    card_style = "width: 100%; height: 100%; border: 2px solid #FFFFFF;"
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="{container_style}">
        <div class="row" style="{container_style}">
            <div class="col-12" style="{container_style}">
                <div class="card" style="{card_style}">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                        La <b>{Unidad}</b> cuenta con un total de <b>{Total_Puestos}</b> puestos, de los cuales <b>{Si_Riesgo}</b> están clasificados como de riesgo. 
                        El puesto más destacado es <b>{puestos[0]}</b>, con un total de <b>{empleados[0]}</b> empleados.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)


#%%%%%%%%%%%%%%%% 
## 
#> Contenedor Quejas-Denuncias y Nivel de atencion - Riesgo Puestos
def CONTENEDOR_QDNA(Tabla):
    # Extracción de datos principales
    Unidad = Tabla.iloc[0, 12]
    
    # Función para extraer datos de grupos de forma segura
    def obtener_valor(tabla, columna, grupo, criterio):
        resultado = (
            tabla.groupby(grupo)[columna]
            .nunique()
            .reset_index()
            .query(criterio)
            .values.tolist()
        )
        return resultado[0] if resultado else ["N/A", 0]

    # Extraer valores específicos
    PREVE = obtener_valor(Tabla, 'EMPLEADO', 'PREVE_OBS', 'PREVE_OBS == "NO APROBADO"')
    QUE_DEN = obtener_valor(Tabla, 'EMPLEADO', 'ESTATUS', 'ESTATUS == "PROCEDENTE"')
    CRITICO = obtener_valor(Tabla, 'EMPLEADO', 'NIVEL_ATENCION', 'NIVEL_ATENCION == "CRITICO"')
    ALTO = obtener_valor(Tabla, 'EMPLEADO', 'NIVEL_ATENCION', 'NIVEL_ATENCION == "ALTO"')

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            La <b>{Unidad}</b> registra <b>{PREVE[1]}</b> empleados con el estatus <b>NO APROBADO</b> en el ámbito del <b>PREVE</b>.
                            En relación con las quejas y denuncias, se contabilizan <b>{QUE_DEN[1]}</b> empleados con el estatus <b>PROCEDENTE</b>.
                            Adicionalmente, la unidad cuenta con <b>{CRITICO[1]}</b> empleados clasificados en el nivel <b>CRITICO</b> y <b>{ALTO[1]}</b> empleados en el nivel <b>ALTO</b>, requeridos para su atención prioritaria.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content


#%%%%%%%%%%%%%%%% 
## 
#> Contenedor empleado y roles - Riesgo Puestos
def ROLES_EMPLEADO(Tabla):
    # Extracción de datos principales
    EMPLEADO = Tabla.iloc[0, 0]
    PUESTO = Tabla.iloc[0, 1]
    SISTEMAS = Tabla['APLICATIVO'].nunique()

    # Verificar que haya suficientes datos para los aplicativos y roles
    aplicativos_roles = Tabla[['APLICATIVO', 'ROL_APP']].head(3).values.tolist()
    while len(aplicativos_roles) < 3:
        aplicativos_roles.append(["N/A", 0])  # Rellenar con valores por defecto si hay menos de 3 filas

    APLICATIVO_1, ROLES_APP_1 = aplicativos_roles[0]
    APLICATIVO_2, ROLES_APP_2 = aplicativos_roles[1]
    APLICATIVO_3, ROLES_APP_3 = aplicativos_roles[2]

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            El empleado <b>{EMPLEADO}</b>, con el puesto de <b>{PUESTO}</b>, tiene acceso a un total de <b>{SISTEMAS}</b> sistemas.
                            Entre los roles asignados por sistema, el mayor porcentaje corresponde a <b>{APLICATIVO_1}</b>, con un total de <b>{ROLES_APP_1}</b> roles.
                            Le sigue <b>{APLICATIVO_2}</b>, con <b>{ROLES_APP_2}</b> roles asignados, y en tercer lugar se encuentra <b>{APLICATIVO_3}</b>, con <b>{ROLES_APP_3}</b> roles.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content


#%%%%%%%%%%%%%%%% 
## 
#> Contenedor Administración-Puestos - Riesgo Aplicativos
def APLICATIVOS_RIESGOS(Tabla):
    # Número total de Administraciones
    ADMINISTRA = Tabla['DESCONCENTRADA'].nunique()
    
    # Agrupación y ordenamiento de datos
    APLICATIVOS_T = (
        Tabla.groupby('DESCONCENTRADA')['APLICATIVO']
        .nunique()
        .reset_index()
        .sort_values(by='APLICATIVO', ascending=False)
    )
    
    PUESTOS_APP_T = (
        Tabla.groupby('PUESTO_NOM')['APLICATIVO']
        .nunique()
        .reset_index()
        .sort_values(by='APLICATIVO', ascending=False)
    )
    
    # Extraer los principales datos, manejando casos con datos insuficientes
    def obtener_top(df, top_n=2):
        resultados = df.head(top_n).values.tolist()
        while len(resultados) < top_n:
            resultados.append(["N/A", 0])  # Valores predeterminados si hay menos datos
        return resultados

    top_desconcentradas = obtener_top(APLICATIVOS_T, 2)
    top_puestos = obtener_top(PUESTOS_APP_T, 3)

    # Variables principales
    DESCONCE_1, NO_APLIC_1 = top_desconcentradas[0]
    DESCONCE_2, NO_APLIC_2 = top_desconcentradas[1]

    PUESTO_N1, APP_T1 = top_puestos[0]
    PUESTO_N2, APP_T2 = top_puestos[1]
    PUESTO_N3, APP_T3 = top_puestos[2]

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            La Desconcentrada cuenta con un total de <b>{ADMINISTRA}</b> Administraciones, 
                            destacando <b>{DESCONCE_1}</b> como la que registra el mayor número de aplicativos, con un total de <b>{NO_APLIC_1}</b>. 
                            Le sigue <b>{DESCONCE_2}</b> con <b>{NO_APLIC_2}</b> aplicativos registrados.
                            <br><br>
                            En cuanto a los puestos con el mayor número de aplicativos asignados, 
                            <b>{PUESTO_N1}</b> ocupa el primer lugar y el mayor porcentaje con un total de <b>{APP_T1}</b> aplicativos diferentes en uso. 
                            Le sigue <b>{PUESTO_N2}</b>, con <b>{APP_T2}</b>, y finalmente <b>{PUESTO_N3}</b> con un total de <b>{APP_T3}</b>.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)


#%%%%%%%%%%%%%%%% 
## 
#> Contenedor Puestos-Aplicativos - Riesgo Aplicativos
def APP_SISTE_MAX(Tabla):
    # Variables principales
    ADMINISTRA = Tabla.iloc[0, 12]
    TOT_PUE = Tabla['PUESTO_NOM'].nunique()

    # Top puestos con el mayor número de aplicativos
    PTO_MAX = (
        Tabla.groupby(['DESCONCENTRADA', 'PUESTO_NOM'])['APLICATIVO']
        .nunique()
        .reset_index()
        .sort_values(by='APLICATIVO', ascending=False)
        .head(3)
    )
    # Manejo de posibles casos donde no hay suficientes datos
    top_puestos = PTO_MAX[['PUESTO_NOM', 'APLICATIVO']].values.tolist()
    while len(top_puestos) < 3:
        top_puestos.append(["N/A", 0])

    # Variables para los puestos
    PTO_M1, APP_M1 = top_puestos[0]
    PTO_M2, APP_M2 = top_puestos[1]
    PTO_M3, APP_M3 = top_puestos[2]

    # Top aplicativos con el mayor número de usuarios
    APP_MAX = (
        Tabla.groupby(['DESCONCENTRADA', 'APLICATIVO'])['EMPLEADO']
        .count()
        .reset_index()
        .sort_values(by='EMPLEADO', ascending=False)
        .head(3)
    )
    # Manejo de posibles casos donde no hay suficientes datos
    top_apps = APP_MAX[['APLICATIVO', 'EMPLEADO']].values.tolist()
    while len(top_apps) < 3:
        top_apps.append(["N/A", 0])

    # Variables para los aplicativos
    APP_U1, EMP_U1 = top_apps[0]
    APP_U2, EMP_U2 = top_apps[1]
    APP_U3, EMP_U3 = top_apps[2]

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            La <b>{ADMINISTRA}</b> cuenta con un total de <b>{TOT_PUE}</b> puestos, 
                            destacando <b>{PTO_M1}</b> como el puesto con el mayor número de aplicativos registrados en uso, con un total de <b>{APP_M1}</b>. 
                            Le siguen <b>{PTO_M2}</b>, que cuenta con <b>{APP_M2}</b> aplicativos, y <b>{PTO_M3}</b>, con un total de <b>{APP_M3}</b> aplicativos.
                            <br><br>
                            En cuanto a los sistemas con el mayor número de usuarios, el liderazgo lo tiene <b>{APP_U1}</b>, con un total de <b>{EMP_U1}</b> usuarios. 
                            A este le sigue <b>{APP_U2}</b>, con <b>{EMP_U2}</b> usuarios, mientras que <b>{APP_U3}</b> ocupa el tercer lugar con un total de <b>{EMP_U3}</b> usuarios.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)


def DENUNCIAS_CONTE(Tabla):
    # Extracción de valores principales
    UNIDAD = Tabla['UNIDAD'].iat[0]
    FOLIOS = Tabla['D5'].count()
    AN_1 = int(Tabla['D6'].min())
    AN_2 = int(Tabla['D6'].max())

    # Conteo por tipo de reporte
    QUEJA = Tabla.query('D10 == "QUEJA"')['D10'].count()
    DENUNCIA = Tabla.query('D10 == "DENUNCIA"')['D10'].count()
    INVESTIGACION = Tabla.query('D10 == "INVESTIGACIÓN"')['D10'].count()

    # Top 3 clasificaciones del asunto
    CLASE_ASUNTO = (
        Tabla['D9']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'CLASIFICACIÓN', 'D9': 'RECURRENCIAS'})
    ).head(3)

    # Manejo de datos faltantes en CLASE_ASUNTO
    top_clasificaciones = CLASE_ASUNTO.values.tolist()
    while len(top_clasificaciones) < 3:
        top_clasificaciones.append(["N/A", 0])

    CLS_1, CLSV_1 = top_clasificaciones[0]
    CLS_2, CLSV_2 = top_clasificaciones[1]
    CLS_3, CLSV_3 = top_clasificaciones[2]

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            La Unidad <b>{UNIDAD}</b> ha reportado un total de <b>{FOLIOS} Folios SIDEQUS </b>, los cuales incluyen <b>{QUEJA} QUEJAS</b>, 
                            <b>{DENUNCIA} DENUNCIAS</b> y <b>{INVESTIGACION} INVESTIGACIONES</b> entre los años <b>{AN_1}</b> y <b>{AN_2}</b>.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content


def DENUN_PTO(Tabla):
    # Top 3 puestos con mayor número de folios registrados
    PUESTOS = (
        Tabla['S6']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'PUESTO', 'S6': 'FOLIOS'})
    ).head(3)

    # Manejo de datos faltantes en PUESTOS
    top_puestos = PUESTOS.values.tolist()
    while len(top_puestos) < 3:
        top_puestos.append(["N/A", 0])

    PTO_1, FL_PTO_1 = top_puestos[0]
    PTO_2, FL_PTO_2 = top_puestos[1]
    PTO_3, FL_PTO_3 = top_puestos[2]

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            En cuanto a los puestos con mayor número de folios registrados, destacan:
                            <ul>
                                <li><b>{PTO_1}</b>: <b>{FL_PTO_1}</b> folios</li>
                                <li><b>{PTO_2}</b>: <b>{FL_PTO_2}</b> folios</li>
                                <li><b>{PTO_3}</b>: <b>{FL_PTO_3}</b> folios</li>
                            </ul>
                            </ul>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content

def CONTE_CLASS_SUNTO(Tabla):

    # Top 3 clasificaciones del asunto
    CLASE_ASUNTO = (
        Tabla['D9']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'CLASIFICACIÓN', 'D9': 'RECURRENCIAS'})
    ).head(3)

    # Manejo de datos faltantes en CLASE_ASUNTO
    top_clasificaciones = CLASE_ASUNTO.values.tolist()
    while len(top_clasificaciones) < 3:
        top_clasificaciones.append(["N/A", 0])

    CLS_1, CLSV_1 = top_clasificaciones[0]
    CLS_2, CLSV_2 = top_clasificaciones[1]
    CLS_3, CLSV_3 = top_clasificaciones[2]

    # Estilos CSS comunes
    text_style = "text-align: justify; font-size: 15px;"

    # Generación del contenido HTML
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%; width: 100%;">
            <div class="col-12" style="height: 100%; width: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b></b></h6>
                        <p class="card-text" style="{text_style}">
                            En términos de la Clasificación del Asunto, los más relevantes son:
                            <ul>
                                <li><b>{CLS_1}</b>: <b>{CLSV_1}</b> recurrencias</li>
                                <li><b>{CLS_2}</b>: <b>{CLSV_2}</b> recurrencias</li>
                                <li><b>{CLS_3}</b>: <b>{CLSV_3}</b> recurrencias</li>
                            </ul>
                            <br>
                            Para un análisis más detallado, la tabla completa está disponible para descarga en formato <b>EXCEL (.xlsx)</b>.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content
