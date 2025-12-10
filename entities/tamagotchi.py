import pygame
from config import *


class TamagotchiEntity:
    """Графическая и игровая сущность тамагочи.
    
    Управляет состоянием, логикой и отрисовкой виртуального питомца.
    Обрабатывает взаимодействия, анимации и игровую механику.
    """
    
    def __init__(self, tamagotchi_data):
        """Инициализирует графическую сущность тамагочи.
        
        Args:
            tamagotchi_data: Объект Tamagotchi с данными состояния питомца.
        """
        self.data = tamagotchi_data
        self.last_update_time = pygame.time.get_ticks()
        # Пороги эволюции в днях: ребенок (0+), подросток (7+), взрослый (14+)
        self.evolution_thresholds = [0, 7, 14]
        # Цвета для каждой стадии эволюции
        self.evolution_colors = [GREEN, BLUE, PURPLE]
        self.is_sleeping = False
        self.sleep_start_time = 0
        self.last_energy_regen = pygame.time.get_ticks()

        # Инициализация шрифтов для отображения текста
        self.small_font = pygame.font.Font(None, 24)

    def update_stats(self):
        """Обновляет статистику тамагочи на основе прошедшего времени.
        
        Реализует постепенную деградацию характеристик и другие временные эффекты.
        """
        current_time = pygame.time.get_ticks()

        # Постепенное снижение характеристик (каждые 30 секунд)
        if current_time - self.last_update_time > 30000:
            self.data.hunger = max(0, self.data.hunger - 5)
            self.data.happiness = max(0, self.data.happiness - 3)
            self.data.cleanliness = max(0, self.data.cleanliness - 2)
            # Энергия не должна снижаться во время сна
            if not self.is_sleeping:
                self.data.energy = max(0, self.data.energy - 4)

            # Прогрессия возраста (1 день = 5 минут игрового времени)
            if current_time - self.last_update_time > 300000:  # 5 минут
                self.data.age += 1
                self.check_evolution()

            # Снижение здоровья на основе низких характеристик
            health_penalty = 0
            if self.data.hunger < 20:
                health_penalty += 2
            if self.data.happiness < 20:
                health_penalty += 2
            if self.data.cleanliness < 20:
                health_penalty += 1
            if self.data.energy < 10:
                health_penalty += 1

            self.data.health = max(0, self.data.health - health_penalty)

            self.last_update_time = current_time

        # Постепенная регенерация энергии во время сна (каждые 10 секунд)
        if self.is_sleeping and current_time - self.last_energy_regen > 10000:
            if self.data.energy < 100:
                self.data.energy = min(100, self.data.energy + 15)  # +15 энергии каждые 10 секунд
                self.last_energy_regen = current_time

                # Небольшой бонус к счастью от хорошего сна
                if current_time - self.sleep_start_time > 30000:  # После 30 секунд сна
                    self.data.happiness = min(100, self.data.happiness + 2)

        # Автоматическое пробуждение при полной энергии
        if self.is_sleeping and self.data.energy >= 100:
            self.is_sleeping = False

    def check_evolution(self):
        """Проверяет, достиг ли тамагочи порога для эволюции.
        
        Returns:
            bool: True если произошла эволюция, False в противном случае.
        """
        current_stage = self.data.evolution_stage
        if current_stage < len(self.evolution_thresholds):
            if self.data.age >= self.evolution_thresholds[current_stage]:
                self.data.evolution_stage += 1
                print(f"🎉 {self.data.name} evolved to stage {self.data.evolution_stage}!")
                return True
        return False

    def feed(self, food_value=20):
        """Кормит тамагочи, увеличивая голод и другие характеристики.
        
        Args:
            food_value: Количество, на которое увеличивается голод.
            
        Returns:
            bool: True если кормление успешно, False если голод уже максимален.
        """
        if self.data.hunger < 100:
            old_hunger = self.data.hunger
            self.data.hunger = min(100, self.data.hunger + food_value)

            # Увеличение счастья при кормлении голодного тамагочи
            if old_hunger < 50:
                self.data.happiness = min(100, self.data.happiness + 5)

            # Небольшой бонус энергии от еды
            if food_value >= 30:  # Существенная пища дает больше энергии
                self.data.energy = min(100, self.data.energy + 5)
            else:
                self.data.energy = min(100, self.data.energy + 2)

            return True
        return False

    def play(self, happiness_boost=15, energy_cost=10):
        """Играет с тамагочи, увеличивая счастье за счет энергии.
        
        Args:
            happiness_boost: Бонус к счастью от игры.
            energy_cost: Стоимость энергии за игру.
            
        Returns:
            bool: True если игра успешна, False если недостаточно энергии.
        """
        if self.data.happiness < 100 and self.data.energy > energy_cost:
            old_happiness = self.data.happiness
            self.data.happiness = min(100, self.data.happiness + happiness_boost)
            self.data.energy = max(0, self.data.energy - energy_cost)

            # Увеличение голода от игры
            self.data.hunger = max(0, self.data.hunger - 3)

            # Больший бонус счастья если энергия была высокой
            if self.data.energy > 70:
                self.data.happiness = min(100, self.data.happiness + 5)

            return True
        return False

    def clean(self):
        """Чистит тамагочи, восстанавливая чистоту до максимума.
        
        Returns:
            bool: True если чистка успешна, False если уже чисто.
        """
        if self.data.cleanliness < 100:
            old_cleanliness = self.data.cleanliness
            self.data.cleanliness = 100

            # Бонус счастья от чистоты
            cleanliness_improvement = 100 - old_cleanliness
            happiness_boost = min(15, cleanliness_improvement // 10)
            self.data.happiness = min(100, self.data.happiness + happiness_boost)

            # Небольшая трата энергии на чистку
            self.data.energy = max(0, self.data.energy - 5)

            return True
        return False

    def sleep(self):
        """Отправляет тамагочи спать для восстановления энергии.
        
        Returns:
            bool: True если успешно уснул, False если уже спит или энергия полная.
        """
        if not self.is_sleeping and self.data.energy < 100:
            self.is_sleeping = True
            self.sleep_start_time = pygame.time.get_ticks()
            self.last_energy_regen = pygame.time.get_ticks()

            # Начальный бонус комфорта при начале сна
            self.data.happiness = min(100, self.data.happiness + 5)
            return True
        return False

    def wake_up(self):
        """Будит тамагочи ото сна.
        
        Returns:
            bool: True если успешно проснулся, False если не спал.
        """
        if self.is_sleeping:
            self.is_sleeping = False
            # Небольшой штраф к счастью если разбудить слишком рано
            sleep_duration = (pygame.time.get_ticks() - self.sleep_start_time) // 1000
            if sleep_duration < 60:  # Меньше 1 минуты
                self.data.happiness = max(0, self.data.happiness - 10)
            return True
        return False

    def heal(self, health_boost=30):
        """Лечит тамагочи, восстанавливая здоровье.
        
        Args:
            health_boost: Количество восстанавливаемого здоровья.
            
        Returns:
            bool: True если лечение успешно, False если здоровье уже полное.
        """
        if self.data.health < 100:
            old_health = self.data.health
            self.data.health = min(100, self.data.health + health_boost)

            # Бонус счастья от улучшения самочувствия
            health_improvement = self.data.health - old_health
            self.data.happiness = min(100, self.data.happiness + (health_improvement // 5))

            # Небольшая трата энергии на процесс исцеления
            self.data.energy = max(0, self.data.energy - 8)

            return True
        return False

    def check_food_collision(self, food_pos, food_size):
        """Проверяет, достаточно ли близко еда для поедания.
        
        Args:
            food_pos: Позиция еды (x, y).
            food_size: Размер еды (радиус).
            
        Returns:
            bool: True если еда достаточно близко для поедания.
        """
        tamagotchi_x, tamagotchi_y = 200, 200  # Позиция тамагочи
        distance = ((food_pos[0] - tamagotchi_x) ** 2 + 
                    (food_pos[1] - tamagotchi_y) ** 2) ** 0.5
        return distance <= (50 + food_size)  # Радиус тамагочи + размер еды

    def eat_food(self, food_item):
        """Применяет эффекты еды к тамагочи.
        
        Args:
            food_item: Объект FoodItem с эффектами еды.
            
        Returns:
            bool: True если еда успешно съедена.
        """
        old_hunger = self.data.hunger
        old_happiness = self.data.happiness
        old_energy = self.data.energy

        # Применение эффектов еды
        self.data.hunger = min(100, self.data.hunger + food_item.hunger_value)
        self.data.happiness = min(100, self.data.happiness + food_item.happiness_boost)
        self.data.energy = min(100, self.data.energy + food_item.energy_boost)

        # Дополнительное счастье если очень голоден
        if old_hunger < 30:
            self.data.happiness = min(100, self.data.happiness + 10)

        # Создание анимации поедания
        self.eating_animation = True
        self.eating_timer = pygame.time.get_ticks()

        return True

    def update_animations(self):
        """Обновляет анимации (поедание и другие)."""
        current_time = pygame.time.get_ticks()

        # Анимация поедания
        if hasattr(self, 'eating_animation') and self.eating_animation:
            if current_time - self.eating_timer > 1000:  # 1 секунда анимации
                self.eating_animation = False

    def draw_eating_effect(self, screen, x, y):
        """Отрисовывает анимацию поедания.
        
        Args:
            screen: Поверхность PyGame для отрисовки.
            x: X-координата тамагочи.
            y: Y-координата тамагочи.
        """
        if hasattr(self, 'eating_animation') and self.eating_animation:
            # Отрисовка сердечек при поедании
            for i in range(3):
                heart_x = x - 20 + i * 20
                heart_y = y - 60
                heart_color = (255, 0, 0)  # Красное сердечко
                pygame.draw.polygon(screen, heart_color, [
                    (heart_x, heart_y + 5),
                    (heart_x + 5, heart_y),
                    (heart_x + 10, heart_y + 5),
                    (heart_x + 5, heart_y + 10)
                ])

    def update_passive_stats(self):
        """Обновляет пассивные характеристики, симулируя взаимодействия между ними."""
        current_time = pygame.time.get_ticks()

        # Высокая чистота медленно увеличивает счастье (каждые 2 минуты)
        if current_time - getattr(self, 'last_passive_update', 0) > 120000:
            if self.data.cleanliness > 80:
                self.data.happiness = min(100, self.data.happiness + 2)
            elif self.data.cleanliness < 30:
                self.data.happiness = max(0, self.data.happiness - 1)

            # Низкий голод быстрее снижает энергию (но не во время сна)
            if self.data.hunger < 20 and not self.is_sleeping:
                self.data.energy = max(0, self.data.energy - 2)

            # Высокое счастье дает небольшую регенерацию энергии
            if self.data.happiness > 80 and self.data.energy < 100:
                self.data.energy = min(100, self.data.energy + 1)

            self.last_passive_update = current_time

    def draw(self, screen, x, y):
        """Отрисовывает тамагочи на экране.
        
        Args:
            screen: Поверхность PyGame для отрисовки.
            x: X-координата для отрисовки.
            y: Y-координата для отрисовки.
        """
        # Получение цвета на основе стадии эволюции
        stage_index = min(self.data.evolution_stage - 1, len(self.evolution_colors) - 1)
        color = self.evolution_colors[stage_index]

        # Отрисовка индикатора сна
        if self.is_sleeping:
            # Анимация ZZZ
            for i in range(3):
                z_x = x + 40 + i * 20
                z_y = y - 40 - i * 5
                z_text = self.small_font.render("z", True, BLUE)
                screen.blit(z_text, (z_x, z_y))

        # Отрисовка тела на основе стадии эволюции
        if self.data.evolution_stage == 1:
            # Стадия ребенка - маленький круг
            pygame.draw.circle(screen, color, (x, y), 40)
        elif self.data.evolution_stage == 2:
            # Стадия подростка - овал
            pygame.draw.ellipse(screen, color, (x - 50, y - 40, 100, 80))
        else:
            # Стадия взрослого - крупнее с деталями
            pygame.draw.ellipse(screen, color, (x - 60, y - 50, 120, 100))

        # Отрисовка глаз (закрыты если спит)
        eye_size = 8 if self.data.evolution_stage == 1 else 10 if self.data.evolution_stage == 2 else 12
        if self.is_sleeping:
            # Закрытые глаза
            pygame.draw.line(screen, BLACK, (x - 25, y - 10), (x - 15, y - 10), 2)
            pygame.draw.line(screen, BLACK, (x + 15, y - 10), (x + 25, y - 10), 2)
        else:
            # Открытые глаза
            pygame.draw.circle(screen, BLACK, (x - 20, y - 10), eye_size)
            pygame.draw.circle(screen, BLACK, (x + 20, y - 10), eye_size)

        # Отрисовка рта на основе уровня счастья
        mouth_y = y + 10
        if self.data.happiness > 70:
            # Счастливый - улыбка
            pygame.draw.arc(screen, BLACK, (x - 15, mouth_y - 5, 30, 20), 0, 3.14, 2)
        elif self.data.happiness > 30:
            # Нейтральный - прямая линия
            pygame.draw.line(screen, BLACK, (x - 15, mouth_y), (x + 15, mouth_y), 2)
        else:
            # Грустный - хмурый вид
            pygame.draw.arc(screen, BLACK, (x - 15, mouth_y + 5, 30, 20), 3.14, 6.28, 2)