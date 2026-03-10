# 1.1 Разработка пользовательского интерфейса

## Страница «Категории уроков»

Пользовательский интерфейс веб-приложения EnglishApp состоит из двух основных областей: верхней навигационной панели и основной рабочей области. Навигационная панель содержит меню выбора разделов системы и информацию о пользователе. Основная область включает hero-секцию с приветствием, статистические карточки, и карточки категорий уроков с информацией о прогрессе (Рисунок 1.1).

![Рисунок 1.1 – Общий вид интерфейса приложения](page_mockups.drawio)

HTML-структура основного контейнера и карточек категорий с информацией о прогрессе представлена в листинге 1.1.

**Листинг 1.1** – HTML-структура главной страницы и карточек категорий

```html
<!-- Навигационная панель -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
  <div class="container">
    <a class="navbar-brand" href="/">
      <i class="bi bi-translate"></i> EnglishApp
    </a>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="/">Главная</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/progress/">Прогресс</a>
      </li>
    </ul>
  </div>
</nav>

<!-- Hero секция -->
<div class="hero-section bg-gradient-primary text-white py-5 mb-5">
  <div class="container">
    <h1 class="display-4 fw-bold mb-4">
      Изучайте английский язык легко и интересно!
    </h1>
    <p class="lead mb-4">
      Интерактивные уроки, практические упражнения и отслеживание прогресса.
    </p>
  </div>
</div>

<!-- Статистика пользователя -->
<div class="container">
  <div class="row mb-5">
    <div class="col-md-4 mb-3">
      <div class="card stat-card h-100">
        <div class="card-body text-center">
          <i class="bi bi-book text-primary" style="font-size: 3rem;"></i>
          <h3 class="mt-3">{{ completed_lessons }}/{{ total_lessons }}</h3>
          <p class="text-muted mb-0">Уроков завершено</p>
        </div>
      </div>
    </div>
    <div class="col-md-4 mb-3">
      <div class="card stat-card h-100">
        <div class="card-body text-center">
          <i class="bi bi-star text-warning" style="font-size: 3rem;"></i>
          <h3 class="mt-3">{{ total_points }}</h3>
          <p class="text-muted mb-0">Всего баллов</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Категории уроков -->
  <h2 class="mb-4">
    <i class="bi bi-folder"></i> Категории уроков
  </h2>
  <div class="row mb-5">
    {% for category in categories %}
    <div class="col-md-4 mb-4">
      <div class="card category-card h-100 shadow-sm">
        <div class="card-body">
          <div class="d-flex align-items-center mb-3">
            <span class="category-icon me-3" style="font-size: 3rem;">
              {{ category.icon }}
            </span>
            <div>
              <h4 class="card-title mb-0">{{ category.name }}</h4>
              <small class="text-muted">{{ category.lesson_count }} уроков</small>
            </div>
          </div>
          <p class="card-text text-muted">
            {{ category.description|truncatewords:15 }}
          </p>
          {% if user.is_authenticated %}
          <div class="mb-3">
            <div class="progress" style="height: 8px;">
              <div class="progress-bar bg-success" role="progressbar" 
                   style="width: {{ category.percentage }}%">
              </div>
            </div>
            <small class="text-muted">
              {{ category.completed_count }}/{{ category.total_count }} завершено
            </small>
          </div>
          {% endif %}
          <a href="{% url 'category_detail' category.slug %}" 
             class="btn btn-primary w-100">
            <i class="bi bi-arrow-right"></i> Изучать
          </a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
```

Для визуального оформления элементов интерфейса использовались каскадные таблицы стилей (CSS) с применением Bootstrap 5 и кастомных стилей. Карточки категорий имеют скругленные углы, эффект тени и анимацию при наведении курсора мыши, что улучшает их восприятие. Для повышения удобства работы реализовано подсвечивание карточек при наведении курсора мыши с эффектом подъема. Основные стилевые правила представлены в листинге 1.2.

**Листинг 1.2** – Ключевые CSS-стили для карточек и прогресс-баров

```css
/* Карточки */
.card {
  border: none;
  border-radius: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,.15) !important;
}

.category-card {
  border-left: 4px solid var(--info-color);
}

.stat-card {
  background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
  border-left: 4px solid var(--primary-color);
}

/* Прогресс-бары */
.progress {
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  transition: width 0.6s ease;
  animation: progressBar 1s ease-out;
}

/* Кнопки */
.btn {
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,.2);
}

/* Hero секция */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 0 0 30px 30px;
  margin-top: -20px;
}
```

Основная логика работы реализована на серверной стороне с использованием Django шаблонов. При загрузке страницы данные о категориях и прогрессе пользователя загружаются из базы данных и отображаются в карточках. Код функции загрузки данных показан в листинге 1.3.

**Листинг 1.3** – Функция загрузки данных категорий и статистики

```python
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
```

Для удобства работы с данными реализована навигация по категориям с отображением прогресса обучения. Каждая карточка категории показывает количество уроков, процент завершения и позволяет перейти к списку уроков. Функции навигации представлены в листинге 1.4.

**Листинг 1.4** – Функция перехода к категории

```python
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
            lesson.user_progress_obj = progress
            lesson.is_completed = progress.completed
            lesson.user_score = progress.score
            # Вычисляем процент выполнения
            if progress.total_points > 0:
                lesson.progress_percentage = int((progress.score / progress.total_points) * 100)
            else:
                lesson.progress_percentage = 0
        except UserProgress.DoesNotExist:
            lesson.user_progress_obj = None
            lesson.is_completed = False
            lesson.user_score = 0
            lesson.progress_percentage = 0
    
    context = {
        'category': category,
        'lessons': lessons,
    }
    return render(request, 'lessons/category_detail.html', context)
```

Интерфейс обеспечивает полный цикл работы с категориями уроков: просмотр статистики, навигацию по категориям, отслеживание прогресса обучения. Все операции выполняются с использованием серверного рендеринга Django, что обеспечивает удобство и эффективность работы с системой.

## Страница «Выполнение упражнения»

