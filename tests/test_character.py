"""
Тесты для модуля entities.character
"""
import unittest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.character import Character


class TestCharacter(unittest.TestCase):
    """Тесты для класса Character"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.character = Character()
    
    def test_init(self):
        """Тест инициализации персонажа"""
        self.assertEqual(self.character.evolution_stage, 1)
        self.assertIsInstance(self.character.customizations, dict)
        self.assertEqual(len(self.character.customizations), 0)
    
    def test_evolve_stage_1_to_2(self):
        """Тест эволюции со стадии 1 на стадию 2"""
        self.character.evolution_stage = 1
        result = self.character.evolve()
        
        self.assertTrue(result)
        self.assertEqual(self.character.evolution_stage, 2)
    
    def test_evolve_stage_2_to_3(self):
        """Тест эволюции со стадии 2 на стадию 3"""
        self.character.evolution_stage = 2
        result = self.character.evolve()
        
        self.assertTrue(result)
        self.assertEqual(self.character.evolution_stage, 3)
    
    def test_evolve_stage_3_max(self):
        """Тест невозможности эволюции на стадии 3"""
        self.character.evolution_stage = 3
        result = self.character.evolve()
        
        self.assertFalse(result)
        self.assertEqual(self.character.evolution_stage, 3)
    
    def test_add_customization(self):
        """Тест добавления предмета кастомизации"""
        self.character.add_customization('шляпа', 1)
        
        self.assertIn('шляпа', self.character.customizations)
        self.assertEqual(self.character.customizations['шляпа'], 1)
    
    def test_add_customization_replace(self):
        """Тест замены существующего предмета кастомизации"""
        self.character.add_customization('шляпа', 1)
        self.character.add_customization('шляпа', 2)
        
        self.assertEqual(self.character.customizations['шляпа'], 2)
        self.assertEqual(len(self.character.customizations), 1)
    
    def test_add_multiple_customizations(self):
        """Тест добавления нескольких предметов кастомизации"""
        self.character.add_customization('шляпа', 1)
        self.character.add_customization('рубашка', 2)
        self.character.add_customization('аксессуар', 3)
        
        self.assertEqual(len(self.character.customizations), 3)
        self.assertEqual(self.character.customizations['шляпа'], 1)
        self.assertEqual(self.character.customizations['рубашка'], 2)
        self.assertEqual(self.character.customizations['аксессуар'], 3)


if __name__ == '__main__':
    unittest.main()

