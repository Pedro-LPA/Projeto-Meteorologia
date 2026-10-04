# %%

import requests
import json
import pandas as pd
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv() #carrega as variaveis de ambiente

api_key = os.getenv("API_KEY") # Pega api key


lat = -12.9714 #Setagem geográfica de salvador
lon = -38.5014

def extract_data(url:str): # Função de extração


    response = requests.get(url)
    return response.json()


def transform_data(data:dict): #Função de transformação, normalização e conversão de tipos


      df2 = pd.json_normalize(data)
      df_limpo = df2.drop(columns="weather")

      rename_map = {
      # Identificação e Localização
      "id": "cidade_id",
      "name": "cidade_nome",
      "coord.lat": "latitude",
      "coord.lon": "longitude",
      "sys.country": "pais",
      "timezone": "fuso_horario",
      "base": "estacao_base",
      "cod": "codigo_status",
      # Métricas Principais (main)
      "main.temp": "temperatura",
      "main.feels_like": "sensacao_termica",
      "main.temp_min": "temperatura_minima",
      "main.temp_max": "temperatura_maxima",
      "main.pressure": "pressao_atmosferica",
      "main.humidity": "umidade",
      "main.sea_level": "pressao_nivel_mar",
      "main.grnd_level": "pressao_nivel_solo",
      # Vento (wind)
      "wind.speed": "vento_velocidade",
      "wind.deg": "vento_direcao_graus",
      "wind.gust": "vento_rajada",
      # Condições Gerais
      "visibility": "visibilidade",
      "clouds.all": "nebulosidade_pct",
      # Dados de Sistema (sys) e Tempo
      "sys.type": "sistema_tipo",
      "sys.id": "sistema_id",
      "sys.sunrise": "nascer_do_sol",
      "sys.sunset": "por_do_sol",
      "dt": "data_hora_medicao",
}

      df = df_limpo.rename(columns=rename_map)

      return df


def load_data(df_param):


      engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/clima_db")

      df_param.to_sql(

            name="dados_clima",
            con=engine,
            if_exists="append",
            index=False,

            )

if __name__ == "__main__": # Função Principal
   response_json = extract_data(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br")
   dados_transformados = transform_data(response_json)
   load_data(dados_transformados)

# %%