Интерфейс страницы выполнения упражнения состоит из навигационной панели, хлебных крошек для навигации и основной рабочей области. Основная область включает карточку упражнения с вопросом, форму для ввода ответа и область для отображения результата проверки. Общий вид интерфейса представлен на рисунке 1.2.

![Рисунок 1.2 – Общий вид страницы выполнения упражнения](page_mockups.drawio)

HTML-структура страницы организована с использованием семантических тегов Bootstrap. Основная форма содержит поля для ввода ответа в зависимости от типа упражнения: множественный выбор, заполнение пропусков, перевод или обычный вопрос (Листинг 1.5).

**Листинг 1.5** – HTML-структура формы выполнения упражнения

```html
<div class="container mt-5 pt-4">
  <!-- Хлебные крошки -->
  <nav aria-label="breadcrumb" class="mb-4">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a href="/">Главная</a></li>
      <li class="breadcrumb-item">
        <a href="/category/{{ lesson.category.slug }}/">
          {{ lesson.category.name }}
        </a>
      </li>
      <li class="breadcrumb-item">
        <a href="/lesson/{{ lesson.slug }}/">{{ lesson.title }}</a>
      </li>
      <li class="breadcrumb-item active">Упражнение</li>
    </ol>
  </nav>

  <div class="row">
    <div class="col-lg-8 mx-auto">
      <div class="card shadow-lg">
        <div class="card-header bg-primary text-white">
          <h3 class="mb-0">
            <i class="bi bi-pencil-square"></i> Упражнение
          </h3>
        </div>
        <div class="card-body p-4">
          <div class="mb-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="badge bg-info">
                <i class="bi bi-star"></i> {{ exercise.points }} баллов
              </span>
              <span class="badge bg-secondary">
                {{ exercise.get_exercise_type_display }}
              </span>
            </div>
            <h4 class="mb-3">{{ exercise.question }}</h4>
          </div>

          <form id="exerciseForm">
            {% csrf_token %}
            <div class="mb-4">
              {% if exercise.exercise_type == 'multiple_choice' %}
                <!-- Множественный выбор -->
                <div class="list-group">
                  {% for option in exercise.options %}
                  <label class="list-group-item">
                    <input type="radio" name="answer" value="{{ option }}" 
                           class="form-check-input me-2" required>
                    {{ option }}
                  </label>
                  {% endfor %}
                </div>
              {% elif exercise.exercise_type == 'fill_blank' %}
                <!-- Заполнение пропусков -->
                <div class="form-group">
                  <label for="answer" class="form-label">Введите ответ:</label>
                  <input type="text" name="answer" id="answer" 
                         class="form-control form-control-lg" 
                         placeholder="Ваш ответ..." required autofocus>
                </div>
              {% elif exercise.exercise_type == 'translation' %}
                <!-- Перевод -->
                <div class="form-group">
                  <label for="answer" class="form-label">
                    Переведите на английский:
                  </label>
                  <textarea name="answer" id="answer" class="form-control" 
                            rows="3" placeholder="Ваш перевод..." 
                            required autofocus></textarea>
                </div>
              {% else %}
                <!-- Обычный вопрос -->
                <div class="form-group">
                  <label for="answer" class="form-label">Ваш ответ:</label>
                  <input type="text" name="answer" id="answer" 
                         class="form-control form-control-lg" 
                         placeholder="Введите ответ..." required autofocus>
                </div>
              {% endif %}
            </div>

            <div id="resultAlert" class="alert d-none mb-3"></div>

            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-primary btn-lg flex-grow-1" 
                      id="submitBtn">
                <i class="bi bi-check-circle"></i> Проверить ответ
              </button>
              <a href="{% url 'lesson_detail' lesson.slug %}" 
                 class="btn btn-outline-secondary btn-lg">
                <i class="bi bi-arrow-left"></i> Назад
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
```

Для визуального оформления элементов интерфейса применялись каскадные таблицы стилей. Форма имеет адаптивное расположение полей с различными типами ввода в зависимости от типа упражнения. Карточка упражнения включает заголовок с информацией о баллах и типе упражнения. Основные стилевые правила представлены в листинге 1.6.

**Листинг 1.6** – CSS-стили формы и карточки упражнения

```css
/* Формы */
.form-control {
  border-radius: 10px;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  animation: glow 1.5s ease-in-out infinite;
}

/* Карточки */
.card {
  border: none;
  border-radius: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card.shadow-lg {
  box-shadow: 0 10px 25px rgba(0,0,0,.15) !important;
}

/* Список для множественного выбора */
.list-group-item {
  border-radius: 10px !important;
  margin-bottom: 5px;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
  cursor: pointer;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  border-color: var(--primary-color);
}

.list-group-item input[type="radio"]:checked + label,
#exerciseForm input[type="radio"]:checked + label {
  background-color: #e7f3ff;
  border-color: var(--primary-color);
}

/* Алерты результатов */
.alert {
  border-radius: 10px;
  border: none;
  animation: slideDown 0.5s ease-out;
}

.alert-success {
  border-left: 4px solid var(--success-color);
}

.alert-danger {
  border-left: 4px solid var(--danger-color);
}
```

Функциональность интерфейса реализована на языке JavaScript. При отправке формы выполняется асинхронный запрос к API для проверки ответа пользователя. В листинге 1.7 приведен код обработки формы и отправки ответа.

**Листинг 1.7** – Функция отправки ответа на проверку

