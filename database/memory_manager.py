"""
In-memory storage for when no database is available.
"""

from datetime import datetime
from .models import Tamagotchi


class MemoryManager:
    """Менеджер для хранения тамагочи в оперативной памяти.
    
    Используется как запасной вариант при недоступности базы данных.
    Данные не сохраняются между запусками приложения.
    """
    
    def __init__(self):
        """Инициализирует менеджер памяти.
        
        Создает пустой список для хранения тамагочи и устанавливает
        начальный идентификатор для новых записей.
        """
        self.tamagotchis = []
        self.next_id = 1
        print("Using in-memory storage (no persistence)")

    def save_tamagotchi(self, tamagotchi):
        """Сохраняет тамагочи в памяти.
        
        Если тамагочи не имеет ID, создает новую запись с новым ID.
        Если ID существует, обновляет существующую запись.
        
        Args:
            tamagotchi: Объект Tamagotchi для сохранения.
            
        Returns:
            bool: True если сохранение прошло успешно, False в случае ошибки.
        """
        try:
            if tamagotchi.id is None:
                # Присваиваем новый ID и добавляем в список
                tamagotchi.id = self.next_id
                self.next_id += 1
                self.tamagotchis.append(tamagotchi)
                print(f"Tamagotchi created with ID: {tamagotchi.id}")
            else:
                # Обновляем существующий объект
                for i, t in enumerate(self.tamagotchis):
                    if t.id == tamagotchi.id:
                        self.tamagotchis[i] = tamagotchi
                        break

            return True
        except Exception as e:
            print(f"Error saving tamagotchi: {e}")
            return False

    def load_tamagotchi(self, tamagotchi_id):
        """Загружает тамагочи из памяти по ID.
        
        Args:
            tamagotchi_id: Идентификатор тамагочи для загрузки.
            
        Returns:
            Tamagotchi or None: Объект Tamagotchi если найден, None если не найден
                                 или произошла ошибка.
        """
        try:
            # Линейный поиск по ID
            for t in self.tamagotchis:
                if t.id == tamagotchi_id:
                    return t
            return None
        except Exception as e:
            print(f"Error loading tamagotchi: {e}")
            return None

    def get_all_tamagotchis(self):
        """Получает все тамагочи из памяти.
        
        Returns:
            list: Копия списка всех объектов Tamagotchi.
        """
        return self.tamagotchis.copy()

    def delete_tamagotchi(self, tamagotchi_id):
        """Удаляет тамагочи из памяти по ID.
        
        Args:
            tamagotchi_id: Идентификатор тамагочи для удаления.
            
        Returns:
            bool: Всегда возвращает True, так как удаление происходит в памяти.
        """
        # Фильтруем список, оставляя только тамагочи с другим ID
        self.tamagotchis = [t for t in self.tamagotchis if t.id != tamagotchi_id]
        return True