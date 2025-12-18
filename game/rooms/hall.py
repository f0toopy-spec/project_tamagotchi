import pygame
import os
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Hall(BaseRoom):
    """Класс главного зала (холла) в игре Tamagotchi Pou."""
    
    def __init__(self):
        """Инициализирует главный зал."""
        # Загружаем фоновое изображение главного зала
        try:
            # Получаем корневую директорию проекта
           
            hall_bg_path = 'assets\images\hall.jpg' 
            
            if os.path.exists(hall_bg_path):
                background_image = pygame.image.load(hall_bg_path).convert()
                print(f"✓ Фоновое изображение главного зала загружено: {hall_bg_path}")
            else:
                print(f"✗ Фоновое изображение не найдено: {hall_bg_path}")
                background_image = None
        except Exception as e:
            print(f"✗ Не удалось загрузить фоновое изображение: {e}")
            background_image = None
        
        # Сохраняем информацию о фоне
        self.background_image = background_image
        
        # Если есть изображение, передаем его в родительский класс
        if background_image:
            super().__init__("Hall", background_image)
            self.background_color = None
        else:
            # Если нет изображения, используем бежевый цвет
            super().__init__("Hall", (180, 160, 140))
            self.background_color = (180, 160, 140)
        
        # Инициализируем атрибуты главного зала
        self.objects = [] if not hasattr(self, 'objects') else self.objects
        self.font = pygame.font.Font(None, 36) if not hasattr(self, 'font') else self.font
        self.small_font = pygame.font.Font(None, 24) if not hasattr(self, 'small_font') else self.small_font
        
        # Настраиваем комнату
        self.setup()

    def setup(self):
        """Настраивает элементы главного зала."""
        # Кнопка статистики
        self.buttons = [
            Button(600, 500, 180, 60, "Статистика", PURPLE)  # Увеличенная кнопка
        ]

        # Объекты комнаты для декорации
        self.objects = []

    def draw(self, screen, tamagotchi):
        """Отрисовывает главный зал."""
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
            screen.fill((180, 160, 140))
        
        # Заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        # Отрисовываем объекты комнаты
        if hasattr(self, 'objects'):
            for obj in self.objects:
                obj.draw(screen)

        # Если нет фонового изображения, рисуем декоративные элементы
        if not self.background_image:
            self.draw_hall_decorations(screen)
        
        # Информационные тексты
        

        # Отрисовываем тамагочи
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.25)

        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)

        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_hall_decorations(self, screen):
        """Рисует декоративные элементы главного зала (используется если нет фонового изображения)."""
        # Мраморный пол с узором
        for i in range(10):
            for j in range(6):
                # Градиентный цвет для плиток
                base_r = 160 + (i + j) % 3 * 10
                base_g = 140 + (i + j) % 3 * 10
                base_b = 120 + (i + j) % 3 * 10
                
                # Плитка
                tile_rect = pygame.Rect(100 + i * 60, 100 + j * 70, 60, 70)
                pygame.draw.rect(screen, (base_r, base_g, base_b), tile_rect)
                
                # Текстура плитки
                for k in range(3):
                    vein_x = 100 + i * 60 + 10 + k * 15
                    vein_y1 = 100 + j * 70 + 10
                    vein_y2 = 100 + j * 70 + 60
                    pygame.draw.line(screen, (base_r + 20, base_g + 20, base_b + 20), 
                                   (vein_x, vein_y1), (vein_x, vein_y2), 2)
                
                # Обводка плитки
                pygame.draw.rect(screen, (140, 120, 100), tile_rect, 1)

        # Роскошная люстра
        # Основной каркас
        pygame.draw.circle(screen, (220, 200, 100), (SCREEN_WIDTH // 2, 80), 25)
        pygame.draw.circle(screen, (200, 180, 80), (SCREEN_WIDTH // 2, 80), 25, 3)
        
        # Металлические держатели
        pygame.draw.line(screen, (150, 150, 150), (SCREEN_WIDTH // 2 - 40, 80), 
                        (SCREEN_WIDTH // 2 + 40, 80), 4)
        pygame.draw.line(screen, (150, 150, 150), (SCREEN_WIDTH // 2, 60), 
                        (SCREEN_WIDTH // 2, 100), 4)
        
        # Подвесные элементы
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            x1 = SCREEN_WIDTH // 2 + 20 * pygame.math.Vector2(1, 0).rotate(angle).x
            y1 = 80 + 20 * pygame.math.Vector2(1, 0).rotate(angle).y
            x2 = SCREEN_WIDTH // 2 + 35 * pygame.math.Vector2(1, 0).rotate(angle).x
            y2 = 80 + 35 * pygame.math.Vector2(1, 0).rotate(angle).y
            
            pygame.draw.line(screen, (200, 180, 80), (x1, y1), (x2, y2), 2)
            pygame.draw.circle(screen, (255, 255, 200), (int(x2), int(y2)), 8)
            pygame.draw.circle(screen, (255, 255, 100), (int(x2), int(y2)), 8, 1)

        # Лестница на второй этаж (сбоку)
        # Основание лестницы
        pygame.draw.polygon(screen, (139, 69, 19), 
                          [(650, 300), (750, 300), (750, 400), (650, 350)])
        pygame.draw.polygon(screen, (120, 60, 15), 
                          [(650, 300), (750, 300), (750, 400), (650, 350)], 2)
        
        # Ступени
        for i in range(8):
            step_y = 300 + i * 12
            step_x1 = 650 + i * 5
            step_x2 = 750
            pygame.draw.line(screen, (160, 120, 80), (step_x1, step_y), (step_x2, step_y), 3)

        # Колонны по бокам
        for x in [150, 650]:
            pygame.draw.rect(screen, (200, 180, 160), (x, 100, 40, 200))
            pygame.draw.rect(screen, (180, 160, 140), (x, 100, 40, 200), 3)
            
            # Капитель колонны
            pygame.draw.rect(screen, (220, 200, 180), (x - 5, 90, 50, 20))
            pygame.draw.rect(screen, (200, 180, 160), (x - 5, 90, 50, 20), 2)
            
            # База колонны
            pygame.draw.rect(screen, (220, 200, 180), (x - 5, 300, 50, 20))
            pygame.draw.rect(screen, (200, 180, 160), (x - 5, 300, 50, 20), 2)

        # Ковер в центре
        carpet_rect = pygame.Rect(300, 350, 200, 100)
        pygame.draw.rect(screen, (150, 50, 50), carpet_rect, border_radius=10)
        pygame.draw.rect(screen, (180, 80, 80), carpet_rect, 3, border_radius=10)
        
        # Узор на ковре
        for i in range(3):
            for j in range(2):
                x = 320 + i * 60
                y = 370 + j * 40
                pygame.draw.circle(screen, (200, 150, 100), (x, y), 15)
                pygame.draw.circle(screen, (180, 130, 80), (x, y), 15, 2)

        # Двери по бокам (для навигации)
        for door_x in [100, 650]:
            pygame.draw.rect(screen, (139, 69, 19), (door_x, 200, 60, 120))
            pygame.draw.rect(screen, (120, 60, 15), (door_x, 200, 60, 120), 3)
            
            # Ручка двери
            pygame.draw.circle(screen, (200, 200, 200), (door_x + 45, 260), 6)
            pygame.draw.circle(screen, (150, 150, 150), (door_x + 45, 260), 6, 1)

    def draw_info_texts(self, screen):
        """Рисует информационные тексты в главном зале."""
        # Приветственное сообщение
        welcome_font = pygame.font.Font(None, 32)
        welcome_text = welcome_font.render("Добро пожаловать в дом Тамагочи!", True, WHITE)
        
        # Фон для текста
        welcome_bg = pygame.Rect(SCREEN_WIDTH // 2 - welcome_text.get_width() // 2 - 20, 
                               395, welcome_text.get_width() + 40, 40)
        pygame.draw.rect(screen, (0, 0, 0, 150), welcome_bg, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 150), welcome_bg, 2, border_radius=10)
        
        screen.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, 400))

        # Подсказка по навигации
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("Используйте стрелки по бокам для навигации по комнатам", True, WHITE)
        
        # Фон для подсказки
        hint_bg = pygame.Rect(SCREEN_WIDTH // 2 - hint_text.get_width() // 2 - 15, 
                           445, hint_text.get_width() + 30, 30)
        pygame.draw.rect(screen, (0, 0, 0, 150), hint_bg, border_radius=8)
        pygame.draw.rect(screen, (100, 100, 100), hint_bg, 2, border_radius=8)
        
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 450))

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в главном зале."""
        # Проверяем наличие атрибутов
        if not hasattr(self, 'buttons'):
            self.buttons = []
        
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обработка других кнопок
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == "Статистика":
                        game_core.stats_window.toggle()  # Переключаем окно статистики
                    return "hall"

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        # По умолчанию остаемся в главном зале
        return "hall"