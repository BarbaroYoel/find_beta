import pandas as pd
import json
import glob
# import os

def crear_data_frame():
 # direccion relativa , modificar  
 ruta_archivos = "/home/barbaro-yoel/Documentos/Estudio/MATCOM/Data Science/1ro/Primer Semestre/IP - ICD/Proyecto ICD-IP/Find Beta/data/restaurants_bars/*.json"

 data = []
 
 for archivo in glob.glob(ruta_archivos):
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = json.load(f)
        data.append(contenido)

 df = pd.DataFrame(data)
 return df

df =crear_data_frame()

print(df)