```javascript
document.getElementById('exerciseForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const form = this;
    const submitBtn = document.getElementById('submitBtn');
    const resultAlert = document.getElementById('resultAlert');
    const answerInput = form.querySelector('[name="answer"]');
    
    // Получаем ответ
    let answer = '';
    if (form.querySelector('[name="answer"]:checked')) {
        answer = form.querySelector('[name="answer"]:checked').value;
    } else if (answerInput) {
        answer = answerInput.value.trim();
    }
    
    if (!answer) {
        resultAlert.className = 'alert alert-warning';
        resultAlert.textContent = 'Пожалуйста, введите ответ';
        resultAlert.classList.remove('d-none');
        return;
    }
    
    // Блокируем кнопку
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Проверка...';
    
    try {
        const response = await fetch('/api/exercise/' + exerciseId + '/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ answer: answer })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.is_correct) {
                resultAlert.className = 'alert alert-success';
                resultAlert.innerHTML = `
                    <h5><i class="bi bi-check-circle"></i> Правильно!</h5>
                    <p class="mb-0">Вы заработали <strong>${data.points_earned}</strong> баллов!</p>
                    ${data.explanation ? '<p class="mb-0 mt-2"><small>' + data.explanation + '</small></p>' : ''}
                `;
                
                // Блокируем форму
                form.querySelectorAll('input, textarea').forEach(input => {
                    input.disabled = true;
                });
                
                if (data.lesson_completed) {
                    setTimeout(() => {
                        alert('Поздравляем! Вы завершили урок!');
                        window.location.href = '/lesson/' + lessonSlug + '/';
                    }, 2000);
                }
            } else {
                resultAlert.className = 'alert alert-danger';
                resultAlert.innerHTML = `
                    <h5><i class="bi bi-x-circle"></i> Неправильно</h5>
                    <p class="mb-1">Правильный ответ: <strong>${data.correct_answer}</strong></p>
                    ${data.explanation ? '<p class="mb-0"><small>' + data.explanation + '</small></p>' : ''}
                `;
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Проверить ответ';
            }
            resultAlert.classList.remove('d-none');
        } else {
            alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'));
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Проверить ответ';
        }
    } catch (error) {
        alert('Ошибка при отправке ответа: ' + error.message);
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Проверить ответ';
    }
});
```

Для работы с различными типами упражнений реализована динамическая система отображения полей ввода. В зависимости от типа упражнения (множественный выбор, заполнение пропусков, перевод, вопрос) отображается соответствующий интерфейс ввода. В листинге 1.8 показана логика обработки ответа на сервере.

**Листинг 1.8** – Функция проверки ответа на сервере

```python
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
```

Отображение результата проверки выполняется автоматически при получении ответа от сервера. При правильном ответе отображается сообщение об успехе с количеством заработанных баллов, при неправильном – показывается правильный ответ и объяснение. Алгоритм отображения результата представлен в листинге 1.9.

**Листинг 1.9** – Функция отображения результата проверки

```javascript
// Обработка успешного ответа
if (data.is_correct) {
    resultAlert.className = 'alert alert-success';
    resultAlert.innerHTML = `
        <h5><i class="bi bi-check-circle"></i> Правильно!</h5>
        <p class="mb-0">Вы заработали <strong>${data.points_earned}</strong> баллов!</p>
        ${data.explanation ? '<p class="mb-0 mt-2"><small>' + data.explanation + '</small></p>' : ''}
    `;
    
    // Блокируем форму после правильного ответа
    form.querySelectorAll('input, textarea').forEach(input => {
        input.disabled = true;
    });
    
    // Если урок завершен, показываем уведомление
    if (data.lesson_completed) {
        setTimeout(() => {
            alert('Поздравляем! Вы завершили урок!');
            window.location.href = '/lesson/' + lessonSlug + '/';
        }, 2000);
    }
} else {
    resultAlert.className = 'alert alert-danger';
    resultAlert.innerHTML = `
        <h5><i class="bi bi-x-circle"></i> Неправильно</h5>
        <p class="mb-1">Правильный ответ: <strong>${data.correct_answer}</strong></p>
        ${data.explanation ? '<p class="mb-0"><small>' + data.explanation + '</small></p>' : ''}
    `;
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Проверить ответ';
}
```

Валидация данных формы осуществляется на клиентской стороне перед отправкой и на серверной стороне при обработке. Проверяются наличие ответа и корректность формата данных. При обнаружении ошибок пользователь получает уведомления. Код валидации и обработки ошибок приведен в листинге 1.10.

**Листинг 1.10** – Функция валидации и обработки ошибок

```javascript
// Валидация ответа перед отправкой
if (!answer) {
    resultAlert.className = 'alert alert-warning';
    resultAlert.textContent = 'Пожалуйста, введите ответ';
    resultAlert.classList.remove('d-none');
    return;
}

// Обработка ошибок при отправке
try {
    const response = await fetch('/api/exercise/' + exerciseId + '/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ answer: answer })
    });
    
    const data = await response.json();
    
    if (!data.success) {
        alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'));
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Проверить ответ';
    }
} catch (error) {
    alert('Ошибка при отправке ответа: ' + error.message);
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Проверить ответ';
}
```

Интерфейс обеспечивает удобное взаимодействие с пользователем через интуитивно понятные элементы управления, мгновенную обратную связь при проверке ответов и защиту от некорректного ввода данных. Все операции выполняются без перезагрузки страницы через асинхронные запросы к API, что повышает удобство работы с системой обучения английскому языку.

## Страница «Детали урока»

Интерфейс страницы детального просмотра урока состоит из навигационной панели, хлебных крошек и основной рабочей области, разделенной на две колонки. Левая колонка содержит теоретический материал, примеры использования и список упражнений. Правая колонка отображает боковую панель с информацией о прогрессе выполнения урока. Общий вид интерфейса представлен на рисунке 1.3.

![Рисунок 1.3 – Общий вид страницы детального просмотра урока](page_mockups.drawio)

HTML-структура страницы организована с использованием адаптивной сетки Bootstrap. Основная область содержит карточки с теоретическим материалом, примерами и списком упражнений. Боковая панель показывает прогресс выполнения урока с визуализацией в виде прогресс-бара (Листинг 1.13).

**Листинг 1.13** – HTML-структура страницы урока

