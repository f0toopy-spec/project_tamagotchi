import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from .models import Tamagotchi


class PostgresManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self._create_tables()
        except Exception as e:
            print(f"Database connection error: {e}")

    def _create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
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
            )
        ''')
        self.connection.commit()
        cursor.close()

    def save_tamagotchi(self, tamagotchi):
        try:
            cursor = self.connection.cursor()
            if tamagotchi.id is None:
                cursor.execute('''
                    INSERT INTO tamagotchis 
                    (name, hunger, happiness, health, cleanliness, energy, age, coins, evolution_stage, last_updated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    RETURNING id
                ''', (tamagotchi.name, tamagotchi.hunger, tamagotchi.happiness,
                      tamagotchi.health, tamagotchi.cleanliness, tamagotchi.energy,
                      tamagotchi.age, tamagotchi.coins, tamagotchi.evolution_stage))
                tamagotchi.id = cursor.fetchone()[0]
            else:
                cursor.execute('''
                    UPDATE tamagotchis 
                    SET name=%s, hunger=%s, happiness=%s, health=%s, cleanliness=%s,
                        energy=%s, age=%s, coins=%s, evolution_stage=%s, last_updated=CURRENT_TIMESTAMP
                    WHERE id=%s
                ''', (tamagotchi.name, tamagotchi.hunger, tamagotchi.happiness,
                      tamagotchi.health, tamagotchi.cleanliness, tamagotchi.energy,
                      tamagotchi.age, tamagotchi.coins, tamagotchi.evolution_stage, tamagotchi.id))

            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error saving tamagotchi: {e}")
            return False

    def load_tamagotchi(self, tamagotchi_id):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM tamagotchis WHERE id = %s', (tamagotchi_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return Tamagotchi.from_dict(result)
            return None
        except Exception as e:
            print(f"Error loading tamagotchi: {e}")
            return None

    def get_all_tamagotchis(self):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM tamagotchis ORDER BY created_at DESC')
            results = cursor.fetchall()
            cursor.close()

            return [Tamagotchi.from_dict(row) for row in results]
        except Exception as e:
            print(f"Error loading tamagotchis: {e}")
            return []