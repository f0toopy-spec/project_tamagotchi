import pygame
import os
import sys

# Добавляем текущую директорию в путь для импорта модулей
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import *
from entities.buttons import Button
from entities.tamagotchi import TamagotchiEntity
from entities.items import Inventory
from database import DatabaseManager


# Определяем заглушку для мини-игры (fallback)
class DummyMiniGame:
    """Заглушка для мини-игры, если основная не доступна."""
    def __init__(self):
        self.running = False
        self.completed = False

    def start(self):
        """Запускает мини-игру."""
        self.running = True

    def handle_events(self, event): 
        """Обрабатывает события (заглушка)."""
        pass

    def update(self): 
        """Обновляет состояние (заглушка)."""
        pass

    def draw(self, screen): 
        """Отрисовывает мини-игру (заглушка)."""
        pass

    def finish(self):
        """Завершает мини-игру и возвращает награды.
        
        Возвращает:
            tuple: (coins, happiness, energy_cost, hunger_cost)
        """
        return 0, 0, 0, 0


# Пытаемся импортировать мини-игры с обработкой ошибок
MINIGAMES_AVAILABLE = False
MemoryGame = DummyMiniGame

try:
    from game.minigames.memory_game import MemoryGame
    MINIGAMES_AVAILABLE = True
    print("✅ Игра на память успешно импортирована")
except ImportError as e:
    print(f"⚠️ Игра на память недоступна: {e}")

# Импорт магазина (старая версия для совместимости)
try:
    from game.shop import Shop
    SHOP_AVAILABLE = True
    print("✅ Магазин успешно импортирован")
except ImportError as e:
    print(f"⚠️ Магазин недоступен: {e}")
    
    # Создаём заглушку для магазина
    class Shop:
        """Заглушка для магазина."""
        def __init__(self):
            self.buttons = []
            self.items = []

        def draw(self, screen, coins, inventory):
            """Отрисовывает сообщение о недоступности магазина."""
            screen.fill(WHITE)
            font = pygame.font.Font(None, 48)
            text = font.render("Магазин недоступен", True, RED)
            screen.blit(text, (300, 300))

        def handle_events(self, event, mouse_pos, tamagotchi, inventory):
            """Обрабатывает события в магазине (заглушка)."""
            return False, "Магазин недоступен"

# Импорт окна статистики
try:
    from game.stats_window import StatsWindow
    STATS_WINDOW_AVAILABLE = True
    print("✅ Окно статистики успешно импортировано")
except ImportError as e:
    print(f"⚠️ Окно статистики недоступно: {e}")
    
    # Заглушка для окна статистики
    class StatsWindow:
        """Заглушка для окна статистики."""
        def __init__(self):
            self.visible = False

        def toggle(self): 
            """Переключает видимость (заглушка)."""
            pass

        def draw(self, screen, tamagotchi): 
            """Отрисовывает окно (заглушка)."""
            pass

        def handle_events(self, event, mouse_pos): 
            """Обрабатывает события (заглушка)."""
            return False

# Импорт комнат
try:
    from game.rooms.hall import Hall
    from game.rooms.shop_room import ShopRoom
    from game.rooms.bedroom import Bedroom
    from game.rooms.playroom import Playroom
    from game.rooms.kitchen import Kitchen
    from game.rooms.bathroom import Bathroom
    ROOMS_AVAILABLE = True
    print("✅ Все комнаты успешно импортированы")
except ImportError as e:
    print(f"⚠️ Комнаты недоступны: {e}")
    ROOMS_AVAILABLE = False
    
    # Заглушки для комнат
    class Hall:
        """Заглушка для главного зала."""
        def __init__(self):
            self.visible = True
            self.name = "Главный зал"

        def draw(self, screen, tamagotchi):
            """Отрисовывает сообщение о недоступности комнат."""
            screen.fill(WHITE)
            font = pygame.font.Font(None, 36)
            text = font.render("Комнаты недоступны", True, BLACK)
            screen.blit(text, (300, 300))

        def handle_events(self, event, mouse_pos, tamagotchi, game_core):
            """Обрабатывает события (заглушка)."""
            return "hall"

        def update(self, tamagotchi): 
            """Обновляет состояние (заглушка)."""
            pass

    # Заглушки для остальных комнат
    class ShopRoom:
        pass

    class Bedroom:
        pass

    class Playroom:
        pass

    class Kitchen:
        pass

    class Bathroom:
        pass


