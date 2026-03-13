CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wikipedia_id TEXT UNIQUE, 
    title TEXT,
    description TEXT,
    image TEXT,
    rarity TEXT,
    attack INTEGER,
    defense INTEGER,
    hp INTEGER,
    category TEXT,
    url TEXT
);

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_id TEXT UNIQUE,
    username TEXT
);

CREATE TABLE IF NOT EXISTS player_card (
    player_id INTEGER,
    card_id INTEGER,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY(player_id, card_id),
    FOREIGN KEY(player_id) REFERENCES players(id),
    FOREIGN KEY(card_id) REFERENCES cards(id)
);