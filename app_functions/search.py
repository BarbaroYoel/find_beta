import pandas as pd
from rapidfuzz.fuzz import partial_ratio

def search_by_municipality(df, municipality):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not isinstance(municipality, str):
        raise ValueError("El argumento 'municipality' debe ser una cadena de texto.")
    
    filtered_df = df[df['municipality'] == municipality]
    
    if filtered_df.empty:
        print(f"No se encontraron resultados para el municipio: {municipality}")
    return filtered_df


def search_by_name(df, name, threshold=80):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not name or not isinstance(name, str):
        raise ValueError("El argumento 'name' debe ser una cadena de texto.")
    
    name = name.lower()
    filtered_rows = []
    
    for _, row in df.iterrows():
       restaurant_name = row.get("name", "").lower()
       if partial_ratio(name, restaurant_name) >= threshold:
          filtered_rows.append(row)
    filtered_df = pd.DataFrame(filtered_rows)
   
    if filtered_df.empty:
        print(f"No se econtraron resultados para el nombre'{name}'.")
    return filtered_df


def search_by_owner(df, owner_type):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not isinstance(owner_type, str):
        raise ValueError("El argumento 'owner_type' debe ser una cadena de texto.")
    
    filtered_df = df[df['owner']==owner_type]
    
    if filtered_df.empty:
        print(f"No se encontraron resultados para el tipo de dueño: {owner_type}")
    return filtered_df.reset_index(drop=True)


def search_by_specialty(df, specialty):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not isinstance(specialty, str):
        raise ValueError("El argumento 'specialty' debe ser una cadena de texto.")
 
    filtered_df = df[df['specialty']==specialty]
   
    if filtered_df.empty:
        print(f"No se encontraron resultados para la especialidad: {specialty}")
    return filtered_df


def search_by_type(df, establishment_type):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not isinstance(establishment_type, str):
        raise ValueError("El argumento 'establishment_type' debe ser una cadena de texto.")
    
    filtered_df = df[df['type']==establishment_type]
    
    if filtered_df.empty:
        print(f"No se encontraron resultados para el tipo de local: {establishment_type}")
    return filtered_df.reset_index(drop=True)


def search_by_rating(df, min_rating):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not isinstance(min_rating, (int, float)):
        raise ValueError("El argumento 'min_rating' debe ser un número.")
    
    filtered_rows = []
    for _, row in df.iterrows():
        ratings = row.get("ratings", {})
        for value in dict(ratings).values(): 
            if isinstance(value, (int, float)) and value >= min_rating:
                filtered_rows.append(row) 
                break
  
    filtered_df = pd.DataFrame(filtered_rows)
    
    if filtered_df.empty:
        print(f"No se encontraron locales con una calificación mínima de {min_rating}.")
    return filtered_df.reset_index(drop=True)


