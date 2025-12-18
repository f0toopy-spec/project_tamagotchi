import pygame
import os
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Kitchen(BaseRoom):
    """Класс кухни в игре Tamagotchi Pou."""
    
    def __init__(self):
        """Инициализирует кухню."""
        # Загружаем фоновое изображение кухни
        try:
            # Получаем корневую директорию проекта
           
            kitchen_bg_path = 'assets\images\gritching.jpg'
            
            if os.path.exists(kitchen_bg_path):
                background_image = pygame.image.load(kitchen_bg_path).convert()
                print(f"✓ Фоновое изображение кухни загружено: {kitchen_bg_path}")
            else:
                print(f"✗ Фоновое изображение не найдено: {kitchen_bg_path}")
                background_image = None
        except Exception as e:
            print(f"✗ Не удалось загрузить фоновое изображение: {e}")
            background_image = None
        
        # Сохраняем информацию о фоне
        self.background_image = background_image
        
        # Если есть изображение, передаем его в родительский класс
        if background_image:
            super().__init__("Kitchen", background_image)
            self.background_color = None
        else:
            # Если нет изображения, используем светло-коричневый цвет
            super().__init__("Kitchen", (200, 180, 150))
            self.background_color = (200, 180, 150)
        
        # Инициализируем атрибуты кухни
        self.objects = [] if not hasattr(self, 'objects') else self.objects
        self.font = pygame.font.Font(None, 36) if not hasattr(self, 'font') else self.font
        self.small_font = pygame.font.Font(None, 24) if not hasattr(self, 'small_font') else self.small_font
        
        # Флаги для обучающих текстов и шкалы голода
        self.show_hunger_text = True
        self.show_instructions = True
        self.hunger_bar_timer = 0
        self.hunger_bar_duration = 2000
        
        # Настраиваем комнату
        self.setup()

    def setup(self):
        """Настраивает элементы кухни."""
        # Кнопка навигации
        self.buttons = [
            Button(50, 500, 180, 60, "Вернуться в зал", GRAY)
        ]

        # Предметы еды на столешнице
        self.food_items = [
            {"name": "Яблоко", "x": 200, "y": 200, "color": RED, "size": 25, "hunger": 20},
            {"name": "Банан", "x": 300, "y": 200, "color": YELLOW, "size": 30, "hunger": 25},
            {"name": "Пицца", "x": 400, "y": 200, "color": (255, 165, 0), "size": 35, "hunger": 50},
            {"name": "Молоко", "x": 500, "y": 200, "color": WHITE, "size": 30, "hunger": 15},
        ]

    def draw(self, screen, tamagotchi):
        """Отрисовывает кухню."""
        # Рисуем фон
        if self.background_image:
            # Масштабируем изображение под размер экрана
            scaled_bg = pygame.transform.scale(self.background_image, screen.get_size())
            screen.blit(scaled_bg, (0, 0))
        elif hasattr(self, 'background_color') and self.background_color:
            # Используем цветной фон
            screen.fill(self.background_color)
        else:
            # Запасной вариант
            screen.fill((200, 180, 150))
        
        # Заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        # Отрисовываем объекты комнаты
        if hasattr(self, 'objects'):
            for obj in self.objects:
                obj.draw(screen)

        # Если нет фонового изображения, рисуем кухонную мебель
        if not self.background_image:
            self.draw_kitchen_furniture(screen)
        
        # Отрисовываем предметы еды
        self.draw_food_items(screen)
        
        # Отрисовываем тамагочи
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
        
        # Отрисовываем информационные тексты
        if tamagotchi:
            self.draw_hunger_info(screen, tamagotchi)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_kitchen_furniture(self, screen):
        """Рисует кухонную мебель (используется если нет фонового изображения)."""
        # Кухонный гарнитур
        # Нижние шкафы
        for i in range(4):
            x = 150 + i * 125
            pygame.draw.rect(screen, (139, 69, 19), (x, 300, 100, 100))
            pygame.draw.rect(screen, (120, 60, 15), (x, 300, 100, 100), 3)
            
            # Ручки шкафов
            pygame.draw.rect(screen, (200, 200, 200), (x + 40, 350, 20, 5))
            pygame.draw.rect(screen, (150, 150, 150), (x + 40, 350, 20, 5), 1)

        # Верхние шкафы
        for i in range(4):
            x = 150 + i * 125
            pygame.draw.rect(screen, (160, 140, 120), (x, 150, 100, 100))
            pygame.draw.rect(screen, (140, 120, 100), (x, 150, 100, 100), 3)

        # Столешница
        pygame.draw.rect(screen, (200, 180, 160), (150, 250, 500, 30))
        
        # Узор столешницы
        for i in range(10):
            x = 150 + i * 50
            pygame.draw.line(screen, (180, 160, 140), (x, 250), (x, 280), 2)

        # Плита (вторая слева)
        pygame.draw.rect(screen, (70, 70, 70), (275, 300, 100, 80))
        pygame.draw.rect(screen, (50, 50, 50), (275, 300, 100, 80), 3)
        
        # Конфорки
        for i in range(2):
            for j in range(2):
                x = 290 + i * 35
                y = 315 + j * 35
                pygame.draw.circle(screen, BLACK, (x, y), 15)
                pygame.draw.circle(screen, (100, 100, 100), (x, y), 15, 2)
        
        # Панель управления
        pygame.draw.rect(screen, (40, 40, 40), (300, 320, 50, 30))
        for i in range(3):
            pygame.draw.circle(screen, (200, 200, 200), (310 + i * 15, 335), 4)

        # Холодильник (справа)
        pygame.draw.rect(screen, (240, 240, 240), (575, 150, 100, 250))
        pygame.draw.rect(screen, (200, 200, 200), (575, 150, 100, 250), 3)
        
        # Дверца холодильника
        pygame.draw.rect(screen, (220, 220, 220), (580, 155, 90, 240))
        
        # Ручка холодильника
        pygame.draw.rect(screen, (180, 180, 180), (645, 250, 5, 40))
        pygame.draw.circle(screen, (180, 180, 180), (647, 250), 5)
        pygame.draw.circle(screen, (180, 180, 180), (647, 290), 5)
        
        # Магнитики на холодильник
        magnets = [(590, 180), (610, 210), (630, 190), (590, 230)]
        colors = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255)]
        for (x, y), color in zip(magnets, colors):
            pygame.draw.circle(screen, color, (x, y), 8)
            pygame.draw.circle(screen, WHITE, (x, y), 8, 1)

        # Раковина (третья слева)
        pygame.draw.rect(screen, (180, 180, 180), (400, 300, 100, 80))
        pygame.draw.ellipse(screen, (150, 200, 255), (410, 310, 80, 50))
        
        # Кран
        pygame.draw.rect(screen, (200, 200, 200), (450, 280, 10, 20))
        pygame.draw.circle(screen, (200, 200, 200), (455, 280), 8)
        
        # Окно над раковиной
        pygame.draw.rect(screen, (135, 206, 235), (420, 160, 60, 40))
        pygame.draw.rect(screen, (100, 150, 200), (420, 160, 60, 40), 3)
        pygame.draw.line(screen, (100, 150, 200), (450, 160), (450, 200), 2)
        pygame.draw.line(screen, (100, 150, 200), (420, 180), (480, 180), 2)

        # Кухонный стол в центре
        pygame.draw.rect(screen, (160, 120, 80), (300, 400, 200, 20))  # Столешница
        pygame.draw.rect(screen, (139, 69, 19), (320, 420, 30, 30))    # Левая ножка
        pygame.draw.rect(screen, (139, 69, 19), (450, 420, 30, 30))    # Правая ножка

    def draw_food_items(self, screen):
        """Рисует предметы еды на кухне."""
        for food in self.food_items:
            # Основной круг еды
            pygame.draw.circle(screen, food["color"], (food["x"], food["y"]), food["size"])
            
            # Обводка
            pygame.draw.circle(screen, BLACK, (food["x"], food["y"]), food["size"], 2)
            
            # Детали для разных типов еды
            if food["name"] == "Яблоко":
                # Черенок яблока
                pygame.draw.rect(screen, (139, 69, 19), (food["x"] - 3, food["y"] - food["size"] - 5, 6, 10))
                # Листик
                pygame.draw.ellipse(screen, GREEN, (food["x"] - 8, food["y"] - food["size"] - 10, 15, 8))
                
            elif food["name"] == "Банан":
                # Концы банана
                pygame.draw.ellipse(screen, (200, 180, 0), (food["x"] - food["size"] + 5, food["y"], 10, 15))
                pygame.draw.ellipse(screen, (150, 120, 0), (food["x"] + food["size"] - 15, food["y"], 10, 15))
                
            elif food["name"] == "Пицца":
                # Кусочки пиццы
                for i in range(6):
                    angle = i * 60 * 3.14159 / 180
                    x = food["x"] + (food["size"] - 5) * pygame.math.Vector2(1, 0).rotate(i * 60).x
                    y = food["y"] + (food["size"] - 5) * pygame.math.Vector2(1, 0).rotate(i * 60).y
                    pygame.draw.line(screen, (200, 100, 50), (food["x"], food["y"]), (x, y), 3)
                
                # Начинка (пепперони)
                for i in range(4):
                    angle = i * 90 * 3.14159 / 180
                    x = food["x"] + (food["size"] // 2) * pygame.math.Vector2(1, 0).rotate(i * 90).x
                    y = food["y"] + (food["size"] // 2) * pygame.math.Vector2(1, 0).rotate(i * 90).y
                    pygame.draw.circle(screen, (200, 0, 0), (int(x), int(y)), 5)
                    
            elif food["name"] == "Молоко":
                # Этикетка на бутылке
                pygame.draw.rect(screen, BLUE, (food["x"] - 15, food["y"] - 10, 30, 20))
                pygame.draw.rect(screen, WHITE, (food["x"] - 15, food["y"] - 10, 30, 20), 2)
                milk_text = self.small_font.render("М", True, WHITE)
                screen.blit(milk_text, (food["x"] - 5, food["y"] - 5))

            # Название еды
            name_text = self.small_font.render(food["name"], True, BLACK)
            
            # Фон для названия
            name_bg = pygame.Rect(food["x"] - 30, food["y"] + food["size"] + 5, 60, 25)
            pygame.draw.rect(screen, (255, 255, 255, 180), name_bg, border_radius=5)
            pygame.draw.rect(screen, BLACK, name_bg, 1, border_radius=5)
            
            screen.blit(name_text, (food["x"] - name_text.get_width() // 2, 
                                   food["y"] + food["size"] + 10))

    def draw_hunger_info(self, screen, tamagotchi):
        """Рисует информацию о голоде тамагочи."""
        # Фон для информации о голоде
        hunger_bg = pygame.Rect(40, 40, 350, 140)
        pygame.draw.rect(screen, (0, 0, 0, 150), hunger_bg, border_radius=10)
        pygame.draw.rect(screen, (150, 100, 50), hunger_bg, 2, border_radius=10)
        
        # Заголовок
        title_text = self.font.render("Состояние голода:", True, WHITE)
        screen.blit(title_text, (50, 50))
        
        # Уровень голода
        hunger_text = self.font.render(f"Голод: {tamagotchi.data.hunger}/100", True, 
                                      GREEN if tamagotchi.data.hunger > 70 else 
                                      YELLOW if tamagotchi.data.hunger > 30 else RED)
        screen.blit(hunger_text, (50, 90))
        
        # Индикатор голода
        hunger_width = 200 * (tamagotchi.data.hunger / 100)
        hunger_bar = pygame.Rect(50, 130, hunger_width, 20)
        hunger_color = GREEN if tamagotchi.data.hunger > 70 else YELLOW if tamagotchi.data.hunger > 30 else RED
        pygame.draw.rect(screen, hunger_color, hunger_bar, border_radius=5)
        pygame.draw.rect(screen, WHITE, (50, 130, 200, 20), 2, border_radius=5)
        
        # Инструкции (скрываются после первого клика)
        if self.show_instructions:
            instructions_bg = pygame.Rect(40, 160, 350, 60)
            pygame.draw.rect(screen, (0, 0, 100, 150), instructions_bg, border_radius=10)
            pygame.draw.rect(screen, BLUE, instructions_bg, 2, border_radius=10)
            
            instructions = self.small_font.render("Кликните на еду, чтобы покормить тамагочи!", True, CYAN if 'CYAN' in globals() else (0, 255, 255))
            screen.blit(instructions, (50, 175))
        
        # Предупреждение о голоде
        if tamagotchi.data.hunger < 30:
            warning_bg = pygame.Rect(40, 220, 350, 40)
            pygame.draw.rect(screen, (255, 50, 0, 150), warning_bg, border_radius=10)
            pygame.draw.rect(screen, RED, warning_bg, 2, border_radius=10)
            
            hungry_text = self.small_font.render("Тамагочи голоден! Покормите его!", True, YELLOW)
            screen.blit(hungry_text, (50, 230))
        
        # Временная шкала голода после кормления
        if self.hunger_bar_timer:
            now = pygame.time.get_ticks()
            if now - self.hunger_bar_timer < self.hunger_bar_duration:
                bar_x, bar_y, bar_w, bar_h = 50, 270, 300, 25
                # Фон шкалы
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
                # Заливка пропорционально уровню голода
                fill_w = int(bar_w * tamagotchi.data.hunger / 100)
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_w, bar_h), border_radius=5)
                # Рамка шкалы
                pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
                
                # Текст "Голод"
                hunger_label = self.small_font.render("Голод:", True, WHITE)
                screen.blit(hunger_label, (bar_x - 60, bar_y + 5))
            else:
                self.hunger_bar_timer = 0

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в кухне."""
        # Проверяем наличие атрибутов
        if not hasattr(self, 'buttons'):
            self.buttons = []
        
        # Сначала даем базовому классу обработать навигацию стрелками
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Любой клик в комнате скрывает подсказочные надписи
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.show_hunger_text = False
            self.show_instructions = False

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем кнопку "Вернуться в зал"
            if self.buttons and self.buttons[0].rect.collidepoint(mouse_pos):
                return "hall"

            # Проверяем предметы еды
            for food in self.food_items:
                distance = ((mouse_pos[0] - food["x"]) ** 2 + (mouse_pos[1] - food["y"]) ** 2) ** 0.5
                if distance <= food["size"]:
                    if tamagotchi:
                        if tamagotchi.feed(food["hunger"]):
                            game_core.show_message(f"Вкусно! Съел {food['name']}! 🍎")
                            self.hunger_bar_timer = pygame.time.get_ticks()
                        else:
                            game_core.show_message("Не достаточно голоден!")
                    return "kitchen"

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        return "kitchen"