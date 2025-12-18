import pygame
import os
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Bedroom(BaseRoom):
    """Класс спальни в игре Tamagotchi Pou."""
    
    def __init__(self):
        """Инициализирует спальню."""
        # Загружаем фоновое изображение спальни
        try:
           
            bedroom_bg_path ='assets\images\cbadroom.jpg' 
            
            if os.path.exists(bedroom_bg_path):
                background_image = pygame.image.load(bedroom_bg_path).convert()
                print(f"✓ Фоновое изображение спальни загружено: {bedroom_bg_path}")
            else:
                print(f"✗ Фоновое изображение не найдено: {bedroom_bg_path}")
                background_image = None
        except Exception as e:
            print(f"✗ Не удалось загрузить фоновое изображение: {e}")
            background_image = None
        
        # Сохраняем информацию о фоне
        self.background_image = background_image
        
        # Если есть изображение, передаем его в родительский класс
        if background_image:
            super().__init__("Bedroom", background_image)
            self.background_color = None
        else:
            # Если нет изображения, используем фиолетово-синий цвет
            super().__init__("Bedroom", (100, 100, 150))
            self.background_color = (100, 100, 150)
        
        # Инициализируем атрибуты спальни
        self.objects = [] if not hasattr(self, 'objects') else self.objects
        self.font = pygame.font.Font(None, 36) if not hasattr(self, 'font') else self.font
        self.small_font = pygame.font.Font(None, 24) if not hasattr(self, 'small_font') else self.small_font
        
        # Настраиваем комнату
        self.setup()

    def setup(self):
        """Настраивает элементы спальни."""
        # Только кнопка сна
        self.buttons = [
            Button(600, 500, 150, 50, "Спать", BLUE)
        ]

    def draw(self, screen, tamagotchi):
        """Отрисовывает спальню."""
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
            screen.fill((100, 100, 150))
        
        # Заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Отрисовываем объекты комнаты
        if hasattr(self, 'objects'):
            for obj in self.objects:
                obj.draw(screen)

        # Если нет фонового изображения, рисуем мебель
        if not self.background_image:
            self.draw_bedroom_furniture(screen, tamagotchi)
        
        # Отрисовываем статус энергии
        if tamagotchi:
            self.draw_energy_status(screen, tamagotchi)
        
        # Отрисовываем тамагочи
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_bedroom_furniture(self, screen, tamagotchi):
        """Рисует мебель спальни (используется если нет фонового изображения)."""
        # Кровать
        pygame.draw.rect(screen, (139, 69, 19), (200, 200, 300, 150), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (210, 210, 280, 130), border_radius=10)
        pygame.draw.rect(screen, (200, 0, 0), (220, 220, 260, 110), border_radius=10)

        # Подушки
        pygame.draw.ellipse(screen, WHITE, (230, 230, 60, 40))
        pygame.draw.ellipse(screen, WHITE, (310, 230, 60, 40))
        pygame.draw.ellipse(screen, (240, 240, 240), (230, 230, 60, 40), 2)
        pygame.draw.ellipse(screen, (240, 240, 240), (310, 230, 60, 40), 2)

        # Ночной столик
        pygame.draw.rect(screen, (160, 120, 80), (150, 250, 60, 100))
        pygame.draw.rect(screen, (140, 100, 60), (150, 250, 60, 100), 2)
        
        # Часы на столике
        pygame.draw.circle(screen, WHITE, (180, 280), 20)
        pygame.draw.circle(screen, BLACK, (180, 280), 20, 2)
        
        # Цифры на часах (упрощенные)
        for i in range(12):
            angle = i * 30 * 3.14159 / 180
            x = 180 + 15 * pygame.math.Vector2(1, 0).rotate(i * 30).x
            y = 280 + 15 * pygame.math.Vector2(1, 0).rotate(i * 30).y
            pygame.draw.circle(screen, BLACK, (int(x), int(y)), 1)
        
        # Стрелки часов
        if tamagotchi:
            # Время зависит от состояния тамагочи
            if tamagotchi.is_sleeping:
                # Ночное время - 2:00
                hour_angle = 60  # 2 часа
                minute_angle = 0
            else:
                # Дневное время - 14:00
                hour_angle = 120  # 14 часов
                minute_angle = 0
            
            # Часовая стрелка
            hour_x = 180 + 8 * pygame.math.Vector2(1, 0).rotate(hour_angle).x
            hour_y = 280 + 8 * pygame.math.Vector2(1, 0).rotate(hour_angle).y
            pygame.draw.line(screen, BLACK, (180, 280), (hour_x, hour_y), 3)
            
            # Минутная стрелка
            minute_x = 180 + 12 * pygame.math.Vector2(1, 0).rotate(minute_angle).x
            minute_y = 280 + 12 * pygame.math.Vector2(1, 0).rotate(minute_angle).y
            pygame.draw.line(screen, BLACK, (180, 280), (minute_x, minute_y), 2)

        # Окно
        pygame.draw.rect(screen, (50, 50, 100), (500, 150, 150, 100))
        pygame.draw.rect(screen, (100, 100, 150), (500, 150, 150, 100), 5)
        pygame.draw.line(screen, (100, 100, 150), (575, 150), (575, 250), 3)
        pygame.draw.line(screen, (100, 100, 150), (500, 200), (650, 200), 3)

        # Вид из окна
        if tamagotchi and tamagotchi.is_sleeping:
            # Ночной вид
            pygame.draw.rect(screen, (30, 30, 50), (505, 155, 140, 90))
            pygame.draw.circle(screen, YELLOW, (575, 200), 15)
            
            # Звезды
            stars = [(520, 170), (540, 190), (560, 165), (590, 180), (610, 195), (630, 175)]
            for x, y in stars:
                pygame.draw.circle(screen, WHITE, (x, y), 2)
                pygame.draw.circle(screen, YELLOW, (x, y), 1)
        else:
            # Дневной вид
            pygame.draw.rect(screen, (135, 206, 235), (505, 155, 140, 90))  # Небо
            pygame.draw.circle(screen, (255, 255, 200), (575, 200), 20)  # Солнце
            
            # Облака
            pygame.draw.ellipse(screen, WHITE, (520, 170, 40, 20))
            pygame.draw.ellipse(screen, WHITE, (540, 165, 35, 25))
            pygame.draw.ellipse(screen, WHITE, (560, 175, 45, 18))

        # Коврик рядом с кроватью
        pygame.draw.ellipse(screen, (150, 100, 50), (350, 350, 100, 60))
        pygame.draw.ellipse(screen, (170, 120, 70), (350, 350, 100, 60), 3)
        
        # Узор на коврике
        pygame.draw.circle(screen, (130, 80, 40), (375, 375), 8)
        pygame.draw.circle(screen, (130, 80, 40), (425, 375), 8)

        # Шкаф
        pygame.draw.rect(screen, (120, 80, 40), (650, 200, 100, 150))
        pygame.draw.rect(screen, (100, 60, 20), (650, 200, 100, 150), 3)
        
        # Ручки шкафа
        pygame.draw.circle(screen, (200, 200, 200), (700, 250), 5)
        pygame.draw.circle(screen, (200, 200, 200), (700, 300), 5)

    def draw_energy_status(self, screen, tamagotchi):
        """Рисует информацию об энергии тамагочи."""
        # Фон для статуса
        status_bg = pygame.Rect(40, 90, 300, 100)
        pygame.draw.rect(screen, (0, 0, 0, 150), status_bg, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 150), status_bg, 2, border_radius=10)
        
        # Заголовок
        title_text = self.font.render("Состояние сна:", True, WHITE)
        screen.blit(title_text, (50, 100))
        
        # Статус сна
        if tamagotchi.is_sleeping:
            sleep_text = self.font.render("Спит ", True, CYAN if 'CYAN' in globals() else (0, 255, 255))
            screen.blit(sleep_text, (250, 100))
            
            # Индикатор сна
            
            
            
            
        else:
            awake_text = self.font.render("Не спит", True, YELLOW)
            screen.blit(awake_text, (250, 100))
        
        # Энергия
        energy_text = self.font.render(f"Энергия: {tamagotchi.data.energy}/100", True, WHITE)
        screen.blit(energy_text, (50, 140))
        
        # Индикатор энергии
        energy_width = 200 * (tamagotchi.data.energy / 100)
        energy_bar = pygame.Rect(50, 170, energy_width, 15)
        energy_color = BLUE if tamagotchi.data.energy > 50 else YELLOW if tamagotchi.data.energy > 20 else RED
        pygame.draw.rect(screen, energy_color, energy_bar, border_radius=3)
        pygame.draw.rect(screen, WHITE, (50, 170, 200, 15), 2, border_radius=3)
        
        # Предупреждение о низкой энергии
        if tamagotchi.data.energy < 30 and not tamagotchi.is_sleeping:
            low_bg = pygame.Rect(40, 210, 320, 30)
            pygame.draw.rect(screen, (255, 100, 0, 150), low_bg, border_radius=5)
            low_text = self.small_font.render("Низкая энергия! Пора спать!", True, YELLOW)
            screen.blit(low_text, (50, 215))

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в спальне."""
        # Проверяем наличие атрибутов
        if not hasattr(self, 'buttons'):
            self.buttons = []
        
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем кнопку "Спать"
            if self.buttons and self.buttons[0].rect.collidepoint(mouse_pos):
                if tamagotchi:
                    if tamagotchi.sleep():
                        game_core.show_message("Тамагочи лег спать... 😴")
                        game_core.auto_save()
                    else:
                        if tamagotchi.is_sleeping:
                            game_core.show_message("Уже спит!")
                        else:
                            game_core.show_message("Еще не устал!")
                return "bedroom"

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        # По умолчанию остаемся в спальне
        return "bedroom"