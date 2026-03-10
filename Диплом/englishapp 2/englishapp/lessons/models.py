from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class LessonCategory(models.Model):
    """Категория уроков (Present, Past, Future)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    icon = models.CharField(max_length=50, default="📚", verbose_name="Иконка")
    
    class Meta:
        verbose_name = "Категория уроков"
        verbose_name_plural = "Категории уроков"
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Урок"""
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE, related_name='lessons', verbose_name="Категория")
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    theory = models.TextField(verbose_name="Теоретический материал")
    examples = models.TextField(verbose_name="Примеры", help_text="Примеры использования, разделенные новой строкой")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['category', 'order']
    
    def __str__(self):
        return f"{self.category.name} - {self.title}"


class ExerciseType(models.TextChoices):
    MULTIPLE_CHOICE = 'multiple_choice', 'Множественный выбор'
    FILL_BLANK = 'fill_blank', 'Заполнение пропусков'
    TRANSLATION = 'translation', 'Перевод'
    QUESTION = 'question', 'Вопрос'


class Exercise(models.Model):
    """Упражнение"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises', verbose_name="Урок")
    exercise_type = models.CharField(max_length=20, choices=ExerciseType.choices, verbose_name="Тип упражнения")
    question = models.TextField(verbose_name="Вопрос/Задание")
    correct_answer = models.TextField(verbose_name="Правильный ответ")
    options = models.JSONField(default=list, blank=True, verbose_name="Варианты ответов", 
                              help_text="Для множественного выбора - список вариантов")
    explanation = models.TextField(blank=True, verbose_name="Объяснение")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    points = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Баллы")
    
    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.question[:50]}"


class UserProgress(models.Model):
    """Прогресс пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress', verbose_name="Пользователь")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress', verbose_name="Урок")
    completed = models.BooleanField(default=False, verbose_name="Завершен")
    score = models.IntegerField(default=0, verbose_name="Баллы")
    total_points = models.IntegerField(default=0, verbose_name="Всего баллов")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начат")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершен")
    
    class Meta:
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"
        unique_together = ['user', 'lesson']
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class UserExerciseAttempt(models.Model):
    """Попытка выполнения упражнения пользователем"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_attempts', verbose_name="Пользователь")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='attempts', verbose_name="Упражнение")
    user_answer = models.TextField(verbose_name="Ответ пользователя")
    is_correct = models.BooleanField(verbose_name="Правильно")
    points_earned = models.IntegerField(default=0, verbose_name="Заработано баллов")
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="Попытка")
    
    class Meta:
        verbose_name = "Попытка выполнения упражнения"
        verbose_name_plural = "Попытки выполнения упражнений"
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.question[:30]}"

