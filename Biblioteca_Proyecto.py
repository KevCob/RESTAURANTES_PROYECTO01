###Biblioteca del proyecto###
import plotly.graph_objects as go 


def c_moda(valor):
    valor_repeticiones = {} 
    for i in valor:
        if i in valor_repeticiones:
            valor_repeticiones[i] += 1
        else:
            valor_repeticiones[i] = 1
    valor_con_mas_repeticiones = max(valor_repeticiones, key=valor_repeticiones.get)
    return valor_con_mas_repeticiones

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

def c_precio_medio(filas):
    precios = []
    for i in ["menu.starters", "menu.mains", "menu.fittings", "menu.pizza", "menu.paste", "menu.additions", "menu.sandwich", "menu.desserts", "menu.cocktails", "menu.drinks", "menu.infusions"]:
        if i in filas and isinstance(filas[i], list):  
            precios.extend([item["price"] for item in filas[i] if isinstance(item, dict) and item.get("price") is not None])
    return round(sum(precios) / len(precios)) if precios else None  

def c_suma_minima(menu):
    categorias_principales = ["pizza", "paste", "mains"]
    bebidas = "drinks"

    precios_principales = [item["price"] for categoria in categorias_principales if categoria in menu for item in menu[categoria] if "price" in item]

    if any(price is None for price in precios_principales):
        return None

    precios_bebidas = [item["price"] for item in menu.get(bebidas, []) if "price" in item]

    if any(price is None for price in precios_bebidas):
        return None

    if precios_principales and precios_bebidas:
        return min(precios_principales) + min(precios_bebidas)
    else:
        return None

def c_adsequible(x, data):
    data["min_sum_price"] = data["menu"].apply(c_suma_minima)
    adsequible = data[(data["min_sum_price"] <= x) & (data["type"] == "Bar-Restaurante")]
    return adsequible[["name", "min_sum_price"]]