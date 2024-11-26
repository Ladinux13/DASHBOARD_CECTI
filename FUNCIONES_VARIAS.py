#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%
#
# TABLERO PARA LAS SUPERVICIONES - CONTENEDORES
#
#> Autor: Ladino Álvarez Ricardo Arturo
#> Área: CECTI

#%%%%%%%%%%%%%%%% Librerias de uso base %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import pandas as pd
from io import BytesIO
import streamlit as st
import geopandas as gpd


@st.cache_data(persist=True, hash_funcs={pd.DataFrame: lambda x: x.to_csv(index=False)})
def Base_Datos(uploaded_file):
    BASE_USO = pd.read_pickle(uploaded_file)
    return (BASE_USO)

@st.cache_data(persist=True, hash_funcs={pd.DataFrame: lambda x: x.to_csv(index=False)})
def Base_Mapa(uploaded_file):
    MAPA_BASE = gpd.read_file(uploaded_file)
    return (MAPA_BASE)


def Puestos_Metricas (Tabla):
    TOTAL_PUESTOS = Tabla.PUESTO_NOM.nunique()
    TOTAL_PUESTOS_RIESGO = Tabla[Tabla['PTO_RIESGO'] == 'SI'].PUESTO_NOM.nunique()
    return (TOTAL_PUESTOS,TOTAL_PUESTOS_RIESGO)


def APLICATIVOS_DETALLES(Tabla):
    ''' '''
    NIVELES = ['CRITICO', 'ALTO', 'MEDIO']
    DETALLE = Tabla[Tabla['NIVEL_ATENCION'].isin(NIVELES)].groupby(['RFC_CORTO','EMPLEADO', 'NOMBRE_EMP', 
                                                                          'PTO_RIESGO', 'PREVE_OBS', 'DENUNCIAS',
                                                                          'NIVEL_ATENCION'])['APLICATIVO'].nunique().reset_index()
    
    SISTEMA = Tabla[Tabla['NIVEL_ATENCION'].isin(NIVELES)].groupby(['NOMBRE_EMP','PUESTO_NOM','APLICATIVO'])['ROL_APP'].\
                          nunique().reset_index().sort_values(by=['ROL_APP'], ascending=False)
    
    return (DETALLE, SISTEMA)


def EXP_TABLA(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.close() 
            processed_data = output.getvalue()
            return processed_data


def DENUNCIAS_INFO(Tabla):
    def Rename_SAT(Data, Pre, Letra):
        Name = ['{}{}'.format(Pre, Letra.format(i+1)) for i in range(len(Data.columns))]
        Dict = dict(zip(Data.columns, Name))
        Data = Data.rename(columns=Dict)
        return Data
        
    Tabla = Rename_SAT(Tabla, 'D', '{}')
    
    FOLIOS = Tabla.groupby(['D1','D10'])['D10'].count().sum()
    
    ASUNTOS = Tabla.D14.value_counts().reset_index().rename({'count':'VALUE'}, axis = 1)

    DENUNCIA_QUEJA = Tabla.D15.value_counts().reset_index().rename({'count':'VALUE'}, axis = 1)

    PUESTOS = Tabla.D8.value_counts().reset_index().rename({'count':'VALUE'}, axis = 1)[:7]

    return (ASUNTOS, DENUNCIA_QUEJA, PUESTOS)
