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
    c.execute("SELECT * FROM cards WHERE wikipedia_id=?", (wikipedia_id,))
    row = c.fetchone()
    if row:
        keys = ["id", "wikipedia_id", "title", "description", "image",
                "rarity", "attack", "defense", "hp", "category", "url"]
        return dict(zip(keys, row))
    return None
    
def insert_card(wikipedia_id, title, description, image, rarity, attack, defense, hp, category, url):
    print("insertando carta")
    c.execute(
        "INSERT OR IGNORE INTO cards (wikipedia_id, title, description, image, rarity, attack, defense, hp, category, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (wikipedia_id, title, description, image, rarity, attack, defense, hp, category, url)
    )
    conn.commit()
    print("carta insertada")

def get_player(discord_id):
    c.execute("SELECT * FROM players WHERE discord_id=?", (discord_id,))
    row = c.fetchone()
    if row:
        return {"id": row[0], "discord_id": row[1], "username": row[2]}
    return None

def insert_player(discord_id, username):
    c.execute(
        "INSERT OR IGNORE INTO players (discord_id, username) VALUES (?, ?)",
        (discord_id, username)
    )
    conn.commit()

def assign_card_to_player(player_id, card_id):
    c.execute(
        "SELECT quantity FROM player_card WHERE player_id=? AND card_id=?",
        (player_id, card_id)
    )
    row = c.fetchone()
    if row:
        c.execute(
            "UPDATE player_card SET quantity=quantity+1 WHERE player_id=? AND card_id=?",
            (player_id, card_id)
        )
    else:
        c.execute(
            "INSERT INTO player_card (player_id, card_id) VALUES (?, ?)",
            (player_id, card_id)
        )
    conn.commit()
    
def get_player_cards(player_id: int) -> list[dict]:
    c.execute("""
        SELECT c.*, pc.quantity 
        FROM cards c
        JOIN player_card pc ON c.id = pc.card_id
        WHERE pc.player_id = ?
    """, (player_id,))
    rows = c.fetchall()
    keys = ["id", "wikipedia_id", "title", "description", "image",
            "rarity", "attack", "defense", "hp", "category", "url", "quantity"]
    return [dict(zip(keys, row)) for row in rows]