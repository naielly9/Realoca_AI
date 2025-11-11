import googlemaps
from geopy.geocoders import Nominatim
import time
import logging
import streamlit as st
geolocator = Nominatim(user_agent="geoapi")
api_key = st.secrets["google"]["api_key"]
gmaps = googlemaps.Client(key=api_key)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from database import Database
db = Database()

logging.basicConfig(level=logging.INFO)

def get_coordinates_from_db(cep):
    with db.conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT latitude, longitude FROM enderecos WHERE cep = ?", (cep,))
        return cur.fetchone()

def save_coordinates_to_db(cep, lat, lon):
    with db.conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE enderecos
            SET latitude = ?, longitude = ?
            WHERE cep = ?
        """, (lat, lon, cep))
        conn.commit()


def get_coordinates(cep):
    cep = cep.strip().replace("-", "")
    if len(cep) != 8:
        logging.warning(f"CEP inválido: {cep}")
        return (None, None)

    cached = get_coordinates_from_db(cep)
    if cached and cached[0] and cached[1]:
        return cached

    try:
        loc = geolocator.geocode(cep, timeout=10)
        if loc:
            save_coordinates_to_db(cep, loc.latitude, loc.longitude)
            return (loc.latitude, loc.longitude)
    except Exception as e:
        logging.warning(f"Erro Nominatim: {e}")
    time.sleep(1) 

    try:
        result = gmaps.geocode(cep)
        print(result)
        if result:
            lat = result[0]['geometry']['location']['lat']
            lon = result[0]['geometry']['location']['lng']
            save_coordinates_to_db(cep, lat, lon)
            logging.info(f"📍 Google Maps → CEP {cep} atualizado → ({lat}, {lon})")
            return (lat, lon)
        else:
            logging.warning(f"🚫 Google Maps não encontrou coordenadas para {cep}")
    except Exception as e:
        logging.warning(f"Erro Google Maps: {e}")

    return (None, None)

""" if __name__ == "__main__":
    with db.conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT cep FROM enderecos WHERE latitude IS NULL OR longitude IS NULL")
        ceps_pendentes = [row[0] for row in cur.fetchall()]

    if not ceps_pendentes:
        logging.info("✅ Todos os CEPs já possuem coordenadas.")
    else:
        logging.info(f"🔍 {len(ceps_pendentes)} CEPs pendentes encontrados.")
        for cep in ceps_pendentes:
            coords = get_coordinates(cep)
            logging.info(f"CEP {cep} atualizado → {coords}") """