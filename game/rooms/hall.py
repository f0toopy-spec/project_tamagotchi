import pygame
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Hall(BaseRoom):
    """Класс главного зала (холла) в игре Tamagotchi Pou.
    
    Главный зал является центральной комнатой дома, откуда осуществляется
    навигация во все остальные комнаты. Служит стартовой точкой и информационным
    центром для игрока.
    
    Особенности:
    - Центральное расположение в навигации между комнатами
    - Декоративные элементы: пол с узором, люстра
    - Приветственное сообщение и подсказки по навигации
    - Кнопка открытия статистики тамагочи
    - Стрелки навигации для перехода в соседние комнаты
    
    Важно: Внутреннее имя комнаты должно совпадать с ключом "hall"
    в словаре GameCore.rooms для корректной работы стрелочной навигации.
    """
    
    def __init__(self):
        """Инициализирует главный зал.
        
        Устанавливает бежевый цвет фона и настраивает базовые
        элементы комнаты. Имя "Hall" должно точно соответствовать
        ключу в GameCore.rooms для корректной работы навигации.
        """
        # Важно: внутреннее имя комнаты должно совпадать с ключом "hall" в GameCore.rooms,
        # чтобы стрелочная навигация возвращала корректный идентификатор комнаты.
        super().__init__("Hall", (180, 160, 140))  # Бежевый фон
        self.setup()

    def setup(self):
        """Настраивает элементы главного зала.
        
        Создает минимальный набор кнопок (только статистика) и
        инициализирует декоративные объекты комнаты.
        """
        # Только необходимые кнопки (статистика)
        self.buttons = [
            Button(600, 500, 150, 50, "Stats", PURPLE)  # Кнопка "Статистика"
        ]

        # Объекты комнаты для декорации
        self.objects = []

    def draw(self, screen, tamagotchi):
        """Отрисовывает главный зал.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            tamagotchi: Объект тамагочи для отображения в центре зала
            
        Порядок отрисовки:
        1. Фон комнаты и заголовок
        2. Декоративные элементы (узор пола, люстра)
        3. Информационные тексты (приветствие, подсказки)
        4. Тамагочи в центре комнаты
        5. Кнопки и стрелки навигации
        """
        # Отрисовываем фон комнаты без тамагочи сначала
        screen.fill(self.background_color)
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        # Отрисовываем объекты комнаты
        for obj in self.objects:
            obj.draw(screen)

        # Затем декоративные элементы холла
        
        # Узор пола (шахматный паттерн)
        for i in range(10):      # 10 плиток по горизонтали
            for j in range(6):   # 6 плиток по вертикали
                # Чередование двух оттенков бежевого для шахматного узора
                color = (160, 140, 120) if (i + j) % 2 == 0 else (170, 150, 130)
                pygame.draw.rect(screen, color, (100 + i * 60, 100 + j * 70, 60, 70))

        # Люстра
        pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH // 2, 80), 20)  # Центральная часть
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2 - 30, 80), (SCREEN_WIDTH // 2 + 30, 80), 3)  # Горизонтальная перекладина
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, 60), (SCREEN_WIDTH // 2, 100), 3)  # Вертикальная перекладина

        # Приветственное сообщение
        welcome_font = pygame.font.Font(None, 32)
        welcome_text = welcome_font.render("Welcome to Tamagotchi House!", True, WHITE)
        screen.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, 400))

        # Подсказка по навигации
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render("Use arrows on sides to navigate between rooms", True, WHITE)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 450))

        # Отрисовываем тамагочи после всех текстур (спереди, в центре комнаты)
        if tamagotchi:
            tamagotchi.draw(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)

        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в главном зале.
        
        Аргументы:
            event: Событие PyGame для обработки
            mouse_pos: Текущая позиция курсора мыши (x, y)
            tamagotchi: Объект тамагочи для взаимодействия
            game_core: Основной объект игры для доступа к общему состоянию
            
        Возвращает:
            str: Имя комнаты для перехода ("hall" или результат навигации)
            
        Механика взаимодействия:
        1. Навигация через стрелки (обрабатывается базовым классом)
        2. Клик на кнопке "Stats": открытие/закрытие окна статистики
        3. Наведение на кнопки для подсветки
        """
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обработка других кнопок
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.text == "Stats":
                        game_core.stats_window.toggle()  # Переключаем окно статистики
                    return "hall"

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        # По умолчанию остаемся в главном зале
        return "hall"