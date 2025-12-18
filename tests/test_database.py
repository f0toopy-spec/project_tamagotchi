"""
Тесты для модулей базы данных (SQLiteManager и MemoryManager)
"""
import unittest
import os
import sys
import tempfile
import shutil

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Tamagotchi
from database.memory_manager import MemoryManager


class TestMemoryManager(unittest.TestCase):
    """Тесты для MemoryManager"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.manager = MemoryManager()
    
    def test_init(self):
        """Тест инициализации менеджера"""
        self.assertEqual(len(self.manager.tamagotchis), 0)
        self.assertEqual(self.manager.next_id, 1)
    
    def test_save_new_tamagotchi(self):
        """Тест сохранения нового тамагочи"""
        t = Tamagotchi(name="Новый")
        result = self.manager.save_tamagotchi(t)
        
        self.assertTrue(result)
        self.assertIsNotNone(t.id)
        self.assertEqual(t.id, 1)
        self.assertEqual(len(self.manager.tamagotchis), 1)
        self.assertEqual(self.manager.next_id, 2)
    
    def test_save_multiple_tamagotchis(self):
        """Тест сохранения нескольких тамагочи"""
        t1 = Tamagotchi(name="Первый")
        t2 = Tamagotchi(name="Второй")
        
        self.manager.save_tamagotchi(t1)
        self.manager.save_tamagotchi(t2)
        
        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)
        self.assertEqual(len(self.manager.tamagotchis), 2)
    
    def test_save_existing_tamagotchi(self):
        """Тест обновления существующего тамагочи"""
        t = Tamagotchi(name="Оригинал")
        self.manager.save_tamagotchi(t)
        original_id = t.id
        
        t.name = "Обновленный"
        t.hunger = 75
        result = self.manager.save_tamagotchi(t)
        
        self.assertTrue(result)
        self.assertEqual(t.id, original_id)
        self.assertEqual(len(self.manager.tamagotchis), 1)
        self.assertEqual(self.manager.tamagotchis[0].name, "Обновленный")
        self.assertEqual(self.manager.tamagotchis[0].hunger, 75)
    
    def test_load_tamagotchi(self):
        """Тест загрузки тамагочи по ID"""
        t = Tamagotchi(name="Для загрузки")
        self.manager.save_tamagotchi(t)
        saved_id = t.id
        
        loaded = self.manager.load_tamagotchi(saved_id)
        
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.id, saved_id)
        self.assertEqual(loaded.name, "Для загрузки")
    
    def test_load_nonexistent_tamagotchi(self):
        """Тест загрузки несуществующего тамагочи"""
        loaded = self.manager.load_tamagotchi(999)
        self.assertIsNone(loaded)
    
    def test_get_all_tamagotchis(self):
        """Тест получения всех тамагочи"""
        t1 = Tamagotchi(name="Первый")
        t2 = Tamagotchi(name="Второй")
        t3 = Tamagotchi(name="Третий")
        
        self.manager.save_tamagotchi(t1)
        self.manager.save_tamagotchi(t2)
        self.manager.save_tamagotchi(t3)
        
        all_tamagotchis = self.manager.get_all_tamagotchis()
        
        self.assertEqual(len(all_tamagotchis), 3)
        self.assertIsInstance(all_tamagotchis, list)
        # Проверяем, что это копия, а не ссылка
        all_tamagotchis.append(Tamagotchi(name="Четвертый"))
        self.assertEqual(len(self.manager.tamagotchis), 3)
    
    def test_delete_tamagotchi(self):
        """Тест удаления тамагочи"""
        t1 = Tamagotchi(name="Первый")
        t2 = Tamagotchi(name="Второй")
        
        self.manager.save_tamagotchi(t1)
        self.manager.save_tamagotchi(t2)
        
        result = self.manager.delete_tamagotchi(t1.id)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tamagotchis), 1)
        self.assertEqual(self.manager.tamagotchis[0].id, t2.id)
        self.assertIsNone(self.manager.load_tamagotchi(t1.id))
    
    def test_delete_nonexistent_tamagotchi(self):
        """Тест удаления несуществующего тамагочи"""
        result = self.manager.delete_tamagotchi(999)
        self.assertTrue(result)  # MemoryManager всегда возвращает True


class TestSQLiteManager(unittest.TestCase):
    """Тесты для SQLiteManager"""
    
    def setUp(self):
        """Настройка перед каждым тестом - используем временную БД"""
        # Создаем временную директорию для тестовой БД
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, 'test_tamagotchi.db')
        
        # Модифицируем путь к БД для тестов
        import database.sqlite_manager as sqlite_module
        test_db_path = self.test_db_path
        test_dir = self.test_dir
        
        def test_connect(manager_self):
            import sqlite3
            os.makedirs(test_dir, exist_ok=True)
            manager_self.connection = sqlite3.connect(
                test_db_path,
                check_same_thread=False
            )
            manager_self.connection.row_factory = sqlite3.Row
            manager_self._create_tables()
        
        # Временно заменяем метод connect
        sqlite_module.SQLiteManager.connect = test_connect
        
        from database.sqlite_manager import SQLiteManager
        self.manager = SQLiteManager()
        self.manager.test_db_path = self.test_db_path
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if hasattr(self.manager, 'connection') and self.manager.connection:
            self.manager.connection.close()
        # Удаляем временную директорию
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_save_new_tamagotchi(self):
        """Тест сохранения нового тамагочи в SQLite"""
        t = Tamagotchi(name="SQLite Тест")
        result = self.manager.save_tamagotchi(t)
        
        self.assertTrue(result)
        self.assertIsNotNone(t.id)
        self.assertGreater(t.id, 0)
    
    def test_load_tamagotchi(self):
        """Тест загрузки тамагочи из SQLite"""
        t = Tamagotchi(name="Для загрузки")
        t.hunger = 60
        t.happiness = 70
        self.manager.save_tamagotchi(t)
        saved_id = t.id
        
        loaded = self.manager.load_tamagotchi(saved_id)
        
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.id, saved_id)
        self.assertEqual(loaded.name, "Для загрузки")
        self.assertEqual(loaded.hunger, 60)
        self.assertEqual(loaded.happiness, 70)
    
    def test_update_tamagotchi(self):
        """Тест обновления существующего тамагочи"""
        t = Tamagotchi(name="Оригинал")
        t.hunger = 50
        self.manager.save_tamagotchi(t)
        original_id = t.id
        
        t.name = "Обновленный"
        t.hunger = 80
        result = self.manager.save_tamagotchi(t)
        
        self.assertTrue(result)
        
        loaded = self.manager.load_tamagotchi(original_id)
        self.assertEqual(loaded.name, "Обновленный")
        self.assertEqual(loaded.hunger, 80)
    
    def test_get_all_tamagotchis(self):
        """Тест получения всех тамагочи"""
        t1 = Tamagotchi(name="Первый")
        t2 = Tamagotchi(name="Второй")
        t3 = Tamagotchi(name="Третий")
        
        self.manager.save_tamagotchi(t1)
        self.manager.save_tamagotchi(t2)
        self.manager.save_tamagotchi(t3)
        
        all_tamagotchis = self.manager.get_all_tamagotchis()
        
        self.assertEqual(len(all_tamagotchis), 3)
        names = [t.name for t in all_tamagotchis]
        self.assertIn("Первый", names)
        self.assertIn("Второй", names)
        self.assertIn("Третий", names)
    
    def test_delete_tamagotchi(self):
        """Тест удаления тамагочи"""
        t = Tamagotchi(name="Для удаления")
        self.manager.save_tamagotchi(t)
        saved_id = t.id
        
        result = self.manager.delete_tamagotchi(saved_id)
        
        self.assertTrue(result)
        loaded = self.manager.load_tamagotchi(saved_id)
        self.assertIsNone(loaded)
    
    def test_load_nonexistent_tamagotchi(self):
        """Тест загрузки несуществующего тамагочи"""
        loaded = self.manager.load_tamagotchi(99999)
        self.assertIsNone(loaded)


if __name__ == '__main__':
    unittest.main()

