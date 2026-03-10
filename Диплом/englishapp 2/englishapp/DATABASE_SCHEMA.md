# Структура базы данных EnglishApp

## 📊 Общая схема

База данных состоит из 5 основных таблиц, связанных между собой:

```
User (Django встроенная)
    ↓
    ├── UserProgress (Прогресс пользователя)
    └── UserExerciseAttempt (Попытки выполнения упражнений)

LessonCategory (Категории уроков)
    ↓
    └── Lesson (Уроки)
        └── Exercise (Упражнения)
            └── UserExerciseAttempt (Попытки выполнения)
```

## 🗂️ Таблицы базы данных

### 1. **lessons_lessoncategory** (Категории уроков)

Хранит категории уроков (Present, Past, Future и т.д.)

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT |
| `name` | VARCHAR(100) | Название категории | NOT NULL |
| `slug` | VARCHAR(50) | URL-адрес категории | UNIQUE, NOT NULL |
| `description` | TEXT | Описание категории | NOT NULL |
| `order` | INTEGER | Порядок сортировки | DEFAULT 0 |
| `icon` | VARCHAR(50) | Иконка (эмодзи) | DEFAULT '📚' |

**Пример данных:**
```
id | name                    | slug      | description                    | order | icon
---|-------------------------|-----------|--------------------------------|-------|-----
1  | Present Tense           | present   | Изучите настоящее время...     | 1     | ⏰
2  | Past Tense              | past      | Изучите прошедшее время...     | 2     | 📜
3  | Future Tense            | future    | Изучите будущее время...       | 3     | 🔮
```

---

### 2. **lessons_lesson** (Уроки)

Хранит уроки с теоретическим материалом

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT |
| `category_id` | INTEGER | Ссылка на категорию | FOREIGN KEY → lessons_lessoncategory.id |
| `title` | VARCHAR(200) | Название урока | NOT NULL |
| `slug` | VARCHAR(200) | URL-адрес урока | UNIQUE, NOT NULL |
| `description` | TEXT | Описание урока | NOT NULL |
| `theory` | TEXT | Теоретический материал | NOT NULL |
| `examples` | TEXT | Примеры использования | NOT NULL |
| `order` | INTEGER | Порядок в категории | DEFAULT 0 |
| `is_active` | BOOLEAN | Активен ли урок | DEFAULT TRUE |
| `created_at` | DATETIME | Дата создания | AUTO, NOT NULL |

**Связи:**
- `category_id` → `lessons_lessoncategory.id` (Many-to-One)

**Пример данных:**
```
id | category_id | title           | slug            | description              | order | is_active
---|-------------|-----------------|-----------------|--------------------------|-------|----------
1  | 1           | Present Simple  | present-simple  | Изучите простое...       | 1     | 1
2  | 1           | Present Cont.   | present-cont    | Изучите длительное...     | 2     | 1
3  | 2           | Past Simple     | past-simple     | Изучите простое...       | 1     | 1
```

---

### 3. **lessons_exercise** (Упражнения)

Хранит упражнения для уроков

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT |
| `lesson_id` | INTEGER | Ссылка на урок | FOREIGN KEY → lessons_lesson.id |
| `exercise_type` | VARCHAR(20) | Тип упражнения | NOT NULL, CHOICES |
| `question` | TEXT | Вопрос/Задание | NOT NULL |
| `correct_answer` | TEXT | Правильный ответ | NOT NULL |
| `options` | JSON | Варианты ответов (для множественного выбора) | DEFAULT [] |
| `explanation` | TEXT | Объяснение ответа | NULL |
| `order` | INTEGER | Порядок в уроке | DEFAULT 0 |
| `points` | INTEGER | Баллы за упражнение | DEFAULT 10, 1-100 |

**Типы упражнений (exercise_type):**
- `multiple_choice` - Множественный выбор
- `fill_blank` - Заполнение пропусков
- `translation` - Перевод
- `question` - Вопрос

**Связи:**
- `lesson_id` → `lessons_lesson.id` (Many-to-One)

**Пример данных:**
```
id | lesson_id | exercise_type   | question                    | correct_answer | points | order
---|-----------|----------------|-----------------------------|----------------|--------|-------
1  | 1         | multiple_choice| Выберите правильный...      | go             | 10     | 1
2  | 1         | fill_blank     | Заполните пропуск...        | works          | 10     | 2
3  | 1         | translation    | Переведите на английский...| I work every... | 15     | 3
```

**Пример JSON для options (множественный выбор):**
```json
["go", "goes", "going", "went"]
```

---

### 4. **lessons_userprogress** (Прогресс пользователя)

