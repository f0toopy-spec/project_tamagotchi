"""
Главный файл для запуска всех тестов проекта
"""
import unittest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_tests():
    """Загружает все тесты из модулей"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Список всех тестовых модулей
    test_modules = [
        'tests.test_models',
        'tests.test_database',
        'tests.test_tamagotchi_entity',
        'tests.test_character',
        'tests.test_items',
        'tests.test_buttons',
        'tests.test_helpers',
        'tests.test_animation',
        'tests.test_game_core',
        'tests.test_postgres_manager',
    ]
    
    # Загружаем тесты из каждого модуля
    for module_name in test_modules:
        try:
            module = __import__(module_name, fromlist=[''])
            tests = loader.loadTestsFromModule(module)
            suite.addTests(tests)
            print(f"[OK] Загружены тесты из {module_name}")
        except Exception as e:
            print(f"[ERROR] Ошибка загрузки тестов из {module_name}: {e}")
    
    return suite


if __name__ == '__main__':
    print("=" * 60)
    print("Запуск всех тестов проекта Tamagotchi Pou")
    print("=" * 60)
    print()
    
    suite = load_tests()
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("=" * 60)
    
    # Возвращаем код выхода: 0 если все успешно, 1 если есть ошибки
    sys.exit(0 if result.wasSuccessful() else 1)

