import pytest
from main import BooksCollector

class TestBooksCollector:
    BOOK1 = "Гордость и предубеждение и зомби"
    BOOK2 = "Что делать, если ваш кот хочет вас убить"
    

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK2)
        assert len(collector.books_genre) == 2

    @pytest.mark.parametrize('name, expected', [
        (BOOK1, True),
        (BOOK2, True),
        ('', False),
        ('A' * 40, True),
        ('A' * 41, False),
    ])
    def test_add_new_book_name_validation(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    def test_add_new_book_duplicate(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK1)
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', 'Фантастика'),
        ('Ужасы', 'Ужасы'),
        ('Несуществующий жанр', ''),
    ])
    def test_set_book_genre(self, collector, genre, expected):
        collector.add_new_book(self.BOOK1)
        collector.set_book_genre(self.BOOK1, genre)
        assert collector.get_book_genre(self.BOOK1) == expected

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK2)
        collector.set_book_genre(self.BOOK1, 'Фантастика')
        collector.set_book_genre(self.BOOK2, 'Ужасы')
        
        assert self.BOOK1 in collector.get_books_with_specific_genre('Фантастика')
        assert self.BOOK2 in collector.get_books_with_specific_genre('Ужасы')
        assert len(collector.get_books_with_specific_genre('Несуществующий')) == 0

    def test_get_books_for_children(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK2)
        collector.set_book_genre(self.BOOK1, 'Фантастика')
        collector.set_book_genre(self.BOOK2, 'Ужасы')
        
        children_books = collector.get_books_for_children()
        assert self.BOOK1 in children_books
        assert self.BOOK2 not in children_books

    def test_get_book_genre_from_dictionary(self, collector):
        collector.books_genre = {
        TestBooksCollector.BOOK1: "Фантастика",
        TestBooksCollector.BOOK2: "Ужасы"
        }
        assert collector.get_book_genre(TestBooksCollector.BOOK1) == "Фантастика"
        assert collector.get_book_genre(TestBooksCollector.BOOK2) == "Ужасы"
        assert collector.get_book_genre("Нет такой книги") is None

    def test_get_books_genre_returns_all_books(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK2)
        collector.set_book_genre(self.BOOK1, "Фантастика")
        
        expected_result = {
            self.BOOK1: "Фантастика",
            self.BOOK2: ""
        }
        assert collector.get_books_genre() == expected_result

    @pytest.mark.parametrize('book, expected', [
        (BOOK1, True),
        (BOOK2, True),
        ('Несуществующая книга', False),
    ])
    def test_add_book_in_favorites(self, collector, book, expected):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK2)
        collector.add_book_in_favorites(book)
        assert (book in collector.favorites) == expected

    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_book_in_favorites(self.BOOK1)
        collector.add_book_in_favorites(self.BOOK1)
        assert len(collector.favorites) == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_book_in_favorites(self.BOOK1)
        collector.delete_book_from_favorites(self.BOOK1)
        assert self.BOOK1 not in collector.favorites

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book(self.BOOK1)
        collector.add_new_book(self.BOOK2)
        collector.add_book_in_favorites(self.BOOK1)
        collector.add_book_in_favorites(self.BOOK2)
        
        favorites = collector.get_list_of_favorites_books()
        assert self.BOOK1 in favorites
        assert self.BOOK2 in favorites
        assert len(favorites) == 2
