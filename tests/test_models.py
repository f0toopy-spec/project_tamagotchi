"""
Тесты для модуля database.models
"""
import unittest
from datetime import datetime
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Tamagotchi


class TestTamagotchi(unittest.TestCase):
    """Тесты для класса Tamagotchi"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.tamagotchi = Tamagotchi(name="Тестовый Питомец")
    
    def test_init_default_values(self):
        """Тест инициализации с значениями по умолчанию"""
        t = Tamagotchi()
        self.assertEqual(t.name, "Pou")
        self.assertEqual(t.hunger, 50)
        self.assertEqual(t.happiness, 50)
        self.assertEqual(t.health, 100)
        self.assertEqual(t.cleanliness, 50)
        self.assertEqual(t.energy, 100)
        self.assertEqual(t.age, 0)
        self.assertEqual(t.coins, 100)
        self.assertEqual(t.evolution_stage, 1)
        self.assertIsNone(t.id)
        self.assertIsInstance(t.created_at, datetime)
        self.assertIsInstance(t.last_updated, datetime)
    
    def test_init_custom_values(self):
        """Тест инициализации с пользовательскими значениями"""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        t = Tamagotchi(id=1, name="Кастомный", created_at=custom_time)
        self.assertEqual(t.id, 1)
        self.assertEqual(t.name, "Кастомный")
        self.assertEqual(t.created_at, custom_time)
    
    def test_to_dict(self):
        """Тест конвертации в словарь"""
        t = Tamagotchi(name="Тест")
        t.hunger = 75
        t.happiness = 80
        data = t.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], "Тест")
        self.assertEqual(data['hunger'], 75)
        self.assertEqual(data['happiness'], 80)
        self.assertEqual(data['health'], 100)
        self.assertEqual(data['cleanliness'], 50)
        self.assertEqual(data['energy'], 100)
        self.assertEqual(data['age'], 0)
        self.assertEqual(data['coins'], 100)
        self.assertEqual(data['evolution_stage'], 1)
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('last_updated', data)
    
    def test_from_dict(self):
        """Тест создания из словаря"""
        data = {
            'id': 5,
            'name': 'Из словаря',
            'hunger': 30,
            'happiness': 40,
            'health': 90,
            'cleanliness': 60,
            'energy': 70,
            'age': 5,
            'coins': 200,
            'evolution_stage': 2,
            'created_at': datetime(2023, 1, 1),
            'last_updated': datetime(2023, 1, 2)
        }
        
        t = Tamagotchi.from_dict(data)
        
        self.assertEqual(t.id, 5)
        self.assertEqual(t.name, 'Из словаря')
        self.assertEqual(t.hunger, 30)
        self.assertEqual(t.happiness, 40)
        self.assertEqual(t.health, 90)
        self.assertEqual(t.cleanliness, 60)
        self.assertEqual(t.energy, 70)
        self.assertEqual(t.age, 5)
        self.assertEqual(t.coins, 200)
        self.assertEqual(t.evolution_stage, 2)
        self.assertEqual(t.created_at, datetime(2023, 1, 1))
        self.assertEqual(t.last_updated, datetime(2023, 1, 2))
    
    def test_from_dict_partial(self):
        """Тест создания из неполного словаря"""
        data = {
            'name': 'Частичный',
            'hunger': 25
        }
        
        t = Tamagotchi.from_dict(data)
        
        self.assertEqual(t.name, 'Частичный')
        self.assertEqual(t.hunger, 25)
        # Остальные значения должны быть по умолчанию
        self.assertEqual(t.happiness, 50)
        self.assertEqual(t.health, 100)
        self.assertEqual(t.evolution_stage, 1)
    
    def test_to_dict_from_dict_roundtrip(self):
        """Тест полного цикла: to_dict -> from_dict"""
        original = Tamagotchi(name="Круг")
        original.hunger = 45
        original.happiness = 55
        original.age = 10
        original.id = 99
        
        data = original.to_dict()
        restored = Tamagotchi.from_dict(data)
        
        self.assertEqual(original.id, restored.id)
        self.assertEqual(original.name, restored.name)
        self.assertEqual(original.hunger, restored.hunger)
        self.assertEqual(original.happiness, restored.happiness)
        self.assertEqual(original.age, restored.age)
        self.assertEqual(original.coins, restored.coins)
        self.assertEqual(original.evolution_stage, restored.evolution_stage)


if __name__ == '__main__':
    unittest.main()