Отслеживает прогресс пользователя по урокам

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT |
| `user_id` | INTEGER | Ссылка на пользователя | FOREIGN KEY → auth_user.id |
| `lesson_id` | INTEGER | Ссылка на урок | FOREIGN KEY → lessons_lesson.id |
| `completed` | BOOLEAN | Завершен ли урок | DEFAULT FALSE |
| `score` | INTEGER | Заработанные баллы | DEFAULT 0 |
| `total_points` | INTEGER | Всего возможных баллов | DEFAULT 0 |
| `started_at` | DATETIME | Дата начала урока | AUTO, NOT NULL |
| `completed_at` | DATETIME | Дата завершения урока | NULL |

**Связи:**
- `user_id` → `auth_user.id` (Many-to-One)
- `lesson_id` → `lessons_lesson.id` (Many-to-One)

**Уникальность:**
- UNIQUE(user_id, lesson_id) - один пользователь может иметь только один прогресс по уроку

**Пример данных:**
```
id | user_id | lesson_id | completed | score | total_points | started_at          | completed_at
---|---------|-----------|-----------|-------|--------------|---------------------|------------------
1  | 1       | 1         | 1         | 35    | 45           | 2024-01-15 10:00:00 | 2024-01-15 11:30:00
2  | 1       | 2         | 0         | 20    | 45           | 2024-01-16 09:00:00 | NULL
3  | 2       | 1         | 1         | 45    | 45           | 2024-01-14 14:00:00 | 2024-01-14 15:00:00
```

---

### 5. **lessons_userexerciseattempt** (Попытки выполнения упражнений)

Хранит все попытки пользователей выполнить упражнения

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Первичный ключ | PRIMARY KEY, AUTO_INCREMENT |
| `user_id` | INTEGER | Ссылка на пользователя | FOREIGN KEY → auth_user.id |
| `exercise_id` | INTEGER | Ссылка на упражнение | FOREIGN KEY → lessons_exercise.id |
| `user_answer` | TEXT | Ответ пользователя | NOT NULL |
| `is_correct` | BOOLEAN | Правильность ответа | NOT NULL |
| `points_earned` | INTEGER | Заработанные баллы | DEFAULT 0 |
| `attempted_at` | DATETIME | Дата попытки | AUTO, NOT NULL |

**Связи:**
- `user_id` → `auth_user.id` (Many-to-One)
- `exercise_id` → `lessons_exercise.id` (Many-to-One)

**Пример данных:**
```
id | user_id | exercise_id | user_answer | is_correct | points_earned | attempted_at
---|---------|-------------|-------------|------------|---------------|------------------
1  | 1       | 1           | go          | 1          | 10            | 2024-01-15 10:05:00
2  | 1       | 2           | work        | 0          | 0             | 2024-01-15 10:10:00
3  | 1       | 2           | works       | 1          | 10            | 2024-01-15 10:12:00
4  | 1       | 3           | I work...   | 1          | 15            | 2024-01-15 10:15:00
```

---

## 🔗 Схема связей (ER-диаграмма)

```
┌─────────────────┐
│  auth_user      │
│  (Django)       │
└────────┬────────┘
         │
         ├─────────────────────────────────┐
         │                                 │
         ▼                                 ▼
┌──────────────────────┐      ┌──────────────────────────────┐
│ lessons_userprogress │      │ lessons_userexerciseattempt  │
│                      │      │                              │
│ - user_id (FK)      │      │ - user_id (FK)               │
│ - lesson_id (FK)    │      │ - exercise_id (FK)           │
│ - completed         │      │ - user_answer                 │
│ - score             │      │ - is_correct                  │
│ - total_points      │      │ - points_earned               │
└──────────┬──────────┘      └──────────────┬───────────────┘
           │                                │
           │                                │
           ▼                                ▼
┌──────────────────────┐      ┌──────────────────────────────┐
│ lessons_lesson       │      │ lessons_exercise             │
│                      │      │                              │
│ - category_id (FK)   │◄─────│ - lesson_id (FK)             │
│ - title              │      │ - exercise_type             │
│ - theory             │      │ - question                   │
│ - examples           │      │ - correct_answer             │
│ - is_active          │      │ - options (JSON)             │
└──────────┬───────────┘      │ - points                     │
           │                  └──────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│ lessons_lessoncategory│
│                      │
│ - name               │
│ - slug               │
│ - description        │
│ - icon               │
│ - order              │
└──────────────────────┘
```

---

## 📈 Типы связей

### One-to-Many (Один ко многим)

1. **LessonCategory → Lesson**
   - Одна категория может содержать много уроков
   - Один урок принадлежит одной категории

2. **Lesson → Exercise**
   - Один урок может содержать много упражнений
   - Одно упражнение принадлежит одному уроку