class GameCore:
    """Основной класс игры, управляющий всеми компонентами.
    
    Атрибуты:
        screen: Поверхность PyGame для отрисовки
        clock: Таймер для управления FPS
        running: Флаг работы игрового цикла
        db: Менеджер базы данных
        current_tamagotchi: Текущий тамагочи
        current_room: Текущая комната
        rooms: Словарь комнат
        inventory: Инвентарь игрока
        current_minigame: Текущая мини-игра
        shop: Магазин
        stats_window: Окно статистики
        message: Текущее сообщение для игрока
    """
    
    def __init__(self, screen):
        """Инициализирует игровое ядро.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.db = DatabaseManager()
        self.current_tamagotchi = None
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)

        # Система комнат
        if ROOMS_AVAILABLE:
            self.current_room = "hall"
            self.rooms = {
                "hall": Hall(),
                "shop": ShopRoom(),
                "bedroom": Bedroom(),
                "playroom": Playroom(),
                "kitchen": Kitchen(),
                "bathroom": Bathroom()
            }

            # Настройка круговой навигации между комнатами
            self.setup_room_navigation()
        else:
            self.current_room = "main"
            print("⚠️ Используется резервный режим - комнаты недоступны")

        # Другие компоненты игры
        self.inventory = Inventory()
        self.current_minigame = None
        self.shop = Shop()  # Старый магазин для совместимости
        self.stats_window = StatsWindow()
        self.in_shop = False
        self.message = ""
        self.message_timer = 0
        self.dragging_food = None
        self.last_auto_save = pygame.time.get_ticks()

        # Система запросов мини-игр
        self.request_minigame_menu = False
        self.in_minigame_menu = False
        
        # Управление музыкой
        self.previous_room = None
        self.current_room_music = None

        # Создаём или загружаем тамагочи
        self.ensure_tamagotchi_exists()
        
        # Сразу запускаем музыку для зала
        if ROOMS_AVAILABLE and self.current_room in self.rooms:
            self.rooms[self.current_room].play_background_music()
            self.current_room_music = self.current_room

    def setup_room_navigation(self):
        """Настраивает круговую навигацию между комнатами."""
        # Определяем порядок комнат для круговой навигации
        room_order = ["hall", "shop", "bedroom", "playroom", "kitchen", "bathroom"]

        # Настраиваем соседей для каждой комнаты
        for i, room_name in enumerate(room_order):
            current_room = self.rooms[room_name]

            # Предыдущая комната (левая стрелка)
            left_index = (i - 1) % len(room_order)
            left_room = self.rooms[room_order[left_index]]

            # Следующая комната (правая стрелка)
            right_index = (i + 1) % len(room_order)
            right_room = self.rooms[room_order[right_index]]

            # Устанавливаем соседей
            current_room.set_neighbors(left_room, right_room)

        print("✅ Настройка навигации по комнатам завершена")
        print("   Круговой порядок:", " → ".join(room_order))

    def ensure_tamagotchi_exists(self):
        """Создаёт тамагочи по умолчанию, если не существует."""
        try:
            all_pets = self.db.get_all_tamagotchis()
            if all_pets:
                self.current_tamagotchi = TamagotchiEntity(all_pets[0])
                print(f"✅ Загружен тамагочи: {self.current_tamagotchi.data.name}")
            else:
                self.create_new_tamagotchi("Мой Пушок")
        except Exception as e:
            print(f"❌ Ошибка загрузки тамагочи: {e}")
            self.create_new_tamagotchi("Мой Пушок")

    def create_new_tamagotchi(self, name="Пушок"):
        """Создаёт нового тамагочи.
        
        Аргументы:
            name: Имя нового тамагочи
            
        Возвращает:
            bool: True если создание успешно, иначе False
        """
        try:
            from database.models import Tamagotchi
            tamagotchi_data = Tamagotchi(name=name)
            if self.db.save_tamagotchi(tamagotchi_data):
                self.current_tamagotchi = TamagotchiEntity(tamagotchi_data)
                print(f"✅ Создан новый тамагочи: {name}")
                return True
            return False
        except Exception as e:
            print(f"❌ Ошибка создания тамагочи: {e}")
            return False

    def handle_events(self):
        """Обрабатывает все события игры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Обработка клавиши ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.in_minigame_menu:
                        self.in_minigame_menu = False
                        # Возобновляем музыку комнаты при закрытии меню мини-игр
                        if ROOMS_AVAILABLE and self.current_room in self.rooms:
                            self.rooms[self.current_room].play_background_music()
                        return
                    elif self.current_minigame and self.current_minigame.running:
                        self.exit_minigame()
                        return
                    elif self.stats_window.visible:
                        self.stats_window.visible = False
                        return
                    elif ROOMS_AVAILABLE and self.current_room != "hall":
                        # Останавливаем музыку текущей комнаты
                        if self.current_room in self.rooms:
                            self.rooms[self.current_room].stop_background_music()
                        
                        self.current_room = "hall"  # Возвращаемся в главный зал
                        self.previous_room = "hall"
                        
                        # Запускаем музыку зала
                        if self.current_room in self.rooms:
                            self.rooms[self.current_room].play_background_music()
                            self.current_room_music = self.current_room
                        
                        self.show_message("Вернулись в главный зал")
                        return
                    return

                # Будим тамагочи пробелом
                if event.key == pygame.K_SPACE:
                    if self.current_tamagotchi and self.current_tamagotchi.is_sleeping:
                        if self.current_tamagotchi.wake_up():
                            self.show_message("Разбудили вашего тамагочи!")
                    return

            mouse_pos = pygame.mouse.get_pos()

            # Если открыто окно статистики, даём ему обработать событие первым
            if hasattr(self, "stats_window") and self.stats_window.visible:
                handled = self.stats_window.handle_events(event, mouse_pos)
                # Если событие обработано окном статистики, не передаём его дальше
                if handled:
                    continue

            # Обработка разных состояний игры
            if self.in_minigame_menu:
                self.handle_minigame_menu_events(event, mouse_pos)

            elif self.current_minigame and self.current_minigame.running:
                self.handle_minigame_events(event)

            elif ROOMS_AVAILABLE:
                # Обработка навигации по комнатам
                if self.current_room in self.rooms:
                    new_room = self.rooms[self.current_room].handle_events(
                        event, mouse_pos, self.current_tamagotchi, self
                    )
                    if new_room and new_room != self.current_room:
                        # Останавливаем музыку текущей комнаты перед переключением
                        if self.current_room in self.rooms:
                            self.rooms[self.current_room].stop_background_music()
                        
                        # Сохраняем предыдущую комнату
                        self.previous_room = self.current_room
                        
                        # Переключаемся на новую комнату
                        self.current_room = new_room
                        
                        # Запускаем музыку для новой комнаты
                        if self.current_room in self.rooms:
                            self.rooms[self.current_room].play_background_music()
                            self.current_room_music = self.current_room
                        
                        # Показываем сообщение о переходе
                        room_name = new_room.capitalize()
                        self.show_message(f"Вошли в {room_name}")

            elif self.in_shop:
                self.handle_shop_events(event)

    def handle_minigame_menu_events(self, event, mouse_pos):
        """Обрабатывает события в меню мини-игр.
        
        Аргументы:
            event: Событие PyGame
            mouse_pos: Позиция курсора мыши
        """
        # Обработка кликов по кнопкам
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Кнопка "Игра на память" (300, 270, 200, 50)
            if pygame.Rect(300, 270, 200, 50).collidepoint(mouse_pos):
                if MemoryGame and MemoryGame != DummyMiniGame:
                    # Останавливаем музыку комнаты перед запуском мини-игры
                    if ROOMS_AVAILABLE and self.current_room in self.rooms:
                        self.rooms[self.current_room].stop_background_music()
                    
                    self.current_minigame = MemoryGame()
                    self.current_minigame.start()
                    self.in_minigame_menu = False

            # Кнопка "Назад" (300, 410, 200, 50)
            elif pygame.Rect(300, 410, 200, 50).collidepoint(mouse_pos):
                self.in_minigame_menu = False
                # Возобновляем музыку комнаты при закрытии меню мини-игр
                if ROOMS_AVAILABLE and self.current_room in self.rooms:
                    self.rooms[self.current_room].play_background_music()

    def handle_minigame_events(self, event):
        """Обрабатывает события во время мини-игры.
        
        Аргументы:
            event: Событие PyGame
        """
        self.current_minigame.handle_events(event)

        # Проверяем, завершилась ли мини-игра сама
        if hasattr(self.current_minigame, 'completed') and self.current_minigame.completed:
            self.exit_minigame()

    def handle_shop_events(self, event):
        """Обрабатывает события в магазине (старая система).
        
        Аргументы:
            event: Событие PyGame
        """
        mouse_pos = pygame.mouse.get_pos()

        # Обработка покупок в магазине
        success, message = self.shop.handle_events(event, mouse_pos, self.current_tamagotchi, self.inventory)
        if success is not None:
            if success:
                self.show_message(message)
                self.auto_save()
            else:
                self.show_message(message)

    def exit_minigame(self):
        """Выходит из текущей мини-игры и применяет награды."""
        if self.current_minigame:
            coins, happiness, energy_cost, hunger_cost = self.current_minigame.finish()
            if self.current_tamagotchi:
                self.current_tamagotchi.data.coins += coins
                self.current_tamagotchi.data.happiness = min(100,
                                                             self.current_tamagotchi.data.happiness + happiness)
                self.current_tamagotchi.data.energy = max(0,
                                                          self.current_tamagotchi.data.energy - energy_cost)
                self.current_tamagotchi.data.hunger = max(0,
                                                          self.current_tamagotchi.data.hunger - hunger_cost)

                message = f"Заработано {coins} монет, {happiness} счастья!"
                if energy_cost > 0:
                    message += f" Потеряно {energy_cost} энергии."
                if hunger_cost > 0:
                    message += f" Потеряно {hunger_cost} сытости."
                self.show_message(message)
                self.auto_save()
            self.current_minigame = None
            
            # Возобновляем музыку комнаты после выхода из мини-игры
            if ROOMS_AVAILABLE and self.current_room in self.rooms:
                self.rooms[self.current_room].play_background_music()

    def show_message(self, message):
        """Показывает сообщение игроку.
        
        Аргументы:
            message: Текст сообщения
        """
        self.message = message
        self.message_timer = pygame.time.get_ticks()

    def auto_save(self):
        """Автосохранение игры."""
        if self.current_tamagotchi:
            self.db.save_tamagotchi(self.current_tamagotchi.data)
            print("💾 Игра автосохранена")

    def draw_minigame_menu(self, mouse_pos):
        """Отрисовывает меню выбора мини-игр.
        
        Аргументы:
            mouse_pos: Позиция курсора мыши
        """
        # Полупрозрачная подложка
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Фон меню
        menu_rect = pygame.Rect(250, 150, 300, 350)
        pygame.draw.rect(self.screen, WHITE, menu_rect, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, menu_rect, 3, border_radius=15)

        # Заголовок
        title = self.font.render("Мини-Игры", True, BLACK)
        self.screen.blit(title, (menu_rect.centerx - title.get_width() // 2, 180))

        instructions = self.small_font.render("Выберите игру!", True, BLACK)
        self.screen.blit(instructions, (menu_rect.centerx - instructions.get_width() // 2, 220))

        # Прямоугольники кнопок
        buttons = [
            {"rect": pygame.Rect(300, 270, 200, 50), "text": "Игра на память", "color": BLUE,
             "available": MemoryGame and MemoryGame != DummyMiniGame},
            {"rect": pygame.Rect(300, 340, 200, 50), "text": "Назад", "color": GRAY, "available": True}
        ]

        for button in buttons:
            # Проверка наведения
            is_hovered = button["rect"].collidepoint(mouse_pos)

            # Отрисовка кнопки
            color = button["color"] if button["available"] else (100, 100, 100)
            if is_hovered and button["available"]:
                color = tuple(min(c + 30, 255) for c in color)

            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2, border_radius=10)

            # Отрисовка текста
            text_color = WHITE if button["available"] else (150, 150, 150)
            text = self.font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

            # Отрисовка текста "Недоступно"
            if not button["available"]:
                unavailable_text = self.small_font.render("(Недоступно)", True, RED)
                self.screen.blit(unavailable_text, (button["rect"].centerx - unavailable_text.get_width() // 2,
                                                    button["rect"].bottom + 5))

        # Подсказка
        hint = self.small_font.render("Нажмите ESC для закрытия меню", True, WHITE)
        self.screen.blit(hint, (menu_rect.centerx - hint.get_width() // 2, 500))

    def draw(self):
        """Отрисовывает текущее состояние игры."""
        if self.in_minigame_menu:
            # Сначала отрисовываем текущую комнату
            if ROOMS_AVAILABLE and self.current_room in self.rooms:
                self.rooms[self.current_room].draw(self.screen, self.current_tamagotchi)

            # Затем отрисовываем меню мини-игр поверх
            mouse_pos = pygame.mouse.get_pos()
            self.draw_minigame_menu(mouse_pos)

        elif self.current_minigame and self.current_minigame.running:
            self.current_minigame.draw(self.screen)
            exit_text = self.small_font.render("Нажмите ESC для выхода из мини-игры", True, BLACK)
            self.screen.blit(exit_text, (50, SCREEN_HEIGHT - 50))

        elif ROOMS_AVAILABLE and self.current_room in self.rooms:
            # Отрисовываем текущую комнату
            self.rooms[self.current_room].draw(self.screen, self.current_tamagotchi)

            # Отрисовываем сообщение (по центру вверху)
            if self.message and pygame.time.get_ticks() - self.message_timer < 3000:
                # Создаём фон сообщения
                message_bg = pygame.Surface((self.screen.get_width(), 40), pygame.SRCALPHA)
                message_bg.fill((0, 0, 0, 150))  # Полупрозрачный чёрный
                self.screen.blit(message_bg, (0, 0))

                # Отрисовываем текст сообщения
                message_text = self.font.render(self.message, True, YELLOW)
                message_x = self.screen.get_width() // 2 - message_text.get_width() // 2
                self.screen.blit(message_text, (message_x, 10))

                # Подсказка по навигации для зала
                if self.current_room == "hall":
                    hint_font = pygame.font.Font(None, 24)
                    hint_text = hint_font.render("← Используйте стрелки для навигации по комнатам →", True, WHITE)
                    hint_x = self.screen.get_width() // 2 - hint_text.get_width() // 2
                    self.screen.blit(hint_text, (hint_x, SCREEN_HEIGHT - 40))

        else:
            # Резервный главный экран
            self.screen.fill(WHITE)
            title = self.font.render("Tamagotchi Pou", True, BLACK)
            self.screen.blit(title, (300, 50))

            if self.current_tamagotchi:
                self.current_tamagotchi.draw(self.screen, 400, 200)
                name_text = self.font.render(f"{self.current_tamagotchi.data.name}", True, BLUE)
                self.screen.blit(name_text, (350, 280))

                coins_text = self.small_font.render(f"Монеты: {self.current_tamagotchi.data.coins}", True, YELLOW)
                self.screen.blit(coins_text, (350, 320))

                # Быстрые иконки статуса
                status_y = 360
                if self.current_tamagotchi.data.hunger < 30:
                    hunger_text = self.small_font.render("🍎 Голоден!", True, RED)
                    self.screen.blit(hunger_text, (350, status_y))
                    status_y += 30
                if self.current_tamagotchi.data.happiness < 30:
                    happy_text = self.small_font.render("😢 Грустный!", True, RED)
                    self.screen.blit(happy_text, (350, status_y))
                    status_y += 30
                if self.current_tamagotchi.data.energy < 30:
                    energy_text = self.small_font.render("⚡ Устал!", True, RED)
                    self.screen.blit(energy_text, (350, status_y))
                    status_y += 30

            # Сообщение о резервном режиме
            fallback_text = self.small_font.render("Система комнат недоступна. Используется резервный режим.", True, RED)
            self.screen.blit(fallback_text, (200, 450))

            instructions = self.small_font.render("Нажмите ESC для выхода", True, BLACK)
            self.screen.blit(instructions, (350, 500))

        # Отрисовываем окно статистики (поверх всего)
        if hasattr(self, 'stats_window'):
            self.stats_window.draw(self.screen, self.current_tamagotchi)

    def update(self):
        """Обновляет состояние игры."""
        # Проверяем, был ли запрос меню мини-игр из игровой комнаты
        if self.request_minigame_menu:
            # Приостанавливаем музыку комнаты при открытии меню мини-игр
            if ROOMS_AVAILABLE and self.current_room in self.rooms:
                self.rooms[self.current_room].stop_background_music()
            self.in_minigame_menu = True
            self.request_minigame_menu = False

        # Обновляем анимации тамагочи
        if self.current_tamagotchi and hasattr(self.current_tamagotchi, 'update_animations'):
            self.current_tamagotchi.update_animations()

        if self.current_minigame and self.current_minigame.running:
            self.current_minigame.update()
            # Проверяем, завершилась ли мини-игра сама
            if hasattr(self.current_minigame, 'completed') and self.current_minigame.completed:
                self.exit_minigame()

        elif self.current_tamagotchi:
            # Обновляем статистику тамагочи
            self.current_tamagotchi.update_stats()
            if hasattr(self.current_tamagotchi, 'update_passive_stats'):
                self.current_tamagotchi.update_passive_stats()

            # Обновляем текущую комнату, если у неё есть метод update
            if ROOMS_AVAILABLE and self.current_room in self.rooms:
                if hasattr(self.rooms[self.current_room], 'update'):
                    self.rooms[self.current_room].update(self.current_tamagotchi)

            # Автосохранение каждые 2 минуты
            current_time = pygame.time.get_ticks()
            if current_time - self.last_auto_save > 120000:  # 2 минуты
                self.auto_save()
                self.last_auto_save = current_time

    def run(self):
        """Запускает главный игровой цикл."""
        print("🎮 Игра запущена!")
        print("🏠 Комнаты доступны:", ROOMS_AVAILABLE)
        print("🎮 Мини-игры доступны:", MINIGAMES_AVAILABLE)
        print("📊 Окно статистики доступно:", STATS_WINDOW_AVAILABLE)

        if ROOMS_AVAILABLE:
            print("↔️ Навигация: Используйте стрелки по бокам для перемещения по комнатам")
            print("⎋ Нажмите ESC для возврата в Главный зал")

        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

        # Сохраняем перед выходом
        if self.current_tamagotchi:
            self.db.save_tamagotchi(self.current_tamagotchi.data)
            print("💾 Игра сохранена перед выходом.")

        pygame.quit()