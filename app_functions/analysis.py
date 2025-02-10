import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_ranking_tastleatlas(data):
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    countries = list(sorted_data.keys())
    ratings = list(sorted_data.values())

    color = "#FF4C4C" 

    plt.figure(figsize=(6, 4))  
    bars = plt.bar(countries, ratings, color=color, edgecolor='black')


    for rating in range(0, int(max(ratings)) + 1, max(1, int(max(ratings)) // 10)):
        plt.axhline(y=rating, color="gray", linestyle="dashed", linewidth=0.7, alpha=0.6)

  
    plt.title("Top 5 Cocinas del Mundo (TasteAtlas)", fontsize=10)
    plt.xlabel("Países", fontsize=8)
    plt.ylabel("Ratings", fontsize=8)
    plt.ylim(min(ratings) - 0.01, max(ratings) + 0.01)
    plt.xticks(fontsize=7) 
    plt.yticks(fontsize=7)  
    plt.tight_layout()

    plt.show()

def plot_local_establishments_from_df(df):
    sorted_df = df.sort_values(by="local_establishments", ascending=False)

    plt.figure(figsize=(12, 6))
    plt.bar(sorted_df['name'], sorted_df['local_establishments'], color='orange', edgecolor='black')

    plt.title('Número de Establecimientos por Municipio', fontsize=16)
    plt.xlabel('Municipios', fontsize=12)
    plt.ylabel('Número de Establecimientos', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def plot_population_comparison(df):
    sorted_df = df.sort_values(by="population", ascending=False)

    municipalities = sorted_df['name']
    total_population = sorted_df['population']
    working_age_population = sorted_df['working_age_population']

    x = np.arange(len(municipalities)) 
    bar_width = 0.35  

    plt.figure(figsize=(14, 7))
    plt.bar(x - bar_width/2, total_population, width=bar_width, label='Población Total', color='skyblue', edgecolor='black')
    plt.bar(x + bar_width/2, working_age_population, width=bar_width, label='Población en Edad de Trabajar', color='orange', edgecolor='black')

    plt.title('Comparación de Población Total y Población en Edad de Trabajar por Municipio', fontsize=16)
    plt.xlabel('Municipio', fontsize=12)
    plt.ylabel('Población', fontsize=12)
    plt.xticks(x, municipalities, rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def plot_population_density_by_municipality(df):
    municipalities = df['name']
    population_density = df['population_density']
    
    plt.figure(figsize=(10, 6))  
    bars = plt.bar(municipalities, population_density, color='skyblue', edgecolor='black')
    
    max_density = max(population_density)
    for density in range(0, int(max_density) + 1, max(1, int(max_density) // 10)):
        plt.axhline(y=density, color="gray", linestyle="dashed", linewidth=0.7, alpha=0.6)
    
    plt.title('Densidad Poblacional por Municipio', fontsize=14)
    plt.xlabel('Municipio', fontsize=12)
    plt.ylabel('Densidad Poblacional (habitantes/km²)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.tight_layout()
    plt.show()

def plot_salary_line(df):
    sorted_df = df.sort_values(by='average_state_salary', ascending=True)

    plt.figure(figsize=(12, 6))
    plt.plot(sorted_df['name'], sorted_df['average_state_salary'], marker='o', color='green', linewidth=3)

   
    plt.title('Salarios Promedio del Estado por Municipio', fontsize=16)
    plt.xlabel('Municipio', fontsize=12)
    plt.ylabel('Salario Promedio del Estado (CUP)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def calculate_municipality_ranking(df):

    weights = {
    'population_density': 4,
    'working_age_population': 2,
    'average_state_salary': 3
    }
    df['population_density_norm'] = df['population_density'] / df['population_density'].max()
    df['working_age_population_norm'] = df['working_age_population'] / df['working_age_population'].max()
    df['average_state_salary_norm'] = df['average_state_salary'] / df['average_state_salary'].max()

    df['score'] = (
        weights['population_density'] * df['population_density_norm'] +
        weights['working_age_population'] * df['working_age_population_norm'] +
        weights['average_state_salary'] * df['average_state_salary_norm']
    )

    df['rank'] = df['score'].rank(ascending=False).astype(int)

    return df.sort_values(by='rank')

def analyze_restaurant_features(df, municipalities, restaurant_type):
    filtered_df = df[(df['municipality'].isin(municipalities)) & (df['specialty'] == restaurant_type)]
    total_restaurants = len(filtered_df)
    
    features = ["phone", "website", "facebook", "instagram", "parking", "reservations", "delivery", "power plant"]
    counts = {}
    for feature in features:
        if feature in ["phone", "website", "facebook", "instagram"]:
            counts[feature] = filtered_df["contacts"].apply(lambda x: bool(x.get(feature))).sum()
        else:
            counts[feature] = filtered_df["services"].apply(lambda x: x.get(feature, False)).sum()
    
    counts["total_restaurants"] = total_restaurants
    return counts

def plot_restaurant_features(counts):
    total = counts["total_restaurants"]
    features = ["phone", "website", "facebook", "instagram", 
                "parking", "reservations", "delivery", "power plant"]
    
    values = [counts[feature] for feature in features]
    percentages = [(v / total) * 100 for v in values]

    fig, ax = plt.subplots(figsize=(8, 5)) 
    bars = ax.bar(features, percentages, color="darkblue", alpha=0.8, edgecolor="black")
    for percent in range(10, 101, 10):
        ax.axhline(y=percent, color="gray", linestyle="dashed", linewidth=0.7, alpha=0.6)
    
    for bar, value, count in zip(bars, percentages, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f"{count}", ha="center", fontsize=10, color="black")

    ax.set_xlabel("Características", fontsize=11)
    ax.set_ylabel("Porcentaje de restaurantes (%)", fontsize=11)  
    ax.set_title("Porcentaje de restaurantes que cumplen cada característica", fontsize=13)
    ax.set_ylim(0, 110)
    plt.xticks(rotation=45)

    plt.tight_layout() 
    plt.show()
    
def plot_avg_menu_prices(df, municipalities, specialty):
    filtered_df = df[df['municipality'].isin(municipalities) & (df['specialty'] == specialty)]
    def avg_price(menu):
        return {category: sum(prices.values()) / len(prices) if prices else 0 
                for category, prices in menu.items()}

    avg_prices = filtered_df['menu'].apply(avg_price)

    avg_prices_df = pd.DataFrame(list(avg_prices))

    avg_prices_by_category = avg_prices_df.mean()

    avg_prices_by_category = avg_prices_by_category[avg_prices_by_category > 0]

    ax = avg_prices_by_category.plot(kind='bar', color='lightgreen', edgecolor='black',
                                     title=f'Precios Promedio del Menú para {specialty} en Municipios Seleccionados')
    
    ax.grid(axis='y', linestyle='--', linewidth=0.7)

    plt.xlabel('Categorías del Menú')
    plt.ylabel('Precio Promedio (CUP)')

    for i, v in enumerate(avg_prices_by_category):
        ax.text(i, v + 2, f'{v:.2f}', ha='center', va='bottom', fontsize=10)
    plt.show()
    
    
    
def analyze_opening_hours(df, municipalities, specialty):
    # Filtrar el DataFrame por municipios y especialidad
    df_filtered = df[(df["municipality"].isin(municipalities)) & (df["specialty"] == specialty)]
    print(f"Restaurantes analizados: {len(df_filtered)}")  # Número de restaurantes analizados

    # Diccionario para contar cuántos restaurantes están abiertos en cada hora (00-23)
    hours_count = {hour: 0 for hour in range(24)}
    
    # Iteramos sobre cada restaurante filtrado
    for _, row in df_filtered.iterrows():
        try:
            schedule_data = row["hours"]  # Diccionario con horarios por día
            
            # Iteramos sobre cada día de la semana
            for day, schedule in schedule_data.items():  
                if isinstance(schedule, str) and "_" in schedule:
                    # Extraer la hora de apertura y cierre
                    opening, closing = map(int, schedule.split("_"))
                    
                    # Convertir de formato HHMM a HH (1000 → 10, 2000 → 20)
                    opening //= 100  
                    closing //= 100  

                    # Registrar las horas en las que el restaurante está abierto
                    for hour in range(opening, closing):
                        if hours_count.get(hour) is not None:
                            hours_count[hour] += 1
        except Exception as e:
            print(f"Error procesando horarios para {row['name']}: {e}")
    
    return hours_count

def plot_opening_hours(hours_count):
    # Filtramos las horas que realmente tienen restaurantes abiertos
    hours = list(hours_count.keys())
    open_counts = list(hours_count.values())
    
    # Verificamos que solo se muestren las horas con datos (si hay horas sin datos, no se muestran)
    if not hours_count:
        print("No hay datos para mostrar.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño ajustado
    
    # Graficamos las barras con borde
    ax.bar(hours, open_counts, color="darkblue", alpha=0.8, edgecolor="black")
    
    # Líneas discontinuas para referencia en el eje Y
    max_count = max(open_counts)
    for count in range(0, max_count + 1, max(1, max_count // 10)):
        ax.axhline(y=count, color="gray", linestyle="dashed", linewidth=0.7, alpha=0.6)
    
    # Añadimos las etiquetas encima de las barras
    for i, v in enumerate(open_counts):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=10, color="white")
    
    # Etiquetas y título
    ax.set_xlabel("Hora del día", fontsize=12)
    ax.set_ylabel("Cantidad de restaurantes abiertos", fontsize=12)
    ax.set_title("Cantidad de restaurantes abiertos por hora", fontsize=14)
    
    # Ajustamos las horas para el eje X (de 0 a 23)
    plt.xticks(range(0, 24, 1))  # Mostrar todas las horas
    plt.grid(axis="x", linestyle="dotted", alpha=0.5)
    
    plt.tight_layout()
    plt.show()
