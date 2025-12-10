"""
Модуль сущностей для игры Tamagotchi Pou.

Этот модуль предоставляет основные классы сущностей, используемые в игре:
- TamagotchiEntity: Основной персонаж (тамагочи)
- Button: Интерактивные кнопки интерфейса
- FoodItem: Предметы еды для кормления
- Inventory: Инвентарь игрока
"""

from .tamagotchi import TamagotchiEntity
from .buttons import Button
from .items import FoodItem, Inventory

__all__ = ['TamagotchiEntity', 'Button', 'FoodItem', 'Inventory']