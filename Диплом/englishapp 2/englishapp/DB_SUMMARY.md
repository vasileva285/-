# Краткая сводка по базе данных EnglishApp

## 📊 Структура БД

База данных состоит из **5 основных таблиц**:

1. **lessons_lessoncategory** - Категории уроков (Present, Past, Future)
2. **lessons_lesson** - Уроки с теорией и примерами
3. **lessons_exercise** - Упражнения (4 типа)
4. **lessons_userprogress** - Прогресс пользователей по урокам
5. **lessons_userexerciseattempt** - Попытки выполнения упражнений

## 🔗 Связи

```
User → UserProgress → Lesson → Exercise
  ↓                      ↑        ↓
UserExerciseAttempt ─────┴────────┘
         ↑
         └── LessonCategory
```

## 📁 Файлы документации

- **DATABASE_SCHEMA.md** - Полное описание структуры БД с SQL запросами
- **DB_VISUALIZATION.txt** - Визуальная диаграмма связей
- **visualize_db.py** - Скрипт для просмотра текущих данных в БД

## 🚀 Быстрый просмотр структуры

```bash
# Просмотр текущих данных
python visualize_db.py

# Просмотр SQL схемы
python manage.py sqlmigrate lessons 0001
```

## 📈 Текущая статистика

Запустите `python visualize_db.py` для просмотра:
- Количество категорий, уроков, упражнений
- Количество пользователей и их прогресс
- Статистика попыток выполнения упражнений

---

**Подробная документация:** См. `DATABASE_SCHEMA.md`

