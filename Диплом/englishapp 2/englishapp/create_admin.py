#!/usr/bin/env python
"""
Скрипт для создания администратора EnglishApp
"""
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishapp.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    print("=" * 60)
    print("СОЗДАНИЕ АДМИНИСТРАТОРА EnglishApp")
    print("=" * 60)
    print()
    
    username = input("Введите имя пользователя (admin): ").strip() or "admin"
    
    # Проверка существования пользователя
    if User.objects.filter(username=username).exists():
        print(f"\n❌ Пользователь '{username}' уже существует!")
        choice = input("Хотите сделать его администратором? (y/n): ").strip().lower()
        if choice == 'y':
            user = User.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"\n✅ Пользователь '{username}' теперь администратор!")
            return
        else:
            print("Отменено.")
            return
    
    email = input("Введите email (опционально): ").strip()
    password = input("Введите пароль: ").strip()
    
    if not password:
        print("\n❌ Пароль не может быть пустым!")
        return
    
    # Создание пользователя
    try:
        user = User.objects.create_user(
            username=username,
            email=email if email else None,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        print("\n" + "=" * 60)
        print("✅ АДМИНИСТРАТОР УСПЕШНО СОЗДАН!")
        print("=" * 60)
        print(f"Имя пользователя: {username}")
        print(f"Email: {email or 'не указан'}")
        print(f"Права: Администратор (staff + superuser)")
        print()
        print("Теперь вы можете войти в админ-панель:")
        print("URL: http://127.0.0.1:8000/admin/")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Ошибка при создании администратора: {e}")

if __name__ == "__main__":
    create_admin()

