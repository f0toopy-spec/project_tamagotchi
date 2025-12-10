import pygame
from .base_room import BaseRoom
from entities.buttons import Button
from config import *


class Bathroom(BaseRoom):
    """Класс ванной комнаты в игре Tamagotchi Pou.
    
    Ванная комната предоставляет интерактивные возможности:
    - Подбор и использование мыла для создания пены
    - Набор воды из раковины для смывания пены
    - Визуальная индикация чистоты тамагочи
    - Интерактивная анимация процесса мытья
    
    Атрибуты:
        holding_soap: Флаг, удерживает ли игрок мыло
        holding_water: Флаг, удерживает ли игрок воду
        soap_pos: Текущая позиция мыла на экране
        water_pos: Текущая позиция воды на экране
        soap_original_pos: Исходная позиция мыла на раковине
        foam_particles: Список частиц пены на тамагочи
        sink_pos: Позиция раковины (источник воды)
    """
    
    def __init__(self):
        """Инициализирует ванную комнату.
        
        Устанавливает светло-голубой цвет фона и настраивает
        интерактивные элементы для процесса мытья.
        """
        super().__init__("Bathroom", (150, 200, 220))  # Светло-голубой фон
        self.setup()

    def setup(self):
        """Настраивает элементы ванной комнаты.
        
        Создает кнопки, устанавливает начальные позиции объектов
        и инициализирует состояние процесса мытья.
        """
        # Кнопки навигации и действий
        self.buttons = [
            Button(50, 500, 150, 50, "Back to Hall", GRAY)
        ]

        # Механика мытья
        self.holding_soap = False      # Флаг удержания мыла
        self.holding_water = False     # Флаг удержания воды
        self.soap_pos = None           # Текущая позиция мыла
        self.water_pos = None          # Текущая позиция воды
        
        # Исходная позиция мыла на раковине (слева от раковины)
        self.soap_original_pos = (270, 360)
        
        # Частицы пены на тамагочи
        # Каждая частица: [x, y, размер, время жизни]
        self.foam_particles = []
        
        # Позиция источника воды (раковина)
        self.sink_pos = (330, 370)

    def draw(self, screen, tamagotchi):
        """Отрисовывает ванную комнату.
        
        Аргументы:
            screen: Поверхность PyGame для отрисовки
            tamagotchi: Объект тамагочи для отображения и взаимодействия
            
        Порядок отрисовки:
        1. Фон комнаты и заголовок
        2. Статические объекты комнаты
        3. Показатель чистоты
        4. Тамагочи
        5. Частицы пены
        6. Интерактивные предметы (мыло, вода)
        7. Кнопки и стрелки навигации
        """
        # Отрисовываем фон комнаты без тамагочи
        screen.fill(self.background_color)
        title = self.font.render(f"{self.name}", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # Отрисовываем объекты комнаты
        for obj in self.objects:
            obj.draw(screen)

        # Отрисовываем сантехнику ванной комнаты
        
        # Ванна
        pygame.draw.rect(screen, (200, 200, 200), (200, 200, 200, 100), border_radius=10)
        pygame.draw.rect(screen, (150, 200, 255), (210, 210, 180, 80), border_radius=10)

        # Унитаз
        pygame.draw.ellipse(screen, WHITE, (450, 250, 80, 50))
        pygame.draw.rect(screen, WHITE, (470, 300, 40, 60))

        # Раковина
        pygame.draw.ellipse(screen, WHITE, (300, 350, 60, 40))
        pygame.draw.rect(screen, (180, 180, 180), (310, 390, 40, 30))

        # Отрисовываем каплю воды на раковине (источник), если вода не взята
        if not self.holding_water:
            sink_x, sink_y = self.sink_pos
            pygame.draw.circle(screen, (150, 200, 255), (int(sink_x), int(sink_y)), 6)
            pygame.draw.circle(screen, (100, 150, 255), (int(sink_x), int(sink_y)), 6, 2)
        
        # Отрисовываем мыло на раковине (если не удерживается)
        if not self.holding_soap:
            soap_x, soap_y = self.soap_original_pos
            # Мыло как маленький синий прямоугольник
            pygame.draw.rect(screen, BLUE, (soap_x - 10, soap_y - 5, 20, 10), border_radius=3)
            pygame.draw.rect(screen, (100, 100, 255), (soap_x - 10, soap_y - 5, 20, 10), 2, border_radius=3)

        # Зеркало
        pygame.draw.rect(screen, (220, 220, 255), (500, 150, 80, 100))
        pygame.draw.rect(screen, (180, 180, 200), (500, 150, 80, 100), 3)

        # Отрисовываем показатель чистоты
        if tamagotchi:
            clean_text = self.font.render(f"Cleanliness: {tamagotchi.data.cleanliness}/100", True, WHITE)
            screen.blit(clean_text, (50, 100))

            # Предупреждение о грязи
            if tamagotchi.data.cleanliness < 30:
                dirty_text = self.small_font.render("Your tamagotchi is dirty! Clean it!", True, YELLOW)
                screen.blit(dirty_text, (50, 140))
        
        # Отрисовываем тамагочи после всех текстур (спереди)
        tamagotchi_x = SCREEN_WIDTH // 2
        tamagotchi_y = SCREEN_HEIGHT // 2
        if tamagotchi:
            tamagotchi.draw(screen, tamagotchi_x, tamagotchi_y)
            
            # Отрисовываем частицы пены на тамагочи
            for foam in self.foam_particles:
                if foam[3] > 0:  # Если время жизни > 0
                    x, y, size, lifetime = foam
                    # Отрисовываем белую пенную пузырьку
                    pygame.draw.circle(screen, WHITE, (int(x), int(y)), size)
                    pygame.draw.circle(screen, (200, 200, 255), (int(x), int(y)), size, 1)
        
        # Отрисовываем мыло, следующее за курсором (если удерживается)
        if self.holding_soap and self.soap_pos:
            soap_x, soap_y = self.soap_pos
            pygame.draw.rect(screen, BLUE, (soap_x - 10, soap_y - 5, 20, 10), border_radius=3)
            pygame.draw.rect(screen, (100, 100, 255), (soap_x - 10, soap_y - 5, 20, 10), 2, border_radius=3)
        
        # Отрисовываем воду, следующую за курсором (если удерживается)
        if self.holding_water and self.water_pos:
            water_x, water_y = self.water_pos
            # Отрисовываем каплю воды
            pygame.draw.circle(screen, (150, 200, 255), (int(water_x), int(water_y)), 8)
            pygame.draw.circle(screen, (100, 150, 255), (int(water_x), int(water_y)), 8, 2)
        
        # Отрисовываем кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Отрисовываем стрелки навигации
        self.draw_navigation_arrows(screen)

    def handle_events(self, event, mouse_pos, tamagotchi, game_core):
        """Обрабатывает события в ванной комнате.
        
        Аргументы:
            event: Событие PyGame для обработки
            mouse_pos: Текущая позиция курсора мыши (x, y)
            tamagotchi: Объект тамагочи для взаимодействия
            game_core: Основной объект игры для доступа к общему состоянию
            
        Возвращает:
            str: Имя комнаты для перехода ("hall" или "bathroom")
            
        Механика взаимодействия:
        - Клик на мыле: взять/положить мыло
        - Клик на воде: взять/положить воду
        - Движение с предметом: предмет следует за курсором
        - Мыло около тамагочи: создает пену
        - Вода около тамагочи: смывает пену и повышает чистоту
        """
        # Сначала обрабатываем навигацию стрелками через базовый класс
        result = super().handle_events(event, mouse_pos, tamagotchi, game_core)
        if result:
            return result

        # Обновляем позицию мыла/воды для следования за курсором
        if self.holding_soap:
            self.soap_pos = mouse_pos
        if self.holding_water:
            self.water_pos = mouse_pos

        # Проверяем, находится ли мыло/вода рядом с тамагочи
        if tamagotchi:
            tamagotchi_x = SCREEN_WIDTH // 2
            tamagotchi_y = SCREEN_HEIGHT // 2
            tamagotchi_radius = 50  # Приблизительный размер тамагочи
            
            # Проверяем взаимодействие с мылом
            if self.holding_soap and self.soap_pos:
                soap_x, soap_y = self.soap_pos
                distance = ((soap_x - tamagotchi_x) ** 2 + (soap_y - tamagotchi_y) ** 2) ** 0.5
                if distance < tamagotchi_radius + 20:
                    # Добавляем частицы пены
                    import random
                    for _ in range(2):
                        foam_x = tamagotchi_x + random.randint(-40, 40)
                        foam_y = tamagotchi_y + random.randint(-40, 40)
                        foam_size = random.randint(3, 8)
                        foam_lifetime = 300  # 5 секунд при 60 FPS
                        self.foam_particles.append([foam_x, foam_y, foam_size, foam_lifetime])
            
            # Проверяем взаимодействие с водой
            if self.holding_water and self.water_pos:
                water_x, water_y = self.water_pos
                distance = ((water_x - tamagotchi_x) ** 2 + (water_y - tamagotchi_y) ** 2) ** 0.5
                if distance < tamagotchi_radius + 20:
                    # Смывание: постепенно удаляем близлежащие пузырьки пены
                    for foam in self.foam_particles:
                        fx, fy, fsize, flife = foam
                        fdistance = ((water_x - fx) ** 2 + (water_y - fy) ** 2) ** 0.5
                        # Если вода проходит над пузырьком, уменьшаем его время жизни быстрее
                        if fdistance < fsize + 15:
                            foam[3] -= 15  # Ускоряем исчезновение этого пузырька

                    # Постепенно увеличиваем чистоту во время мытья
                    if tamagotchi.data.cleanliness < 100:
                        tamagotchi.data.cleanliness = min(100, tamagotchi.data.cleanliness + 0.5)

        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Если мы удерживаем какой-либо предмет (мыло или воду), кладем все по левому клику
            if self.holding_soap or self.holding_water:
                self.holding_soap = False
                self.soap_pos = None  # Мыло отрисовывается в исходной позиции, когда не удерживается
                self.holding_water = False
                self.water_pos = self.sink_pos  # Визуально возвращаем каплю воды к крану
                # После сброса предметов этот клик только кладет их, больше ничего не делает
                return "bathroom"

            # Проверяем кнопку "Назад"
            if self.buttons[0].rect.collidepoint(mouse_pos):
                # Сбрасываем состояние мытья
                self.holding_soap = False
                self.holding_water = False
                return "hall"
            
            # Проверяем взятие/возврат мыла
            soap_x, soap_y = self.soap_original_pos
            distance_to_soap = ((mouse_pos[0] - soap_x) ** 2 + (mouse_pos[1] - soap_y) ** 2) ** 0.5

            # Берем мыло с раковины
            if not self.holding_soap and distance_to_soap < 20:
                self.holding_soap = True
                self.soap_pos = mouse_pos
                game_core.show_message("Picked up soap! Rub it on your tamagotchi!")

            # Возвращаем мыло на раковину, если уже держим его
            elif self.holding_soap and distance_to_soap < 20:
                self.holding_soap = False
                self.soap_pos = None
                game_core.show_message("Put the soap back.")
            
            # Проверяем взятие/возврат воды у раковины
            elif True:
                sink_x, sink_y = self.sink_pos
                distance_to_sink = ((mouse_pos[0] - sink_x) ** 2 + (mouse_pos[1] - sink_y) ** 2) ** 0.5

                # Берем воду из раковины
                if not self.holding_water and distance_to_sink < 30:
                    self.holding_water = True
                    self.water_pos = mouse_pos
                    game_core.show_message("Got water! Rinse the foam off!")

                # Возвращаем воду на раковину, если уже держим ее
                elif self.holding_water and distance_to_sink < 30:
                    self.holding_water = False
                    self.water_pos = self.sink_pos
                    game_core.show_message("Put the water back.")

        # Дополнительно: если игрок отпускает левую кнопку мыши с предметом в руке - тоже сбрасываем
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.holding_soap or self.holding_water:
                self.holding_soap = False
                self.soap_pos = None
                self.holding_water = False
                self.water_pos = self.sink_pos

        # Обновляем состояние наведения на кнопки
        for button in self.buttons:
            button.check_hover(mouse_pos)

        # По умолчанию остаемся в ванной, пока не нажмут кнопку/стрелку
        return "bathroom"
    
    def update(self, tamagotchi):
        """Обновляет состояние частиц пены и процесса мытья.
        
        Аргументы:
            tamagotchi: Объект тамагочи для обновления состояния
            
        Уменьшает время жизни частиц пены и удаляет те,
        у которых время жизни истекло.
        """
        # Обновляем время жизни частиц пены
        for foam in self.foam_particles:
            foam[3] -= 1  # Уменьшаем время жизни
        # Удаляем истекшие частицы пены
        self.foam_particles = [f for f in self.foam_particles if f[3] > 0]