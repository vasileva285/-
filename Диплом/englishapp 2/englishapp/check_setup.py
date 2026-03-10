#!/usr/bin/env python3
"""
Скрипт для проверки работоспособности приложения EnglishApp
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Проверяет существование файла"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} НЕ НАЙДЕН: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Проверяет существование директории"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} НЕ НАЙДЕНА: {dirpath}")
        return False

def main():
    print("=" * 60)
    print("ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА EnglishApp")
    print("=" * 60)
    print()
    
    base_dir = Path(__file__).parent
    errors = []
    
    # Проверка основных файлов проекта
    print("\n📁 Основные файлы проекта:")
    files_to_check = [
        (base_dir / "manage.py", "manage.py"),
        (base_dir / "requirements.txt", "requirements.txt"),
        (base_dir / "README.md", "README.md"),
        (base_dir / "englishapp" / "settings.py", "settings.py"),
        (base_dir / "englishapp" / "urls.py", "urls.py"),
    ]
    
    for filepath, desc in files_to_check:
        if not check_file_exists(filepath, desc):
            errors.append(f"Отсутствует: {desc}")
    
    # Проверка приложения lessons
    print("\n📚 Файлы приложения lessons:")
    lessons_files = [
        (base_dir / "lessons" / "models.py", "models.py"),
        (base_dir / "lessons" / "views.py", "views.py"),
        (base_dir / "lessons" / "urls.py", "urls.py"),
        (base_dir / "lessons" / "forms.py", "forms.py"),
        (base_dir / "lessons" / "admin.py", "admin.py"),
    ]
    
    for filepath, desc in lessons_files:
        if not check_file_exists(filepath, desc):
            errors.append(f"Отсутствует: lessons/{desc}")
    
    # Проверка management команд
    print("\n🔧 Management команды:")
    management_files = [
        (base_dir / "lessons" / "management" / "__init__.py", "__init__.py"),
        (base_dir / "lessons" / "management" / "commands" / "__init__.py", "commands/__init__.py"),
        (base_dir / "lessons" / "management" / "commands" / "load_initial_data.py", "load_initial_data.py"),
    ]
    
    for filepath, desc in management_files:
        if not check_file_exists(filepath, desc):
            errors.append(f"Отсутствует: lessons/management/{desc}")
    
    # Проверка template tags
    print("\n🏷️ Template tags:")
    tag_files = [
        (base_dir / "lessons" / "templatetags" / "__init__.py", "__init__.py"),
        (base_dir / "lessons" / "templatetags" / "lesson_tags.py", "lesson_tags.py"),
    ]
    
    for filepath, desc in tag_files:
        if not check_file_exists(filepath, desc):
            errors.append(f"Отсутствует: lessons/templatetags/{desc}")
    
    # Проверка шаблонов
    print("\n📄 HTML шаблоны:")
    templates = [
        (base_dir / "templates" / "base.html", "base.html"),
        (base_dir / "templates" / "lessons" / "home.html", "home.html"),
        (base_dir / "templates" / "lessons" / "register.html", "register.html"),
        (base_dir / "templates" / "lessons" / "login.html", "login.html"),
        (base_dir / "templates" / "lessons" / "category_detail.html", "category_detail.html"),
        (base_dir / "templates" / "lessons" / "lesson_detail.html", "lesson_detail.html"),
        (base_dir / "templates" / "lessons" / "exercise_detail.html", "exercise_detail.html"),
        (base_dir / "templates" / "lessons" / "progress.html", "progress.html"),
    ]
    
    for filepath, desc in templates:
        if not check_file_exists(filepath, desc):
            errors.append(f"Отсутствует: templates/{desc}")
    
    # Проверка статических файлов
    print("\n🎨 Статические файлы:")
    static_files = [
        (base_dir / "static" / "css" / "style.css", "style.css"),
        (base_dir / "static" / "js" / "main.js", "main.js"),
    ]
    
    for filepath, desc in static_files:
        if not check_file_exists(filepath, desc):
            errors.append(f"Отсутствует: static/{desc}")
    
    # Проверка директорий
    print("\n📂 Директории:")
    directories = [
        (base_dir / "templates", "templates"),
        (base_dir / "templates" / "lessons", "templates/lessons"),
        (base_dir / "static", "static"),
        (base_dir / "static" / "css", "static/css"),
        (base_dir / "static" / "js", "static/js"),
    ]
    
    for dirpath, desc in directories:
        if not check_directory_exists(dirpath, desc):
            errors.append(f"Отсутствует директория: {desc}")
    
    # Итоги
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ НАЙДЕНО ОШИБОК: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
        return 1
    else:
        print("✅ ВСЕ ФАЙЛЫ И ДИРЕКТОРИИ НА МЕСТЕ!")
        print("\n📋 Следующие шаги для запуска:")
        print("   1. Установите зависимости: pip install -r requirements.txt")
        print("   2. Примените миграции: python manage.py migrate")
        print("   3. Загрузите данные: python manage.py load_initial_data")
        print("   4. Запустите сервер: python manage.py runserver")
        return 0

if __name__ == "__main__":
    sys.exit(main())

