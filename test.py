import os
import sys

print(" Testing Python imports and paths...")

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f" Current directory: {current_dir}")
print(" Python path:")
for path in sys.path:
    print(f"  - {path}")

print("\n Checking for files...")
files_to_check = [
    'database/__init__.py',
    'database/sqlite_manager.py',
    'database/models.py',
    'game/__init__.py',
    'game/core.py',
    'entities/__init__.py',
    'entities/tamagotchi.py',
    'entities/buttons.py'
]

for file in files_to_check:
    full_path = os.path.join(current_dir, file)
    exists = os.path.exists(full_path)
    print(f"  {file}: {' EXISTS' if exists else ' MISSING'}")

print("\n Testing imports...")
try:
    from database.sqlite_manager import SQLiteManager
    print(" SQLiteManager imported successfully")
except ImportError as e:
    print(f" SQLiteManager import failed: {e}")

try:
    from database.models import Tamagotchi
    print(" Tamagotchi model imported successfully")
except ImportError as e:
    print(f" Tamagotchi import failed: {e}")

try:
    from entities.buttons import Button
    print(" Button imported successfully")
except ImportError as e:
    print(f" Button import failed: {e}")

try:
    from entities.tamagotchi import TamagotchiEntity
    print(" TamagotchiEntity imported successfully")
except ImportError as e:
    print(f" TamagotchiEntity import failed: {e}")

print("\n If all imports fail, we'll use the single-file version.")
input("Press Enter to continue...")