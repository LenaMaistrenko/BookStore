from datetime import date
class Employee:

    def __init__(self, full_name, position, contact_phone, email):
        self.full_name = full_name
        self.position = position
        self.contact_phone = contact_phone
        self.email = email

    def __str__(self):
        return f"{self.full_name}, {self.position}, {self.contact_phone}, {self.email}"

class Book:
    def __init__(self, title, publication_year, author, genre, cost_price, potential_sale_price):
        self.title = title
        self.publication_year = publication_year
        self.author = author
        self.genre = genre
        self.cost_price = cost_price
        self.potential_sale_price = potential_sale_price

    def __str__(self):
        return f"{self.title}, {self.publication_year}, {self.author}, {self.genre}, {self.cost_price}, {self.potential_sale_price}"

class Sale:
    def __init__(self, employee, book, sale_date, actual_sale_price):
        self.employee = employee
        self.book = book
        self.sale_date = sale_date
        self.actual_sale_price = actual_sale_price

    def __str__(self):
        return f"{self.book.title} sold by {self.employee.full_name} on {self.sale_date} for {self.actual_sale_price}"

class EntityFactory:
    @staticmethod
    def create_employee(full_name, position, contact_phone, email):
        return Employee(full_name, position, contact_phone, email)

    @staticmethod
    def create_book(title, publication_year, author, genre, cost_price, potential_sale_price):
        return Book(title, publication_year, author, genre, cost_price, potential_sale_price)

    @staticmethod
    def create_sale(employee, book, sale_date, actual_sale_price):
        return Sale(employee, book, sale_date, actual_sale_price)
class Observable:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()

class EmployeeManager(Observable):
    def __init__(self):
        super().__init__()
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        self.notify()

    def remove_employee(self, employee):
        self.employees.remove(employee)
        self.notify()

class BookManager(Observable):
    def __init__(self):
        super().__init__()
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        self.notify()

    def remove_book(self, book):
        self.books.remove(book)
        self.notify()
class SaleManager(Observable):
    def __init__(self):
        super().__init__()
        self.sales = []

    def make_sale(self, employee, book, sale_date, actual_sale_price):
        sale = EntityFactory.create_sale(employee, book, sale_date, actual_sale_price)
        self.sales.append(sale)
        self.notify()

class Bookstore:
    _instance = None

    def __init__(self):
        if Bookstore._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.employee_manager = EmployeeManager()
            self.book_manager = BookManager()
            self.sale_manager = SaleManager()
            self.report_strategy = None
            Bookstore._instance = self

    @staticmethod
    def get_instance():
        if Bookstore._instance is None:
            Bookstore()
        return Bookstore._instance