```html
<div class="container mt-5 pt-4">
  <!-- Хлебные крошки -->
  <nav aria-label="breadcrumb" class="mb-4">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a href="/">Главная</a></li>
      <li class="breadcrumb-item">
        <a href="/category/{{ lesson.category.slug }}/">
          {{ lesson.category.name }}
        </a>
      </li>
      <li class="breadcrumb-item active">{{ lesson.title }}</li>
    </ol>
  </nav>

  <div class="row">
    <!-- Основной контент -->
    <div class="col-lg-8">
      <!-- Теоретический материал -->
      <div class="card mb-4 shadow-sm">
        <div class="card-header bg-primary text-white">
          <h3 class="mb-0">
            <i class="bi bi-book"></i> Теоретический материал
          </h3>
        </div>
        <div class="card-body">
          <div class="theory-content">
            {{ lesson.theory|linebreaks }}
          </div>
        </div>
      </div>

      <!-- Примеры -->
      <div class="card mb-4 shadow-sm">
        <div class="card-header bg-info text-white">
          <h4 class="mb-0">
            <i class="bi bi-lightbulb"></i> Примеры
          </h4>
        </div>
        <div class="card-body">
          <ul class="list-unstyled">
            {% for example in examples_list %}
            <li class="mb-2">
              <i class="bi bi-arrow-right text-primary"></i> 
              <span class="example-text">{{ example }}</span>
            </li>
            {% endfor %}
          </ul>
        </div>
      </div>

      <!-- Упражнения -->
      <div class="card mb-4 shadow-sm">
        <div class="card-header bg-success text-white">
          <h4 class="mb-0">
            <i class="bi bi-pencil-square"></i> Упражнения
          </h4>
        </div>
        <div class="card-body">
          <div class="list-group">
            {% for exercise in exercises %}
            <div class="list-group-item">
              <div class="d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                  <h6 class="mb-1">Упражнение {{ forloop.counter }}</h6>
                  <p class="mb-1 text-muted">{{ exercise.question|truncatewords:15 }}</p>
                  <small class="text-muted">
                    <i class="bi bi-star"></i> {{ exercise.points }} баллов
                  </small>
                </div>
                <div class="ms-3 text-end">
                  {% if exercise.id in exercise_stats %}
                    {% with stats=exercise_stats|get_item:exercise.id %}
                      {% if stats.correct_count > 0 %}
                      <span class="badge bg-success d-block mb-2">
                        <i class="bi bi-check-circle"></i> Выполнено
                      </span>
                      {% else %}
                      <span class="badge bg-secondary d-block mb-2">
                        <i class="bi bi-circle"></i> Не выполнено
                      </span>
                      {% endif %}
                    {% endwith %}
                  {% endif %}
                  <a href="{% url 'exercise_detail' lesson.slug exercise.id %}" 
                     class="btn btn-sm btn-primary">
                    <i class="bi bi-play"></i> Выполнить
                  </a>
                </div>
              </div>
            </div>
            {% endfor %}
          </div>
        </div>
      </div>
    </div>

    <!-- Боковая панель прогресса -->
    <div class="col-lg-4">
      <div class="card shadow-sm sticky-top">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">
            <i class="bi bi-graph-up"></i> Прогресс
          </h5>
        </div>
        <div class="card-body">
          <div class="mb-3">
            <div class="d-flex justify-content-between mb-2">
              <span>Баллы:</span>
              <strong>{{ progress.score }} / {{ progress.total_points }}</strong>
            </div>
            <div class="progress" style="height: 20px;">
              <div class="progress-bar {% if progress.completed %}bg-success{% else %}bg-warning{% endif %}" 
                   role="progressbar" 
                   style="width: {{ progress.percentage }}%">
                {{ progress.percentage }}%
              </div>
            </div>
          </div>
          {% if progress.completed %}
          <div class="alert alert-success">
            <i class="bi bi-check-circle"></i> Урок завершен!
          </div>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
</div>
```

Для визуального оформления страницы урока применялись каскадные таблицы стилей с цветовым кодированием различных секций. Теоретический материал отображается в синей карточке, примеры – в голубой, упражнения – в зеленой. Боковая панель прогресса имеет фиксированное положение при прокрутке страницы. Основные стилевые правила представлены в листинге 1.14.

**Листинг 1.14** – CSS-стили для страницы урока

```css
/* Теоретический контент */
.theory-content {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #495057;
}

.theory-content p {
    margin-bottom: 1rem;
}

/* Примеры */
.example-text {
    font-style: italic;
    color: #6c757d;
    font-size: 1.05rem;
}

/* Липкая боковая панель */
.sticky-top {
    position: sticky;
    top: 80px;
    z-index: 1020;
}

/* Карточки с цветовым кодированием */
.card-header.bg-primary {
    background-color: #0d6efd !important;
}

.card-header.bg-info {
    background-color: #0dcaf0 !important;
}

.card-header.bg-success {
    background-color: #198754 !important;
}

/* Список упражнений */
.list-group-item {
    border-radius: 10px !important;
    margin-bottom: 5px;
    border: 2px solid #e9ecef;
    transition: all 0.3s ease;
}

.list-group-item:hover {
    background-color: #f8f9fa;
    border-color: var(--primary-color);
}
```

Функциональность страницы урока реализована на серверной стороне с использованием Django шаблонов. При загрузке страницы выполняется загрузка теоретического материала, примеров и списка упражнений из базы данных. Для каждого упражнения проверяется статус выполнения пользователем. Код функции загрузки данных урока показан в листинге 1.15.

**Листинг 1.15** – Функция загрузки данных урока

```python
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
    
    # Формируем статистику по упражнениям
    exercise_stats = {}
    for exercise in exercises:
        exercise_attempts = [a for a in attempts if a.exercise_id == exercise.id]
        exercise_stats[exercise.id] = {
            'attempts': exercise_attempts,
            'correct_count': sum(1 for a in exercise_attempts if a.is_correct),
            'total_count': len(exercise_attempts),
        }
    
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
```

Для удобства навигации реализована система хлебных крошек (breadcrumbs), позволяющая пользователю легко перемещаться между разделами приложения. При клике на упражнение происходит переход на страницу выполнения с сохранением контекста урока. Интерфейс обеспечивает интуитивно понятную навигацию и быстрый доступ ко всем элементам урока.

## Дополнительные возможности интерфейса

### Анимации и эффекты

Для улучшения пользовательского опыта реализованы различные анимации и визуальные эффекты. При загрузке страницы элементы появляются с эффектом плавного появления (fade-in), карточки поднимаются при наведении курсора, прогресс-бары анимируются при обновлении значений. Код анимаций представлен в листинге 1.11.

**Листинг 1.11** – CSS-анимации для элементов интерфейса

