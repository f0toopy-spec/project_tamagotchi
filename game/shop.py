import pygame
from entities.buttons import Button
from entities.items import FoodItem
from config import *


class Shop:
    """Класс, представляющий магазин еды в игре Tamagotchi Pou.
    
    Магазин позволяет игроку покупать различные виды еды для своего тамагочи.
    Каждый вид еды имеет разные характеристики и стоимость.
    
    Атрибуты:
        food_items: Список доступных товаров (FoodItem)
        buttons: Список кнопок для покупки товаров
    """
    
    def __init__(self):
        """Инициализирует магазин с доступными товарами."""
        # Определяем доступные товары
        self.food_items = [
            FoodItem("Яблоко", 20, 5, 2, 10, RED),
            FoodItem("Банан", 25, 7, 3, 15, YELLOW),
            FoodItem("Пицца", 50, 15, 5, 30, (255, 165, 0)),  # Оранжевый
            FoodItem("Бургер", 40, 12, 4, 25, (139, 69, 19)),  # Коричневый
            FoodItem("Мороженое", 15, 20, 1, 20, (255, 192, 203)),  # Розовый
            FoodItem("Энергетический батончик", 10, 5, 25, 35, (210, 180, 140)),  # Бежевый
        ]

        self.buttons = []
        self.setup_ui()

    def setup_ui(self):
        """Настраивает пользовательский интерфейс магазина."""
        for i, item in enumerate(self.food_items):
            # Создаём кнопку для каждого товара
            button = Button(100, 150 + i * 70, 400, 60,
                            f"{item.name} - {item.price} монет")
            self.buttons.append((button, item))

    def draw(self, screen, coins, inventory):
        """Отрисовывает интерфейс магазина.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            coins: Количество монет у игрока
            inventory: Инвентарь игрока
        """
        # Заливаем фон
        screen.fill(LIGHT_YELLOW)
        
        # Рисуем декоративные элементы магазина
        # Полки
        for i in range(3):
            shelf_y = 140 + i * 80
            shelf_rect = pygame.Rect(80, shelf_y, 640, 10)
            pygame.draw.rect(screen, BROWN, shelf_rect)
        
        # Табличка с названием магазина
        sign_rect = pygame.Rect(300, 30, 200, 60)
        pygame.draw.rect(screen, RED, sign_rect, border_radius=10)
        pygame.draw.rect(screen, GOLD, sign_rect, 3, border_radius=10)
        
        # Заголовок магазина
        font = pygame.font.Font(None, 48)
        title = font.render("МАГАЗИН ЕДЫ", True, WHITE)
        screen.blit(title, (sign_rect.centerx - title.get_width() // 2, 
                           sign_rect.centery - title.get_height() // 2))

        # Отображение количества монет
        coins_font = pygame.font.Font(None, 36)
        coins_text = coins_font.render(f"Монеты: {coins}", True, YELLOW)
        screen.blit(coins_text, (600, 50))
        
        # Иконка монет
        pygame.draw.circle(screen, GOLD, (580, 65), 15)
        coin_font = pygame.font.Font(None, 24)
        coin_symbol = coin_font.render("$", True, BLACK)
        screen.blit(coin_symbol, (575, 55))

        # Информация о свободном месте в инвентаре
        space_font = pygame.font.Font(None, 32)
        space_text = space_font.render(
            f"Место в инвентаре: {len(inventory.food_items)}/{inventory.max_items}", 
            True, DARK_GREEN
        )
        screen.blit(space_text, (50, 100))
        
        # Индикатор заполненности
        fill_percent = len(inventory.food_items) / inventory.max_items
        bar_width = 200
        bar_height = 20
        bar_x = 50
        bar_y = 130
        
        # Фон индикатора
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Заливка индикатора
        fill_width = int(bar_width * fill_percent)
        if fill_percent < 0.7:
            fill_color = GREEN
        elif fill_percent < 0.9:
            fill_color = YELLOW
        else:
            fill_color = RED
        pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))

        small_font = pygame.font.Font(None, 28)

        # Отрисовка товаров и кнопок
        for i, (button, item) in enumerate(self.buttons):
            # Рисуем кнопку
            button.draw(screen)
            
            # Рисуем иконку товара слева от кнопки
            item_x = 60
            item_y = button.rect.y + button.rect.height // 2
            pygame.draw.circle(screen, item.color, (item_x, item_y), 25)
            
            # Отображаем характеристики товара
            effects_text = small_font.render(
                f"🍎 +{item.hunger_value} 😊 +{item.happiness_boost} ⚡ +{item.energy_boost}",
                True, BLACK
            )
            screen.blit(effects_text, (520, button.rect.y + 15))

            # Индикатор возможности покупки
            if coins >= item.price and len(inventory.food_items) < inventory.max_items:
                afford_text = small_font.render("Купить ✓", True, GREEN)
                afford_bg = pygame.Rect(520, button.rect.y + 35, 120, 20)
                pygame.draw.rect(screen, (200, 255, 200), afford_bg, border_radius=5)
            elif len(inventory.food_items) >= inventory.max_items:
                afford_text = small_font.render("Инвентарь полон", True, RED)
                afford_bg = pygame.Rect(520, button.rect.y + 35, 140, 20)
                pygame.draw.rect(screen, (255, 200, 200), afford_bg, border_radius=5)
            else:
                afford_text = small_font.render("Недостаточно монет", True, RED)
                afford_bg = pygame.Rect(520, button.rect.y + 35, 160, 20)
                pygame.draw.rect(screen, (255, 200, 200), afford_bg, border_radius=5)
            
            pygame.draw.rect(screen, BLACK, afford_bg, 1, border_radius=5)
            screen.blit(afford_text, (afford_bg.x + 5, afford_bg.y))
        
        # Инструкция для игрока
        instruction_font = pygame.font.Font(None, 24)
        instruction = instruction_font.render("Нажмите на товар, чтобы купить его", True, DARK_GRAY)
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 40))
        
        # Подсказка по управлению
        hint = instruction_font.render("Нажмите ESC, чтобы выйти из магазина", True, DARK_GRAY)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 20))

    def handle_events(self, event, mouse_pos, tamagotchi, inventory):
        """Обрабатывает события в магазине.
        
        Аргументы:
            event: Событие PyGame
            mouse_pos: Позиция курсора мыши (x, y)
            tamagotchi: Объект тамагочи игрока
            inventory: Инвентарь игрока
            
        Возвращает:
            tuple: (success, message) - успех покупки и сообщение
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button, item in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    # Проверяем, хватает ли монет
                    if tamagotchi.data.coins >= item.price:
                        # Проверяем, есть ли место в инвентаре
                        if len(inventory.food_items) < inventory.max_items:
                            # Списание монет
                            tamagotchi.data.coins -= item.price
                            
                            # Создаём новый экземпляр еды
                            new_food = FoodItem(
                                item.name, 
                                item.hunger_value, 
                                item.happiness_boost,
                                item.energy_boost, 
                                item.price, 
                                item.color
                            )
                            
                            # Добавляем в инвентарь
                            if inventory.add_food(new_food):
                                return True, f"Куплено: {item.name}!"
                            else:
                                # Возвращаем монеты, если не удалось добавить
                                tamagotchi.data.coins += item.price
                                return False, "Не удалось добавить в инвентарь."
                        else:
                            return False, "Инвентарь полон!"
                    else:
                        return False, f"Недостаточно монет! Нужно {item.price}."
        
        # Возвращаем значения по умолчанию, если покупка не совершена
        return False, ""