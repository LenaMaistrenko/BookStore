import unittest
from datetime import date, datetime
from main import Bookstore, EmployeeManager, BookManager, SaleManager, EntityFactory

class TestBookstore(unittest.TestCase):

    def setUp(self):

        self.bookstore = Bookstore.get_instance()
        self.bookstore.employee_manager = EmployeeManager()
        self.bookstore.book_manager = BookManager()
        self.bookstore.sale_manager = SaleManager()


        self.employee = EntityFactory.create_employee("Don", "Sales", "111111111", "qwerty@asdf.com")
        self.book = EntityFactory.create_book("Math", 2021, "Pascal", "math", 10.0, 12.5)
        self.sale_date = date(2023, 5, 1)
        self.sale = EntityFactory.create_sale(self.employee, self.book, self.sale_date, 25.0)

    def test_add_employee(self):
        self.bookstore.employee_manager.add_employee(self.employee)
        self.assertIn(self.employee, self.bookstore.employee_manager.employees)

    def test_remove_employee(self):
        self.bookstore.employee_manager.add_employee(self.employee)
        self.bookstore.employee_manager.remove_employee(self.employee)
        self.assertNotIn(self.employee, self.bookstore.employee_manager.employees)

    def test_add_book(self):
        self.bookstore.book_manager.add_book(self.book)
        self.assertIn(self.book, self.bookstore.book_manager.books)

    def test_remove_book(self):
        self.bookstore.book_manager.add_book(self.book)
        self.bookstore.book_manager.remove_book(self.book)
        self.assertNotIn(self.book, self.bookstore.book_manager.books)