```css
/* Анимация появления */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Анимация подъема */
@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Анимация прогресс-бара */
@keyframes progressBar {
    from {
        width: 0%;
    }
}

/* Применение анимаций */
.card {
    animation: fadeIn 0.5s ease;
}

.animate-slide-up {
    animation: slideUp 0.6s ease-out;
}

.progress-bar {
    transition: width 0.6s ease;
    animation: progressBar 1s ease-out;
}

/* Эффект при наведении */
.animate-lift-on-hover:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}
```

### Адаптивный дизайн

Интерфейс приложения полностью адаптивен и корректно отображается на различных устройствах: десктопах, планшетах и смартфонах. Использована система сеток Bootstrap 5 с адаптивными классами. Медиа-запросы для мобильных устройств представлены в листинге 1.12.

**Листинг 1.12** – Адаптивные стили для мобильных устройств

```css
/* Адаптивный дизайн */
@media (max-width: 768px) {
    body {
        padding-top: 60px;
    }
    
    .hero-section {
        padding: 2rem 0 !important;
    }
    
    .display-4 {
        font-size: 2rem;
    }
    
    .card-body {
        padding: 1rem;
    }
    
    .btn-lg {
        padding: 10px 20px;
        font-size: 1rem;
    }
}
```

Интерфейс веб-приложения EnglishApp обеспечивает интуитивно понятное взаимодействие с пользователем, современный дизайн с анимациями и полную адаптивность для всех типов устройств, что способствует эффективному обучению английскому языку.

## Описание макетов страниц

В данном разделе представлено детальное описание каждого макета страницы веб-приложения EnglishApp. Все макеты разработаны с использованием единого стиля оформления и адаптивного дизайна.

### Макет 1: Главная страница (Home Page)

**Назначение:** Главная страница приложения служит точкой входа для пользователей и предоставляет обзор доступных категорий уроков и статистики обучения.

**Структура макета:**

