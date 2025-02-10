###Biblioteca del proyecto###
import pandas as pd
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import folium as fl
import ipywidgets as wi
from collections import Counter
from IPython.display import display
import Biblioteca_Proyecto as bp
import os
import json


def c_porciento(parte, total):
    if total == 0:
        return "Error"
    else: 
        return (parte/total)*100 

def c_media(datos):
    suma = sum(datos)
    n = len(datos)
    media = suma / n
    return media

def c_media_diccionario(datos):
    promedios = {}
    for i, valores in datos.items():
        if valores:
            suma = sum(valores)
            n = len(valores)
            media = suma / n
            promedios[i] = media
        else:
            promedios[i] = 0 
    return promedios

def c_mediana(datos):
    datos_ordenados = sorted(datos)
    n = len(datos)
    if n % 2 == 1:
        mediana = datos_ordenados[n // 2]
    else:
        mediana = (datos_ordenados[n // 2 - 1] + datos_ordenados[n // 2]) / 2
    return mediana
    
def c_grafico(datos, nombre_categoria, color):
    nombres = [item[0] for item in datos]
    frecuencias = [item[1] for item in datos]
    return go.Bar(x=nombres, y=frecuencias, name=nombre_categoria, marker_color=color)

def i_nombre(nombre):
    nombre_igualado = nombre.lower().strip()
    return nombre_igualado



def encontrar_comunes(data, tipo_menu):
    nombres = []
    comunes = []
    
    for i, row in data.iterrows():
        menus = row["menu"]
        if isinstance(menus, dict) and tipo_menu in menus:
            for item in menus[tipo_menu]:
                nombre = item.get("item_name")
                if nombre is not None:
                    nombre_igualado = i_nombre(nombre)
                    nombres.append(nombre_igualado)
    counter = Counter(nombres)
    tres_mas_comunes = counter.most_common(3)
    for nombre, frecuencia in tres_mas_comunes:
        comunes.append((nombre, frecuencia))
    
    return comunes

def obtener_restaurantes_por_municipio(data, municipio):
    resultados = []

    for i, row in data.iterrows():
        ubicacion = row.get('location', {})
        if ubicacion.get('municipe', '').lower().strip() == municipio.lower().strip():
            nombre_restaurante = row.get('name', 'Desconocido')
            menu = row.get('menu', {})
            platos_principales = menu.get('mains', [])

            if platos_principales:
                platos_principales = [i for i in platos_principales if i.get('price') is not None]

                if platos_principales:
                    plato_mas_caro = platos_principales[0]
                    for i in platos_principales:
                        if i['price'] > plato_mas_caro['price']:
                            plato_mas_caro = i

                    plato_mas_barato = platos_principales[0]
                    for i in platos_principales:
                        if i['price'] < plato_mas_barato['price']:
                            plato_mas_barato = i

                    resultados.append({
                        'nombre_restaurante': nombre_restaurante,
                        'plato_mas_caro': plato_mas_caro.get('item_name', 'N/A'),
                        'precio_mas_caro': plato_mas_caro.get('price', 'N/A'),
                        'plato_mas_barato': plato_mas_barato.get('item_name', 'N/A'),
                        'precio_mas_barato': plato_mas_barato.get('price', 'N/A')
                    })

    return pd.DataFrame(resultados)


def obtener_cinco_platos_mas_caros(data2):
    def obtener_precio(plato):
        return plato.get("price")  

    platos_principales = data2.get("menu.mains")

    todos_platos = []
    for lista_platos in platos_principales:
        if isinstance(lista_platos, list):
            todos_platos.extend(lista_platos)

    platos_sin_null = []
    for plato in todos_platos: 
        if "price" in plato and plato["price"] is not None:
            platos_sin_null.append(plato)

    platos_principales_ordenados = sorted(platos_sin_null, reverse=True, key=obtener_precio)
    cinco_platos_caros = platos_principales_ordenados[:5]

    nombres = []
    precios = []
    for plato in cinco_platos_caros:
        nombres.append(plato.get("item_name", "Desconocido")) 
        precios.append(plato.get("price", 0))

    return nombres, precios

def contar_establecimientos(data):
    tipo = data["type"]
    municipios_principales = data["location.municipe"].str.lower().str.strip()

    plaza_count = 0
    octubre_count = 0
    vieja_count = 0

    for i in range(len(tipo)):
        if tipo[i] in ["Cafeteria", "Restaurante-Cafeteria", "Bar-Restaurante-Cafeteria"]:
            municipio = municipios_principales[i]
            if municipio == "plaza de la revolucion":
                plaza_count += 1
            elif municipio == "10 de octubre":
                octubre_count += 1
            elif municipio == "habana vieja":
                vieja_count += 1

    return {"Plaza": plaza_count, "10 de Octubre": octubre_count, "La Habana Vieja": vieja_count}


def obtener_precios_platos_principales(data, municipios):
    precios = {municipio: [] for municipio in municipios}

    data['location.municipe'] = data['location.municipe'].str.strip()

    data_filtrado = data[data['location.municipe'].isin(municipios)]

    for i, row in data_filtrado.iterrows():
        municipio = row['location.municipe']
        mains = row['menu.mains']
        for plato in mains:
            if plato['price'] is not None:
                precios[municipio].append(plato['price'])

    return precios

def calcular_porcentaje_restaurantes_cubanos(dataframe, municipios_interes):
    restaurantes_interes = []
    for i, row in dataframe.iterrows():
        if row['location.municipe'].lower().strip() in municipios_interes:
            restaurantes_interes.append(row.to_dict())

    total_restaurantes = {municipio: 0 for municipio in municipios_interes}
    for restaurante in restaurantes_interes:
        municipio = restaurante['location.municipe'].lower().strip()
        total_restaurantes[municipio] += 1

    restaurantes_cubanos = []
    for restaurante in restaurantes_interes:
        if isinstance(restaurante['specialized_food'], list):
            specialized_food_clean = [food.lower().strip() for food in restaurante['specialized_food']]
            if "cubana" in specialized_food_clean or "comida cubana" in specialized_food_clean :
                restaurantes_cubanos.append(restaurante)

    cubanos_por_municipio = {municipio: 0 for municipio in municipios_interes}
    for restaurante in restaurantes_cubanos:
        municipio = restaurante['location.municipe'].lower().strip()
        cubanos_por_municipio[municipio] += 1

    porcentaje_cubanos = {}
    for municipio in municipios_interes:
        if total_restaurantes[municipio] > 0:
            porcentaje_cubanos[municipio] = (cubanos_por_municipio[municipio] / total_restaurantes[municipio]) * 100
        else:
            porcentaje_cubanos[municipio] = 0


    return porcentaje_cubanos