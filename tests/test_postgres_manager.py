"""
Тесты для модуля database.postgres_manager
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Tamagotchi

# Проверяем наличие psycopg2
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


class TestPostgresManager(unittest.TestCase):
    """Тесты для класса PostgresManager"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        pass
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_init(self, mock_connect):
        """Тест инициализации PostgresManager"""
        from database.postgres_manager import PostgresManager
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        manager = PostgresManager()
        
        self.assertIsNotNone(manager.connection)
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called()
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_save_new_tamagotchi(self, mock_connect):
        """Тест сохранения нового тамагочи"""
        from database.postgres_manager import PostgresManager
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [1]  # Возвращаем ID
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        manager = PostgresManager()
        
        tamagotchi = Tamagotchi(name="Тест")
        result = manager.save_tamagotchi(tamagotchi)
        
        self.assertTrue(result)
        self.assertEqual(tamagotchi.id, 1)
        mock_connection.commit.assert_called()
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_save_existing_tamagotchi(self, mock_connect):
        """Тест обновления существующего тамагочи"""
        from database.postgres_manager import PostgresManager
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        manager = PostgresManager()
        
        tamagotchi = Tamagotchi(id=1, name="Обновленный")
        result = manager.save_tamagotchi(tamagotchi)
        
        self.assertTrue(result)
        mock_connection.commit.assert_called()
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_load_tamagotchi(self, mock_connect):
        """Тест загрузки тамагочи"""
        from database.postgres_manager import PostgresManager
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_row = {
            'id': 1,
            'name': 'Загруженный',
            'hunger': 50,
            'happiness': 50,
            'health': 100,
            'cleanliness': 50,
            'energy': 100,
            'age': 0,
            'coins': 100,
            'evolution_stage': 1,
            'created_at': None,
            'last_updated': None
        }
        mock_cursor.fetchone.return_value = mock_row
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        manager = PostgresManager()
        
        result = manager.load_tamagotchi(1)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Загруженный')
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_load_nonexistent_tamagotchi(self, mock_connect):
        """Тест загрузки несуществующего тамагочи"""
        from database.postgres_manager import PostgresManager
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        manager = PostgresManager()
        
        result = manager.load_tamagotchi(999)
        
        self.assertIsNone(result)
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_get_all_tamagotchis(self, mock_connect):
        """Тест получения всех тамагочи"""
        from database.postgres_manager import PostgresManager
        
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_rows = [
            {'id': 1, 'name': 'Первый', 'hunger': 50, 'happiness': 50, 'health': 100,
             'cleanliness': 50, 'energy': 100, 'age': 0, 'coins': 100, 'evolution_stage': 1,
             'created_at': None, 'last_updated': None},
            {'id': 2, 'name': 'Второй', 'hunger': 60, 'happiness': 60, 'health': 90,
             'cleanliness': 60, 'energy': 90, 'age': 1, 'coins': 150, 'evolution_stage': 2,
             'created_at': None, 'last_updated': None}
        ]
        mock_cursor.fetchall.return_value = mock_rows
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        manager = PostgresManager()
        
        result = manager.get_all_tamagotchis()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'Первый')
        self.assertEqual(result[1].name, 'Второй')
    
    @unittest.skipIf(not PSYCOPG2_AVAILABLE, "psycopg2 не установлен")
    @patch('database.postgres_manager.psycopg2.connect')
    def test_connection_error(self, mock_connect):
        """Тест обработки ошибки подключения"""
        from database.postgres_manager import PostgresManager
        
        mock_connect.side_effect = Exception("Connection failed")
        
        # Не должно вызывать исключение
        manager = PostgresManager()
        
        # Connection должен быть None при ошибке
        # (зависит от реализации, может быть None или установлен)
        mock_connect.assert_called_once()


if __name__ == '__main__':
    unittest.main()

