"""
Тесты для модуля entities.items
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.items import FoodItem, Inventory


class TestFoodItem(unittest.TestCase):
    """Тесты для класса FoodItem"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        try:
            import pygame
            pygame.init()
        except:
            pass
        
        self.food = FoodItem(
            name="Яблоко",
            hunger_value=20,
            happiness_boost=10,
            energy_boost=5,
            price=10,
            color=(255, 0, 0)
        )
    
    def test_init(self):
        """Тест инициализации предмета еды"""
        self.assertEqual(self.food.name, "Яблоко")
        self.assertEqual(self.food.hunger_value, 20)
        self.assertEqual(self.food.happiness_boost, 10)
        self.assertEqual(self.food.energy_boost, 5)
        self.assertEqual(self.food.price, 10)
        self.assertEqual(self.food.color, (255, 0, 0))
        self.assertFalse(self.food.dragging)
        self.assertIsNone(self.food.original_pos)
        self.assertIsNone(self.food.current_pos)
        self.assertEqual(self.food.size, 30)
    
    def test_check_click_hit(self):
        """Тест проверки клика по предмету (попадание)"""
        self.food.current_pos = (100, 100)
        result = self.food.check_click((100, 100))
        self.assertTrue(result)
    
    def test_check_click_miss(self):
        """Тест проверки клика по предмету (промах)"""
        self.food.current_pos = (100, 100)
        result = self.food.check_click((200, 200))
        self.assertFalse(result)
    
    def test_check_click_no_position(self):
        """Тест проверки клика без установленной позиции"""
        self.food.current_pos = None
        result = self.food.check_click((100, 100))
        self.assertFalse(result)
    
    def test_start_drag(self):
        """Тест начала перетаскивания"""
        self.food.current_pos = (100, 100)
        self.food.start_drag((100, 100))
        
        self.assertTrue(self.food.dragging)
        self.assertEqual(self.food.original_pos, (100, 100))
    
    def test_update_drag(self):
        """Тест обновления позиции при перетаскивании"""
        self.food.current_pos = (100, 100)
        self.food.dragging = True
        self.food.update_drag((150, 150))
        
        self.assertEqual(self.food.current_pos, (150, 150))
    
    def test_update_drag_not_dragging(self):
        """Тест обновления позиции без перетаскивания"""
        self.food.current_pos = (100, 100)
        self.food.dragging = False
        self.food.update_drag((150, 150))
        
        self.assertEqual(self.food.current_pos, (100, 100))
    
    def test_stop_drag(self):
        """Тест завершения перетаскивания"""
        self.food.original_pos = (100, 100)
        self.food.dragging = True
        result = self.food.stop_drag()
        
        self.assertFalse(self.food.dragging)
        self.assertEqual(result, (100, 100))
    
    @patch('pygame.font.Font')
    @patch('pygame.draw.circle')
    def test_draw(self, mock_circle, mock_font):
        """Тест отрисовки предмета еды"""
        mock_screen = Mock()
        self.food.draw(mock_screen, 100, 100)
        
        self.assertEqual(self.food.current_pos, (100, 100))
        mock_circle.assert_called_once()


class TestInventory(unittest.TestCase):
    """Тесты для класса Inventory"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        try:
            import pygame
            pygame.init()
        except:
            pass
        
        self.inventory = Inventory()
        self.food1 = FoodItem("Яблоко", 20, 10, 5, 10, (255, 0, 0))
        self.food2 = FoodItem("Банан", 15, 8, 3, 8, (255, 255, 0))
    
    def test_init(self):
        """Тест инициализации инвентаря"""
        self.assertEqual(len(self.inventory.food_items), 0)
        self.assertEqual(self.inventory.max_items, 6)
    
    def test_add_food_success(self):
        """Тест успешного добавления еды в инвентарь"""
        result = self.inventory.add_food(self.food1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.inventory.food_items), 1)
        self.assertIn(self.food1, self.inventory.food_items)
    
    def test_add_food_full(self):
        """Тест добавления еды в полный инвентарь"""
        # Заполняем инвентарь
        for i in range(6):
            food = FoodItem(f"Еда{i}", 10, 5, 2, 5, (0, 0, 0))
            self.inventory.add_food(food)
        
        result = self.inventory.add_food(self.food1)
        
        self.assertFalse(result)
        self.assertEqual(len(self.inventory.food_items), 6)
        self.assertNotIn(self.food1, self.inventory.food_items)
    
    def test_remove_food_success(self):
        """Тест успешного удаления еды из инвентаря"""
        self.inventory.add_food(self.food1)
        result = self.inventory.remove_food(self.food1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.inventory.food_items), 0)
        self.assertNotIn(self.food1, self.inventory.food_items)
    
    def test_remove_food_not_found(self):
        """Тест удаления несуществующей еды"""
        result = self.inventory.remove_food(self.food1)
        
        self.assertFalse(result)
        self.assertEqual(len(self.inventory.food_items), 0)
    
    def test_add_multiple_foods(self):
        """Тест добавления нескольких предметов еды"""
        self.inventory.add_food(self.food1)
        self.inventory.add_food(self.food2)
        
        self.assertEqual(len(self.inventory.food_items), 2)
        self.assertIn(self.food1, self.inventory.food_items)
        self.assertIn(self.food2, self.inventory.food_items)
    
    @patch('pygame.font.Font')
    @patch('pygame.draw.rect')
    @patch('pygame.draw.circle')
    def test_draw(self, mock_circle, mock_rect, mock_font):
        """Тест отрисовки инвентаря"""
        self.inventory.add_food(self.food1)
        mock_screen = Mock()
        # Делаем mock_screen похожим на pygame.Surface
        mock_screen.blit = Mock()
        
        self.inventory.draw(mock_screen)
        
        # Проверяем, что были вызовы отрисовки
        self.assertGreater(mock_rect.call_count, 0)


if __name__ == '__main__':
    unittest.main()

