import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt

DIC_COLORES = {'verde':["#009966"],
               'ro_am_na':["#FFE9C5", "#F7B261","#D8841C", "#dd722a","#C24C31", "#BC3B26"],
               'az_verd': ["#CBECEF", "#81D3CD", "#0FB7B3", "#009999"],
               'ax_viol': ["#D9D9ED", "#2F399B", "#1A1F63", "#262947"],
               'ofiscal': ["#F9F9F9", "#2635bf"]}
st.set_page_config(layout='wide')

datos = pd.read_csv('datasets/finanzas_territoriales.csv')
mapa = gpd.read_parquet('datasets/muns.parquet')
mapa.columns = ['Código Entidad', 'geometry']
mapa['Código Entidad'] = mapa['Código Entidad'].astype(int)


ingresos_ind = ['Ingresos tributarios', 
                'Ingresos no tributarios', 
                'Transferencias de los ingresos corrientes', 
                'Ingresos de capital']
gastos_ind = ['Funcionamiento', 
              'Intereses de deuda pública', 
              'Gastos de capital (Inversión)']
st.title("Finanzas territoriales")

tab1, tab2, tab3 = st.tabs(['Presupuesto',
                            'Mapa',
                            'Treemap'])



with tab1:
        # 
        deptos = datos['Departamento'].unique().tolist()
        depto = st.selectbox("Seleccione el departamento", deptos)
        filtro_depto = datos[datos['Departamento'] == depto]
        entidades = filtro_depto['Entidad'].unique().tolist()
        entidad = st.selectbox("Seleccione la entidad", entidades)
        filtro_entidad = filtro_depto[filtro_depto['Entidad'] == entidad]
        
        st.header("Ingresos")
        filtro_ingresos = filtro_entidad[filtro_entidad['tipo_item'] == 'Ingresos']


        piv_2024 = (filtro_ingresos
                    .groupby('Año')['Valor_24']
                    .sum()
                    .reset_index())

        piv_corr = filtro_ingresos.groupby('Año')['Valor_24'].sum().reset_index()

        #piv_2024['Apropiación a precios constantes (2024)'] /= 1000

        fig = make_subplots(rows=1, cols=2, x_title='Año',  )
        
        fig.add_trace(
            go.Line(
                x=piv_2024['Año'], y=piv_2024['Valor_24'], 
                name='Valor_24', line=dict(color=DIC_COLORES['ax_viol'][1])
            ),
            row=1, col=1
        )

        piv_tipo_gasto = (filtro_ingresos
                        .groupby(['Año', 'Indicador'])['Valor_24']
                        .sum()
                        .reset_index())
        piv_tipo_gasto['total'] = piv_tipo_gasto.groupby(['Año'])['Valor_24'].transform('sum')

        piv_tipo_gasto['%'] = ((piv_tipo_gasto['Valor_24'] / piv_tipo_gasto['total']) * 100).round(2)



            
        for i, group in piv_tipo_gasto.groupby('Indicador'):
            fig.add_trace(go.Bar(
                x=group['Año'],
                y=group['%'],
                name=i
            ), row=1, col=2)

        fig.update_layout(barmode='stack', hovermode='x unified')
        fig.update_layout(width=1000, height=500, legend=dict(orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1), title='Histórico general <br><sup>Cifras en millones de pesos</sup>', yaxis_tickformat='.0f')


        st.plotly_chart(fig, key=17)

        st.header("Gastos")

        filtro_gastos = filtro_entidad[filtro_entidad['tipo_item'] == 'Gastos']
        piv_2024 = (filtro_gastos
                    .groupby('Año')['Valor_24']
                    .sum()
                    .reset_index())

        piv_corr = filtro_gastos.groupby('Año')['Valor_24'].sum().reset_index()

        #piv_2024['Apropiación a precios constantes (2024)'] /= 1000

        fig = make_subplots(rows=1, cols=2, x_title='Año',  )
        
        fig.add_trace(
            go.Line(
                x=piv_2024['Año'], y=piv_2024['Valor_24'], 
                name='Valor_24', line=dict(color=DIC_COLORES['ax_viol'][1])
            ),
            row=1, col=1
        )

        piv_tipo_gasto = (filtro_gastos
                        .groupby(['Año', 'Indicador'])['Valor_24']
                        .sum()
                        .reset_index())
        piv_tipo_gasto['total'] = piv_tipo_gasto.groupby(['Año'])['Valor_24'].transform('sum')

        piv_tipo_gasto['%'] = ((piv_tipo_gasto['Valor_24'] / piv_tipo_gasto['total']) * 100).round(2)



            
        for i, group in piv_tipo_gasto.groupby('Indicador'):
            fig.add_trace(go.Bar(
                x=group['Año'],
                y=group['%'],
                name=i
            ), row=1, col=2)

        fig.update_layout(barmode='stack', hovermode='x unified')
        fig.update_layout(width=1000, height=500, legend=dict(orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1), title='Histórico general <br><sup>Cifras en millones de pesos</sup>', yaxis_tickformat='.0f')


        st.plotly_chart(fig, key=27)


