from django.core.management.base import BaseCommand
from lessons.models import LessonCategory, Lesson, Exercise


class Command(BaseCommand):
    help = 'Загружает начальные данные для приложения (категории, уроки, упражнения)'

    def handle(self, *args, **options):
        self.stdout.write('Создание категорий уроков...')
        
        # Создаем категории
        present_category, created = LessonCategory.objects.get_or_create(
            slug='present',
            defaults={
                'name': 'Present Tense (Настоящее время)',
                'description': 'Изучите настоящее время в английском языке: Present Simple, Present Continuous, Present Perfect.',
                'order': 1,
                'icon': '⏰'
            }
        )
        
        past_category, created = LessonCategory.objects.get_or_create(
            slug='past',
            defaults={
                'name': 'Past Tense (Прошедшее время)',
                'description': 'Изучите прошедшее время в английском языке: Past Simple, Past Continuous, Past Perfect.',
                'order': 2,
                'icon': '📜'
            }
        )
        
        future_category, created = LessonCategory.objects.get_or_create(
            slug='future',
            defaults={
                'name': 'Future Tense (Будущее время)',
                'description': 'Изучите будущее время в английском языке: Future Simple, Future Continuous, Future Perfect.',
                'order': 3,
                'icon': '🔮'
            }
        )

        games_category, created = LessonCategory.objects.get_or_create(
            slug='games',
            defaults={
                'name': 'Игры и мини‑тесты',
                'description': 'Мини‑игры для тренировки времен и слов в контексте.',
                'order': 4,
                'icon': '🎮'
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Категории созданы!'))
        
        # Создаем уроки для Present Tense
        self.stdout.write('Создание уроков для Present Tense...')
        
        lesson1, created = Lesson.objects.get_or_create(
            slug='present-simple',
            defaults={
                'category': present_category,
                'title': 'Present Simple',
                'description': 'Изучите простое настоящее время - основу английской грамматики.',
                'theory': '''Present Simple используется для выражения:
1. Постоянных действий и фактов: "The sun rises in the east" (Солнце встает на востоке)
2. Привычек и регулярных действий: "I go to school every day" (Я хожу в школу каждый день)
3. Расписаний и программ: "The train leaves at 8 AM" (Поезд отправляется в 8 утра)

Формула:
- Утверждение: I/You/We/They + глагол (work)
- Утверждение: He/She/It + глагол + s/es (works)
- Отрицание: do/does + not + глагол
- Вопрос: Do/Does + подлежащее + глагол?''',
                'examples': '''I work every day.
She works in a hospital.
They don't like coffee.
Does he speak English?
We usually have breakfast at 8 AM.''',
                'order': 1
            }
        )
        
        lesson2, created = Lesson.objects.get_or_create(
            slug='present-continuous',
            defaults={
                'category': present_category,
                'title': 'Present Continuous',
                'description': 'Изучите настоящее длительное время для действий, происходящих сейчас.',
                'theory': '''Present Continuous используется для выражения:
1. Действий, происходящих в момент речи: "I am reading a book now" (Я читаю книгу сейчас)
2. Временных действий: "She is working in London this month" (Она работает в Лондоне в этом месяце)
3. Планов на ближайшее будущее: "We are going to the cinema tonight" (Мы идем в кино сегодня вечером)

Формула:
- Утверждение: am/is/are + глагол + ing
- Отрицание: am/is/are + not + глагол + ing
- Вопрос: Am/Is/Are + подлежащее + глагол + ing?''',
                'examples': '''I am reading a book now.
She is cooking dinner.
They are not playing football.
Are you listening to me?
He is studying at the moment.''',
                'order': 2
            }
        )
        
        # Создаем уроки для Past Tense
        self.stdout.write('Создание уроков для Past Tense...')
        
        lesson3, created = Lesson.objects.get_or_create(
            slug='past-simple',
            defaults={
                'category': past_category,
                'title': 'Past Simple',
                'description': 'Изучите простое прошедшее время для действий в прошлом.',
                'theory': '''Past Simple используется для выражения:
1. Завершенных действий в прошлом: "I visited Paris last year" (Я посетил Париж в прошлом году)
2. Последовательности действий: "I woke up, brushed my teeth, and had breakfast" (Я проснулся, почистил зубы и позавтракал)
3. Привычек в прошлом: "When I was young, I played football" (Когда я был молодым, я играл в футбол)

Формула:
- Утверждение: глагол + ed (правильные) или вторая форма (неправильные)
- Отрицание: did + not + глагол (в первой форме)
- Вопрос: Did + подлежащее + глагол (в первой форме)?''',
                'examples': '''I visited London last summer.
She didn't go to school yesterday.
Did you see that movie?
We played tennis yesterday.
He didn't finish his homework.''',
                'order': 1
            }
        )
        
        # Создаем уроки для Future Tense
        self.stdout.write('Создание уроков для Future Tense...')
        
        lesson4, created = Lesson.objects.get_or_create(
            slug='future-simple',
            defaults={
                'category': future_category,
                'title': 'Future Simple',
                'description': 'Изучите простое будущее время для действий в будущем.',
                'theory': '''Future Simple используется для выражения:
1. Спонтанных решений: "I'll help you" (Я помогу тебе)
2. Предсказаний: "It will rain tomorrow" (Завтра будет дождь)
3. Обещаний: "I will call you later" (Я позвоню тебе позже)

Формула:
- Утверждение: will/shall + глагол (в первой форме)
- Отрицание: will/shall + not + глагол
- Вопрос: Will/Shall + подлежащее + глагол?

Сокращения: will not = won't, shall not = shan't''',
                'examples': '''I will go to the store tomorrow.
She won't come to the party.
Will you help me?
They will finish the project next week.
I shall return soon.''',
                'order': 1
            }
        )

        # Мини‑игра "Угадай время"
        self.stdout.write('Создание мини‑игр...')

        guess_tense_lesson, created = Lesson.objects.get_or_create(
            slug='guess-the-tense',
            defaults={
                'category': games_category,
                'title': 'Игра: Угадай время',
                'description': 'Читаем предложение или короткую историю и выбираем, в каком времени оно написано.',
                'theory': '''В этой мини‑игре вы тренируете распознавание времен.

1. Читайте предложение или маленький контекст.
2. Выберите, какое это время: Present, Past или Future (иногда с указанием вида, например Present Continuous).
3. Получайте мгновенную проверку и объяснение.

Пример:
"He is cooking dinner now" → Present Continuous (настоящее длительное время).''',
                'examples': '''He is cooking dinner now.
I visited London last summer.
They will finish the project next week.''',
                'order': 1
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Уроки созданы!'))
        
        # Создаем упражнения для Present Simple
        self.stdout.write('Создание упражнений...')
        
        # Упражнения для lesson1 (Present Simple)
        Exercise.objects.get_or_create(
            lesson=lesson1,
            order=1,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Выберите правильный вариант: I ___ to school every day.',
                'correct_answer': 'go',
                'options': ['go', 'goes', 'going', 'went'],
                'explanation': 'С подлежащим "I" используется форма "go" без окончания.',
                'points': 10
            }
        )
        
        Exercise.objects.get_or_create(
            lesson=lesson1,
            order=2,
            defaults={
                'exercise_type': 'fill_blank',
                'question': 'Заполните пропуск: She ___ (work) in a hospital.',
                'correct_answer': 'works',
                'explanation': 'С подлежащим "She" (3-е лицо единственного числа) глагол принимает окончание -s.',
                'points': 10
            }
        )
        
        Exercise.objects.get_or_create(
            lesson=lesson1,
            order=3,
            defaults={
                'exercise_type': 'translation',
                'question': 'Переведите на английский: "Они не любят кофе."',
                'correct_answer': 'They don\'t like coffee|They do not like coffee',
                'explanation': 'Отрицание в Present Simple: do/does + not + глагол.',
                'points': 15
            }
        )
        
        Exercise.objects.get_or_create(
            lesson=lesson1,
            order=4,
            defaults={
                'exercise_type': 'question',
                'question': 'Составьте вопрос: ___ he speak English?',
                'correct_answer': 'Does',
                'explanation': 'Вопрос в Present Simple начинается с Do/Does.',
                'points': 10
            }
        )
        
        # Упражнения для lesson2 (Present Continuous)
        Exercise.objects.get_or_create(
            lesson=lesson2,
            order=1,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Выберите правильный вариант: I ___ a book now.',
                'correct_answer': 'am reading',
                'options': ['am reading', 'read', 'reads', 'reading'],
                'explanation': 'Present Continuous: am/is/are + глагол + ing.',
                'points': 10
            }
        )
        
        Exercise.objects.get_or_create(
            lesson=lesson2,
            order=2,
            defaults={
                'exercise_type': 'fill_blank',
                'question': 'Заполните пропуск: She ___ (cook) dinner now.',
                'correct_answer': 'is cooking',
                'explanation': 'С подлежащим "She" используется "is" + глагол + ing.',
                'points': 10
            }
        )
        
        # Упражнения для lesson3 (Past Simple)
        Exercise.objects.get_or_create(
            lesson=lesson3,
            order=1,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Выберите правильный вариант: I ___ London last summer.',
                'correct_answer': 'visited',
                'options': ['visit', 'visits', 'visited', 'visiting'],
                'explanation': 'Past Simple: глагол + ed для правильных глаголов.',
                'points': 10
            }
        )
        
        Exercise.objects.get_or_create(
            lesson=lesson3,
            order=2,
            defaults={
                'exercise_type': 'fill_blank',
                'question': 'Заполните пропуск: She ___ (not go) to school yesterday.',
                'correct_answer': "didn't go",
                'explanation': 'Отрицание в Past Simple: did + not + глагол в первой форме.',
                'points': 10
            }
        )
        
        # Упражнения для lesson4 (Future Simple)
        Exercise.objects.get_or_create(
            lesson=lesson4,
            order=1,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Выберите правильный вариант: I ___ to the store tomorrow.',
                'correct_answer': 'will go',
                'options': ['go', 'will go', 'going', 'went'],
                'explanation': 'Future Simple: will + глагол в первой форме.',
                'points': 10
            }
        )
        
        Exercise.objects.get_or_create(
            lesson=lesson4,
            order=2,
            defaults={
                'exercise_type': 'translation',
                'question': 'Переведите на английский: "Я помогу тебе завтра."',
                'correct_answer': 'I will help you tomorrow|I\'ll help you tomorrow',
                'explanation': 'Future Simple для обещаний и планов.',
                'points': 15
            }
        )

        # Мини‑игра "Угадай время": выбор времени по предложению/истории
        Exercise.objects.get_or_create(
            lesson=guess_tense_lesson,
            order=1,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Прочитайте: "He is cooking dinner now." Какое это время?',
                'correct_answer': 'Present Continuous',
                'options': ['Present Simple', 'Present Continuous', 'Past Simple', 'Future Simple'],
                'explanation': 'Форма am/is/are + глагол + ing показывает Present Continuous: действие происходит прямо сейчас.',
                'points': 10
            }
        )

        Exercise.objects.get_or_create(
            lesson=guess_tense_lesson,
            order=2,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Прочитайте: "I visited London last summer." Какое это время?',
                'correct_answer': 'Past Simple',
                'options': ['Present Simple', 'Past Simple', 'Present Perfect', 'Future Simple'],
                'explanation': 'Есть указание на завершенный момент в прошлом (last summer) и прошедшая форма глагола visited → Past Simple.',
                'points': 10
            }
        )

        Exercise.objects.get_or_create(
            lesson=guess_tense_lesson,
            order=3,
            defaults={
                'exercise_type': 'multiple_choice',
                'question': 'Прочитайте: "They will finish the project next week." Какое это время?',
                'correct_answer': 'Future Simple',
                'options': ['Present Continuous', 'Past Simple', 'Future Simple', 'Present Perfect'],
                'explanation': 'Сочетание will + глагол (finish) + указание на будущее (next week) → Future Simple.',
                'points': 10
            }
        )

        self.stdout.write(self.style.SUCCESS('Упражнения созданы!'))
        self.stdout.write(self.style.SUCCESS('\nВсе начальные данные успешно загружены!'))
        self.stdout.write(self.style.SUCCESS('Теперь вы можете запустить сервер и начать использовать приложение.'))

