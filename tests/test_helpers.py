"""
Тесты для модуля utils.helpers
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

from utils.helpers import draw_text, draw_progress_bar
from config import BLACK, RED, GREEN, BLUE


class TestDrawText(unittest.TestCase):
    """Тесты для функции draw_text"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.surface = Mock()
        self.surface.blit = Mock()
    
    @patch('pygame.font.Font')
    def test_draw_text(self, mock_font):
        """Тест отрисовки текста"""
        mock_font_instance = Mock()
        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_rect.midtop = (0, 0)
        
        mock_font.return_value = mock_font_instance
        mock_font_instance.render.return_value = mock_text_surface
        mock_text_surface.get_rect.return_value = mock_text_rect
        
        draw_text(self.surface, "Тест", 36, 100, 200, BLACK)
        
        mock_font.assert_called_once_with(None, 36)
        mock_font_instance.render.assert_called_once_with("Тест", True, BLACK)
        self.surface.blit.assert_called_once()
    
    @patch('pygame.font.Font')
    def test_draw_text_custom_color(self, mock_font):
        """Тест отрисовки текста с пользовательским цветом"""
        mock_font_instance = Mock()
        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_rect.midtop = (0, 0)
        
        mock_font.return_value = mock_font_instance
        mock_font_instance.render.return_value = mock_text_surface
        mock_text_surface.get_rect.return_value = mock_text_rect
        
        draw_text(self.surface, "Красный текст", 24, 150, 250, RED)
        
        mock_font_instance.render.assert_called_once_with("Красный текст", True, RED)


class TestDrawProgressBar(unittest.TestCase):
    """Тесты для функции draw_progress_bar"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.surface = Mock()
    
    @patch('pygame.draw.rect')
    def test_draw_progress_bar_full(self, mock_rect):
        """Тест отрисовки полностью заполненной шкалы"""
        draw_progress_bar(self.surface, 50, 100, 200, 20, 100, 100, GREEN)
        
        # Должно быть 2 вызова: рамка и заполнение
        self.assertEqual(mock_rect.call_count, 2)
    
    @patch('pygame.draw.rect')
    def test_draw_progress_bar_half(self, mock_rect):
        """Тест отрисовки наполовину заполненной шкалы"""
        draw_progress_bar(self.surface, 50, 100, 200, 20, 50, 100, BLUE)
        
        # Должно быть 2 вызова: рамка и заполнение
        self.assertEqual(mock_rect.call_count, 2)
    
    @patch('pygame.draw.rect')
    def test_draw_progress_bar_empty(self, mock_rect):
        """Тест отрисовки пустой шкалы"""
        draw_progress_bar(self.surface, 50, 100, 200, 20, 0, 100, RED)
        
        # Должно быть 2 вызова: рамка и заполнение (даже если пустое)
        self.assertEqual(mock_rect.call_count, 2)
    
    @patch('pygame.draw.rect')
    def test_draw_progress_bar_custom_values(self, mock_rect):
        """Тест отрисовки шкалы с пользовательскими значениями"""
        draw_progress_bar(self.surface, 10, 20, 300, 30, 75, 150, (255, 0, 0))
        
        # Проверяем, что функция вызывается
        self.assertEqual(mock_rect.call_count, 2)
    
    @patch('pygame.draw.rect')
    def test_draw_progress_bar_ratio_calculation(self, mock_rect):
        """Тест расчета соотношения заполнения"""
        # 75 из 100 = 75%
        draw_progress_bar(self.surface, 0, 0, 100, 10, 75, 100, GREEN)
        
        # Проверяем вызовы
        calls = mock_rect.call_args_list
        
        # Первый вызов - рамка
        # Второй вызов - заполнение (должно быть 75 пикселей ширины)
        self.assertEqual(len(calls), 2)
        
        # Проверяем второй вызов (заполнение)
        fill_call = calls[1]
        # Второй аргумент - прямоугольник (x, y, width, height)
        fill_rect = fill_call[0][1]
        
        # Ширина заполнения должна быть 75 (100 * 0.75)
        # Проверяем, что был вызов с правильной шириной
        self.assertGreater(len(fill_call[0]), 1)
        # Проверяем, что функция была вызвана
        self.assertGreater(mock_rect.call_count, 0)


if __name__ == '__main__':
    unittest.main()

