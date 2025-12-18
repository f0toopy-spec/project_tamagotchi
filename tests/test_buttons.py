"""
Тесты для модуля entities.buttons
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pygame
    pygame.init()
except:
    pass

from entities.buttons import Button, CloseButton, TabButton
from config import BLUE, RED, GRAY, WHITE, BLACK


class TestButton(unittest.TestCase):
    """Тесты для класса Button"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.button = Button(100, 100, 200, 50, "Тест", BLUE)
    
    def test_init(self):
        """Тест инициализации кнопки"""
        self.assertEqual(self.button.text, "Тест")
        self.assertEqual(self.button.color, BLUE)
        self.assertFalse(self.button.is_hovered)
        self.assertFalse(self.button.clicked)
        self.assertIsNotNone(self.button.rect)
        self.assertEqual(self.button.rect.x, 100)
        self.assertEqual(self.button.rect.y, 100)
        self.assertEqual(self.button.rect.width, 200)
        self.assertEqual(self.button.rect.height, 50)
    
    def test_check_hover_inside(self):
        """Тест проверки наведения курсора (внутри кнопки)"""
        result = self.button.check_hover((150, 125))
        
        self.assertTrue(result)
        self.assertTrue(self.button.is_hovered)
    
    def test_check_hover_outside(self):
        """Тест проверки наведения курсора (вне кнопки)"""
        result = self.button.check_hover((50, 50))
        
        self.assertFalse(result)
        self.assertFalse(self.button.is_hovered)
    
    def test_is_clicked_mouse_down(self):
        """Тест проверки клика (нажатие мыши)"""
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (150, 125)
        
        result = self.button.is_clicked(event)
        
        self.assertTrue(result)
        self.assertTrue(self.button.clicked)
    
    def test_is_clicked_mouse_up(self):
        """Тест проверки клика (отпускание мыши)"""
        self.button.clicked = True
        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        event.pos = (150, 125)
        
        result = self.button.is_clicked(event)
        
        self.assertFalse(result)
        self.assertFalse(self.button.clicked)
    
    def test_is_clicked_outside(self):
        """Тест проверки клика вне кнопки"""
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (50, 50)
        
        result = self.button.is_clicked(event)
        
        self.assertFalse(result)
        self.assertFalse(self.button.clicked)
    
    def test_handle_event_mouse_motion(self):
        """Тест обработки события движения мыши"""
        event = Mock()
        event.type = pygame.MOUSEMOTION
        event.pos = (150, 125)
        
        result = self.button.handle_event(event)
        
        self.assertFalse(result)
        self.assertTrue(self.button.is_hovered)
    
    def test_handle_event_click(self):
        """Тест обработки события клика"""
        # Нажатие
        event_down = Mock()
        event_down.type = pygame.MOUSEBUTTONDOWN
        event_down.button = 1
        event_down.pos = (150, 125)
        
        result_down = self.button.handle_event(event_down)
        self.assertTrue(result_down)
        self.assertTrue(self.button.clicked)
        
        # Отпускание
        event_up = Mock()
        event_up.type = pygame.MOUSEBUTTONUP
        event_up.button = 1
        event_up.pos = (150, 125)
        
        result_up = self.button.handle_event(event_up)
        self.assertTrue(result_up)
        self.assertFalse(self.button.clicked)
    
    @patch('pygame.font.Font')
    @patch('pygame.draw.rect')
    def test_draw(self, mock_rect, mock_font):
        """Тест отрисовки кнопки"""
        mock_screen = Mock()
        self.button.draw(mock_screen)
        
        # Проверяем, что были вызовы отрисовки
        self.assertGreater(mock_rect.call_count, 0)
    
    @patch('pygame.font.Font')
    @patch('pygame.draw.rect')
    def test_draw_hovered(self, mock_rect, mock_font):
        """Тест отрисовки кнопки при наведении"""
        mock_screen = Mock()
        self.button.is_hovered = True
        self.button.draw(mock_screen)
        
        # Проверяем, что были вызовы отрисовки
        self.assertGreater(mock_rect.call_count, 0)


class TestCloseButton(unittest.TestCase):
    """Тесты для класса CloseButton"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.button = CloseButton(100, 100)
    
    def test_init(self):
        """Тест инициализации кнопки закрытия"""
        self.assertEqual(self.button.text, "X")
        self.assertEqual(self.button.color, RED)
        self.assertEqual(self.button.rect.width, 40)
        self.assertEqual(self.button.rect.height, 40)
        self.assertEqual(self.button.rect.x, 100)
        self.assertEqual(self.button.rect.y, 100)


class TestTabButton(unittest.TestCase):
    """Тесты для класса TabButton"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.button = TabButton(100, 100, 150, 40, "Вкладка")
    
    def test_init(self):
        """Тест инициализации кнопки вкладки"""
        self.assertEqual(self.button.text, "Вкладка")
        self.assertEqual(self.button.color, GRAY)
        self.assertEqual(self.button.text_color, BLACK)
        self.assertEqual(self.button.rect.width, 150)
        self.assertEqual(self.button.rect.height, 40)


if __name__ == '__main__':
    unittest.main()

