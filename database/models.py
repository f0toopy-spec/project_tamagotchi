from datetime import datetime


class Tamagotchi:
    """Класс, представляющий виртуального питомца Tamagotchi.
    
    Хранит все атрибуты состояния питомца и предоставляет методы
    для сериализации и десериализации.
    """
    
    def __init__(self, id=None, name="Pou", created_at=None):
        """Инициализирует нового тамагочи с заданными параметрами.
        
        Args:
            id: Идентификатор тамагочи. Если None, тамагочи считается новым.
            name: Имя тамагочи. По умолчанию "Pou".
            created_at: Время создания тамагочи. Если None, используется текущее время.
        """
        self.id = id
        self.name = name
        self.hunger = 50          # Уровень голода (0-100)
        self.happiness = 50       # Уровень счастья (0-100)
        self.health = 100         # Уровень здоровья (0-100)
        self.cleanliness = 50     # Уровень чистоты (0-100)
        self.energy = 100         # Уровень энергии (0-100)
        self.age = 0              # Возраст в днях
        self.coins = 100          # Количество монет
        self.created_at = created_at or datetime.now()
        self.last_updated = datetime.now()
        self.evolution_stage = 1  # Стадия эволюции (1: ребенок, 2: подросток, 3: взрослый)

    def to_dict(self):
        """Конвертирует объект Tamagotchi в словарь для сериализации.
        
        Returns:
            dict: Словарь со всеми атрибутами тамагочи. Подходит для сохранения
                  в базу данных или передачи между слоями приложения.
        """
        return {
            'id': self.id,
            'name': self.name,
            'hunger': self.hunger,
            'happiness': self.happiness,
            'health': self.health,
            'cleanliness': self.cleanliness,
            'energy': self.energy,
            'age': self.age,
            'coins': self.coins,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'evolution_stage': self.evolution_stage
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект Tamagotchi из словаря.
        
        Фабричный метод для десериализации данных из базы данных
        или другого источника.
        
        Args:
            data: Словарь с данными тамагочи. Может содержать не все поля.
            
        Returns:
            Tamagotchi: Новый объект Tamagotchi с данными из словаря.
        """
        tamagotchi = cls()
        tamagotchi.id = data.get('id')
        tamagotchi.name = data.get('name', 'Pou')
        tamagotchi.hunger = data.get('hunger', 50)
        tamagotchi.happiness = data.get('happiness', 50)
        tamagotchi.health = data.get('health', 100)
        tamagotchi.cleanliness = data.get('cleanliness', 50)
        tamagotchi.energy = data.get('energy', 100)
        tamagotchi.age = data.get('age', 0)
        tamagotchi.coins = data.get('coins', 100)
        tamagotchi.created_at = data.get('created_at', datetime.now())
        tamagotchi.last_updated = data.get('last_updated', datetime.now())
        tamagotchi.evolution_stage = data.get('evolution_stage', 1)
        return tamagotchi