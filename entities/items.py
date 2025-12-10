import pygame
from config import *


class FoodItem:
    """Класс, представляющий предмет еды в игре.
    
    Атрибуты:
        name: Название еды
        hunger_value: Значение насыщения (сколько восполняет голод)
        happiness_boost: Бонус к счастью
        energy_boost: Бонус к энергии
        price: Цена в магазине
        color: Цвет для отрисовки
        dragging: Флаг перетаскивания
        original_pos: Исходная позиция до перетаскивания
        current_pos: Текущая позиция на экране
        size: Размер для отрисовки
    """
    
    def __init__(self, name, hunger_value, happiness_boost, energy_boost, price, color):
        """Инициализирует предмет еды.
        
        Аргументы:
            name: Название еды
            hunger_value: Значение насыщения
            happiness_boost: Бонус к счастью
            energy_boost: Бонус к энергии
            price: Цена в магазине
            color: Цвет для отрисовки
        """
        self.name = name
        self.hunger_value = hunger_value
        self.happiness_boost = happiness_boost
        self.energy_boost = energy_boost
        self.price = price
        self.color = color
        self.dragging = False
        self.original_pos = None
        self.current_pos = None
        self.size = 30

    def draw(self, screen, x, y):
        """Отрисовывает предмет еды на экране.
        
        Аргументы:
            screen: Поверхность для отрисовки
            x: X-координата центра
            y: Y-координата центра
        """
        self.current_pos = (x, y)
        pygame.draw.circle(screen, self.color, (x, y), self.size)

        # Отрисовка названия еды
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=(x, y + self.size + 15))
        screen.blit(text, text_rect)

    def check_click(self, pos):
        """Проверяет, был ли клик на предмете.
        
        Аргументы:
            pos: Позиция клика (x, y)
            
        Возвращает:
            bool: True если клик был на предмете, иначе False
        """
        if self.current_pos is None:
            return False
        x, y = self.current_pos
        distance = ((pos[0] - x) ** 2 + (pos[1] - y) ** 2) ** 0.5
        return distance <= self.size

    def start_drag(self, pos):
        """Начинает перетаскивание предмета.
        
        Аргументы:
            pos: Позиция начала перетаскивания
        """
        self.dragging = True
        self.original_pos = self.current_pos

    def update_drag(self, pos):
        """Обновляет позицию перетаскиваемого предмета.
        
        Аргументы:
            pos: Новая позиция курсора
        """
        if self.dragging:
            self.current_pos = pos

    def stop_drag(self):
        """Завершает перетаскивание предмета.
        
        Возвращает:
            tuple: Исходную позицию предмета до перетаскивания
        """
        self.dragging = False
        return self.original_pos


class Inventory:
    """Класс, представляющий инвентарь игрока.
    
    Атрибуты:
        food_items: Список предметов еды в инвентаре
        max_items: Максимальное количество предметов в инвентаре
    """
    
    def __init__(self):
        """Инициализирует пустой инвентарь."""
        self.food_items = []
        self.max_items = 6

    def add_food(self, food_item):
        """Добавляет предмет еды в инвентарь.
        
        Аргументы:
            food_item: Объект FoodItem для добавления
            
        Возвращает:
            bool: True если добавление успешно, False если инвентарь полон
        """
        if len(self.food_items) < self.max_items:
            self.food_items.append(food_item)
            return True
        return False

    def remove_food(self, food_item):
        """Удаляет предмет еды из инвентаря.
        
        Аргументы:
            food_item: Объект FoodItem для удаления
            
        Возвращает:
            bool: True если удаление успешно, False если предмет не найден
        """
        if food_item in self.food_items:
            self.food_items.remove(food_item)
            return True
        return False

    def draw(self, screen):
        """Отрисовывает инвентарь на экране.
        
        Аргументы:
            screen: Поверхность для отрисовки
        """
        # Отрисовка фона инвентаря
        inventory_rect = pygame.Rect(50, 450, 700, 120)
        pygame.draw.rect(screen, GRAY, inventory_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, inventory_rect, 2, border_radius=10)

        # Отрисовка заголовка инвентаря
        font = pygame.font.Font(None, 24)
        title = font.render("Инвентарь (Перетащите еду к тамагочи)", True, BLACK)
        screen.blit(title, (inventory_rect.x + 10, inventory_rect.y + 10))

        # Отрисовка предметов еды в инвентаре
        for i, food in enumerate(self.food_items):
            x = inventory_rect.x + 60 + i * 100
            y = inventory_rect.y + 60
            food.draw(screen, x, y)