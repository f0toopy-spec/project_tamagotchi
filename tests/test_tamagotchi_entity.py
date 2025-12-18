"""
Тесты для модуля entities.tamagotchi
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Tamagotchi
from entities.tamagotchi import TamagotchiEntity


class TestTamagotchiEntity(unittest.TestCase):
    """Тесты для класса TamagotchiEntity"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Инициализируем pygame для тестов
        try:
            import pygame
            pygame.init()
        except:
            pass
        
        self.tamagotchi_data = Tamagotchi(name="Тестовый")
        self.entity = TamagotchiEntity(self.tamagotchi_data)
    
    def test_init(self):
        """Тест инициализации TamagotchiEntity"""
        self.assertEqual(self.entity.data, self.tamagotchi_data)
        self.assertIsNotNone(self.entity.last_update_time)
        self.assertEqual(len(self.entity.evolution_thresholds), 3)
        self.assertEqual(len(self.entity.evolution_colors), 3)
        self.assertFalse(self.entity.is_sleeping)
        self.assertEqual(self.entity.sleep_start_time, 0)
    
    def test_check_evolution_stage_1_to_2(self):
        """Тест эволюции со стадии 1 на стадию 2"""
        self.entity.data.age = 7
        self.entity.data.evolution_stage = 1
        result = self.entity.check_evolution()
        self.assertTrue(result)
        self.assertEqual(self.entity.data.evolution_stage, 2)
    
    def test_check_evolution_stage_2_to_3(self):
        """Тест эволюции со стадии 2 на стадию 3"""
        self.entity.data.age = 14
        self.entity.data.evolution_stage = 2
        result = self.entity.check_evolution()
        self.assertTrue(result)
        self.assertEqual(self.entity.data.evolution_stage, 3)
    
    def test_check_evolution_no_evolution(self):
        """Тест отсутствия эволюции при недостаточном возрасте"""
        self.entity.data.age = 5
        self.entity.data.evolution_stage = 1
        result = self.entity.check_evolution()
        self.assertFalse(result)
        self.assertEqual(self.entity.data.evolution_stage, 1)
    
    def test_feed_success(self):
        """Тест успешного кормления"""
        self.entity.data.hunger = 50
        result = self.entity.feed(20)
        self.assertTrue(result)
        self.assertEqual(self.entity.data.hunger, 70)
    
    def test_feed_max_hunger(self):
        """Тест кормления при максимальном голоде"""
        self.entity.data.hunger = 100
        result = self.entity.feed(20)
        self.assertFalse(result)
        self.assertEqual(self.entity.data.hunger, 100)
    
    def test_feed_hungry_bonus(self):
        """Тест бонуса счастья при кормлении голодного тамагочи"""
        self.entity.data.hunger = 30
        self.entity.data.happiness = 50
        self.entity.feed(20)
        self.assertGreater(self.entity.data.happiness, 50)
    
    def test_play_success(self):
        """Тест успешной игры"""
        self.entity.data.happiness = 50
        self.entity.data.energy = 50
        result = self.entity.play()
        self.assertTrue(result)
        self.assertGreater(self.entity.data.happiness, 50)
        self.assertLess(self.entity.data.energy, 50)
    
    def test_play_insufficient_energy(self):
        """Тест игры при недостаточной энергии"""
        self.entity.data.happiness = 50
        self.entity.data.energy = 5
        result = self.entity.play(energy_cost=10)
        self.assertFalse(result)
    
    def test_play_max_happiness(self):
        """Тест игры при максимальном счастье"""
        self.entity.data.happiness = 100
        self.entity.data.energy = 50
        result = self.entity.play()
        self.assertFalse(result)
    
    def test_clean_success(self):
        """Тест успешной чистки"""
        self.entity.data.cleanliness = 50
        result = self.entity.clean()
        self.assertTrue(result)
        self.assertEqual(self.entity.data.cleanliness, 100)
    
    def test_clean_already_clean(self):
        """Тест чистки уже чистого тамагочи"""
        self.entity.data.cleanliness = 100
        result = self.entity.clean()
        self.assertFalse(result)
    
    def test_sleep_success(self):
        """Тест успешного засыпания"""
        self.entity.data.energy = 50
        self.entity.is_sleeping = False
        result = self.entity.sleep()
        self.assertTrue(result)
        self.assertTrue(self.entity.is_sleeping)
        self.assertGreater(self.entity.sleep_start_time, 0)
    
    def test_sleep_already_sleeping(self):
        """Тест засыпания уже спящего тамагочи"""
        self.entity.is_sleeping = True
        result = self.entity.sleep()
        self.assertFalse(result)
    
    def test_sleep_full_energy(self):
        """Тест засыпания при полной энергии"""
        self.entity.data.energy = 100
        result = self.entity.sleep()
        self.assertFalse(result)
    
    def test_wake_up_success(self):
        """Тест успешного пробуждения"""
        self.entity.is_sleeping = True
        result = self.entity.wake_up()
        self.assertTrue(result)
        self.assertFalse(self.entity.is_sleeping)
    
    def test_wake_up_not_sleeping(self):
        """Тест пробуждения неспящего тамагочи"""
        self.entity.is_sleeping = False
        result = self.entity.wake_up()
        self.assertFalse(result)
    
    def test_heal_success(self):
        """Тест успешного лечения"""
        self.entity.data.health = 50
        result = self.entity.heal(30)
        self.assertTrue(result)
        self.assertEqual(self.entity.data.health, 80)
    
    def test_heal_max_health(self):
        """Тест лечения при максимальном здоровье"""
        self.entity.data.health = 100
        result = self.entity.heal(30)
        self.assertFalse(result)
    
    def test_check_food_collision(self):
        """Тест проверки столкновения с едой"""
        # Позиция тамагочи: (200, 200)
        food_pos = (200, 200)  # Та же позиция
        food_size = 20
        result = self.entity.check_food_collision(food_pos, food_size)
        self.assertTrue(result)
    
    def test_check_food_collision_far(self):
        """Тест проверки столкновения с далекой едой"""
        food_pos = (500, 500)  # Далеко
        food_size = 20
        result = self.entity.check_food_collision(food_pos, food_size)
        self.assertFalse(result)
    
    def test_eat_food(self):
        """Тест поедания еды"""
        from entities.items import FoodItem
        food = FoodItem("Яблоко", 20, 10, 5, 10, (255, 0, 0))
        
        # Устанавливаем значения ниже максимума для проверки увеличения
        self.entity.data.hunger = 50
        self.entity.data.happiness = 50
        self.entity.data.energy = 50
        
        old_hunger = self.entity.data.hunger
        old_happiness = self.entity.data.happiness
        old_energy = self.entity.data.energy
        
        result = self.entity.eat_food(food)
        
        self.assertTrue(result)
        self.assertGreaterEqual(self.entity.data.hunger, old_hunger)
        self.assertGreaterEqual(self.entity.data.happiness, old_happiness)
        self.assertGreaterEqual(self.entity.data.energy, old_energy)
        self.assertTrue(hasattr(self.entity, 'eating_animation'))
    
    @patch('pygame.time.get_ticks')
    def test_update_stats_degradation(self, mock_ticks):
        """Тест деградации характеристик со временем"""
        mock_ticks.return_value = 35000  # 35 секунд
        self.entity.last_update_time = 0
        
        old_hunger = self.entity.data.hunger
        old_happiness = self.entity.data.happiness
        old_cleanliness = self.entity.data.cleanliness
        
        self.entity.update_stats()
        
        self.assertLess(self.entity.data.hunger, old_hunger)
        self.assertLess(self.entity.data.happiness, old_happiness)
        self.assertLess(self.entity.data.cleanliness, old_cleanliness)
    
    @patch('pygame.time.get_ticks')
    def test_update_stats_energy_regen_sleeping(self, mock_ticks):
        """Тест регенерации энергии во время сна"""
        self.entity.is_sleeping = True
        self.entity.sleep_start_time = 0
        self.entity.last_energy_regen = 0
        self.entity.data.energy = 50
        mock_ticks.return_value = 15000  # 15 секунд
        
        self.entity.update_stats()
        
        self.assertGreater(self.entity.data.energy, 50)
    
    @patch('pygame.time.get_ticks')
    def test_update_stats_auto_wake_up(self, mock_ticks):
        """Тест автоматического пробуждения при полной энергии"""
        self.entity.is_sleeping = True
        self.entity.data.energy = 100
        mock_ticks.return_value = 1000
        
        self.entity.update_stats()
        
        self.assertFalse(self.entity.is_sleeping)
    
    def test_update_animations(self):
        """Тест обновления анимаций"""
        self.entity.eating_animation = True
        self.entity.eating_timer = 0
        
        with patch('pygame.time.get_ticks', return_value=2000):
            self.entity.update_animations()
            self.assertFalse(self.entity.eating_animation)


if __name__ == '__main__':
    unittest.main()

