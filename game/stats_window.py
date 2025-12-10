import pygame
from entities.buttons import Button, CloseButton, TabButton
from config import *


class StatsWindow:
    """Класс окна статистики тамагочи.
    
    Окно отображает подробную статистику, достижения и историю тамагочи.
    Поддерживает вкладки и прокрутку контента.
    
    Атрибуты:
        visible: Флаг видимости окна
        current_tab: Текущая активная вкладка
        window_rect: Прямоугольник окна
        close_button: Кнопка закрытия
        tab_buttons: Кнопки переключения вкладок
        scroll_offsets: Смещения прокрутки для каждой вкладка
        max_scrolls: Максимальные значения прокрутки для каждой вкладки
    """
    
    def __init__(self):
        """Инициализирует окно статистики."""
        self.visible = False
        self.current_tab = "stats"  # Возможные значения: stats, achievements, history
        self.window_rect = pygame.Rect(100, 50, 600, 500)
        self.close_button = CloseButton(self.window_rect.right - 50, self.window_rect.y + 10)

        # Создание кнопок вкладок
        self.tab_buttons = [
            TabButton(self.window_rect.x + 20, self.window_rect.y + 60, 150, 40, "Статистика"),
            TabButton(self.window_rect.x + 190, self.window_rect.y + 60, 180, 40, "Достижения"),
            TabButton(self.window_rect.x + 380, self.window_rect.y + 60, 150, 40, "История")
        ]

        # Шрифты
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)

        # Состояние прокрутки для каждой вкладки
        self.scroll_offsets = {
            "stats": 0,
            "achievements": 0,
            "history": 0
        }
        self.max_scrolls = {
            "stats": 0,
            "achievements": 0,
            "history": 0
        }
        self.scroll_speed = 30
        self.scroll_margin = 20

    def toggle(self):
        """Переключает видимость окна."""
        self.visible = not self.visible

    def draw(self, screen, tamagotchi):
        """Отрисовывает окно статистики.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            tamagotchi: Объект тамагочи, статистику которого отображаем
        """
        if not self.visible or not tamagotchi:
            return

        # Рисуем фон окна с тенью
        pygame.draw.rect(screen, (50, 50, 50),
                         (self.window_rect.x + 5, self.window_rect.y + 5,
                          self.window_rect.width, self.window_rect.height),
                         border_radius=15)
        pygame.draw.rect(screen, WHITE, self.window_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, self.window_rect, 3, border_radius=15)

        # Заголовок окна
        title = self.title_font.render(f"Статистика {tamagotchi.data.name}", True, PURPLE)
        screen.blit(title, (self.window_rect.centerx - title.get_width() // 2, self.window_rect.y + 15))

        # Кнопка закрытия
        self.close_button.draw(screen)

        # Кнопки вкладок
        for button in self.tab_buttons:
            # Подсвечиваем активную вкладку
            if (self.current_tab == "stats" and button.text == "Статистика") or \
                    (self.current_tab == "achievements" and button.text == "Достижения") or \
                    (self.current_tab == "history" and button.text == "История"):
                button.color = BLUE
                button.hover_color = (80, 80, 255)
            else:
                button.color = GRAY
                button.hover_color = (200, 200, 200)
            button.draw(screen)

        # Отрисовка контента в зависимости от текущей вкладки с учётом прокрутки
        content_rect = pygame.Rect(
            self.window_rect.x + 20,
            self.window_rect.y + 120,
            self.window_rect.width - 40,
            self.window_rect.height - 160
        )

        current_offset = self.scroll_offsets.get(self.current_tab, 0)

        if self.current_tab == "stats":
            self.draw_stats_tab(screen, content_rect, tamagotchi, current_offset)
        elif self.current_tab == "achievements":
            self.draw_achievements_tab(screen, content_rect, tamagotchi, current_offset)
        elif self.current_tab == "history":
            self.draw_history_tab(screen, content_rect, tamagotchi, current_offset)
        
        # Показываем индикатор прокрутки, если контент не помещается
        self.draw_scroll_indicator(screen, content_rect)

    def draw_scroll_indicator(self, screen, content_rect):
        """Отрисовывает индикатор прокрутки, если контент не помещается.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            content_rect: Прямоугольник области контента
        """
        max_scroll = self.max_scrolls.get(self.current_tab, 0)
        if max_scroll > 0:
            current_offset = self.scroll_offsets.get(self.current_tab, 0)
            
            # Рисуем полосу прокрутки справа
            scrollbar_width = 10
            scrollbar_x = content_rect.right - scrollbar_width - 5
            
            # Высота ползунка пропорциональна видимой области
            thumb_height = max(20, content_rect.height * (content_rect.height / (content_rect.height + max_scroll)))
            
            # Позиция ползунка
            thumb_y = content_rect.y + (current_offset / max_scroll) * (content_rect.height - thumb_height)
            
            # Фон полосы прокрутки - используем серый цвет
            pygame.draw.rect(screen, (180, 180, 180), (scrollbar_x, content_rect.y, scrollbar_width, content_rect.height))
            
            # Ползунок - используем тёмно-серый цвет
            pygame.draw.rect(screen, (80, 80, 80), (scrollbar_x, thumb_y, scrollbar_width, thumb_height), border_radius=5)
            
            # Подсказка
            hint = self.small_font.render("Используйте колёсико мыши для прокрутки", True, (100, 100, 100))
            screen.blit(hint, (content_rect.x, content_rect.bottom + 15))

    def draw_stats_tab(self, screen, rect, tamagotchi, offset):
        """Отрисовывает вкладку со статистикой.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            rect: Прямоугольник области контента
            tamagotchi: Объект тамагочи
            offset: Смещение прокрутки
        """
        # Отрисовка детальной статистики
        stats_y = rect.y + 20 - offset

        # Раздел базовой информации
        header = self.header_font.render("Основная информация", True, BLACK)
        if rect.y <= stats_y <= rect.bottom:
            screen.blit(header, (rect.x + 10, stats_y))
        stats_y += 40

        basic_info = [
            f"Имя: {tamagotchi.data.name}",
            f"Возраст: {tamagotchi.data.age} дней",
            f"Стадия эволюции: {tamagotchi.data.evolution_stage}",
            f"Монеты: {tamagotchi.data.coins}",
            f"Создан: {tamagotchi.data.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(tamagotchi.data.created_at, 'strftime') else 'Неизвестно'}",
            f"Последнее обновление: {tamagotchi.data.last_updated.strftime('%Y-%m-%d %H:%M') if hasattr(tamagotchi.data.last_updated, 'strftime') else 'Неизвестно'}"
        ]

        for i, info in enumerate(basic_info):
            line_y = stats_y + i * 30
            if rect.y <= line_y <= rect.bottom:
                text = self.text_font.render(info, True, BLACK)
                screen.blit(text, (rect.x + 20, line_y))

        # Раздел статусных полос
        stats_y += len(basic_info) * 30 + 40

        header = self.header_font.render("Показатели", True, BLACK)
        if rect.y <= stats_y <= rect.bottom:
            screen.blit(header, (rect.x + 10, stats_y))
        stats_y += 40

        # Определяем показатели с цветами
        stats = [
            ("Голод", tamagotchi.data.hunger, RED if tamagotchi.data.hunger < 30 else GREEN),
            ("Счастье", tamagotchi.data.happiness, RED if tamagotchi.data.happiness < 30 else YELLOW),
            ("Здоровье", tamagotchi.data.health, RED if tamagotchi.data.health < 30 else GREEN),
            ("Чистота", tamagotchi.data.cleanliness, RED if tamagotchi.data.cleanliness < 30 else BLUE),
            ("Энергия", tamagotchi.data.energy, RED if tamagotchi.data.energy < 30 else PURPLE)
        ]

        bar_width = 300
        bar_height = 25

        for i, (name, value, color) in enumerate(stats):
            line_y = stats_y + i * 40
            bar_x = rect.x + 200
            bar_y = line_y

            if rect.y - bar_height <= line_y <= rect.bottom:
                # Метка
                label = self.text_font.render(f"{name}: {value}/100", True, BLACK)
                screen.blit(label, (rect.x + 20, line_y))

                # Фон полосы
                pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

                # Заливка полосы
                fill_width = int((value / 100) * bar_width)
                pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height))

                # Рамка полосы
                pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 2)

                # Процент
                percent_text = self.small_font.render(f"{value}%", True, BLACK)
                screen.blit(percent_text, (bar_x + bar_width + 10, bar_y))

        # Сообщения о статусе
        stats_y += len(stats) * 40 + 40

        status_header = self.header_font.render("Текущее состояние", True, BLACK)
        if rect.y <= stats_y <= rect.bottom:
            screen.blit(status_header, (rect.x + 10, stats_y))
        stats_y += 40

        status_messages = self.get_status_messages(tamagotchi)
        for i, message in enumerate(status_messages):
            line_y = stats_y + i * 30
            if rect.y <= line_y <= rect.bottom:
                text = self.text_font.render(f"• {message}", True, BLACK)
                screen.blit(text, (rect.x + 20, line_y))

        # Обновляем максимальную прокрутку для этой вкладки
        basic_info_height = len(basic_info) * 30
        stats_height = len(stats) * 40
        messages_height = len(status_messages) * 30
        content_height = 20 + basic_info_height + 40 + 40 + stats_height + 40 + 40 + messages_height
        self.max_scrolls["stats"] = max(0, content_height - rect.height - self.scroll_margin)

    def get_status_messages(self, tamagotchi):
        """Возвращает сообщения о текущем состоянии тамагочи.
        
        Аргументы:
            tamagotchi: Объект тамагочи
            
        Возвращает:
            list: Список сообщений о состоянии
        """
        messages = []

        if tamagotchi.data.hunger < 20:
            messages.append("Очень голоден! Срочно нужна еда!")
        elif tamagotchi.data.hunger < 50:
            messages.append("Начинает голодать")
        else:
            messages.append("Хорошо накормлен")

        if tamagotchi.data.happiness < 20:
            messages.append("Очень несчастен! Нужно внимание!")
        elif tamagotchi.data.happiness < 50:
            messages.append("Чувствует себя немного грустно")
        else:
            messages.append("Счастлив и доволен")

        if tamagotchi.data.health < 30:
            messages.append("Болен! Нужно лечение!")
        elif tamagotchi.data.health < 70:
            messages.append("Чувствует себя неважно")
        else:
            messages.append("Здоров и силён")

        if tamagotchi.data.cleanliness < 30:
            messages.append("Очень грязный! Нужно помыться!")
        elif tamagotchi.data.cleanliness < 70:
            messages.append("Мог бы быть почище")
        else:
            messages.append("Чист и свеж")

        if tamagotchi.data.energy < 20:
            messages.append("Изнурён! Нужно поспать!")
        elif tamagotchi.data.energy < 50:
            messages.append("Начинает уставать")
        else:
            messages.append("Энергичен")

        if tamagotchi.is_sleeping:
            messages.append("В данный момент спит")

        return messages

    def draw_achievements_tab(self, screen, rect, tamagotchi, offset):
        """Отрисовывает вкладку с достижениями.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            rect: Прямоугольник области контента
            tamagotchi: Объект тамагочи
            offset: Смещение прокрутки
        """
        # Заголовок достижений
        header_y = rect.y + 20 - offset
        header = self.header_font.render("Достижения", True, BLACK)
        if rect.y <= header_y <= rect.bottom:
            screen.blit(header, (rect.x + 10, header_y))

        # Определяем достижения
        achievements = [
            {
                "name": "Первый друг",
                "description": "Создать своего первого тамагочи",
                "completed": tamagotchi.data.age > 0,
                "icon": "👶"
            },
            {
                "name": "Сытый и довольный",
                "description": "Держать голод выше 80 в течение 5 дней",
                "completed": tamagotchi.data.age >= 5,
                "icon": "🍎"
            },
            {
                "name": "Счастливчик",
                "description": "Держать счастье выше 90 в течение 3 дней",
                "completed": tamagotchi.data.age >= 3,
                "icon": "😊"
            },
            {
                "name": "Чистюля",
                "description": "Поддерживать чистоту 100 в течение 24 часов",
                "completed": tamagotchi.data.age >= 1,
                "icon": "🧼"
            },
            {
                "name": "Энерджайзер",
                "description": "Пройти 10 мини-игр",
                "completed": False,  # Можно отслеживать в базе данных
                "icon": "⚡"
            },
            {
                "name": "Мастер эволюции",
                "description": "Достичь 3 стадии эволюции",
                "completed": tamagotchi.data.evolution_stage >= 3,
                "icon": "🌟"
            },
            {
                "name": "Богач",
                "description": "Накопить 1000 монет",
                "completed": tamagotchi.data.coins >= 1000,
                "icon": "💰"
            },
            {
                "name": "Ветеран",
                "description": "Прожить 30 дней",
                "completed": tamagotchi.data.age >= 30,
                "icon": "🎖️"
            }
        ]

        y_offset = rect.y + 70 - offset
        for i, achievement in enumerate(achievements):
            line_y = y_offset + i * 70
            if rect.y - 40 <= line_y <= rect.bottom:
                # Иконка и название достижения
                icon_text = self.header_font.render(achievement["icon"], True, BLACK)
                screen.blit(icon_text, (rect.x + 20, line_y))

                # Статус достижения
                status_color = GREEN if achievement["completed"] else GRAY
                status_text = "✓ Выполнено" if achievement["completed"] else "○ Заблокировано"

                name_text = self.text_font.render(achievement["name"], True, status_color)
                screen.blit(name_text, (rect.x + 60, line_y))

                desc_text = self.small_font.render(achievement["description"], True, BLACK)
                screen.blit(desc_text, (rect.x + 60, line_y + 25))

                status_label = self.small_font.render(status_text, True, status_color)
                screen.blit(status_label, (rect.x + rect.width - 120, line_y))

        # Подсчитываем высоту контента
        content_height = len(achievements) * 70
        self.max_scrolls["achievements"] = max(0, content_height - rect.height - self.scroll_margin)

    def draw_history_tab(self, screen, rect, tamagotchi, offset):
        """Отрисовывает вкладку с историей.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            rect: Прямоугольник области контента
            tamagotchi: Объект тамагочи
            offset: Смещение прокрутки
        """
        # Заголовок истории
        header_y = rect.y + 20 - offset
        header = self.header_font.render("История активности", True, BLACK)
        if rect.y <= header_y <= rect.bottom:
            screen.blit(header, (rect.x + 10, header_y))

        # Пример истории (можно расширить реальными логами из базы данных)
        history_items = [
            f"День {tamagotchi.data.age}: {tamagotchi.data.name} создан!",
            f"День {max(0, tamagotchi.data.age - 1)}: Покормлен",
            f"День {max(0, tamagotchi.data.age - 2)}: Поиграли вместе",
            f"День {max(0, tamagotchi.data.age - 3)}: Помыли",
            f"Эволюция: Достигнута стадия {tamagotchi.data.evolution_stage}",
            f"Текущие монеты: {tamagotchi.data.coins}",
            f"Общий возраст: {tamagotchi.data.age} дней"
        ]

        y_offset = rect.y + 70 - offset
        for i, item in enumerate(history_items):
            line_y = y_offset + i * 35
            if rect.y <= line_y <= rect.bottom:
                text = self.text_font.render(f"• {item}", True, BLACK)
                screen.blit(text, (rect.x + 20, line_y))

        # Полезные советы
        y_offset += len(history_items) * 35 + 40
        tips_header_y = y_offset
        tips_header = self.header_font.render("Полезные советы", True, BLUE)
        if rect.y <= tips_header_y <= rect.bottom:
            screen.blit(tips_header, (rect.x + 10, tips_header_y))
        y_offset += 40

        tips = [
            "Кормите тамагочи, когда голод низкий",
            "Играйте в мини-игры, чтобы заработать монеты",
            "Поддерживайте чистоту для бонуса к счастью",
            "Сон постепенно восстанавливает энергию",
            "Покупайте еду в магазине для лучших эффектов",
            "Регулярно проверяйте статистику тамагочи",
            "Разные виды еды имеют разные эффекты"
        ]

        for i, tip in enumerate(tips):
            line_y = y_offset + i * 30
            if rect.y <= line_y <= rect.bottom:
                text = self.text_font.render(f"💡 {tip}", True, (0, 100, 0))
                screen.blit(text, (rect.x + 20, line_y))

        # Подсчитываем высоту контента
        history_items_height = len(history_items) * 35
        tips_height = len(tips) * 30
        content_height = 20 + history_items_height + 40 + 40 + tips_height
        self.max_scrolls["history"] = max(0, content_height - rect.height - self.scroll_margin)

    def handle_events(self, event, mouse_pos):
        """Обрабатывает события окна статистики.
        
        Аргументы:
            event: Событие PyGame
            mouse_pos: Позиция курсора мыши (x, y)
            
        Возвращает:
            bool: True если событие обработано окном, иначе False
        """
        if not self.visible:
            return False

        # Проверка кнопки закрытия
        if self.close_button.handle_event(event):
            self.visible = False
            return True

        # Проверка кнопок вкладок
        for button in self.tab_buttons:
            if button.handle_event(event):
                if button.text == "Статистика":
                    self.current_tab = "stats"
                    self.scroll_offsets["stats"] = 0
                elif button.text == "Достижения":
                    self.current_tab = "achievements"
                    self.scroll_offsets["achievements"] = 0
                elif button.text == "История":
                    self.current_tab = "history"
                    self.scroll_offsets["history"] = 0
                return True

        # Прокрутка колёсиком мыши, когда курсор над окном
        if event.type == pygame.MOUSEWHEEL:
            if self.window_rect.collidepoint(mouse_pos):
                current = self.scroll_offsets.get(self.current_tab, 0)
                max_scroll = self.max_scrolls.get(self.current_tab, 0)
                # event.y > 0 = колесо вверх → прокрутка вверх (смещение уменьшается)
                current -= event.y * self.scroll_speed
                current = max(0, min(current, max_scroll))
                self.scroll_offsets[self.current_tab] = current
                return True

        # Проверка кликов внутри окна (блокировка кликов позади окна)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.window_rect.collidepoint(mouse_pos):
                return True  # Блокируем клики позади окна

        return False