import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_ranking_tastleatlas(data):
    countries = list(data.keys())
    ratings = list(data.values())


    plt.figure(figsize=(6, 4))  
    bars = plt.bar(countries, ratings, color="skyblue", edgecolor='black')


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
    plt.bar(sorted_df['name'], sorted_df['average_state_salary'], color='orange', edgecolor='black')

   
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
    
    

    
    
def plot_avg_menu_price(df,municipalities,specialty):
    filtered_df = df[df['municipality'].isin(municipalities) & (df['specialty'] == specialty)]
    avg_menu={
        "breakfasts":[],
        "starters":[],
        "main_courses":[] ,
        "additions": [],
        "fittings":[],
        "desserts": [],
        "drinks":[],
        "plus": []
    } 
    
    for _,row in filtered_df.iterrows():
      menu=row.get("menu",{})
      
      for category,items in menu.items():
        all_dish=[]
        if isinstance(items, dict):
          for price in items.values():
            all_dish.append(price)
        if len(all_dish)!=0:
            avg_menu[category].append(sum(all_dish)/len(all_dish)) 
    
    for category,avg in avg_menu.items():
        if len(avg)!=0:
         avg_menu[category]=sum(avg)/len(avg)
    
    list_category=list(avg_menu.keys())
    list_price=list(avg_menu.values())
    
    list_category=list_category[1:-1]
    list_price=list_price[1:-1]
    
    print(list_category)
    print(list_price)

    plt.figure(figsize=(12, 6))
    plt.bar(list_category, list_price, color='skyblue', edgecolor='black')

    plt.title('Precios por Categorías en el Menú', fontsize=16)
    plt.xlabel('Categorías', fontsize=12)
    plt.ylabel('Precios', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()