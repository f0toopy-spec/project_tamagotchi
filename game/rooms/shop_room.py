import pygame
import os
import math
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class ShopRoom(BaseRoom):
    """Класс магазина в игре Tamagotchi Pou."""
    
    def __init__(self):
        """Инициализирует комнату магазина."""
        # Загружаем фоновое изображение магазина
        try:
            # Получаем корневую директорию проекта
            
            shop_bg_path = 'assets\images\shop.jpg'
            
            if os.path.exists(shop_bg_path):
                background_image = pygame.image.load(shop_bg_path).convert()
                print(f"✓ Фоновое изображение магазина загружено: {shop_bg_path}")
            else:
                print(f"✗ Фоновое изображение не найдено: {shop_bg_path}")
                background_image = None
        except Exception as e:
            print(f"✗ Не удалось загрузить фоновое изображение: {e}")
            background_image = None
        
        # Сохраняем информацию о фоне
        self.background_image = background_image
        
        # Если есть изображение, передаем его в родительский класс
        if background_image:
            super().__init__("Shop", background_image)
            self.background_color = None
        else:
            # Если нет изображения, используем синий цвет
            super().__init__("Shop", (50, 150, 200))
            self.background_color = (50, 150, 200)
        
        # Загружаем изображение продавца
        self.seller_image = None
        try:
            # Получаем корневую директорию проекта
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Пробуем разные пути к изображению продавца
            path='assets\images\seller.png'
            
            
            print(f"Проверяю путь к продавцу: {path}")
            if os.path.exists(path):
                self.seller_image = pygame.image.load(path).convert_alpha()
                    
                print(f"✓ Изображение продавца загружено: {path}")
                
            else:
                    print(f"  Файл не найден: {path}")
            
            if self.seller_image is None:
                print("⚠ Изображение продавца не найдено. Использую рисованного продавца.")
        except Exception as e:
            print(f"Ошибка загрузки продавца: {e}")
            # Создаем тестовое изображение продавца, если файл не найден
            self.create_test_seller_image()
        
        # Инициализируем атрибуты магазина
        self.items = []
        self.buttons = []
        self.selected_item = None
        self.objects = [] if not hasattr(self, 'objects') else self.objects
        self.font = pygame.font.Font(None, 36) if not hasattr(self, 'font') else self.font
        self.small_font = pygame.font.Font(None, 24) if not hasattr(self, 'small_font') else self.small_font
        
        # Параметры для продавца
        self.seller_x = 150
        self.seller_y = 500
        self.seller_width = 100
        self.seller_height = 120
        
        # Для анимации облачка речи
        self.speech_timer = 0
        self.current_speech = 0
        self.speeches = [
            "Купи что-нибудь!",
            "Лучшие цены!",
            "Свежие товары!",
            "Специальное предложение!",
            "Качественные товары!"
        ]
        
        # Настраиваем магазин
        self.setup()
    
    def create_test_seller_image(self):
        """Создает тестовое изображение продавца, если файл не найден."""
        try:
            # Создаем поверхность с прозрачностью
            surface = pygame.Surface((self.seller_width, self.seller_height), pygame.SRCALPHA)
            
            # Тело продавца
            pygame.draw.ellipse(surface, (255, 200, 150, 255), (25, 5, 30, 40))  # Голова
            pygame.draw.rect(surface, (100, 100, 200, 255), (15, 45, 50, 40))  # Тело
            pygame.draw.rect(surface, (50, 50, 100, 255), (25, 55, 30, 20))  # Рубашка
            
            # Черты лица
            pygame.draw.circle(surface, (0, 0, 0, 255), (35, 20), 3)  # Левый глаз
            pygame.draw.circle(surface, (0, 0, 0, 255), (45, 20), 3)  # Правый глаз
            pygame.draw.arc(surface, (0, 0, 0, 255), (35, 30, 20, 10), 0, 3.14, 2)  # Улыбка
            
            self.seller_image = surface
            print("✓ Создано тестовое изображение продавца")
        except Exception as e:
            print(f"Ошибка создания тестового изображения: {e}")
            self.seller_image = None

    def setup(self):
        """Настраивает элементы магазина."""
        # Товары магазина
        self.items = [
            {"name": "Яблоко", "price": 10, "type": "food", "effect": 20, "color": RED, "x": 150, "y": 135},
            {"name": "Пицца", "price": 30, "type": "food", "effect": 50, "color": (255, 165, 0), "x": 300, "y": 135},
            {"name": "Лекарство", "price": 50, "type": "health", "effect": 40, "color": GREEN, "x": 450, "y": 135},
            {"name": "Мяч", "price": 25, "type": "toy", "effect": 30, "color": YELLOW, "x": 600, "y": 135},
            {"name": "Мыло", "price": 15, "type": "clean", "effect": 100, "color": BLUE, "x": 150, "y": 275},
            {"name": "Энергетик", "price": 40, "type": "energy", "effect": 80, "color": PURPLE, "x": 300, "y": 275},
        ]

        # Только кнопка покупки
        self.buttons = [
            Button(600, 500, 150, 50, "Купить", GREEN)
        ]

    def draw(self, screen, tamagotchi):
        """Отрисовывает комнату магазина."""
        # Проверяем, что атрибуты инициализированы
        if not hasattr(self, 'items'):
            self.items = []
        if not hasattr(self, 'buttons'):
            self.buttons = []
        if not hasattr(self, 'selected_item'):
            self.selected_item = None
        
        # Рисуем фон
        if self.background_image:
            # Масштабируем изображение под размер экрана
            scaled_bg = pygame.transform.scale(self.background_image, screen.get_size())
            screen.blit(scaled_bg, (0, 0))
        elif hasattr(self, 'background_color') and self.background_color:
            # Используем цветной фон
            screen.fill(self.background_color)
        else:
            # Запасной вариант - черный фон
            screen.fill((0, 0, 0))
        
        # Заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Отрисовываем объекты комнаты
        if hasattr(self, 'objects'):
            for obj in self.objects:
                obj.draw(screen)

        # Отрисовываем полки магазина
        self.draw_shelves(screen)
        
        # Отрисовываем товары на полках
        self.draw_items(screen)
        
        # Отрисовываем продавца
        self.draw_seller(screen)
        
        # Отрисовываем облачко речи
        self.draw_speech_bubble(screen)

        # Отрисовываем отображение монет
        if tamagotchi:
            self.draw_coins_display(screen, tamagotchi)
            
            # Отрисовываем информацию о выбранном товаре
            self.draw_selected_item_info(screen)

        # Отрисовываем тамагочи
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_shelves(self, screen):
        """Рисует полки магазина."""
        # Основная полка
        pygame.draw.rect(screen, (139, 69, 19), (100, 100, 600, 300), border_radius=10)
        # Внутренняя часть полки
        pygame.draw.rect(screen, (160, 120, 80), (110, 110, 580, 280), border_radius=10)
        # Деревянная текстура (вертикальные полосы)
        for x in range(110, 690, 20):
            pygame.draw.line(screen, (150, 100, 50), (x, 110), (x, 390), 1)

    def draw_items(self, screen):
        """Рисует товары на полках."""
        for item in self.items:
            # Подсветка выбранного товара
            border_color = YELLOW if self.selected_item == item else BLACK
            border_width = 3 if self.selected_item == item else 1

            # Отрисовываем товар как круг
            pygame.draw.circle(screen, item["color"], (item["x"], item["y"]), 25)
            pygame.draw.circle(screen, border_color, (item["x"], item["y"]), 25, border_width)

            # Отбрасываем тень
            

            # Отрисовываем название и цену товара
            name_text = self.small_font.render(item["name"], True, WHITE)
            name_rect = name_text.get_rect(center=(item["x"], item["y"] - 35))
            # Фон для названия
            name_bg = pygame.Rect(name_rect.x - 5, name_rect.y - 2, name_rect.width + 10, name_rect.height + 4)
            pygame.draw.rect(screen, (0, 0, 0, 150), name_bg, border_radius=3)
            screen.blit(name_text, name_rect)

            price_text = self.small_font.render(f"{item['price']} монет", True, YELLOW)
            price_rect = price_text.get_rect(center=(item["x"], item["y"] - 15))
            # Фон для цены
            price_bg = pygame.Rect(price_rect.x - 5, price_rect.y - 2, price_rect.width + 10, price_rect.height + 4)
            pygame.draw.rect(screen, (0, 0, 0, 150), price_bg, border_radius=3)
            screen.blit(price_text, price_rect)

    def draw_seller(self, screen):
        """Отрисовывает продавца из PNG изображения."""
        
        if self.seller_image is not None:
            # Масштабируем изображение если нужно
            scaled_seller = pygame.transform.scale(
                self.seller_image, 
                (self.seller_width, self.seller_height)
            )
            
            # Позиционируем продавца с легкой анимацией дыхания
            y_offset = math.sin(pygame.time.get_ticks() * 0.003) * 2
            seller_rect = scaled_seller.get_rect(center=(self.seller_x, self.seller_y + y_offset))
            screen.blit(scaled_seller, seller_rect)
            
            # Отбрасываем тень
            shadow = pygame.Surface((self.seller_width - 10, 10), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 80))
            shadow_rect = shadow.get_rect(center=(self.seller_x, self.seller_y + self.seller_height//2 + 20))
            screen.blit(shadow, shadow_rect)
        else:
            # Запасной вариант - рисованный продавец
            y_offset = math.sin(pygame.time.get_ticks() * 0.003) * 2
            current_y = self.seller_y + y_offset
            
            # Тело
            pygame.draw.ellipse(screen, (100, 100, 200), 
                              (self.seller_x - 25, current_y + 10, 50, 60))
            # Голова
            pygame.draw.circle(screen, (255, 200, 150), 
                             (self.seller_x, current_y - 15), 25)
            # Черты лица
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.seller_x - 8, current_y - 20), 3)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.seller_x + 8, current_y - 20), 3)
            pygame.draw.arc(screen, (0, 0, 0), 
                          (self.seller_x - 10, current_y - 10, 20, 15), 0, 3.14, 2)

    def draw_speech_bubble(self, screen):
        """Рисует облачко с репликой продавца."""
        # Обновляем таймер для смены реплик
        self.speech_timer += 1
        if self.speech_timer > 180:  # Меняем реплику каждые 3 секунды (при 60 FPS)
            self.speech_timer = 0
            self.current_speech = (self.current_speech + 1) % len(self.speeches)
        
        # Позиция облачка
        bubble_x = self.seller_x + 60  # Смещаем влево
        bubble_y = self.seller_y - 50 
        
        # Рисуем облачко
        bubble_rect = pygame.Rect(bubble_x, bubble_y, 190, 60)
        pygame.draw.ellipse(screen, (255, 255, 255), bubble_rect)  # Белый фон
        pygame.draw.ellipse(screen, (100, 100, 100), bubble_rect, 2)  # Серая обводка
        
        # Хвостик облачка
        tail_points = [
            (bubble_x + 10, bubble_y + 20),
            (bubble_x -10 , bubble_y),
            (bubble_x + 10, bubble_y + 40)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), tail_points)  # Белый
        pygame.draw.polygon(screen, (100, 100, 100), tail_points, 2)  # Серая обводка
        
        # Текст реплики
        speech_font = pygame.font.Font(None, 20)
        speech_text = speech_font.render(self.speeches[self.current_speech], True, (0, 0, 0))
        text_rect = speech_text.get_rect(center=(bubble_x + 90, bubble_y + 30))
        screen.blit(speech_text, text_rect)

    def draw_coins_display(self, screen, tamagotchi):
        """Рисует отображение количества монет."""
        coins_text = self.font.render(f"Монеты: {tamagotchi.data.coins}", True, YELLOW)
        
        # Фон для текста монет для лучшей читаемости
        coins_bg = pygame.Rect(45, 50, 200, 35)
        pygame.draw.rect(screen, (0, 0, 0, 160), coins_bg, border_radius=8)
        pygame.draw.rect(screen, (255, 215, 0), coins_bg, 2, border_radius=8)  # Золотой цвет
        screen.blit(coins_text, (75, 60))
        
        # Иконка монеты
        pygame.draw.circle(screen, (255, 215, 0), (60, 65), 12)  # Золотой
        pygame.draw.circle(screen, (255, 255, 0), (60, 65), 12, 2)  # Желтая обводка
        coin_font = pygame.font.Font(None, 18)
        coin_symbol = coin_font.render("$", True, BLACK)
        screen.blit(coin_symbol, (56, 59))

    def draw_selected_item_info(self, screen):
        """Рисует информацию о выбранном товаре."""
        if self.selected_item:
            item = self.selected_item
            info_y = 400
            
            # Фон для информации
            info_bg = pygame.Rect(45, 395, 350, 100)
            pygame.draw.rect(screen, (0, 0, 0, 180), info_bg, border_radius=10)
            if self.selected_item["color"]:
                pygame.draw.rect(screen, self.selected_item["color"], info_bg, 3, border_radius=10)
            
            # Заголовок
            title_text = self.small_font.render("Выбранный товар:", True, WHITE)
            screen.blit(title_text, (50, info_y))
            
            # Название товара
            name_text = self.small_font.render(f"Название: {item['name']}", True, WHITE)
            screen.blit(name_text, (50, info_y + 25))
            
            # Эффект
            effect_color = GREEN if item['effect'] > 50 else YELLOW if item['effect'] > 20 else WHITE
            effect_text = self.small_font.render(f"Эффект: +{item['effect']} {item['type']}", 
                                                True, effect_color)
            screen.blit(effect_text, (50, info_y + 50))
            
            # Цена
            price_text = self.small_font.render(f"Цена: {item['price']} монет", True, YELLOW)
            screen.blit(price_text, (50, info_y + 75))

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в магазине."""
        # Проверяем наличие атрибутов
        if not hasattr(self, 'buttons'):
            self.buttons = []
        if not hasattr(self, 'items'):
            self.items = []
        if not hasattr(self, 'selected_item'):
            self.selected_item = None
        
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем кнопку "Купить"
            if self.buttons and self.buttons[0].rect.collidepoint(mouse_pos):
                if self.selected_item and tamagotchi:
                    if tamagotchi.data.coins >= self.selected_item["price"]:
                        # Списание монет
                        tamagotchi.data.coins -= self.selected_item["price"]

                        # Применение эффекта товара в зависимости от типа
                        item_type = self.selected_item["type"]
                        effect = self.selected_item["effect"]
                        
                        if item_type == "food":
                            tamagotchi.data.hunger = min(100, tamagotchi.data.hunger + effect)
                        elif item_type == "health":
                            tamagotchi.data.health = min(100, tamagotchi.data.health + effect)
                        elif item_type == "toy":
                            tamagotchi.data.happiness = min(100, tamagotchi.data.happiness + effect)
                        elif item_type == "clean":
                            tamagotchi.data.cleanliness = 100  # Мыло полностью очищает
                        elif item_type == "energy":
                            tamagotchi.data.energy = min(100, tamagotchi.data.energy + effect)

                        game_core.show_message(f"Куплено: {self.selected_item['name']}!")
                        game_core.auto_save()  # Автосохранение после покупки
                        self.selected_item = None  # Сброс выбранного товара
                    else:
                        game_core.show_message("Недостаточно монет!")
                else:
                    game_core.show_message("Сначала выберите товар!")
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