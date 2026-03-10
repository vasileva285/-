#!/usr/bin/env python
"""
Скрипт для визуализации структуры базы данных EnglishApp
"""
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishapp.settings')
django.setup()

from lessons.models import LessonCategory, Lesson, Exercise, UserProgress, UserExerciseAttempt
from django.contrib.auth.models import User
from django.db.models import Sum

def print_database_structure():
    """Выводит структуру базы данных с примерами данных"""
    
    print("=" * 80)
    print("СТРУКТУРА БАЗЫ ДАННЫХ EnglishApp")
    print("=" * 80)
    print()
    
    # 1. Категории
    print("📁 КАТЕГОРИИ УРОКОВ (lessons_lessoncategory)")
    print("-" * 80)
    categories = LessonCategory.objects.all().order_by('order')
    if categories.exists():
        for cat in categories:
            lesson_count = cat.lessons.filter(is_active=True).count()
            print(f"  ID: {cat.id} | {cat.icon} {cat.name} ({cat.slug})")
            print(f"       Описание: {cat.description[:60]}...")
            print(f"       Уроков: {lesson_count} | Порядок: {cat.order}")
            print()
    else:
        print("  (нет категорий)")
    print()
    
    # 2. Уроки
    print("📚 УРОКИ (lessons_lesson)")
    print("-" * 80)
    lessons = Lesson.objects.filter(is_active=True).select_related('category').order_by('category', 'order')
    if lessons.exists():
        for lesson in lessons:
            exercise_count = lesson.exercises.count()
            print(f"  ID: {lesson.id} | {lesson.category.icon} {lesson.title} ({lesson.slug})")
            print(f"       Категория: {lesson.category.name}")
            print(f"       Упражнений: {exercise_count} | Порядок: {lesson.order}")
            print(f"       Описание: {lesson.description[:60]}...")
            print()
    else:
        print("  (нет уроков)")
    print()
    
    # 3. Упражнения
    print("✏️  УПРАЖНЕНИЯ (lessons_exercise)")
    print("-" * 80)
    exercises = Exercise.objects.select_related('lesson', 'lesson__category').order_by('lesson', 'order')[:20]
    if exercises.exists():
        for ex in exercises:
            print(f"  ID: {ex.id} | {ex.get_exercise_type_display()}")
            print(f"       Урок: {ex.lesson.title}")
            print(f"       Вопрос: {ex.question[:50]}...")
            print(f"       Баллы: {ex.points} | Порядок: {ex.order}")
            if ex.options:
                print(f"       Варианты: {ex.options}")
            print()
    else:
        print("  (нет упражнений)")
    print()
    
    # 4. Пользователи и прогресс
    print("👥 ПОЛЬЗОВАТЕЛИ И ПРОГРЕСС")
    print("-" * 80)
    users = User.objects.all()[:5]
    if users.exists():
        for user in users:
            progress_count = UserProgress.objects.filter(user=user).count()
            completed_count = UserProgress.objects.filter(user=user, completed=True).count()
            total_points = UserProgress.objects.filter(user=user).aggregate(
                total=Sum('score')
            )['total'] or 0
            
            print(f"  Пользователь: {user.username} (ID: {user.id})")
            print(f"       Прогресс: {completed_count}/{progress_count} уроков завершено")
            print(f"       Баллы: {total_points}")
            print()
    else:
        print("  (нет пользователей)")
    print()
    
    # 5. Статистика попыток
    print("📊 СТАТИСТИКА ПОПЫТОК")
    print("-" * 80)
    total_attempts = UserExerciseAttempt.objects.count()
    correct_attempts = UserExerciseAttempt.objects.filter(is_correct=True).count()
    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
    
    print(f"  Всего попыток: {total_attempts}")
    print(f"  Правильных: {correct_attempts}")
    print(f"  Точность: {accuracy:.1f}%")
    print()
    
    # 6. Сводная статистика
    print("=" * 80)
    print("СВОДНАЯ СТАТИСТИКА")
    print("=" * 80)
    print(f"  Категорий: {LessonCategory.objects.count()}")
    print(f"  Уроков: {Lesson.objects.filter(is_active=True).count()}")
    print(f"  Упражнений: {Exercise.objects.count()}")
    print(f"  Пользователей: {User.objects.count()}")
    print(f"  Записей прогресса: {UserProgress.objects.count()}")
    print(f"  Попыток выполнения: {UserExerciseAttempt.objects.count()}")
    print()
    
    # 7. Связи
    print("=" * 80)
    print("СВЯЗИ МЕЖДУ ТАБЛИЦАМИ")
    print("=" * 80)
    print("""
  LessonCategory (1) ──→ (N) Lesson
       │
       └─── Каждая категория содержит много уроков
  
  Lesson (1) ──→ (N) Exercise
       │
       └─── Каждый урок содержит много упражнений
  
  User (1) ──→ (N) UserProgress
       │
       └─── Каждый пользователь имеет прогресс по многим урокам
  
  User (1) ──→ (N) UserExerciseAttempt
       │
       └─── Каждый пользователь делает много попыток
  
  Lesson (1) ──→ (N) UserProgress
       │
       └─── Каждый урок имеет прогресс от многих пользователей
  
  Exercise (1) ──→ (N) UserExerciseAttempt
       │
       └─── Каждое упражнение имеет много попыток
    """)

if __name__ == "__main__":
    print_database_structure()

