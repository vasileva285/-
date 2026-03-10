from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import LessonCategory, Lesson, Exercise, UserProgress, UserExerciseAttempt


class ExerciseInline(admin.TabularInline):
    """Inline для добавления упражнений прямо в урок"""
    model = Exercise
    extra = 1
    fields = ('exercise_type', 'question', 'correct_answer', 'options', 'explanation', 'points', 'order')
    ordering = ('order',)


@admin.register(LessonCategory)
class LessonCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'lesson_count', 'order', 'is_active']
    list_editable = ['order']
    list_filter = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'icon', 'description', 'order')
        }),
    )
    
    def lesson_count(self, obj):
        """Количество уроков в категории"""
        count = obj.lessons.filter(is_active=True).count()
        url = reverse('admin:lessons_lesson_changelist')
        return format_html('<a href="{}?category__id__exact={}">{} уроков</a>', url, obj.id, count)
    lesson_count.short_description = 'Уроков'
    
    def is_active(self, obj):
        """Проверка активности категории"""
        return obj.lessons.filter(is_active=True).exists()
    is_active.boolean = True
    is_active.short_description = 'Активна'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'exercise_count', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'theory']
    inlines = [ExerciseInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'title', 'slug', 'description', 'order', 'is_active')
        }),
        ('Теоретический материал', {
            'fields': ('theory', 'examples'),
            'classes': ('wide',),
            'description': 'Введите теоретический материал и примеры. Примеры разделяйте новой строкой.'
        }),
    )
    readonly_fields = ['created_at']
    
    def exercise_count(self, obj):
        """Количество упражнений в уроке"""
        count = obj.exercises.count()
        if count > 0:
            url = reverse('admin:lessons_exercise_changelist')
            return format_html('<a href="{}?lesson__id__exact={}">{} упражнений</a>', url, obj.id, count)
        return '0 упражнений'
    exercise_count.short_description = 'Упражнений'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'lesson', 'exercise_type', 'points', 'order', 'preview']
    list_filter = ['exercise_type', 'lesson__category', 'lesson']
    list_editable = ['order', 'points']
    search_fields = ['question', 'correct_answer', 'explanation']
    fieldsets = (
        ('Основная информация', {
            'fields': ('lesson', 'exercise_type', 'question', 'order', 'points')
        }),
        ('Ответы', {
            'fields': ('correct_answer', 'options', 'explanation'),
            'description': mark_safe(
                '<strong>Для множественного выбора:</strong> укажите правильный ответ в "Правильный ответ", '
                'а варианты в "Варианты ответов" в формате JSON массива: ["вариант1", "вариант2", "вариант3"]<br>'
                '<strong>Для перевода:</strong> можно указать несколько правильных вариантов через |: "вариант1|вариант2"'
            )
        }),
    )
    
    def question_short(self, obj):
        """Короткая версия вопроса"""
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_short.short_description = 'Вопрос'
    
    def preview(self, obj):
        """Предпросмотр упражнения"""
        if obj.exercise_type == 'multiple_choice' and obj.options:
            options_html = ''.join([f'<li>{opt}</li>' for opt in obj.options[:3]])
            return format_html(
                '<strong>Тип:</strong> {}<br><strong>Варианты:</strong><ul>{}</ul>',
                obj.get_exercise_type_display(),
                mark_safe(options_html)
            )
        return format_html('<strong>Тип:</strong> {}', obj.get_exercise_type_display())
    preview.short_description = 'Предпросмотр'
    
    def get_form(self, request, obj=None, **kwargs):
        """Кастомная форма с подсказками"""
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['options'].help_text = (
            'Для множественного выбора: ["Вариант 1", "Вариант 2", "Вариант 3"]'
        )
        form.base_fields['correct_answer'].help_text = (
            'Для перевода можно указать несколько вариантов через |: "вариант1|вариант2"'
        )
        return form


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'score_display', 'progress_percent', 'started_at', 'completed_at']
    list_filter = ['completed', 'lesson__category', 'started_at']
    search_fields = ['user__username', 'user__email', 'lesson__title']
    readonly_fields = ['started_at', 'completed_at']
    date_hierarchy = 'started_at'
    
    def score_display(self, obj):
        """Отображение баллов"""
        return f"{obj.score} / {obj.total_points}"
    score_display.short_description = 'Баллы'
    
    def progress_percent(self, obj):
        """Процент выполнения"""
        if obj.total_points > 0:
            percent = int((obj.score / obj.total_points) * 100)
            color = 'green' if percent == 100 else 'orange' if percent >= 50 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}%</span>',
                color, percent
            )
        return '0%'
    progress_percent.short_description = 'Прогресс'


@admin.register(UserExerciseAttempt)
class UserExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_short', 'user_answer_short', 'is_correct', 'points_earned', 'attempted_at']
    list_filter = ['is_correct', 'exercise__exercise_type', 'attempted_at']
    search_fields = ['user__username', 'exercise__question', 'user_answer']
    readonly_fields = ['attempted_at']
    date_hierarchy = 'attempted_at'
    
    def exercise_short(self, obj):
        """Короткая версия упражнения"""
        return obj.exercise.question[:40] + '...' if len(obj.exercise.question) > 40 else obj.exercise.question
    exercise_short.short_description = 'Упражнение'
    
    def user_answer_short(self, obj):
        """Короткая версия ответа"""
        return obj.user_answer[:30] + '...' if len(obj.user_answer) > 30 else obj.user_answer
    user_answer_short.short_description = 'Ответ пользователя'


# Настройка админ-панели
admin.site.site_header = "EnglishApp - Администрирование"
admin.site.site_title = "EnglishApp Admin"
admin.site.index_title = "Панель управления"

