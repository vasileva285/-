from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .models import LessonCategory, Lesson, Exercise, UserProgress, UserExerciseAttempt
from .forms import UserRegistrationForm, UserProfileForm


def home(request):
    """Главная страница"""
    if request.user.is_authenticated:
        # Получаем статистику пользователя
        total_lessons = Lesson.objects.filter(is_active=True).count()
        completed_lessons = UserProgress.objects.filter(
            user=request.user, 
            completed=True
        ).count()
        total_points = UserProgress.objects.filter(
            user=request.user
        ).aggregate(total=Sum('score'))['total'] or 0
        
        # Получаем последние уроки
        recent_progress = UserProgress.objects.filter(
            user=request.user
        ).select_related('lesson', 'lesson__category').order_by('-started_at')[:5]
        
        # Получаем категории с прогрессом
        categories = LessonCategory.objects.annotate(
            lesson_count=Count('lessons', filter=Q(lessons__is_active=True))
        ).prefetch_related('lessons')
        
        for category in categories:
            category.completed_count = UserProgress.objects.filter(
                user=request.user,
                lesson__category=category,
                completed=True
            ).count()
            category.total_count = category.lesson_count
            # Вычисляем процент для шаблона
            if category.total_count > 0:
                category.percentage = int((category.completed_count / category.total_count) * 100)
            else:
                category.percentage = 0
        
        context = {
            'categories': categories,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'total_points': total_points,
            'recent_progress': recent_progress,
        }
    else:
        categories = LessonCategory.objects.annotate(
            lesson_count=Count('lessons', filter=Q(lessons__is_active=True))
        )
        context = {
            'categories': categories,
        }
    
    return render(request, 'lessons/home.html', context)


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'lessons/register.html', {'form': form})


@login_required
def category_detail(request, slug):
    """Детальная страница категории"""
    category = get_object_or_404(LessonCategory, slug=slug)
    lessons = Lesson.objects.filter(
        category=category, 
        is_active=True
    ).select_related('category').order_by('order')
    
    # Получаем прогресс для каждого урока
    for lesson in lessons:
        try:
            progress = UserProgress.objects.get(user=request.user, lesson=lesson)
            # Используем обычные атрибуты Python, а не related field
            lesson.user_progress_obj = progress
            lesson.is_completed = progress.completed
            lesson.user_score = progress.score
            # Вычисляем процент выполнения
            if progress.total_points > 0:
                lesson.progress_percentage = int((progress.score / progress.total_points) * 100)
            else:
                lesson.progress_percentage = 0
        except UserProgress.DoesNotExist:
            # Не присваиваем related field, используем обычные атрибуты
            lesson.user_progress_obj = None
            lesson.is_completed = False
            lesson.user_score = 0
            lesson.progress_percentage = 0
    
    context = {
        'category': category,
        'lessons': lessons,
    }
    return render(request, 'lessons/category_detail.html', context)


@login_required
def lesson_detail(request, slug):
    """Детальная страница урока с теорией"""
    lesson = get_object_or_404(Lesson, slug=slug, is_active=True)
    
    # Получаем или создаем прогресс
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    # Вычисляем процент выполнения
    if progress.total_points > 0:
        progress.percentage = int((progress.score / progress.total_points) * 100)
    else:
        progress.percentage = 0
    
    # Получаем упражнения
    exercises = Exercise.objects.filter(lesson=lesson).order_by('order')
    
    # Получаем попытки пользователя
    attempts = UserExerciseAttempt.objects.filter(
        user=request.user,
        exercise__lesson=lesson
    ).select_related('exercise')
    
    # Формируем статистику по упражнениям (используем список для удобства в шаблоне)
    exercise_stats_list = []
    for exercise in exercises:
        exercise_attempts = [a for a in attempts if a.exercise_id == exercise.id]
        exercise_stats_list.append({
            'exercise_id': exercise.id,
            'attempts': exercise_attempts,
            'correct_count': sum(1 for a in exercise_attempts if a.is_correct),
            'total_count': len(exercise_attempts),
        })
    
    # Также создаем словарь для обратной совместимости
    exercise_stats = {item['exercise_id']: item for item in exercise_stats_list}
    
    # Разбиваем примеры на список
    examples_list = [ex.strip() for ex in lesson.examples.split('\n') if ex.strip()]
    
    context = {
        'lesson': lesson,
        'progress': progress,
        'exercises': exercises,
        'exercise_stats': exercise_stats,
        'examples_list': examples_list,
    }
    return render(request, 'lessons/lesson_detail.html', context)


@login_required
def exercise_detail(request, lesson_slug, exercise_id):
    """Страница выполнения упражнения"""
    lesson = get_object_or_404(Lesson, slug=lesson_slug, is_active=True)
    exercise = get_object_or_404(Exercise, id=exercise_id, lesson=lesson)
    
    # Получаем прогресс урока
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    # Получаем предыдущие попытки
    previous_attempts = UserExerciseAttempt.objects.filter(
        user=request.user,
        exercise=exercise
    ).order_by('-attempted_at')[:5]
    
    context = {
        'lesson': lesson,
        'exercise': exercise,
        'progress': progress,
        'previous_attempts': previous_attempts,
    }
    return render(request, 'lessons/exercise_detail.html', context)


