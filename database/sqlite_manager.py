import sqlite3
import os
from datetime import datetime
from .models import Tamagotchi


class SQLiteManager:
    """Менеджер для работы с SQLite базой данных Tamagotchi.
    
    Отвечает за подключение к базе данных, создание таблиц и выполнение
    CRUD операций над объектами Tamagotchi.
    """
    
    def __init__(self):
        """Инициализирует менеджер и устанавливает соединение с базой данных."""
        self.connection = None
        self.connect()

    def connect(self):
        """Устанавливает соединение с SQLite базой данных.
        
        Создает директорию для базы данных если она не существует,
        подключается к файлу базы данных и создает необходимые таблицы.
        
        Raises:
            Exception: Если не удается установить соединение с базой данных.
        """
        try:
            # Создаем директорию для базы данных если она не существует
            os.makedirs('database', exist_ok=True)
            self.connection = sqlite3.connect(
                'database/tamagotchi.db', 
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            print("✅ SQLite database connected successfully!")
        except Exception as e:
            print(f"❌ SQLite connection error: {e}")

    def _create_tables(self):
        """Создает таблицы в базе данных если они не существуют.
        
        Создает основную таблицу 'tamagotchis' со всеми необходимыми полями
        для хранения состояния тамагочи.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tamagotchis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
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
        """Сохраняет объект Tamagotchi в базу данных.
        
        Если у тамагочи нет ID, создает новую запись. Если ID существует,
        обновляет существующую запись.
        
        Args:
            tamagotchi: Объект Tamagotchi для сохранения.
            
        Returns:
            bool: True если сохранение прошло успешно, False в случае ошибки.
        """
        try:
            cursor = self.connection.cursor()
            if tamagotchi.id is None:
                # Создаем новую запись
                cursor.execute('''
                    INSERT INTO tamagotchis 
                    (name, hunger, happiness, health, cleanliness, energy, age, coins, evolution_stage)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (tamagotchi.name, tamagotchi.hunger, tamagotchi.happiness,
                      tamagotchi.health, tamagotchi.cleanliness, tamagotchi.energy,
                      tamagotchi.age, tamagotchi.coins, tamagotchi.evolution_stage))
                tamagotchi.id = cursor.lastrowid
                print(f"✅ New tamagotchi created! ID: {tamagotchi.id}")
            else:
                # Обновляем существующую запись
                cursor.execute('''
                    UPDATE tamagotchis 
                    SET name=?, hunger=?, happiness=?, health=?, cleanliness=?,
                        energy=?, age=?, coins=?, evolution_stage=?, last_updated=CURRENT_TIMESTAMP
                    WHERE id=?
                ''', (tamagotchi.name, tamagotchi.hunger, tamagotchi.happiness,
                      tamagotchi.health, tamagotchi.cleanliness, tamagotchi.energy,
                      tamagotchi.age, tamagotchi.coins, tamagotchi.evolution_stage, tamagotchi.id))
                print(f"✅ Tamagotchi updated! ID: {tamagotchi.id}")

            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"❌ Error saving tamagotchi: {e}")
            return False

    def load_tamagotchi(self, tamagotchi_id):
        """Загружает тамагочи из базы данных по ID.
        
        Args:
            tamagotchi_id: Идентификатор тамагочи для загрузки.
            
        Returns:
            Tamagotchi or None: Объект Tamagotchi если найден, None если не найден
                                 или произошла ошибка.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM tamagotchis WHERE id = ?', (tamagotchi_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                print(f"✅ Loaded tamagotchi ID: {tamagotchi_id}")
                return Tamagotchi.from_dict(dict(result))
            print(f"❌ No tamagotchi found with ID: {tamagotchi_id}")
            return None
        except Exception as e:
            print(f"❌ Error loading tamagotchi: {e}")
            return None

    def get_all_tamagotchis(self):
        """Получает все тамагочи из базы данных.
        
        Returns:
            list: Список объектов Tamagotchi, отсортированных по дате создания
                  (от новых к старым). Возвращает пустой список в случае ошибки.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM tamagotchis ORDER BY created_at DESC')
            results = cursor.fetchall()
            cursor.close()

            tamagotchis = [Tamagotchi.from_dict(dict(row)) for row in results]
            print(f"✅ Loaded {len(tamagotchis)} tamagotchi(s)")
            return tamagotchis
        except Exception as e:
            print(f"❌ Error loading tamagotchis: {e}")
            return []

    def delete_tamagotchi(self, tamagotchi_id):
        """Удаляет тамагочи из базы данных по ID.
        
        Args:
            tamagotchi_id: Идентификатор тамагочи для удаления.
            
        Returns:
            bool: True если удаление прошло успешно, False в случае ошибки.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM tamagotchis WHERE id = ?', (tamagotchi_id,))
            self.connection.commit()
            cursor.close()
            print(f"✅ Deleted tamagotchi ID: {tamagotchi_id}")
            return True
        except Exception as e:
            print(f"❌ Error deleting tamagotchi: {e}")
            return False