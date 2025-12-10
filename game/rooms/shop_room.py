import pygame
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class ShopRoom(BaseRoom):
    """Класс магазина в игре Tamagotchi Pou.
    
    Магазин предоставляет возможность покупать различные предметы
    для улучшения состояния тамагочи: еду, лекарства, игрушки, средства гигиены.
    Покупки совершаются за игровые монеты, которые можно заработать в мини-играх.
    
    Особенности:
    - Различные товары на полках с ценами и эффектами
    - Продавец с репликами
    - Отображение текущего количества монет игрока
    - Выбор товара перед покупкой
    - Навигация через стрелки (кнопка "Назад" удалена)
    """
    
    def __init__(self):
        """Инициализирует комнату магазина.
        
        Устанавливает синий цвет фона и инициализирует состояние
        выбранного товара перед покупкой.
        """
        super().__init__("Shop", (50, 150, 200))  # Синий фон
        self.selected_item = None  # Выбранный товар для покупки
        self.setup()

    def setup(self):
        """Настраивает элементы магазина.
        
        Создает список товаров с их характеристиками и кнопки
        для совершения покупок. Товары размещены на двух полках.
        """
        # Товары магазина
        self.items = [
            # Немного поднимаем предметы выше, чтобы подписи не "уходили" в текстуру стола
            {"name": "Apple", "price": 10, "type": "food", "effect": 20, "color": RED, "x": 150, "y": 135},
            {"name": "Pizza", "price": 30, "type": "food", "effect": 50, "color": (255, 165, 0), "x": 300, "y": 135},
            {"name": "Medicine", "price": 50, "type": "health", "effect": 40, "color": GREEN, "x": 450, "y": 135},
            {"name": "Ball", "price": 25, "type": "toy", "effect": 30, "color": YELLOW, "x": 600, "y": 135},
            {"name": "Soap", "price": 15, "type": "clean", "effect": 100, "color": BLUE, "x": 150, "y": 275},
            {"name": "Energy Drink", "price": 40, "type": "energy", "effect": 80, "color": PURPLE, "x": 300, "y": 275},
        ]

        # Только кнопка покупки, кнопка "Назад" удалена (используйте стрелки)
        self.buttons = [
            Button(600, 500, 150, 50, "Buy", GREEN)  # Кнопка "Купить"
        ]

    def draw(self, screen, tamagotchi):
        """Отрисовывает комнату магазина.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            tamagotchi: Объект тамагочи для отображения и взаимодействия
            
        Порядок отрисовки:
        1. Фон комнаты и заголовок
        2. Полки магазина
        3. Товары на полках с подписями
        4. Продавец с облачком реплики
        5. Отображение монет игрока
        6. Информация о выбранном товаре
        7. Тамагочи в центре магазина
        8. Кнопки и стрелки навигации
        """
        # Отрисовываем фон комнаты без тамагочи сначала
        screen.fill(self.background_color)
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Отрисовываем объекты комнаты
        for obj in self.objects:
            obj.draw(screen)

        # Отрисовываем полки магазина
        pygame.draw.rect(screen, (139, 69, 19), (100, 100, 600, 300), border_radius=10)  # Основная полка
        pygame.draw.rect(screen, (160, 120, 80), (110, 110, 580, 280), border_radius=10)  # Внутренняя часть полки

        # Отрисовываем товары на полках (поверх текстур стола)
        for item in self.items:
            # Подсветка выбранного товара
            border_color = YELLOW if self.selected_item == item else BLACK
            border_width = 3 if self.selected_item == item else 1

            # Отрисовываем товар как круг
            pygame.draw.circle(screen, item["color"], (item["x"], item["y"]), 25)
            pygame.draw.circle(screen, border_color, (item["x"], item["y"]), 25, border_width)

            # Отрисовываем название и цену товара чуть выше, чтобы их не перекрывали текстуры
            name_text = self.small_font.render(item["name"], True, WHITE)
            name_rect = name_text.get_rect(center=(item["x"], item["y"] - 35))
            screen.blit(name_text, name_rect)

            price_text = self.small_font.render(f"{item['price']} coins", True, YELLOW)
            price_rect = price_text.get_rect(center=(item["x"], item["y"] - 15))
            screen.blit(price_text, price_rect)

        # Отрисовываем продавца
        pygame.draw.circle(screen, (255, 200, 150), (700, 100), 30)  # Голова
        pygame.draw.rect(screen, (100, 100, 200), (680, 130, 40, 40))  # Тело

        # Отрисовываем облачко реплики
        pygame.draw.ellipse(screen, WHITE, (620, 50, 150, 60))
        pygame.draw.polygon(screen, WHITE, [(670, 110), (690, 90), (710, 110)])
        speech_font = pygame.font.Font(None, 20)
        speech_text = speech_font.render("Buy something!", True, BLACK)
        screen.blit(speech_text, (650, 70))

        # Отрисовываем отображение монет
        if tamagotchi:
            coins_text = self.font.render(f"Coins: {tamagotchi.data.coins}", True, YELLOW)
            screen.blit(coins_text, (50, 80))

            # Отрисовываем информацию о выбранном товаре
            if self.selected_item:
                item = self.selected_item
                info_y = 400
                info_text = self.small_font.render(f"Selected: {item['name']}", True, WHITE)
                screen.blit(info_text, (50, info_y))

                effect_text = self.small_font.render(f"Effect: +{item['effect']} {item['type']}", True, WHITE)
                screen.blit(effect_text, (50, info_y + 25))

                price_text = self.small_font.render(f"Price: {item['price']} coins", True, YELLOW)
                screen.blit(price_text, (50, info_y + 50))
        
        # Отрисовываем тамагочи после всех текстур (спереди)
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в магазине.
        
        Аргументы:
            event: Событие PyGame для обработки
            mouse_pos: Текущая позиция курсора мыши (x, y)
            tamagotchi: Объект тамагочи для взаимодействия
            game_core: Основной объект игры для доступа к общему состоянию
            
        Возвращает:
            str: Имя комнаты для перехода ("shop" или результат навигации)
            
        Механика взаимодействия:
        1. Клик на товаре: выбор товара для покупки (подсветка желтой рамкой)
        2. Клик на кнопке "Buy": покупка выбранного товара (списание монет, применение эффекта)
        3. Клик на стрелках навигации: переход в соседние комнаты
        """
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем кнопку "Купить"
            if self.buttons[0].rect.collidepoint(mouse_pos):
                if self.selected_item and tamagotchi:
                    if tamagotchi.data.coins >= self.selected_item["price"]:
                        # Списание монет
                        tamagotchi.data.coins -= self.selected_item["price"]

                        # Применение эффекта товара в зависимости от типа
                        if self.selected_item["type"] == "food":
                            tamagotchi.data.hunger = min(100, tamagotchi.data.hunger + self.selected_item["effect"])
                        elif self.selected_item["type"] == "health":
                            tamagotchi.data.health = min(100, tamagotchi.data.health + self.selected_item["effect"])
                        elif self.selected_item["type"] == "toy":
                            tamagotchi.data.happiness = min(100,
                                                            tamagotchi.data.happiness + self.selected_item["effect"])
                        elif self.selected_item["type"] == "clean":
                            tamagotchi.data.cleanliness = 100  # Мыло полностью очищает
                        elif self.selected_item["type"] == "energy":
                            tamagotchi.data.energy = min(100, tamagotchi.data.energy + self.selected_item["effect"])

                        game_core.show_message(f"Bought {self.selected_item['name']}!")
                        game_core.auto_save()  # Автосохранение после покупки
                        self.selected_item = None  # Сброс выбранного товара
                    else:
                        game_core.show_message("Not enough coins!")
                else:
                    game_core.show_message("Select an item first!")
                return "shop"

            # Проверяем выбор товара
            for item in self.items:
                # Расчет расстояния от клика до центра товара
                distance = ((mouse_pos[0] - item["x"]) ** 2 + (mouse_pos[1] - item["y"]) ** 2) ** 0.5
                if distance <= 25:  # Клик по товару
                    self.selected_item = item
                    return "shop"

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        # По умолчанию остаемся в магазине
        return "shop"