1. **Навигационная панель (верхняя часть)**
   - Логотип приложения "EnglishApp" с иконкой перевода
   - Меню навигации: "Главная", "Прогресс", "Настройки"
   - Кнопки аутентификации: "Войти" / "Выйти" (в зависимости от статуса пользователя)
   - Цветовая схема: синий фон (#0d6efd) с белым текстом

2. **Hero-секция (приветственный блок)**
   - Заголовок: "Изучайте английский язык легко и интересно!"
   - Подзаголовок с описанием возможностей приложения
   - Кнопки действий: "Начать обучение" и "Войти" (для неавторизованных пользователей)
   - Цветовая схема: градиент от фиолетового (#667eea) к пурпурному (#764ba2)

3. **Статистические карточки (для авторизованных пользователей)**
   - **Карточка 1:** Количество завершенных уроков
     - Иконка: 📚 (книга)
     - Формат: "5/10 уроков завершено"
     - Цветовая схема: белый фон с синей левой границей
   
   - **Карточка 2:** Общее количество баллов
     - Иконка: ⭐ (звезда)
     - Формат: "250 баллов"
     - Цветовая схема: белый фон с желтой левой границей
   
   - **Карточка 3:** Количество недавних уроков
     - Иконка: 🔥 (огонь)
     - Формат: "3 недавних урока"
     - Цветовая схема: белый фон с красной левой границей

4. **Секция категорий уроков**
   - Заголовок: "Категории уроков" с иконкой папки
   - Карточки категорий (по 3 в ряд на десктопе):
     - **Карточка категории содержит:**
       - Иконка категории (⏰, 📜, 🔮)
       - Название категории (например, "Present Tense")
       - Краткое описание
       - Количество уроков в категории
       - Визуальный прогресс-бар с процентом выполнения
       - Кнопка "Изучать →"
     - Цветовая схема: светлый фон с цветной левой границей (голубая, желтая, красная)

**Особенности макета:**
- Адаптивная сетка: 3 колонки на десктопе, 2 на планшете, 1 на мобильном
- Анимации при наведении: карточки поднимаются вверх с эффектом тени
- Прогресс-бары с анимацией заполнения
- Единый стиль карточек с закругленными углами

### Макет 2: Страница категории (Category Detail Page)

**Назначение:** Страница отображает все уроки, входящие в выбранную категорию, с информацией о прогрессе выполнения каждого урока.

**Структура макета:**

1. **Хлебные крошки (breadcrumbs)**
   - Навигационная цепочка: Главная → Название категории
   - Позволяет быстро вернуться на предыдущий уровень

2. **Заголовок категории**
   - Большая карточка с градиентным фоном (фиолетовый → пурпурный)
   - Иконка категории крупного размера
   - Название категории (например, "Present Tense")
   - Полное описание категории
   - Цветовая схема: градиентный фон с белым текстом

3. **Список уроков**
   - Каждая карточка урока содержит:
     - Иконка урока: 📖 (книга)
     - Название урока (например, "Present Simple")
     - Краткое описание урока
     - Статус выполнения:
       - ✓ Завершен (зеленый бейдж)
       - ⏳ В процессе (желтый бейдж)
       - Отсутствует (серый бейдж)
     - Информация о баллах: "35/45 баллов"
     - Визуальный прогресс-бар с процентом выполнения
     - Кнопка действия: "Продолжить" или "Начать"
   
   - **Цветовая схема карточек:**
     - Завершенный урок: зеленый фон (#d1e7dd) с зеленой границей
     - Урок в процессе: желтый фон (#fff3cd) с желтой границей
     - Не начатый урок: белый фон с серой границей

**Особенности макета:**
- Вертикальное расположение карточек уроков
- Визуальная индикация статуса выполнения
- Адаптивная ширина карточек
- Плавные переходы при наведении

### Макет 3: Страница урока (Lesson Detail Page)

**Назначение:** Страница предоставляет полную информацию об уроке: теоретический материал, примеры использования и список упражнений.

**Структура макета:**

1. **Хлебные крошки**
   - Навигационная цепочка: Главная → Категория → Название урока

2. **Основная область (левая колонка, 8/12 ширины)**

   a. **Карточка теоретического материала**
      - Заголовок: 📚 "Теоретический материал"
      - Цветовая схема: синий фон (#cfe2ff) с синей границей
      - Содержимое:
        - Описание грамматического правила
        - Формулы и структуры
        - Особенности использования
      - Форматирование: нумерованные списки, выделение ключевых моментов

   b. **Карточка примеров**
      - Заголовок: 💡 "Примеры"
      - Цветовая схема: голубой фон (#d1ecf1) с голубой границей
      - Содержимое:
        - Список примеров предложений
        - Формат: маркированный список с иконками стрелок
        - Примеры выделены курсивом

   c. **Карточка упражнений**
      - Заголовок: ✏️ "Упражнения"
      - Цветовая схема: зеленый фон (#d1e7dd) с зеленой границей
      - Содержимое:
        - Список упражнений с нумерацией
        - Для каждого упражнения:
          - Статус выполнения: ✓ Выполнено или [ ] Не выполнено
          - Тип упражнения и количество баллов
          - Кнопка "Выполнить"
        - Формат: вертикальный список с разделителями

3. **Боковая панель (правая колонка, 4/12 ширины)**

   **Карточка прогресса:**
   - Заголовок: 📊 "Прогресс"
   - Цветовая схема: синий фон (#cfe2ff) с синей границей
   - Содержимое:
     - Текущие баллы: "35 / 45"
     - Визуальный прогресс-бар с процентом (78%)
     - Статус завершения: "✓ Урок завершен!" (если применимо)
   - Особенность: фиксированное положение при прокрутке (sticky)

**Особенности макета:**
- Двухколоночная компоновка с адаптивным переключением на одну колонку на мобильных
- Цветовое кодирование секций для быстрой ориентации
- Липкая боковая панель для постоянного отображения прогресса
- Четкое разделение контента по функциональным блокам

### Макет 4: Страница упражнения (Exercise Detail Page)

**Назначение:** Страница для выполнения конкретного упражнения с интерактивной формой ввода ответа и мгновенной проверкой результата.

**Структура макета:**

1. **Хлебные крошки**
   - Навигационная цепочка: Главная → Категория → Урок → Упражнение

2. **Основная карточка упражнения**
   - Заголовок: ✏️ "Упражнение"
   - Цветовая схема: белый фон с синей границей (толщина 3px)
   - Верхняя панель информации:
     - Бейдж с количеством баллов: ⭐ "10 баллов"
     - Бейдж с типом упражнения: "Множественный выбор"
   
   - **Область вопроса:**
     - Текст вопроса крупным шрифтом
     - Пример: "Выберите правильный вариант: I ___ to school every day."
   
   - **Область ввода ответа (зависит от типа упражнения):**
     
     **Для множественного выбора:**
     - Радио-кнопки с вариантами ответов:
       - ○ go
       - ○ goes
       - ○ going
       - ○ went
     - Стиль: список с возможностью выбора одного варианта
     
     **Для заполнения пропусков:**
     - Текстовое поле ввода
     - Плейсхолдер: "Ваш ответ..."
     
     **Для перевода:**
     - Многострочное текстовое поле
     - Плейсхолдер: "Ваш перевод..."
     
     **Для обычного вопроса:**
     - Текстовое поле ввода
     - Плейсхолдер: "Введите ответ..."

   - **Панель действий:**
     - Кнопка "Проверить ответ" (основная, синяя)
     - Кнопка "Назад" (вторичная, серая)

3. **Область результата (появляется после проверки)**
   - **При правильном ответе:**
     - Цветовая схема: зеленый фон (#d1e7dd) с зеленой границей
     - Иконка: ✅
     - Сообщение: "Правильно! Вы заработали 10 баллов!"
     - Дополнительное объяснение (если есть)
   
   - **При неправильном ответе:**
     - Цветовая схема: красный фон с красной границей
     - Иконка: ❌
     - Сообщение: "Неправильно"
     - Показ правильного ответа
     - Дополнительное объяснение (если есть)

4. **История попыток (опционально)**
   - Заголовок: "Предыдущие попытки"
   - Список предыдущих ответов с отметками правильности
   - Временные метки попыток

**Особенности макета:**
- Центрированная компоновка (максимальная ширина 8/12 колонок)
- Динамическое отображение формы в зависимости от типа упражнения
- Мгновенная обратная связь без перезагрузки страницы
- Блокировка формы после правильного ответа
- Анимация появления результата

### Макет 5: Страница прогресса (Progress Page)

**Назначение:** Страница отображает общую статистику обучения пользователя и детальный прогресс по каждой категории.

**Структура макета:**

1. **Заголовок страницы**
   - "Мой прогресс" или "Прогресс обучения"
   - Иконка: 📊

2. **Карточка общей статистики**
   - Цветовая схема: голубой фон (#e7f3ff) с синей границей
   - Содержимое:
     - 📚 Количество завершенных уроков: "5/10 уроков"
     - ⭐ Общее количество баллов: "250 баллов"
     - ✓ Количество правильных ответов: "45/50 правильных"
     - 📈 Процент точности: "90% точность"
   - Формат: горизонтальное расположение метрик в одной строке

3. **Карточка прогресса по категориям**
   - Заголовок: 📁 "Прогресс по категориям"
   - Цветовая схема: желтый фон (#fff3cd) с желтой границей
   - Содержимое:
     - Для каждой категории:
       - Иконка категории (⏰, 📜, 🔮)
       - Название категории
       - Визуальный прогресс-бар с процентом
       - Количество завершенных уроков: "2/2 завершено"
     - Примеры:
       - "⏰ Present Tense: [████████░░ 80%] 2/2 завершено"
       - "📜 Past Tense: [████░░░░░░ 40%] 1/2 завершено"
       - "🔮 Future Tense: [░░░░░░░░░░ 0%] 0/1 завершено"

**Особенности макета:**
- Визуальное представление прогресса через прогресс-бары
- Группировка информации по категориям
- Цветовое кодирование для быстрого восприятия
- Компактное отображение большого объема информации

### Макет 6: Настройки профиля (Profile Settings Page)

**Назначение:** Страница позволяет пользователю просматривать и редактировать информацию своего профиля, а также просматривать личную статистику.

**Структура макета:**

1. **Заголовок страницы**
   - "Настройки профиля" или "Мой профиль"
   - Иконка: ⚙️

2. **Карточка статистики пользователя**
   - Цветовая схема: голубой фон (#e7f3ff) с синей границей
   - Содержимое:
     - 👤 Имя пользователя: "anastasia"
     - 📚 Количество завершенных уроков: "5/10 уроков"
     - ⭐ Общее количество баллов: "250 баллов"
   - Формат: компактное горизонтальное расположение

3. **Карточка формы редактирования профиля**
   - Заголовок: ⚙️ "Редактировать профиль"
   - Цветовая схема: белый фон с синей границей
   - Поля формы:
     - **Имя пользователя:** [anastasia] (нельзя изменить, отображается как текст)
     - **Имя:** [текстовое поле для ввода]
     - **Фамилия:** [текстовое поле для ввода]
     - **Email:** [текстовое поле для ввода]
   - Кнопка действия: "Сохранить изменения" (синяя, основная)

**Особенности макета:**
- Простая и понятная форма редактирования
- Визуальное разделение статистики и формы редактирования
- Защита от изменения имени пользователя
- Валидация полей на клиентской и серверной стороне

### Макет 7: Страница регистрации (Register Page)

**Назначение:** Страница для создания нового аккаунта пользователя в системе.

**Структура макета:**

1. **Заголовок страницы**
   - "Регистрация" или "Создать аккаунт"
   - Иконка: 👤

2. **Карточка формы регистрации**
   - Цветовая схема: белый фон с синей границей
   - Поля формы:
     - **Имя пользователя:** [текстовое поле для ввода]
     - **Email:** [текстовое поле для ввода]
     - **Имя:** [текстовое поле для ввода]
     - **Фамилия:** [текстовое поле для ввода]
     - **Пароль:** [поле для ввода пароля с маскировкой]
     - **Подтверждение пароля:** [поле для ввода пароля с маскировкой]
   - Кнопка действия: "Зарегистрироваться" (синяя, основная)
   - Ссылка: "Уже есть аккаунт? Войти" (переход на страницу входа)

**Особенности макета:**
- Центрированная форма (максимальная ширина 6/12 колонок)
- Валидация полей в реальном времени
- Индикация требований к паролю
- Сообщения об ошибках валидации

### Макет 8: Страница входа (Login Page)

**Назначение:** Страница для аутентификации существующих пользователей в системе.

**Структура макета:**

1. **Заголовок страницы**
   - "Вход" или "Войти в аккаунт"
   - Иконка: 🔐

2. **Карточка формы входа**
   - Цветовая схема: белый фон с синей границей
   - Поля формы:
     - **Имя пользователя:** [текстовое поле для ввода]
     - **Пароль:** [поле для ввода пароля с маскировкой]
   - Кнопка действия: "Войти" (синяя, основная)
   - Ссылка: "Нет аккаунта? Зарегистрироваться" (переход на страницу регистрации)
   - Опционально: чекбокс "Запомнить меня"

**Особенности макета:**
- Минималистичный дизайн с фокусом на простоте входа
- Центрированная форма (максимальная ширина 6/12 колонок)
- Обработка ошибок аутентификации
- Быстрый переход между регистрацией и входом

## Общие принципы дизайна макетов

### Цветовая схема

Приложение использует единую цветовую палитру на основе Bootstrap 5:

- **Основной цвет (Primary):** #0d6efd (синий) - для основных действий и навигации
- **Успех (Success):** #198754 (зеленый) - для завершенных элементов и правильных ответов
- **Предупреждение (Warning):** #ffc107 (желтый) - для элементов в процессе
- **Опасность (Danger):** #dc3545 (красный) - для ошибок и неправильных ответов
- **Информация (Info):** #0dcaf0 (голубой) - для информационных блоков
- **Градиенты:** Фиолетовый (#667eea) → Пурпурный (#764ba2) - для hero-секций

### Типографика

- **Заголовки:** Жирный шрифт, размер от 18px до 24px
- **Основной текст:** Обычный шрифт, размер 14-16px
- **Мелкий текст:** Размер 12px, серый цвет (#6c757d)
- **Шрифт:** 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif

### Компоненты интерфейса

1. **Карточки (Cards):**
   - Закругленные углы (15px)
   - Тень при наведении
   - Цветная левая граница для категоризации
   - Внутренние отступы (padding)

2. **Кнопки (Buttons):**
   - Закругленные углы (10px)
   - Эффект подъема при наведении
   - Размеры: обычные и большие (btn-lg)

3. **Прогресс-бары:**
   - Закругленные углы (10px)
   - Анимация заполнения
   - Цветовое кодирование статуса

4. **Формы:**
   - Закругленные поля ввода (10px)
   - Цветная граница при фокусе
   - Валидация в реальном времени

### Адаптивность

Все макеты адаптированы для трех типов устройств:

- **Десктоп (>992px):** Полная компоновка с несколькими колонками
- **Планшет (768px-992px):** Упрощенная компоновка с 2 колонками
- **Мобильный (<768px):** Одноколоночная компоновка с вертикальным расположением элементов

### Анимации

Применяются следующие анимационные эффекты:

- **Появление элементов:** fadeIn, slideUp
- **При наведении:** подъем карточек, изменение тени
- **Прогресс-бары:** плавное заполнение
- **Кнопки:** эффект подъема при наведении
- **Формы:** подсветка при фокусе

Все макеты страниц разработаны с учетом принципов удобства использования (usability), доступности (accessibility) и современного веб-дизайна, обеспечивая интуитивно понятный и эффективный пользовательский опыт при изучении английского языка.

## Формы создания и редактирования контента

### Форма учета урока

Форма учета урока, включающая таблицу с обязательными параметрами: категория, название урока, описание, теоретический материал, примеры использования, порядок отображения и статус активности. Макет предусматривает возможность добавления, редактирования и сохранения записей в базе данных через административную панель Django.

**Обязательные параметры формы урока:**

1. **Категория урока** (обязательное поле)
   - Выбор из существующих категорий (Present Tense, Past Tense, Future Tense)
   - Связь с моделью `LessonCategory` через внешний ключ
   - Валидация: категория должна существовать в базе данных

2. **Название урока** (обязательное поле)
   - Текстовое поле, максимальная длина 200 символов
   - Автоматическая генерация URL (slug) на основе названия
   - Валидация: название должно быть уникальным в рамках категории

3. **Описание урока** (обязательное поле)
   - Многострочное текстовое поле
   - Краткое описание содержания урока для пользователей
   - Отображается на странице категории

4. **Теоретический материал** (обязательное поле)
   - Многострочное текстовое поле с расширенным редактором
   - Основной контент урока с грамматическими правилами
   - Поддержка форматирования текста (абзацы, списки)
   - Отображается на странице детального просмотра урока

5. **Примеры использования** (обязательное поле)
   - Многострочное текстовое поле
   - Примеры предложений, разделенные новой строкой
   - Автоматическое преобразование в список при отображении
   - Помогает пользователям понять практическое применение правил

6. **Порядок отображения** (обязательное поле)
   - Числовое поле, значение по умолчанию: 0
   - Определяет последовательность уроков в категории
   - Сортировка по возрастанию значения

7. **Статус активности** (обязательное поле)
   - Булево поле (чекбокс)
   - Определяет видимость урока для пользователей
   - Неактивные уроки скрыты из общего списка

**Дополнительные параметры:**

- **URL (slug):** Автоматически генерируется из названия, уникальный идентификатор для URL-адреса
- **Дата создания:** Автоматически устанавливается при создании записи
- **Связанные упражнения:** Отображаются в inline-форме при редактировании урока

**Функциональность формы:**

- **Добавление записи:** Создание нового урока с заполнением всех обязательных полей
- **Редактирование записи:** Изменение параметров существующего урока
- **Сохранение в БД:** Валидация данных и сохранение в таблицу `lessons_lesson`
- **Inline-редактирование упражнений:** Возможность добавления упражнений непосредственно в форме урока
- **Предпросмотр:** Отображение количества связанных упражнений в списке уроков

### Форма учета упражнения

Форма учета упражнения, включающая таблицу с обязательными параметрами: урок, тип упражнения, вопрос/задание, правильный ответ, варианты ответов (для множественного выбора), баллы за выполнение, порядок отображения и объяснение правильного ответа. Макет предусматривает возможность добавления, редактирования и сохранения записей в базе данных через административную панель Django.

**Обязательные параметры формы упражнения:**

1. **Урок** (обязательное поле)
   - Выбор из существующих уроков
   - Связь с моделью `Lesson` через внешний ключ
   - Валидация: урок должен существовать в базе данных
   - Группировка упражнений по урокам

2. **Тип упражнения** (обязательное поле)
   - Выпадающий список с вариантами:
     - **Множественный выбор** (Multiple Choice) - выбор одного правильного варианта из нескольких
     - **Заполнение пропусков** (Fill Blank) - ввод текста в пропущенное место
     - **Перевод** (Translation) - перевод предложения на английский язык
     - **Вопрос** (Question) - ответ на вопрос в свободной форме
   - Определяет интерфейс выполнения упражнения пользователем

3. **Вопрос/Задание** (обязательное поле)
   - Многострочное текстовое поле
   - Формулировка задания для пользователя
   - Может содержать примеры, подсказки, контекст
   - Отображается на странице выполнения упражнения

4. **Правильный ответ** (обязательное поле)
   - Текстовое поле
   - Для типа "Перевод": можно указать несколько вариантов через символ "|" (например, "go|goes")
   - Используется для автоматической проверки ответа пользователя
   - Сравнение выполняется без учета регистра и лишних пробелов

5. **Варианты ответов** (обязательное для множественного выбора)
   - JSON-поле для хранения массива вариантов
   - Формат: `["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"]`
   - Используется только для типа "Множественный выбор"
   - Минимум 2 варианта, рекомендуется 3-4 варианта
   - Один из вариантов должен совпадать с правильным ответом

6. **Баллы за выполнение** (обязательное поле)
   - Числовое поле, значение по умолчанию: 10
   - Диапазон значений: от 1 до 100 баллов
   - Начисляются пользователю при правильном ответе
   - Влияют на общий прогресс урока

7. **Порядок отображения** (обязательное поле)
   - Числовое поле, значение по умолчанию: 0
   - Определяет последовательность упражнений в уроке
   - Сортировка по возрастанию значения

**Дополнительные параметры:**

- **Объяснение** (опциональное поле)
  - Многострочное текстовое поле
  - Пояснение правильного ответа
  - Отображается пользователю после проверки ответа
  - Помогает понять ошибки и закрепить материал

**Функциональность формы:**

- **Добавление записи:** Создание нового упражнения с заполнением всех обязательных полей
- **Редактирование записи:** Изменение параметров существующего упражнения
- **Сохранение в БД:** Валидация данных и сохранение в таблицу `lessons_exercise`
- **Валидация вариантов ответов:** Проверка корректности JSON-формата для множественного выбора
- **Предпросмотр:** Отображение типа упражнения и вариантов ответов в списке
- **Связь с уроком:** Автоматическое обновление общего количества баллов урока при изменении баллов упражнения

**Особенности работы с формой:**

- **Динамическая валидация:** В зависимости от выбранного типа упражнения меняются требования к полям
- **Inline-добавление:** Упражнения можно добавлять непосредственно при создании/редактировании урока
- **Массовое редактирование:** Возможность изменения порядка и баллов для нескольких упражнений одновременно
- **Поиск и фильтрация:** Поиск по тексту вопроса, фильтрация по типу упражнения и уроку
- **Защита данных:** Валидация на уровне модели и формы предотвращает сохранение некорректных данных

Обе формы интегрированы в административную панель Django и обеспечивают полный цикл управления образовательным контентом: от создания урока до добавления упражнений и их последующего редактирования. Все операции выполняются с валидацией данных и сохранением в реляционную базу данных PostgreSQL/SQLite, что гарантирует целостность и согласованность данных в системе обучения английскому языку.