with tab2:
        deptos = datos['Departamento'].unique().tolist()
        depto = st.selectbox("Seleccione el departamento", deptos, key=109)
        filtro_depto = datos[datos['Departamento'] == depto]
        years = filtro_depto['Año'].unique().tolist()
        year = st.selectbox("Seleccione el año", years, key=119)
        filtro_year = filtro_depto[filtro_depto['Año'] == year]
        tipo = st.selectbox("Seleccione entre ingresos y gastos", ['Ingresos', 'Gastos'])

        if tipo == 'Ingresos':
            filtro_tipo = filtro_year[filtro_year['Indicador'].isin(ingresos_ind)]
            tipo_ingreso = st.selectbox("Seleccione un tipo de ingreso", ingresos_ind, key=141)
            filtro_tipo = filtro_tipo[filtro_tipo['Indicador'] == tipo_ingreso]
        else:
            filtro_tipo = filtro_year[filtro_year['Indicador'].isin(gastos_ind)]
            tipo_gasto = st.selectbox("Seleccione un tipo de ingreso", gastos_ind, key=198)
            filtro_tipo = filtro_tipo[filtro_tipo['Indicador'] == tipo_gasto]
              
        
        filtro_datos = filtro_tipo[['Código Entidad', 'Valor_24']]


        merge = filtro_datos.merge(mapa, how='left')
        fig, ax = plt.subplots(1, 1, figsize=(10, 16))
        ax.set_axis_off()
        merge = gpd.GeoDataFrame(merge)
        merge.plot(column='Valor_24', ax=ax)

        st.pyplot(fig)
      
      
with tab3:
    deptos = datos['Departamento'].unique().tolist()
    depto = st.selectbox("Seleccione el departamento", deptos, key=201)
    filtro_depto = datos[datos['Departamento'] == depto]

    entidades = filtro_depto['Entidad'].unique().tolist()
    entidad = st.selectbox("Seleccione la entidad", entidades, key=3454)
    filtro_entidad = filtro_depto[filtro_depto['Entidad'] == entidad]
    years = filtro_entidad['Año'].unique().tolist()
    year = st.selectbox("Seleccione el año", years, key=214)
    filtro_year = filtro_entidad[filtro_entidad['Año'] == year]

    tab1, tab2 = st.tabs(['Ingreso', 'Gasto'])

    with tab1:
        filtro_tipo = filtro_year[filtro_year['Indicador'].isin(ingresos_ind)]

        fig = px.treemap(filtro_tipo, 
                        path=[px.Constant('Ingreso'), 'Indicador'],
                        values='Valor_24',
                        color_discrete_sequence=[DIC_COLORES['ax_viol'][1],
                                                 DIC_COLORES['ro_am_na'][3],
                                                 DIC_COLORES['az_verd'][2],
                                                 DIC_COLORES['az_verd'][0]],
                        title="Matriz de composición anual de ingreso del PGN <br><sup>Cifras en miles de millones de pesos</sup>")
        
        fig.update_layout(width=1000, height=600)
        
        st.plotly_chart(fig)

    with tab2:
        filtro_tipo = filtro_year[filtro_year['Indicador'].isin(gastos_ind)]

        fig = px.treemap(filtro_tipo, 
                        path=[px.Constant('Gasto'), 'Indicador'],
                        values='Valor_24',
                        color_discrete_sequence=[DIC_COLORES['ax_viol'][1],
                                                 DIC_COLORES['ro_am_na'][3],
                                                 DIC_COLORES['az_verd'][2]],
                        title="Matriz de composición anual de ingreso del PGN <br><sup>Cifras en miles de millones de pesos</sup>")
        
        fig.update_layout(width=1000, height=600)
        
        st.plotly_chart(fig)

