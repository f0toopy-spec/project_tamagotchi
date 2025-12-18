"""
Тесты для модуля utils.animation
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

from utils.animation import Animation, SpriteSheet


class TestAnimation(unittest.TestCase):
    """Тесты для класса Animation"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем моки кадров
        self.frame1 = Mock()
        self.frame2 = Mock()
        self.frame3 = Mock()
        self.frames = [self.frame1, self.frame2, self.frame3]
        self.animation = Animation(self.frames, frame_duration=100)
    
    def test_init(self):
        """Тест инициализации анимации"""
        self.assertEqual(len(self.animation.frames), 3)
        self.assertEqual(self.animation.frame_duration, 100)
        self.assertEqual(self.animation.current_frame, 0)
        self.assertIsNotNone(self.animation.last_update)
    
    def test_get_current_frame(self):
        """Тест получения текущего кадра"""
        frame = self.animation.get_current_frame()
        self.assertEqual(frame, self.frame1)
    
    @patch('pygame.time.get_ticks')
    def test_update_no_change(self, mock_ticks):
        """Тест обновления без смены кадра (не прошло достаточно времени)"""
        mock_ticks.return_value = 50  # Прошло только 50 мс
        self.animation.last_update = 0
        
        self.animation.update()
        
        self.assertEqual(self.animation.current_frame, 0)
    
    @patch('pygame.time.get_ticks')
    def test_update_frame_change(self, mock_ticks):
        """Тест обновления со сменой кадра"""
        mock_ticks.return_value = 150  # Прошло 150 мс
        self.animation.last_update = 0
        
        self.animation.update()
        
        self.assertEqual(self.animation.current_frame, 1)
    
    @patch('pygame.time.get_ticks')
    def test_update_loop(self, mock_ticks):
        """Тест зацикливания анимации"""
        self.animation.current_frame = 2  # Последний кадр
        mock_ticks.return_value = 150
        self.animation.last_update = 0
        
        self.animation.update()
        
        # Должен вернуться к первому кадру
        self.assertEqual(self.animation.current_frame, 0)
    
    @patch('pygame.time.get_ticks')
    def test_update_multiple_frames(self, mock_ticks):
        """Тест обновления нескольких кадров"""
        # Устанавливаем начальное время
        self.animation.last_update = 0
        
        # Используем side_effect для последовательных значений времени
        # После первого update() last_update станет 101, поэтому для второго нужно > 201
        # После второго update() last_update станет 202, поэтому для третьего нужно > 302
        mock_ticks.side_effect = [101, 202, 303]
        
        # Первое обновление - прошло 101 мс (больше 100)
        self.animation.update()
        self.assertEqual(self.animation.current_frame, 1)
        self.assertEqual(self.animation.last_update, 101)
        
        # Второе обновление - разница 202-101=101 мс (больше 100)
        self.animation.update()
        self.assertEqual(self.animation.current_frame, 2)
        self.assertEqual(self.animation.last_update, 202)
        
        # Третье обновление - разница 303-202=101 мс (больше 100, зацикливание)
        self.animation.update()
        self.assertEqual(self.animation.current_frame, 0)
        self.assertEqual(self.animation.last_update, 303)


class TestSpriteSheet(unittest.TestCase):
    """Тесты для класса SpriteSheet"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем мок изображения
        self.mock_image = Mock()
        self.mock_image.get_rect.return_value = Mock(width=300, height=200)
        self.mock_image.subsurface = Mock(side_effect=lambda rect: Mock())
    
    def test_init(self):
        """Тест инициализации спрайт-листа"""
        spritesheet = SpriteSheet(self.mock_image, 100, 100)
        
        self.assertEqual(spritesheet.frame_width, 100)
        self.assertEqual(spritesheet.frame_height, 100)
        self.assertEqual(spritesheet.sheet, self.mock_image)
    
    def test_load_frames(self):
        """Тест загрузки кадров из спрайт-листа"""
        # Изображение 300x200, кадры 100x100
        # Должно быть 3 кадра по ширине и 2 по высоте = 6 кадров
        spritesheet = SpriteSheet(self.mock_image, 100, 100)
        
        frames = spritesheet.load_frames()
        
        # Проверяем, что было создано правильное количество кадров
        self.assertGreater(len(frames), 0)
        self.assertEqual(len(spritesheet.frames), len(frames))
    
    def test_load_frames_custom_size(self):
        """Тест загрузки кадров с пользовательскими размерами"""
        # Изображение 300x200, кадры 50x50
        # Должно быть 6 кадров по ширине и 4 по высоте = 24 кадра
        spritesheet = SpriteSheet(self.mock_image, 50, 50)
        
        frames = spritesheet.load_frames()
        
        # Проверяем, что были вызовы subsurface
        self.assertGreater(self.mock_image.subsurface.call_count, 0)
    
    def test_frames_property(self):
        """Тест свойства frames"""
        spritesheet = SpriteSheet(self.mock_image, 100, 100)
        
        self.assertIsInstance(spritesheet.frames, list)
        # Проверяем, что frames содержит элементы
        self.assertGreater(len(spritesheet.frames), 0)
        # Проверяем, что load_frames возвращает список
        loaded_frames = spritesheet.load_frames()
        self.assertIsInstance(loaded_frames, list)
        self.assertEqual(len(spritesheet.frames), len(loaded_frames))


if __name__ == '__main__':
    unittest.main()

