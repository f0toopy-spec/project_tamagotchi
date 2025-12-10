-- Initial database setup
CREATE TABLE IF NOT EXISTS tamagotchis (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    hunger INTEGER DEFAULT 50,
    happiness INTEGER DEFAULT 50,
    health INTEGER DEFAULT 100,
    cleanliness INTEGER DEFAULT 50,
    energy INTEGER DEFAULT 100,
    age INTEGER DEFAULT 0,
    coins INTEGER DEFAULT 100,
    evolution_stage INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items table for shop
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    price INTEGER NOT NULL,
    effect_value INTEGER NOT NULL
);

-- Insert default items
INSERT INTO items (name, type, price, effect_value) VALUES
('Apple', 'food', 10, 15),
('Pizza', 'food', 30, 40),
('Ball', 'toy', 20, 20),
('Medicine', 'health', 50, 50),
('Soap', 'clean', 15, 100)
ON CONFLICT DO NOTHING;