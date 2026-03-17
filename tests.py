import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

        # Тест 1 -  метод, который тестируем - add_new_book_
    # 1.1. положительный тест - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector() 

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # книги попали в словарь
        assert len(collector.get_books_genre()) == 2
        assert 'Гордость и предубеждение и зомби' in collector.get_books_genre()
        assert 'Что делать, если ваш кот хочет вас убить' in collector.get_books_genre()

       #1.2. дубликат не добавился
    def test_add_new_book_not_add_duplicate(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Гордость и предубеждение и зомби')  # второй раз
        # дубликат не добавился
        assert len(collector.get_books_genre()) == 1

        #1.3.  Граничные значения, параметризация и негативные тесты (0, 1 и 40, 41 знаков)
    @pytest.mark.parametrize(
        'name, add',
        [
            ('', False),                 # длина 0  -> не добавить
            ('A', True),                 # длина 1  -> добавить
            ('A' * 40, True),            # длина 40 -> добавить
            ('A' * 41, False),           # длина 41 -> не добавить
        ]
    )
    def test_add_new_book_boundary_tests(self, name, add):
        collector = BooksCollector()

        collector.add_new_book(name)

        if add:
            assert name in collector.get_books_genre()
        else:
            assert name not in collector.get_books_genre()

        #2.  Тесты на метод set_book_genre(self, name, genre)

        # 2.1. положительный тест - правильное соответствие, добавляет
    def test_set_book_genre_set_for_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        assert collector.get_book_genre('Гордость и предубеждение и зомби') == 'Ужасы'

        # 2.2. негативный тест - Книги нет в коллекции — жанр не должен установиться
    def test_set_book_genre_not_set_if_book_not_exists(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая книга', 'Ужасы')
        assert collector.get_book_genre('Несуществующая книга') is None

        # 2.3. негативный тест - Жанра не существует
    def test_set_book_genre_not_set_if_genre_invalid(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Нонфикшен')
    # жанр не определился, осталась пустая строка 
        assert collector.get_book_genre('Гордость и предубеждение и зомби') == ''

 
        #3.  Тесты на метод get_book_genre(self, name)

        # 3.1. положительный тест получаем жанр книги по её имени
    def test_get_book_genre_genre_true(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        assert collector.get_book_genre('Гордость и предубеждение и зомби') == 'Ужасы'   

        # 3.2. негативный тест - Книги нет в коллекции
    def test_get_book_genre_book_not_exists(self):
        collector = BooksCollector()
        result = collector.get_book_genre('Несуществующая книга')
        assert result is None  # dict.get()  None для несуществующего ключа

        # 3.3. тест параметризацией на 3 варианта (жанр, без жанра и несущ.книги)
    @pytest.mark.parametrize(
    'book_name, expected_result',
    [
        ('Гордость и предубеждение и зомби', 'Ужасы'),  # книга с жанром
        ('Книга без жанра', ''),                       # книга без жанра
        ('Несуществующая', None),                      # книги нет
    ]
)
    def test_get_book_genre_all_cases(self, book_name, expected_result):
        collector = BooksCollector()
    
        if book_name == 'Гордость и предубеждение и зомби':
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, 'Ужасы')
        elif book_name == 'Книга без жанра':
            collector.add_new_book(book_name)
        result = collector.get_book_genre(book_name)
        assert result == expected_result


        #4. Тесты на get_books_with_specific_genre(self, genre) - выводим список книг с определённым жанром
        # 4.1. положительный тест - выводит список с опр. жанром
    def test_get_books_with_specific_genre_add_list_success(self):
        collector = BooksCollector()
    
            # добавляем книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    
            # устанавливаем жанр
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить', 'Ужасы')
    
            # проверяем результат
        result = collector.get_books_with_specific_genre('Ужасы')
        assert len(result) == 2
        assert 'Гордость и предубеждение и зомби' in result
        assert 'Что делать, если ваш кот хочет вас убить' in result

        # 4.2. параметризированный тест на сумму книг по жанрам
    @pytest.mark.parametrize(
    'genre, expected_count',
    [
        ('Ужасы', 2),           # есть книги этого жанра
        ('Фантастика', 0),      # нет книг этого жанра
        ('Романтика', 0),       # невалидный жанр
    ]
)
    def test_get_books_with_specific_genre_parametrized(self, genre, expected_count):
        collector = BooksCollector()
    
        # добавляем книги с жанром Ужасы
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить', 'Ужасы')
    
        result = collector.get_books_with_specific_genre(genre)
        assert len(result) == expected_count



        # 5. Позитивный тест для get_books_genre()
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
    
    # добавляем книги с разными жанрами
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
    
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        # эта книга без жанра (по умолчанию '')
    
        expected = {
        'Гордость и предубеждение и зомби': 'Ужасы',
        'Что делать, если ваш кот хочет вас убить': ''
    }
    
        result = collector.get_books_genre()
    
        assert result == expected

    #6 Тест get_books_for_children(self) Проверка двух вариантов положительный и отрицательный
    #6.1. Позитивный тест 
    def test_get_books_for_children_true(self):
        collector = BooksCollector()
    
        collector.add_new_book('Король лев')
        collector.set_book_genre('Король лев', 'Мультфильмы')
        result = collector.get_books_for_children()
        assert 'Король лев' in result

    #6.2 Негативный тест
    def test_get_books_for_children_false(self):
        collector = BooksCollector()
        collector.add_new_book('Молчание  ягнят')
        collector.set_book_genre('Молчание  ягнят', 'Ужасы')
        result = collector.get_books_for_children()
        assert 'Молчание  ягнят' not in result

    #7 Тест add_book_in_favorites(self, name)
    #7.1  Позитивный кейс – книга есть в словаре, попадает в избранное
    def test_add_book_in_favorites_adds_when_book_exists(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        assert 'Гордость и предубеждение и зомби' in collector.favorites
        assert len(collector.favorites) == 1

    #7.2 Проверка на дубли, что добавление одного и того же - не 2, а 1
    def test_add_book_in_favorites_not_duplicated(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')

        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        assert collector.favorites.count('Гордость и предубеждение и зомби') == 1

    #7.3 Негативный тест – книги нет в books_genre, избранное пустое
    def test_add_book_in_favorites_ignore_if_not_in_books_genre(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert collector.favorites == []

    #8. Тест на метод delete_book_from_favorites(self, name)- удаляем книгу из Избранного
    # позитивный - удаляем существующую книгу из избранного
    def test_delete_book_from_favorites_removes_if_exists(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')

        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector.delete_book_from_favorites('Гордость и предубеждение и зомби')

        assert 'Гордость и предубеждение и зомби' not in collector.favorites
        assert len(collector.favorites) == 0

    # 9. Тест на метод get_list_of_favorites_books() получаем список Избранных книг
    # позитивный - вывод всех добавленныех в избранное книг
    def test_get_list_of_favorites_books_returns_all_added(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.set_book_genre('Гордость и предубеждение и зомби', 'Ужасы')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        collector.set_book_genre('Что делать, если ваш кот хочет вас убить', 'Ужасы')

        collector.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector.add_book_in_favorites('Что делать, если ваш кот хочет вас убить')

        result = collector.get_list_of_favorites_books()

        expected = ['Гордость и предубеждение и зомби', 'Что делать, если ваш кот хочет вас убить']
        assert result == expected