3. **User → UserProgress**
   - Один пользователь может иметь прогресс по многим урокам
   - Один прогресс принадлежит одному пользователю

4. **User → UserExerciseAttempt**
   - Один пользователь может иметь много попыток
   - Одна попытка принадлежит одному пользователю

5. **Lesson → UserProgress**
   - Один урок может иметь прогресс от многих пользователей
   - Один прогресс относится к одному уроку

6. **Exercise → UserExerciseAttempt**
   - Одно упражнение может иметь много попыток
   - Одна попытка относится к одному упражнению

---

## 🔍 Примеры запросов

### Получить все уроки категории "Present"
```sql
SELECT * FROM lessons_lesson 
WHERE category_id = (
    SELECT id FROM lessons_lessoncategory WHERE slug = 'present'
);
```

### Получить прогресс пользователя
```sql
SELECT 
    l.title,
    up.score,
    up.total_points,
    up.completed
FROM lessons_userprogress up
JOIN lessons_lesson l ON up.lesson_id = l.id
WHERE up.user_id = 1;
```

### Получить статистику по упражнениям
```sql
SELECT 
    e.question,
    COUNT(uea.id) as total_attempts,
    SUM(CASE WHEN uea.is_correct THEN 1 ELSE 0 END) as correct_attempts
FROM lessons_exercise e
LEFT JOIN lessons_userexerciseattempt uea ON e.id = uea.exercise_id
GROUP BY e.id;
```

### Получить все упражнения урока с правильными ответами пользователя
```sql
SELECT 
    e.question,
    e.exercise_type,
    uea.user_answer,
    uea.is_correct,
    uea.attempted_at
FROM lessons_exercise e
LEFT JOIN lessons_userexerciseattempt uea 
    ON e.id = uea.exercise_id AND uea.user_id = 1
WHERE e.lesson_id = 1
ORDER BY e.order;
```

---

## 📊 Статистика и аналитика

### Таблицы для статистики:

1. **Прогресс по категориям:**
```sql
SELECT 
    lc.name,
    COUNT(DISTINCT up.user_id) as users_count,
    AVG(CASE WHEN up.completed THEN 1.0 ELSE 0.0 END) * 100 as completion_rate
FROM lessons_lessoncategory lc
LEFT JOIN lessons_lesson l ON lc.id = l.category_id
LEFT JOIN lessons_userprogress up ON l.id = up.lesson_id
GROUP BY lc.id;
```

2. **Топ пользователей по баллам:**
```sql
SELECT 
    u.username,
    SUM(up.score) as total_score
FROM auth_user u
JOIN lessons_userprogress up ON u.id = up.user_id
GROUP BY u.id
ORDER BY total_score DESC
LIMIT 10;
```

3. **Сложность упражнений (по проценту правильных ответов):**
```sql
SELECT 
    e.id,
    e.question,
    COUNT(uea.id) as attempts,
    AVG(CASE WHEN uea.is_correct THEN 1.0 ELSE 0.0 END) * 100 as success_rate
FROM lessons_exercise e
LEFT JOIN lessons_userexerciseattempt uea ON e.id = uea.exercise_id
GROUP BY e.id
ORDER BY success_rate ASC;
```

---

## 🗄️ Индексы

Для оптимизации производительности созданы следующие индексы:

- `lessons_lessoncategory.slug` - UNIQUE
- `lessons_lesson.slug` - UNIQUE
- `lessons_lesson.category_id` - INDEX
- `lessons_exercise.lesson_id` - INDEX
- `lessons_userprogress(user_id, lesson_id)` - UNIQUE
- `lessons_userexerciseattempt.user_id` - INDEX
- `lessons_userexerciseattempt.exercise_id` - INDEX
- `lessons_userexerciseattempt.attempted_at` - INDEX

---

## 💾 Размер базы данных

**Примерные размеры (для 1000 пользователей, 50 уроков, 200 упражнений):**

- `lessons_lessoncategory`: ~5 KB (3-5 категорий)
- `lessons_lesson`: ~500 KB (50 уроков с теорией)
- `lessons_exercise`: ~100 KB (200 упражнений)
- `lessons_userprogress`: ~200 KB (1000 пользователей × 50 уроков × 40% активности)
- `lessons_userexerciseattempt`: ~5 MB (1000 пользователей × 10 попыток × 500 байт)

**Общий размер:** ~6 MB

---

## 🔐 Безопасность

- Все внешние ключи имеют `ON DELETE CASCADE` - при удалении родительской записи удаляются дочерние
- Пользователи не могут напрямую изменять данные других пользователей
- Все запросы проходят через Django ORM с валидацией

---

**База данных оптимизирована для быстрого доступа и масштабируемости!** 🚀