@login_required
@require_http_methods(["POST"])
def submit_exercise(request, exercise_id):
    """Обработка ответа на упражнение"""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    try:
        data = json.loads(request.body)
        user_answer = data.get('answer', '').strip()
        
        # Проверяем ответ в зависимости от типа упражнения
        is_correct = False
        if exercise.exercise_type == 'multiple_choice':
            is_correct = user_answer.lower() == exercise.correct_answer.lower()
        elif exercise.exercise_type == 'fill_blank':
            # Для заполнения пропусков сравниваем без учета регистра и пробелов
            is_correct = user_answer.lower().strip() == exercise.correct_answer.lower().strip()
        elif exercise.exercise_type == 'translation':
            # Для перевода более мягкая проверка
            correct_variants = [v.strip().lower() for v in exercise.correct_answer.split('|')]
            is_correct = user_answer.lower().strip() in correct_variants
        elif exercise.exercise_type == 'question':
            # Для вопросов сравниваем без учета регистра
            is_correct = user_answer.lower().strip() == exercise.correct_answer.lower().strip()
        else:
            is_correct = user_answer.lower().strip() == exercise.correct_answer.lower().strip()
        
        # Сохраняем попытку
        points_earned = exercise.points if is_correct else 0
        attempt = UserExerciseAttempt.objects.create(
            user=request.user,
            exercise=exercise,
            user_answer=user_answer,
            is_correct=is_correct,
            points_earned=points_earned
        )
        
        # Обновляем прогресс урока
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=exercise.lesson
        )
        
        if is_correct:
            # Обновляем только если еще не было правильного ответа на это упражнение
            existing_correct = UserExerciseAttempt.objects.filter(
                user=request.user,
                exercise=exercise,
                is_correct=True
            ).exists()
            
            if not existing_correct:
                progress.score += points_earned
                progress.total_points += exercise.points
        
        # Проверяем, все ли упражнения выполнены правильно
        all_exercises = Exercise.objects.filter(lesson=exercise.lesson)
        correct_attempts = UserExerciseAttempt.objects.filter(
            user=request.user,
            exercise__lesson=exercise.lesson,
            is_correct=True
        ).values('exercise').distinct().count()
        
        if correct_attempts >= all_exercises.count():
            progress.completed = True
            from django.utils import timezone
            if not progress.completed_at:
                progress.completed_at = timezone.now()
        
        progress.save()
        
        return JsonResponse({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': exercise.correct_answer,
            'explanation': exercise.explanation,
            'points_earned': points_earned,
            'total_score': progress.score,
            'lesson_completed': progress.completed,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
def progress_view(request):
    """Страница прогресса пользователя"""
    # Общая статистика
    total_lessons = Lesson.objects.filter(is_active=True).count()
    completed_lessons = UserProgress.objects.filter(
        user=request.user, 
        completed=True
    ).count()
    total_points = UserProgress.objects.filter(
        user=request.user
    ).aggregate(total=Sum('score'))['total'] or 0
    
    # Прогресс по категориям
    categories_progress = []
    categories = LessonCategory.objects.all()
    for category in categories:
        category_lessons = Lesson.objects.filter(category=category, is_active=True)
        category_completed = UserProgress.objects.filter(
            user=request.user,
            lesson__category=category,
            completed=True
        ).count()
        categories_progress.append({
            'category': category,
            'total': category_lessons.count(),
            'completed': category_completed,
            'percentage': int((category_completed / category_lessons.count() * 100) if category_lessons.count() > 0 else 0)
        })
    
    # Последние достижения
    recent_completions = UserProgress.objects.filter(
        user=request.user,
        completed=True
    ).select_related('lesson', 'lesson__category').order_by('-completed_at')[:10]
    
    # Статистика по упражнениям
    total_attempts = UserExerciseAttempt.objects.filter(user=request.user).count()
    correct_attempts = UserExerciseAttempt.objects.filter(
        user=request.user,
        is_correct=True
    ).count()
    accuracy = int((correct_attempts / total_attempts * 100) if total_attempts > 0 else 0)
    
    context = {
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'total_points': total_points,
        'categories_progress': categories_progress,
        'recent_completions': recent_completions,
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'accuracy': accuracy,
    }
    return render(request, 'lessons/progress.html', context)


@login_required
def profile_settings(request):
    """Страница настроек профиля пользователя"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile_settings')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Статистика пользователя
    total_lessons = Lesson.objects.filter(is_active=True).count()
    completed_lessons = UserProgress.objects.filter(
        user=request.user, 
        completed=True
    ).count()
    total_points = UserProgress.objects.filter(
        user=request.user
    ).aggregate(total=Sum('score'))['total'] or 0
    
    # Дата регистрации
    date_joined = request.user.date_joined
    
    context = {
        'form': form,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'total_points': total_points,
        'date_joined': date_joined,
    }
    return render(request, 'lessons/profile_settings.html', context)
