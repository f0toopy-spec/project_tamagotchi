import pygame
import os
from entities.buttons import Button
from config import *


class BaseRoom:
    """Базовый класс для всех комнат в игре Tamagotchi Pou.
    
    Предоставляет общую функциональность для всех комнат:
    - Отображение фона и объектов комнаты
    - Навигация между комнатами с помощью стрелок
    - Управление фоновой музыкой
    - Обработка событий взаимодействия
    
    Атрибуты:
        name: Название комнаты
        background_color: Цвет фона комнаты
        buttons: Список кнопок в комнате
        objects: Список объектов в комнате
        left_room: Ссылка на левую соседнюю комнату
        right_room: Ссылка на правую соседнюю комнату
        music_playing: Флаг воспроизведения музыки
        current_music_file: Путь к текущему файлу музыки
    """
    
    def __init__(self, name, background_color):
        """Инициализирует базовые свойства комнаты.
        
        Аргументы:
            name: Название комнаты (например, "Зал", "Спальня")
            background_color: Цвет фона комнаты в формате RGB
        """
        self.name = name
        self.background_color = background_color
        self.buttons = []  # Кнопки для взаимодействия в комнате
        self.objects = []  # Объекты декора в комнате
        self.font = pygame.font.Font(None, 36)      # Основной шрифт
        self.small_font = pygame.font.Font(None, 28)  # Мелкий шрифт

        # Свойства навигации между комнатами
        self.left_room = None   # Левая соседняя комната
        self.right_room = None  # Правая соседняя комната

        # Кнопки-стрелки для навигации
        self.left_arrow = None   # Стрелка влево
        self.right_arrow = None  # Стрелка вправо
        
        # Свойства для управления музыкой
        self.music_playing = False      # Флаг воспроизведения музыки
        self.current_music_file = None  # Текущий файл музыки
        
        # Инициализация микшера PyGame, если еще не инициализирован
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def setup(self):
        """Настройка объектов и кнопок комнаты.
        
        Примечание:
            Этот метод должен быть переопределен в дочерних классах
            для настройки специфичных для комнаты объектов и кнопок.
        """
        pass

    def set_neighbors(self, left_room, right_room):
        """Устанавливает соседние комнаты для навигации.
        
        Аргументы:
            left_room: Комната слева (при переходе по левой стрелке)
            right_room: Комната справа (при переходе по правой стрелке)
            
        Создает стрелки навигации, если соседние комнаты существуют.
        """
        self.left_room = left_room
        self.right_room = right_room

        # Создаем кнопки-стрелки, если есть соседние комнаты
        if left_room:
            self.left_arrow = {
                'rect': pygame.Rect(20, SCREEN_HEIGHT // 2 - 50, 60, 100),  # Прямоугольник стрелки
                'color': (200, 200, 200, 180),      # Цвет в покое (полупрозрачный)
                'hover_color': (255, 255, 255, 220)  # Цвет при наведении
            }

        if right_room:
            self.right_arrow = {
                'rect': pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - 50, 60, 100),
                'color': (200, 200, 200, 180),
                'hover_color': (255, 255, 255, 220)
            }

    def draw(self, screen, tamagotchi):
        """Отрисовывает комнату на экране.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            tamagotchi: Объект тамагочи для отображения в комнате
            
        Порядок отрисовки:
        1. Фон комнаты
        2. Заголовок комнаты
        3. Объекты комнаты (фон)
        4. Тамагочи (передний план)
        5. Кнопки взаимодействия
        6. Стрелки навигации
        """
        # Заливаем фон комнаты
        screen.fill(self.background_color)

        # Отрисовываем заголовок комнаты
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        # Отрисовываем объекты комнаты (позади тамагочи)
        for obj in self.objects:
            obj.draw(screen)

        # Отрисовываем тамагочи (поверх объектов комнаты)
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Отрисовываем кнопки взаимодействия
        for button in self.buttons:
            button.draw(screen)

        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def draw_navigation_arrows(self, screen):
        """Отрисовывает левую и правую стрелки навигации.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            
        Стрелки отображаются с эффектами:
        - Изменение цвета при наведении
        - Подсказка с названием соседней комнаты
        - Полупрозрачный фон для лучшей читаемости
        """
        # Отрисовка левой стрелки, если существует
        if self.left_arrow:
            arrow = self.left_arrow
            # Выбираем цвет в зависимости от состояния наведения
            color = arrow['hover_color'] if arrow.get('hovered', False) else arrow['color']

            # Отрисовка фона стрелки (полупрозрачного)
            s = pygame.Surface((arrow['rect'].width, arrow['rect'].height), pygame.SRCALPHA)
            s.fill(color)
            screen.blit(s, arrow['rect'])

            # Отрисовка рамки стрелки
            pygame.draw.rect(screen, BLACK, arrow['rect'], 2, border_radius=10)

            # Отрисовка символа стрелки "←"
            arrow_font = pygame.font.Font(None, 48)
            arrow_text = arrow_font.render("←", True, BLACK)
            text_rect = arrow_text.get_rect(center=arrow['rect'].center)
            screen.blit(arrow_text, text_rect)

            # Отрисовка подсказки с названием комнаты при наведении
            if arrow.get('hovered', False) and self.left_room:
                hint_font = pygame.font.Font(None, 24)
                hint_text = hint_font.render(self.left_room.name, True, WHITE)
                hint_rect = hint_text.get_rect(
                    midbottom=(arrow['rect'].centerx, arrow['rect'].top - 8)
                )
                # Полупрозрачный фон для подсказки
                bg_rect = hint_rect.inflate(10, 6)  # Увеличиваем прямоугольник
                s_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                s_bg.fill((0, 0, 0, 160))  # Полупрозрачный черный
                screen.blit(s_bg, bg_rect.topleft)
                screen.blit(hint_text, hint_rect)

        # Отрисовка правой стрелки, если существует (аналогично левой)
        if self.right_arrow:
            arrow = self.right_arrow
            color = arrow['hover_color'] if arrow.get('hovered', False) else arrow['color']

            s = pygame.Surface((arrow['rect'].width, arrow['rect'].height), pygame.SRCALPHA)
            s.fill(color)
            screen.blit(s, arrow['rect'])

            pygame.draw.rect(screen, BLACK, arrow['rect'], 2, border_radius=10)

            arrow_font = pygame.font.Font(None, 48)
            arrow_text = arrow_font.render("→", True, BLACK)
            text_rect = arrow_text.get_rect(center=arrow['rect'].center)
            screen.blit(arrow_text, text_rect)

            if arrow.get('hovered', False) and self.right_room:
                hint_font = pygame.font.Font(None, 24)
                hint_text = hint_font.render(self.right_room.name, True, WHITE)
                hint_rect = hint_text.get_rect(
                    midbottom=(arrow['rect'].centerx, arrow['rect'].top - 8)
                )
                bg_rect = hint_rect.inflate(10, 6)
                s_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                s_bg.fill((0, 0, 0, 160))
                screen.blit(s_bg, bg_rect.topleft)
                screen.blit(hint_text, hint_rect)

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в комнате, включая навигацию.
        
        Аргументы:
            event: Событие PyGame для обработки
            mouse_pos: Текущая позиция курсора мыши (x, y)
            tamagotchi: Объект тамагочи для взаимодействия
            game_core: Основной объект игры для доступа к общему состоянию
            
        Возвращает:
            str или None: Имя комнаты для перехода или None, если переход не требуется
        """
        # Проверка наведения на стрелки
        if self.left_arrow:
            self.left_arrow['hovered'] = self.left_arrow['rect'].collidepoint(mouse_pos)

        if self.right_arrow:
            self.right_arrow['hovered'] = self.right_arrow['rect'].collidepoint(mouse_pos)

        # Проверка кликов по стрелкам
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.left_arrow and self.left_arrow['rect'].collidepoint(mouse_pos):
                # Возвращаем имя левой комнаты в нижнем регистре без пробелов
                return self.left_room.name.lower().replace(" ", "") if self.left_room else None

            if self.right_arrow and self.right_arrow['rect'].collidepoint(mouse_pos):
                # Возвращаем имя правой комнаты в нижнем регистре без пробелов
                return self.right_room.name.lower().replace(" ", "") if self.right_room else None

        return None  # Возвращаем None, если переход не требуется

    def update(self, tamagotchi):
        """Обновляет состояние комнаты.
        
        Аргументы:
            tamagotchi: Объект тамагочи для обновления состояния
            
        Примечание:
            Этот метод должен быть переопределен в дочерних классах
            для обновления специфичной для комнаты логики.
        """
        pass
    
    def play_background_music(self):
        """Загружает и воспроизводит фоновую музыку для этой комнаты.
        
        Алгоритм поиска музыки:
        1. Ищет файлы с именами, соответствующими названию комнаты
        2. Если не находит - ищет общие фоновые музыкальные файлы
        3. Поддерживает форматы: .mp3
        
        Примеры имен файлов для комнаты "Hall":
        - hall.mp3, hall_music.mp3, hall-bg.mp3, hall_bg.mp3
        """
        try:
            # Останавливаем текущую музыку, если она играет
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            # Ищем файлы музыки в директории assets/sounds
            music_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'sounds')
            music_files = []  # Список найденных файлов музыки
            
            if os.path.exists(music_dir):
                room_name_lower = self.name.lower()  # "hall", "bed room"
                room_name_no_space = room_name_lower.replace(" ", "")  # "hall", "bedroom"
                
                # Создаем список возможных шаблонов имен файлов
                patterns = [
                    room_name_lower,          # "hall"
                    room_name_no_space,       # "bedroom"
                    f"{room_name_lower}_",    # "hall_"
                    f"{room_name_no_space}_", # "bedroom_"
                    f"{room_name_lower}-",    # "hall-"
                    f"{room_name_no_space}-", # "bedroom-"
                ]
                
                # Ищем файлы, соответствующие шаблонам
                all_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3'))]
                
                for file in all_files:
                    file_lower = file.lower()
                    # Проверяем, соответствует ли файл любому шаблону
                    for pattern in patterns:
                        if file_lower.startswith(pattern):
                            music_files.append(os.path.join(music_dir, file))
                            break
                
                # Если не найдена специфичная музыка, ищем общую фоновую музыку
                if not music_files:
                    general_music = [f for f in all_files if 'background' in f.lower()]
                    if general_music:
                        music_files = [os.path.join(music_dir, f) for f in general_music]
            
            if music_files:
                # Воспроизводим первый найденный файл музыки
                self.current_music_file = music_files[0]
                pygame.mixer.music.load(music_files[0])
                pygame.mixer.music.set_volume(0.4)  # Устанавливаем громкость 40%
                pygame.mixer.music.play(-1)         # Воспроизводим в цикле
                self.music_playing = True
                print(f"🎵 Playing music for {self.name}: {os.path.basename(music_files[0])}")
            else:
                # Если файлы не найдены, продолжаем без музыки
                # Пользователь может добавить файлы музыки при желании
                self.music_playing = False
        except Exception as e:
            # Обработка ошибок загрузки музыки
            print(f"⚠️ Could not play background music for {self.name}: {e}")
            self.music_playing = False
    
    def stop_background_music(self):
        """Останавливает фоновую музыку для этой комнаты."""
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()  # Останавливаем музыку
            self.music_playing = False     # Сбрасываем флаг
            self.current_music_file = None  # Очищаем путь к файлу
        except Exception as e:
            print(f"⚠️ Could not stop background music for {self.name}: {e}")
            self.music_playing = False