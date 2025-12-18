import pygame
import os
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Bathroom(BaseRoom):
    """Класс ванной комнаты в игре Tamagotchi Pou."""
    
    def __init__(self):
        """Инициализирует ванную комнату."""
        # Загружаем фоновое изображение ванной комнаты
        try:
            # Получаем корневую директорию проекта
          
            bathroom_bg_path = 'assets\images\zawaw.jpg'
            
            if os.path.exists(bathroom_bg_path):
                background_image = pygame.image.load(bathroom_bg_path).convert()
                print(f"✓ Фоновое изображение ванной комнаты загружено: {bathroom_bg_path}")
            else:
                print(f"✗ Фоновое изображение не найдено: {bathroom_bg_path}")
                background_image = None
        except Exception as e:
            print(f"✗ Не удалось загрузить фоновое изображение: {e}")
            background_image = None
        
        # Сохраняем информацию о фоне
        self.background_image = background_image
        
        # Если есть изображение, передаем его в родительский класс
        if background_image:
            super().__init__("Bathroom", background_image)
            self.background_color = None
        else:
            # Если нет изображения, используем светло-голубой цвет
            super().__init__("Bathroom", (150, 200, 220))
            self.background_color = (150, 200, 220)
        
        # Инициализируем атрибуты ванной комнаты
        self.objects = [] if not hasattr(self, 'objects') else self.objects
        self.font = pygame.font.Font(None, 36) if not hasattr(self, 'font') else self.font
        self.small_font = pygame.font.Font(None, 24) if not hasattr(self, 'small_font') else self.small_font
        
        # Механика мытья
        self.holding_soap = False
        self.holding_water = False
        self.soap_pos = None
        self.water_pos = None
        self.soap_original_pos = (270, 360)
        self.foam_particles = []
        self.sink_pos = (330, 370)
        
        # Настраиваем комнату
        self.setup()

    def setup(self):
        """Настраивает элементы ванной комнаты."""
        # Кнопки навигации
        self.buttons = [
            Button(50, 500, 180, 60, "Вернуться в зал", GRAY)
        ]

    def draw(self, screen, tamagotchi):
        """Отрисовывает ванную комнату."""
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
            screen.fill((150, 200, 220))
        
        # Заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        # Отрисовываем объекты комнаты
        if hasattr(self, 'objects'):
            for obj in self.objects:
                obj.draw(screen)

        # Если нет фонового изображения, рисуем сантехнику
        if not self.background_image:
            self.draw_bathroom_fixtures(screen)
        
        # Отрисовываем интерактивные элементы
        self.draw_interactive_elements(screen)
        
        # Отрисовываем показатель чистоты
        if tamagotchi:
            self.draw_cleanliness_info(screen, tamagotchi)
        
        # Отрисовываем тамагочи
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            
            # Отрисовываем частицы пены на тамагочи
            for foam in self.foam_particles:
                if foam[3] > 0:
                    x, y, size, lifetime = foam
                    pygame.draw.circle(screen, WHITE, (int(x), int(y)), size)
                    pygame.draw.circle(screen, (200, 200, 255), (int(x), int(y)), size, 1)
        
        # Отрисовываем мыло, следующее за курсором
        if self.holding_soap and self.soap_pos:
            soap_x, soap_y = self.soap_pos
            self.draw_soap(screen, soap_x, soap_y)
        
        # Отрисовываем воду, следующую за курсором
        if self.holding_water and self.water_pos:
            water_x, water_y = self.water_pos
            self.draw_water_drop(screen, water_x, water_y)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_bathroom_fixtures(self, screen):
        """Рисует сантехнику ванной комнаты (используется если нет фонового изображения)."""
        # Ванна
        pygame.draw.rect(screen, (200, 200, 200), (200, 200, 200, 100), border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), (200, 200, 200, 100), 3, border_radius=10)
        
        # Вода в ванне
        pygame.draw.rect(screen, (150, 200, 255), (210, 210, 180, 80), border_radius=8)
        
        # Края ванны
        pygame.draw.rect(screen, (180, 180, 180), (200, 180, 200, 20), border_radius=5)
        
        # Смеситель для ванны
        pygame.draw.rect(screen, (200, 200, 200), (295, 170, 10, 20))
        pygame.draw.circle(screen, (220, 220, 220), (300, 170), 8)
        pygame.draw.rect(screen, (180, 180, 180), (290, 175, 20, 5))
        
        # Унитаз
        pygame.draw.ellipse(screen, WHITE, (450, 250, 80, 50))
        pygame.draw.ellipse(screen, (180, 180, 180), (450, 250, 80, 50), 3)
        pygame.draw.rect(screen, WHITE, (470, 300, 40, 60))
        pygame.draw.rect(screen, (180, 180, 180), (470, 300, 40, 60), 3)
        
        # Крышка унитаза
        pygame.draw.ellipse(screen, (220, 220, 220), (455, 245, 70, 20))
        
        # Раковина
        pygame.draw.ellipse(screen, WHITE, (300, 350, 60, 40))
        pygame.draw.ellipse(screen, (180, 180, 180), (300, 350, 60, 40), 3)
        
        # Пьедестал раковины
        pygame.draw.rect(screen, (180, 180, 180), (310, 390, 40, 30))
        pygame.draw.rect(screen, (150, 150, 150), (310, 390, 40, 30), 2)
        
        # Смеситель для раковины
        pygame.draw.rect(screen, (200, 200, 200), (327, 335, 6, 15))
        pygame.draw.circle(screen, (220, 220, 220), (330, 335), 6)
        pygame.draw.rect(screen, (180, 180, 180), (325, 340, 10, 3))
        
        # Зеркало над раковиной
        pygame.draw.rect(screen, (220, 220, 255), (280, 180, 100, 120))
        pygame.draw.rect(screen, (180, 180, 200), (280, 180, 100, 120), 3)
        
        # Рама зеркала
        pygame.draw.rect(screen, (150, 150, 180), (275, 175, 110, 130), 5, border_radius=5)
        
        # Отражение в зеркале (упрощенное)
        pygame.draw.ellipse(screen, (200, 200, 240), (300, 210, 60, 40))
        
        # Полотенцедержатель
        pygame.draw.rect(screen, (160, 140, 120), (200, 330, 80, 5))
        pygame.draw.rect(screen, (140, 120, 100), (200, 330, 80, 5), 1)
        
        # Полотенце
        pygame.draw.rect(screen, (200, 230, 255), (205, 310, 70, 20), border_radius=3)
        pygame.draw.rect(screen, (180, 210, 235), (205, 310, 70, 20), 2, border_radius=3)
        
        # Душ (сбоку)
        pygame.draw.rect(screen, (180, 180, 200), (550, 200, 60, 100))
        pygame.draw.rect(screen, (150, 150, 170), (550, 200, 60, 100), 3)
        
        # Лейка душа
        pygame.draw.circle(screen, (200, 200, 200), (580, 210), 15)
        pygame.draw.circle(screen, (180, 180, 180), (580, 210), 15, 2)
        
        # Поддон душа
        pygame.draw.rect(screen, (160, 160, 180), (560, 320, 40, 30))
        pygame.draw.rect(screen, (140, 140, 160), (560, 320, 40, 30), 2)
        
        # Плитка на стенах
        for i in range(8):
            for j in range(4):
                x = 150 + i * 60
                y = 150 + j * 50
                tile_color = (170, 190, 210) if (i + j) % 2 == 0 else (160, 180, 200)
                pygame.draw.rect(screen, tile_color, (x, y, 60, 50))
                pygame.draw.rect(screen, (140, 160, 180), (x, y, 60, 50), 1)

    def draw_interactive_elements(self, screen):
        """Рисует интерактивные элементы (мыло, воду)."""
        # Отрисовываем каплю воды на раковине, если вода не взята
        if not self.holding_water:
            sink_x, sink_y = self.sink_pos
            self.draw_water_drop(screen, sink_x, sink_y)
        
        # Отрисовываем мыло на раковине, если не удерживается
        if not self.holding_soap:
            soap_x, soap_y = self.soap_original_pos
            self.draw_soap(screen, soap_x, soap_y)

    def draw_soap(self, screen, x, y):
        """Рисует кусок мыла."""
        # Основная часть мыла
        pygame.draw.rect(screen, BLUE, (x - 12, y - 8, 24, 16), border_radius=5)
        pygame.draw.rect(screen, (100, 100, 255), (x - 12, y - 8, 24, 16), 2, border_radius=5)
        
        # Текстура мыла (пузырьки)
        for i in range(3):
            bubble_x = x - 5 + i * 5
            bubble_y = y - 3 + (i % 2) * 6
            pygame.draw.circle(screen, (150, 150, 255), (bubble_x, bubble_y), 2)
        
        # Надпись на мыле
        soap_text = self.small_font.render("M", True, WHITE)
        screen.blit(soap_text, (x - 4, y - 6))

    def draw_water_drop(self, screen, x, y):
        """Рисует каплю воды."""
        # Основная капля
        pygame.draw.circle(screen, (150, 200, 255), (int(x), int(y)), 8)
        pygame.draw.circle(screen, (100, 150, 255), (int(x), int(y)), 8, 2)
        
        # Блик на капле
        pygame.draw.circle(screen, (200, 230, 255), (int(x - 2), int(y - 2)), 3)
        
        # Падающие капли (анимация)
        drop_time = pygame.time.get_ticks() % 1000 / 1000
        if drop_time < 0.5:
            drop_y = y + 5 + drop_time * 10
            pygame.draw.circle(screen, (150, 200, 255, 150), (int(x), int(drop_y)), 4)

    def draw_cleanliness_info(self, screen, tamagotchi):
        """Рисует информацию о чистоте тамагочи."""
        # Фон для информации
        clean_bg = pygame.Rect(40, 40, 350, 140)
        pygame.draw.rect(screen, (0, 0, 0, 150), clean_bg, border_radius=10)
        pygame.draw.rect(screen, (100, 150, 200), clean_bg, 2, border_radius=10)
        
        # Заголовок
        title_text = self.font.render("Состояние чистоты:", True, WHITE)
        screen.blit(title_text, (50, 50))
        
        # Уровень чистоты
        clean_text = self.font.render(f"Чистота: {tamagotchi.data.cleanliness}/100", True, 
                                     CYAN if 'CYAN' in globals() else (0, 255, 255))
        screen.blit(clean_text, (50, 90))
        
        # Индикатор чистоты
        clean_width = 200 * (tamagotchi.data.cleanliness / 100)
        clean_bar = pygame.Rect(50, 130, clean_width, 20)
        clean_color = CYAN if tamagotchi.data.cleanliness > 70 else (100, 200, 255) if tamagotchi.data.cleanliness > 30 else (100, 100, 200)
        pygame.draw.rect(screen, clean_color, clean_bar, border_radius=5)
        pygame.draw.rect(screen, WHITE, (50, 130, 200, 20), 2, border_radius=5)
        
        # Инструкции
        instructions_bg = pygame.Rect(40, 160, 350, 80)
        pygame.draw.rect(screen, (0, 50, 100, 150), instructions_bg, border_radius=10)
        pygame.draw.rect(screen, BLUE, instructions_bg, 2, border_radius=10)
        
        inst1 = self.small_font.render("1. Возьмите мыло, потрите тамагочи", True, WHITE)
        inst2 = self.small_font.render("2. Возьмите воду, смойте пену", True, WHITE)
        screen.blit(inst1, (50, 170))
        screen.blit(inst2, (50, 195))
        
        # Предупреждение о грязи
        if tamagotchi.data.cleanliness < 30:
            warning_bg = pygame.Rect(40, 240, 350, 40)
            pygame.draw.rect(screen, (255, 100, 0, 150), warning_bg, border_radius=10)
            pygame.draw.rect(screen, (255, 150, 0), warning_bg, 2, border_radius=10)
            
            dirty_text = self.small_font.render("Тамагочи грязный! Помойте его!", True, YELLOW)
            screen.blit(dirty_text, (50, 250))

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в ванной комнате."""
        # Проверяем наличие атрибутов
        if not hasattr(self, 'buttons'):
            self.buttons = []
        
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обновляем позицию мыла/воды для следования за курсором
        if self.holding_soap:
            self.soap_pos = mouse_pos
        if self.holding_water:
            self.water_pos = mouse_pos

        # Проверяем взаимодействие с тамагочи
        if tamagotchi:
            tamagotchi_x = SCREEN_WIDTH // 2
            tamagotchi_y = SCREEN_HEIGHT // 2
            tamagotchi_radius = 50
            
            # Взаимодействие с мылом (создание пены)
            if self.holding_soap and self.soap_pos:
                soap_x, soap_y = self.soap_pos
                distance = ((soap_x - tamagotchi_x) ** 2 + (soap_y - tamagotchi_y) ** 2) ** 0.5
                if distance < tamagotchi_radius + 20:
                    import random
                    for _ in range(2):
                        foam_x = tamagotchi_x + random.randint(-40, 40)
                        foam_y = tamagotchi_y + random.randint(-40, 40)
                        foam_size = random.randint(3, 8)
                        foam_lifetime = 300
                        self.foam_particles.append([foam_x, foam_y, foam_size, foam_lifetime])
            
            # Взаимодействие с водой (смывание пены)
            if self.holding_water and self.water_pos:
                water_x, water_y = self.water_pos
                distance = ((water_x - tamagotchi_x) ** 2 + (water_y - tamagotchi_y) ** 2) ** 0.5
                if distance < tamagotchi_radius + 20:
                    # Смывание пены
                    for foam in self.foam_particles:
                        fx, fy, fsize, flife = foam
                        fdistance = ((water_x - fx) ** 2 + (water_y - fy) ** 2) ** 0.5
                        if fdistance < fsize + 15:
                            foam[3] -= 15

                    # Увеличение чистоты
                    if tamagotchi.data.cleanliness < 100:
                        tamagotchi.data.cleanliness = min(100, tamagotchi.data.cleanliness + 0.5)
                        # Автосохранение при мытье
                        if int(tamagotchi.data.cleanliness) % 20 == 0:
                            if hasattr(game_core, 'auto_save'):
                                game_core.auto_save()

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Если держим предмет - кладем его
            if self.holding_soap or self.holding_water:
                self.holding_soap = False
                self.soap_pos = None
                self.holding_water = False
                self.water_pos = self.sink_pos
                return "bathroom"

            # Проверяем кнопку "Вернуться в зал"
            if self.buttons and self.buttons[0].rect.collidepoint(mouse_pos):
                self.holding_soap = False
                self.holding_water = False
                return "hall"
            
            # Проверяем взятие мыла
            soap_x, soap_y = self.soap_original_pos
            distance_to_soap = ((mouse_pos[0] - soap_x) ** 2 + (mouse_pos[1] - soap_y) ** 2) ** 0.5

            if not self.holding_soap and distance_to_soap < 20:
                self.holding_soap = True
                self.soap_pos = mouse_pos
                game_core.show_message("Взяли мыло! Потрите тамагочи!")

            elif self.holding_soap and distance_to_soap < 20:
                self.holding_soap = False
                self.soap_pos = None
                game_core.show_message("Положили мыло.")
            
            # Проверяем взятие воды
            sink_x, sink_y = self.sink_pos
            distance_to_sink = ((mouse_pos[0] - sink_x) ** 2 + (mouse_pos[1] - sink_y) ** 2) ** 0.5

            if not self.holding_water and distance_to_sink < 30:
                self.holding_water = True
                self.water_pos = mouse_pos
                game_core.show_message("Взяли воду! Смойте пену!")

            elif self.holding_water and distance_to_sink < 30:
                self.holding_water = False
                self.water_pos = self.sink_pos
                game_core.show_message("Вернули воду.")

        # При отпускании левой кнопки мыши с предметом
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.holding_soap or self.holding_water:
                self.holding_soap = False
                self.soap_pos = None
                self.holding_water = False
                self.water_pos = self.sink_pos

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        return "bathroom"
    
    def update(self, tamagotchi):
        """Обновляет состояние частиц пены."""
        # Обновляем время жизни частиц пены
        for foam in self.foam_particles:
            foam[3] -= 1
        # Удаляем истекшие частицы пены
        self.foam_particles = [f for f in self.foam_particles if f[3] > 0]