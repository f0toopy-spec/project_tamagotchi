import pygame
from config import *


class Button:
    """Класс кнопки с поддержкой hover-эффекта и кликов.
    
    Предоставляет универсальную кнопку для пользовательского интерфейса
    с визуальными эффектами при наведении и нажатии.
    """
    
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=(100, 100, 255), text_color=WHITE):
        """Инициализирует кнопку с заданными параметрами.
        
        Args:
            x: X-координата левого верхнего угла кнопки.
            y: Y-координата левого верхнего угла кнопки.
            width: Ширина кнопки в пикселях.
            height: Высота кнопки в пикселях.
            text: Текст, отображаемый на кнопке.
            color: Основной цвет кнопки (по умолчанию BLUE).
            hover_color: Цвет кнопки при наведении курсора.
            text_color: Цвет текста на кнопке (по умолчанию WHITE).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 32)
        self.clicked = False

    def draw(self, screen):
        """Отрисовывает кнопку на указанной поверхности.
        
        Args:
            screen: Поверхность PyGame для отрисовки.
        """
        # Выбор цвета: hover_color если курсор над кнопкой, иначе обычный цвет
        color = self.hover_color if self.is_hovered else self.color

        # Отрисовка кнопки с эффектом тени при нажатии
        if self.clicked:
            # Тень (темнее, смещена вправо-вниз)
            pygame.draw.rect(screen, (color[0] // 2, color[1] // 2, color[2] // 2),
                             (self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height),
                             border_radius=10)
            # Основная кнопка
            pygame.draw.rect(screen, color,
                             (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
                             border_radius=10)
        else:
            # Обычная кнопка без эффекта нажатия
            pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Обводка кнопки
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)

        # Отрисовка текста
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        """Проверяет, находится ли курсор над кнопкой.
        
        Args:
            pos: Кортеж (x, y) с координатами курсора.
            
        Returns:
            bool: True если курсор над кнопкой, False в противном случае.
        """
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, event):
        """Проверяет, была ли кнопка нажата в данном событии.
        
        Args:
            event: Событие PyGame для обработки.
            
        Returns:
            bool: True если кнопка была нажата, False в противном случае.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
        return False

    def handle_event(self, event):
        """Обрабатывает события мыши для этой кнопки.
        
        Args:
            event: Событие PyGame для обработки.
            
        Returns:
            bool: True если кнопка была нажата и отпущена (клик), False в противном случае.
        """
        if event.type == pygame.MOUSEMOTION:
            # Обновление состояния hover при движении мыши
            self.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Начало нажатия
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Завершение нажатия (клик)
            if self.clicked and self.rect.collidepoint(event.pos):
                self.clicked = False
                return True
            self.clicked = False
        return False


class CloseButton(Button):
    """Специальная кнопка для закрытия окон.
    
    Наследуется от Button и предоставляет стилизованную кнопку закрытия.
    """
    
    def __init__(self, x, y):
        """Инициализирует кнопку закрытия.
        
        Args:
            x: X-координата левого верхнего угла кнопки.
            y: Y-координата левого верхнего угла кнопки.
        """
        super().__init__(x, y, 40, 40, "X", RED, (255, 100, 100))


class TabButton(Button):
    """Кнопка для вкладок в окнах статистики.
    
    Наследуется от Button с настройками для использования во вкладках.
    """
    
    def __init__(self, x, y, width, height, text):
        """Инициализирует кнопку вкладки.
        
        Args:
            x: X-координата левого верхнего угла кнопки.
            y: Y-координата левого верхнего угла кнопки.
            width: Ширина кнопки в пикселях.
            height: Высота кнопки в пикселях.
            text: Текст, отображаемый на вкладке.
        """
        super().__init__(x, y, width, height, text, GRAY, (200, 200, 200), BLACK)
        # Используем меньший шрифт для вкладок, чтобы текст помещался
        self.font = pygame.font.Font(None, 28)