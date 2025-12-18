import pygame
import os
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Playroom(BaseRoom):
    """Класс игровой комнаты в игре Tamagotchi Pou."""
    
    def __init__(self):
        """Инициализирует игровую комнату."""
        # Загружаем фоновое изображение игровой комнаты
        try:
            # Получаем корневую директорию проекта
            
            playroom_bg_path = 'assets\images\playroom.jpg'
            
            if os.path.exists(playroom_bg_path):
                background_image = pygame.image.load(playroom_bg_path).convert()
                print(f"✓ Фоновое изображение игровой комнаты загружено: {playroom_bg_path}")
            else:
                print(f"✗ Фоновое изображение не найдено: {playroom_bg_path}")
                background_image = None
        except Exception as e:
            print(f"✗ Не удалось загрузить фоновое изображение: {e}")
            background_image = None
        
        # Сохраняем информацию о фоне
        self.background_image = background_image
        
        # Если есть изображение, передаем его в родительский класс
        if background_image:
            super().__init__("Playroom", background_image)
            self.background_color = None
        else:
            # Если нет изображения, используем зеленый цвет
            super().__init__("Playroom", (150, 200, 100))
            self.background_color = (150, 200, 100)
        
        # Инициализируем атрибуты игровой комнаты
        self.objects = [] if not hasattr(self, 'objects') else self.objects
        self.font = pygame.font.Font(None, 36) if not hasattr(self, 'font') else self.font
        self.small_font = pygame.font.Font(None, 24) if not hasattr(self, 'small_font') else self.small_font
        
        # Настраиваем комнату
        self.setup()

    def setup(self):
        """Настраивает элементы игровой комнаты."""
        # Кнопки навигации и действий
        self.buttons = [
            Button(250, 500, 200, 50, "Играть с мячом", YELLOW),
            Button(450, 500, 150, 50, "Мини-игры", BLUE)
        ]

    def draw(self, screen, tamagotchi):
        """Отрисовывает игровую комнату."""
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
            screen.fill((150, 200, 100))
        
        # Заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Отрисовываем объекты комнаты
        if hasattr(self, 'objects'):
            for obj in self.objects:
                obj.draw(screen)

        # Если нет фонового изображения, рисуем игровые предметы
        if not self.background_image:
            self.draw_playroom_objects(screen)
        
        # Отрисовываем статус счастья
        if tamagotchi:
            self.draw_happiness_status(screen, tamagotchi)
        
        # Отрисовываем тамагочи
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_playroom_objects(self, screen):
        """Рисует игровые предметы (используется если нет фонового изображения)."""
        # Ящик с игрушками
        pygame.draw.rect(screen, (139, 69, 19), (100, 200, 100, 80))
        pygame.draw.rect(screen, (160, 120, 80), (105, 205, 90, 70))
        
        # Игрушки в ящике
        pygame.draw.circle(screen, RED, (130, 230), 15)
        pygame.draw.rect(screen, BLUE, (160, 220, 25, 25))
        pygame.draw.circle(screen, YELLOW, (180, 250), 12)

        # Мяч
        pygame.draw.circle(screen, RED, (300, 250), 30)
        pygame.draw.circle(screen, WHITE, (300, 250), 30, 2)
        # Узор на мяче
        pygame.draw.line(screen, WHITE, (280, 250), (320, 250), 2)
        pygame.draw.line(screen, WHITE, (300, 230), (300, 270), 2)

        # Кубики
        pygame.draw.rect(screen, BLUE, (400, 220, 40, 40))
        # Точки на кубике
        pygame.draw.circle(screen, WHITE, (410, 230), 4)
        pygame.draw.circle(screen, WHITE, (430, 250), 4)
        
        pygame.draw.rect(screen, GREEN, (450, 220, 40, 40))
        # Точки на кубике
        pygame.draw.circle(screen, WHITE, (460, 230), 4)
        pygame.draw.circle(screen, WHITE, (470, 240), 4)
        pygame.draw.circle(screen, WHITE, (480, 250), 4)
        
        pygame.draw.rect(screen, YELLOW, (500, 220, 40, 40))
        # Точки на кубике
        for i in range(3):
            for j in range(2):
                pygame.draw.circle(screen, WHITE, (510 + i*10, 230 + j*10), 3)

        # Горка
        pygame.draw.polygon(screen, (255, 200, 0), [(600, 300), (650, 200), (700, 300)])
        pygame.draw.line(screen, BLACK, (625, 250), (625, 300), 3)
        pygame.draw.line(screen, BLACK, (650, 200), (650, 300), 3)
        
        # Лестница горки
        for i in range(5):
            y = 280 - i * 15
            pygame.draw.line(screen, (139, 69, 19), (630, y), (670, y), 3)

        # Ковер для игр
        pygame.draw.rect(screen, (200, 150, 100), (200, 350, 400, 100), border_radius=15)
        pygame.draw.rect(screen, (180, 130, 80), (200, 350, 400, 100), 3, border_radius=15)
        
        # Узор на ковре
        for i in range(4):
            x = 220 + i * 100
            pygame.draw.circle(screen, (220, 180, 120), (x, 400), 20)
            pygame.draw.circle(screen, (180, 130, 80), (x, 400), 20, 2)

    def draw_happiness_status(self, screen, tamagotchi):
        """Рисует информацию о состоянии тамагочи."""
        # Фон для статусов
      
        
        # Счастье
        happiness_text = self.font.render(f"Счастье: {tamagotchi.data.happiness}/100", True, YELLOW)
        screen.blit(happiness_text, (50, 100))
        
        # Индикатор счастья
        happiness_width = 200 * (tamagotchi.data.happiness / 100)
        happiness_bar = pygame.Rect(50, 130, happiness_width, 15)
        happiness_color = GREEN if tamagotchi.data.happiness > 70 else YELLOW if tamagotchi.data.happiness > 30 else RED
        pygame.draw.rect(screen, happiness_color, happiness_bar, border_radius=3)
        pygame.draw.rect(screen, WHITE, (50, 130, 200, 15), 2, border_radius=3)
        
        # Энергия
        energy_text = self.font.render(f"Энергия: {tamagotchi.data.energy}/100", True, CYAN)
        screen.blit(energy_text, (50, 160))
        
        # Индикатор энергии
        energy_width = 200 * (tamagotchi.data.energy / 100)
        energy_bar = pygame.Rect(50, 190, energy_width, 15)
        energy_color = BLUE if tamagotchi.data.energy > 50 else YELLOW if tamagotchi.data.energy > 20 else RED
        pygame.draw.rect(screen, energy_color, energy_bar, border_radius=3)
        pygame.draw.rect(screen, WHITE, (50, 190, 200, 15), 2, border_radius=3)
        
        # Предупреждение о грустном состоянии
        if tamagotchi.data.happiness < 30:
            sad_bg = pygame.Rect(40, 210, 320, 30)
            pygame.draw.rect(screen, (255, 0, 0, 150), sad_bg, border_radius=5)
            sad_text = self.small_font.render("Ваш тамагочи грустит! Поиграйте с ним!", True, YELLOW)
            screen.blit(sad_text, (50, 215))

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в игровой комнате."""
        # Проверяем наличие атрибутов
        if not hasattr(self, 'buttons'):
            self.buttons = []
        
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем кнопку "Играть с мячом"
            if self.buttons and self.buttons[0].rect.collidepoint(mouse_pos):
                if tamagotchi:
                    if tamagotchi.play():
                        game_core.show_message("Поиграли с тамагочи в мяч! 🎾")
                        game_core.auto_save()
                    else:
                        game_core.show_message("Недостаточно энергии для игры!")
                return "playroom"

            # Проверяем кнопку "Мини-игры"
            if self.buttons and len(self.buttons) > 1 and self.buttons[1].rect.collidepoint(mouse_pos):
                if tamagotchi and tamagotchi.data.energy >= 20:
                    game_core.request_minigame_menu = True
                    return "playroom"
                else:
                    game_core.show_message("Недостаточно энергии для мини-игр!")
                return "playroom"

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        # По умолчанию остаемся в игровой комнате
        return "playroom"