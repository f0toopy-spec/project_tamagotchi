"""
Тесты для модуля game.core
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pygame
    pygame.init()
except:
    pass

from database.models import Tamagotchi
from entities.tamagotchi import TamagotchiEntity


class TestGameCore(unittest.TestCase):
    """Тесты для класса GameCore"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_screen = Mock()
        self.mock_screen.get_width.return_value = 800
        self.mock_screen.get_height.return_value = 600
    
    @patch('game.core.DatabaseManager')
    @patch('game.core.ROOMS_AVAILABLE', False)
    def test_init(self, mock_db_manager):
        """Тест инициализации GameCore"""
        from game.core import GameCore
        
        mock_db = Mock()
        mock_db.get_all_tamagotchis.return_value = []
        mock_db.save_tamagotchi.return_value = True
        mock_db_manager.return_value = mock_db
        
        game = GameCore(self.mock_screen)
        
        self.assertEqual(game.screen, self.mock_screen)
        self.assertTrue(game.running)
        self.assertIsNotNone(game.clock)
        self.assertIsNotNone(game.inventory)
    
    @patch('game.core.DatabaseManager')
    @patch('game.core.ROOMS_AVAILABLE', False)
    def test_create_new_tamagotchi(self, mock_db_manager):
        """Тест создания нового тамагочи"""
        from game.core import GameCore
        
        mock_db = Mock()
        mock_db.get_all_tamagotchis.return_value = []
        mock_db.save_tamagotchi.return_value = True
        mock_db_manager.return_value = mock_db
        
        game = GameCore(self.mock_screen)
        result = game.create_new_tamagotchi("Новый Питомец")
        
        self.assertTrue(result)
        self.assertIsNotNone(game.current_tamagotchi)
        mock_db.save_tamagotchi.assert_called()
    
    @patch('game.core.DatabaseManager')
    @patch('game.core.ROOMS_AVAILABLE', False)
    def test_ensure_tamagotchi_exists_with_existing(self, mock_db_manager):
        """Тест загрузки существующего тамагочи"""
        from game.core import GameCore
        
        existing_tamagotchi = Tamagotchi(name="Существующий")
        mock_db = Mock()
        mock_db.get_all_tamagotchis.return_value = [existing_tamagotchi]
        mock_db_manager.return_value = mock_db
        
        game = GameCore(self.mock_screen)
        
        self.assertIsNotNone(game.current_tamagotchi)
        self.assertEqual(game.current_tamagotchi.data.name, "Существующий")
    
    @patch('game.core.DatabaseManager')
    @patch('game.core.ROOMS_AVAILABLE', False)
    def test_show_message(self, mock_db_manager):
        """Тест показа сообщения"""
        from game.core import GameCore
        
        mock_db = Mock()
        mock_db.get_all_tamagotchis.return_value = []
        mock_db.save_tamagotchi.return_value = True
        mock_db_manager.return_value = mock_db
        
        game = GameCore(self.mock_screen)
        game.show_message("Тестовое сообщение")
        
        self.assertEqual(game.message, "Тестовое сообщение")
        self.assertGreater(game.message_timer, 0)
    
    @patch('game.core.DatabaseManager')
    @patch('game.core.ROOMS_AVAILABLE', False)
    @patch('pygame.time.get_ticks')
    def test_auto_save(self, mock_ticks, mock_db_manager):
        """Тест автосохранения"""
        from game.core import GameCore
        
        mock_ticks.return_value = 0
        
        tamagotchi_data = Tamagotchi(name="Тест")
        mock_db = Mock()
        mock_db.get_all_tamagotchis.return_value = [tamagotchi_data]
        mock_db.save_tamagotchi.return_value = True
        mock_db_manager.return_value = mock_db
        
        game = GameCore(self.mock_screen)
        game.auto_save()
        
        mock_db.save_tamagotchi.assert_called()
    
    @patch('game.core.DatabaseManager')
    @patch('game.core.ROOMS_AVAILABLE', False)
    def test_exit_minigame(self, mock_db_manager):
        """Тест выхода из мини-игры"""
        from game.core import GameCore
        
        mock_db = Mock()
        mock_db.get_all_tamagotchis.return_value = []
        mock_db.save_tamagotchi.return_value = True
        mock_db_manager.return_value = mock_db
        
        game = GameCore(self.mock_screen)
        
        # Создаем мок мини-игры
        mock_minigame = Mock()
        mock_minigame.finish.return_value = (10, 5, 2, 1)  # coins, happiness, energy_cost, hunger_cost
        game.current_minigame = mock_minigame
        
        game.exit_minigame()
        
        self.assertIsNone(game.current_minigame)
        mock_minigame.finish.assert_called_once()


if __name__ == '__main__':
    unittest.main()

