import sqlite3
import json
from pathlib import Path

# Obtener la ruta absoluta del directorio donde está tcg_api.py
BASE_DIR = Path(__file__).parent

# Abrir el SQL relativo a tcg_api.py
sql_path = BASE_DIR / "create_db.sql"

conn = sqlite3.connect(BASE_DIR / "tcg.db")
c = conn.cursor()
c.executescript(sql_path.read_text())
conn.commit()

def get_card(wikipedia_id):
    print(c)
    c.execute("SELECT * FROM cards WHERE wikipedia_id=?", (wikipedia_id,))
    card = c.fetchone()
    print(f"Existe?: {card}")
    if card:
        return card
    return None
    
def insert_card(wikipedia_id, title, description, image, rarity, attack, defense, hp, category, url):
    print("insertando carta")
    c.execute(
        "INSERT OR IGNORE INTO cards (wikipedia_id, title, description, image, rarity, attack, defense, hp, category, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (wikipedia_id, title, description, image, rarity, attack, defense, hp, category, url)
    )
    conn.commit()
    print("carta insertada")


# Obtener o crear jugador
def obtener_o_crear_jugador(discord_id, nombre):
    c.execute("SELECT * FROM jugadores WHERE discord_id=?", (discord_id,))
    jugador = c.fetchone()
    if jugador:
        return jugador
    c.execute(
        "INSERT INTO jugadores (discord_id, nombre) VALUES (?, ?)",
        (discord_id, nombre)
    )
    conn.commit()
    c.execute("SELECT * FROM jugadores WHERE discord_id=?", (discord_id,))
    return c.fetchone()


# Asignar card a jugador
def asignar_card_a_jugador(discord_id, nombre, card):
    jugador = obtener_o_crear_jugador(discord_id, nombre)
    card_id = card[0]  # id de la card en la DB
    jugador_id = jugador[0]

    # Ver si ya tiene la card
    c.execute(
        "SELECT cantidad FROM jugador_cards WHERE jugador_id=? AND card_id=?",
        (jugador_id, card_id)
    )
    row = c.fetchone()
    if row:
        # Si ya tiene la card, aumentamos la cantidad
        c.execute(
            "UPDATE jugador_cards SET cantidad=cantidad+1 WHERE jugador_id=? AND card_id=?",
            (jugador_id, card_id)
        )
    else:
        # Si no la tiene, insertamos
        c.execute(
            "INSERT INTO jugador_cards (jugador_id, card_id) VALUES (?, ?)",
            (jugador_id, card_id)
        )
    conn.commit()