def search_by_open_locals(df,day,time):
    if not isinstance(df,pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not isinstance(day,str) or not isinstance(time,str) or len(time)!=4:
        raise ValueError("El argumento 'day' debe ser un texto y 'time' debe ser una hora válida en formato 'HHMM'.")
   
    time=int(time)
    day=day.lower()
    filtered_rows=[]
   
    for _, row in df.iterrows():
        hours = row.get("hours",{})
        if day in hours:
          schedule = hours[day]
          if schedule and "_" in schedule:
            opening_time, closing_time = str(schedule).split("_")
            opening_time = int(opening_time)
            closing_time = int(closing_time)
            if opening_time <= closing_time:
                if opening_time <= time <= closing_time:
                    filtered_rows.append(row)
            else:
                if time >= opening_time or time <= closing_time:
                   filtered_rows.append(row)
  
    open_df=pd.DataFrame(filtered_rows)
    
    if open_df.empty:
        print(f"No se encontraron locales abiertos el {day} a las {time}.")
    return open_df.reset_index(drop=True)    
    
    
def search_by_services(df, services):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df' debe ser un DataFrame de Pandas.")
    if not services or not isinstance(services, list):
        raise ValueError("Los servicios deben proporcionarse como una lista no vacía.")
  
    filtered_rows=[]

    for _, row in df.iterrows():
       services_dic=row.get("services",{})
       all = True
       for service in services:
            if service not in services_dic or services_dic[service] is None or not services_dic[service]:
                all = False
                break
       if all:
        filtered_rows.append(row)
    
    df_filtrado =pd.DataFrame(filtered_rows)
    if df_filtrado.empty:
        print("No se encontraron locales que ofrezcan todos los servicios especificados.")
    return df_filtrado.reset_index(drop=True)


def search_by_payment_methods(df, payment_methods):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("La entrada debe ser un objeto pandas DataFrame.")
    if not payment_methods or not isinstance(payment_methods, list):
        raise ValueError("Los métodos de pago deben proporcionarse como una lista no vacía.")
    
    filtered_rows = []
    for _, row in df.iterrows():
    
        row_payment_methods = row.get('payment_methods', [])
        meets_criteria = True
        for method in payment_methods:
            if method not in row_payment_methods:
                meets_criteria = False
                break

        if meets_criteria:
            filtered_rows.append(row)

    df_filtered = pd.DataFrame(filtered_rows)
    if df_filtered.empty:
        print("No se encontraron locales que acepten todos los métodos de pago especificados.")
    return df_filtered.reset_index(drop=True)
    
    
def search_by_dish(df, dish, threshold=80):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("La entrada debe ser un objeto pandas DataFrame.")
    
    if not dish or not isinstance(dish, str):
        raise ValueError("La consulta del plato debe ser un texto válido no vacío.")
   
    dish = dish.lower()
    filtered_rows = []
    
    for _, row in df.iterrows():
        menu = row.get("menu", {})
        if not isinstance(menu, dict) or not menu:
            continue 
        
        found = False
        for category, items in menu.items():
            if isinstance(items, dict):
                for item_name in items.keys():
                    if partial_ratio(dish, item_name.lower()) >= threshold:
                        found = True
                        break
            if found:
                break
        
        if found:
            filtered_rows.append(row)
    
    df_filtered = pd.DataFrame(filtered_rows)
    
    if df_filtered.empty:
        print(f"No se encontraron locales que ofrezcan platos relacionados con '{dish}'.")
    
    return df_filtered.reset_index(drop=True)
 
 
def search_by_dish_and_price(df, dish, dish_max_price, threshold=80):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("La entrada debe ser un DataFrame de pandas.")
    if not dish or not isinstance(dish, str):
        raise ValueError("La búsqueda del plato debe ser una cadena no vacía.")
    if not isinstance(dish_max_price, (int, float)) or dish_max_price < 0:
        raise ValueError("El precio máximo debe ser un número positivo.")

    dish = dish.lower()
    filtered_rows = []

    for _, row in df.iterrows():  
        menu = row.get("menu", {})
        if isinstance(menu, dict):  
            for category, items in menu.items():  
                if isinstance(items, dict): 
                    for menu_dish, price in items.items():
                        if isinstance(price, (int, float)) and price is not None:
                            if partial_ratio(dish, menu_dish.lower()) >= threshold and price <= dish_max_price:
                                filtered_rows.append(row) 
                                break  

    df_filtered = pd.DataFrame(filtered_rows)  
    if df_filtered.empty:
        print(f"No se encontraron restaurantes que ofrezcan '{dish}' por debajo de {dish_max_price:.2f}.")
    
    return df_filtered


def filter_by_average_price(df, average_price): 
    if not isinstance(df, pd.DataFrame):
        raise ValueError("La entrada debe ser un DataFrame de pandas.")
    if not isinstance(average_price, (int, float)) or average_price < 0:
        raise ValueError("El precio promedio debe ser un número positivo.")
   
    filtered_rows = []  
    for _, row in df.iterrows():  
        menu = row.get("menu", {})
        all_prices = []  

        if isinstance(menu, dict):  
            for category, items in menu.items():
                if isinstance(items, dict): 
                    for price in items.values(): 
                        if isinstance(price, (int, float)) and price is not None: 
                            all_prices.append(price)  
        if all_prices: 
            avg_price = sum(all_prices) / len(all_prices) 
            row['average_price'] = avg_price  
            
            if avg_price <= average_price:  
                filtered_rows.append(row)  
  
    df_filtered = pd.DataFrame(filtered_rows)
    if df_filtered.empty:
        print(f"No se encontraron restaurantes con un precio promedio menor o igual a {average_price:.2f}.")
    
   
    return df_filtered.reset_index(drop=True)


def generic_search(df, name=None, municipality=None, day=None, time=None, 
                   owner_type=None, specialty=None, establishment_type=None,
                   min_rating=None, services=None, payment_methods=None, 
                   dish=None, dish_max_price=None, average_price=None):
   
    if municipality:
        df = search_by_municipality(df, municipality)
    if name:
        df = search_by_name(df, name)
    if owner_type:
        df = search_by_owner(df, owner_type)
    if specialty:
        df = search_by_specialty(df, specialty)
    if establishment_type:
        df = search_by_type(df, establishment_type)
    if min_rating is not None:
        df = search_by_rating(df, min_rating)
    if day and time:
        df = search_by_open_locals(df, day, time)
    if services:
        df = search_by_services(df, services)
    if payment_methods:
        df = search_by_payment_methods(df, payment_methods)
    if dish:
        df = search_by_dish(df, dish)
    if (dish_max_price and dish) is not None:
        df = search_by_dish_and_price(df, dish, dish_max_price)
    if average_price is not None:
        df = filter_by_average_price(df,average_price)

    return df.reset_index(drop=True)