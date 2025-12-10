"""
Модуль утилит для анимаций в игре Tamagotchi Pou.

Содержит классы для работы с анимациями и спрайт-листами,
что позволяет создавать плавные анимации персонажей и объектов.
"""

import pygame


class Animation:
    """Класс для управления анимацией с использованием последовательности кадров.
    
    Позволяет создавать циклические анимации с заданной скоростью смены кадров.
    Подходит для анимации персонажей, эффектов и интерактивных элементов.
    
    Атрибуты:
        frames: Список кадров анимации (поверхности PyGame)
        frame_duration: Длительность отображения одного кадра в миллисекундах
        current_frame: Индекс текущего отображаемого кадра
        last_update: Время последнего обновления кадра (в миллисекундах)
    """
    
    def __init__(self, frames, frame_duration=100):
        """Инициализирует анимацию.
        
        Аргументы:
            frames: Список поверхностей PyGame, представляющих кадры анимации
            frame_duration: Длительность отображения одного кадра в миллисекундах (по умолчанию 100)
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """Обновляет текущий кадр анимации.
        
        Проверяет, прошло ли достаточно времени с последнего обновления,
        и переключает на следующий кадр, если это так.
        Анимация зацикливается: после последнего кадра переходит к первому.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            # Переходим к следующему кадру с зацикливанием
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self):
        """Возвращает текущий кадр анимации.
        
        Возвращает:
            pygame.Surface: Текущий кадр анимации для отрисовки
        """
        return self.frames[self.current_frame]


class SpriteSheet:
    """Класс для работы со спрайт-листами (spritesheet).
    
    Спрайт-лист - это одно изображение, содержащее несколько кадров анимации,
    расположенных в виде сетки. Этот класс позволяет загружать и разделять
    спрайт-лист на отдельные кадры для использования в анимациях.
    
    Атрибуты:
        sheet: Исходное изображение спрайт-листа
        frame_width: Ширина одного кадра в пикселях
        frame_height: Высота одного кадра в пикселях
        frames: Список извлеченных кадров из спрайт-листа
    """
    
    def __init__(self, image, frame_width, frame_height):
        """Инициализирует спрайт-лист.
        
        Аргументы:
            image: Изображение спрайт-листа (pygame.Surface)
            frame_width: Ширина одного кадра в пикселях
            frame_height: Высота одного кадра в пикселях
        """
        self.sheet = image
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = self.load_frames()

    def load_frames(self):
        """Загружает все кадры из спрайт-листа.
        
        Разделяет изображение спрайт-листа на отдельные кадры
        на основе заданных размеров кадра.
        
        Возвращает:
            list: Список поверхностей PyGame, представляющих отдельные кадры
            
        
        """
        frames = []
        sheet_rect = self.sheet.get_rect()

        # Проходим по спрайт-листу в виде сетки
        for y in range(0, sheet_rect.height, self.frame_height):
            for x in range(0, sheet_rect.width, self.frame_width):
                # Создаем прямоугольник для текущего кадра
                rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
                # Извлекаем кадр из спрайт-листа
                frame = self.sheet.subsurface(rect)
                frames.append(frame)

        return frames