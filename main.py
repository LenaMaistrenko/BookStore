import pickle
from datetime import date, datetime


# Класи сутностей
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
        return f"{self.employee.full_name}, {self.book.title}, {self.sale_date}, {self.actual_sale_price}"


# Фабричний метод
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


# Спостерігач
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


# Менеджери
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


# Стратегія
class ReportStrategy:
    def generate_report(self, data):
        pass


class EmployeeReportStrategy(ReportStrategy):
    def generate_report(self, data):
        report = "Employee Report\n"
        for employee in data:
            report += str(employee) + "\n"
        return report


class BookReportStrategy(ReportStrategy):
    def generate_report(self, data):
        report = "Book Report\n"
        for book in data:
            report += str(book) + "\n"
        return report


class SaleReportStrategy(ReportStrategy):
    def generate_report(self, data):
        report = "Sale Report\n"
        for sale in data:
            report += str(sale) + "\n"
        return report


class Bookstore:
    _instance = None

    def __init__(self):
        self.employee_manager = EmployeeManager()
        self.book_manager = BookManager()
        self.sale_manager = SaleManager()
        self.report_strategy = None

    @staticmethod
    def get_instance():
        if Bookstore._instance is None:
            Bookstore._instance = Bookstore()
        return Bookstore._instance

    def set_report_strategy(self, strategy):
        self.report_strategy = strategy

    def generate_report(self):
        if self.report_strategy:
            if isinstance(self.report_strategy, EmployeeReportStrategy):
                return self.report_strategy.generate_report(self.employee_manager.employees)
            elif isinstance(self.report_strategy, BookReportStrategy):
                return self.report_strategy.generate_report(self.book_manager.books)
            elif isinstance(self.report_strategy, SaleReportStrategy):
                return self.report_strategy.generate_report(self.sale_manager.sales)
        return "No report strategy set."

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as f:
            Bookstore._instance = pickle.load(f)
        return Bookstore._instance

    # Нові методи
    def get_book_report(self):
        self.set_report_strategy(BookReportStrategy())
        return self.generate_report()

    def get_sale_report(self):
        self.set_report_strategy(SaleReportStrategy())
        return self.generate_report()

    def get_sales_by_date(self, sale_date):
        sales = [sale for sale in self.sale_manager.sales if sale.sale_date == sale_date]
        return SaleReportStrategy().generate_report(sales)

    def get_sales_by_period(self, start_date, end_date):
        sales = [sale for sale in self.sale_manager.sales if start_date <= sale.sale_date <= end_date]
        return SaleReportStrategy().generate_report(sales)

    def get_sales_by_employee(self, employee_name):
        sales = [sale for sale in self.sale_manager.sales if sale.employee.full_name == employee_name]
        return SaleReportStrategy().generate_report(sales)

    def get_bestseller_book(self, start_date, end_date):
        sales = [sale for sale in self.sale_manager.sales if start_date <= sale.sale_date <= end_date]
        book_sales = {}
        for sale in sales:
            if sale.book.title in book_sales:
                book_sales[sale.book.title] += 1
            else:
                book_sales[sale.book.title] = 1
        bestseller = max(book_sales, key=book_sales.get)
        return f"Bestseller Book: {bestseller}"

    def get_top_employee(self, start_date, end_date):
        sales = [sale for sale in self.sale_manager.sales if start_date <= sale.sale_date <= end_date]
        employee_sales = {}
        for sale in sales:
            if sale.employee.full_name in employee_sales:
                employee_sales[sale.employee.full_name] += sale.actual_sale_price
            else:
                employee_sales[sale.employee.full_name] = sale.actual_sale_price
        top_employee = max(employee_sales, key=employee_sales.get)
        return f"Top Employee: {top_employee}"

    def get_total_profit(self, start_date, end_date):
        sales = [sale for sale in self.sale_manager.sales if start_date <= sale.sale_date <= end_date]
        total_profit = sum(sale.actual_sale_price - sale.book.cost_price for sale in sales)
        return f"Total Profit: {total_profit}"

    def get_popular_author(self, start_date, end_date):
        sales = [sale for sale in self.sale_manager.sales if start_date <= sale.sale_date <= end_date]
        author_sales = {}
        for sale in sales:
            if sale.book.author in author_sales:
                author_sales[sale.book.author] += 1
            else:
                author_sales[sale.book.author] = 1
        popular_author = max(author_sales, key=author_sales.get)
        return f"Popular Author: {popular_author}"

    def get_popular_genre(self, start_date, end_date):
        sales = [sale for sale in self.sale_manager.sales if start_date <= sale.sale_date <= end_date]
        genre_sales = {}
        for sale in sales:
            if sale.book.genre in genre_sales:
                genre_sales[sale.book.genre] += 1
            else:
                genre_sales[sale.book.genre] = 1
        popular_genre = max(genre_sales, key=genre_sales.get)
        return f"Popular Genre: {popular_genre}"


# Меню
def main_menu():
    bookstore = Bookstore.get_instance()

    while True:
        print("\nBookstore Management System")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Add Book")
        print("4. Remove Book")
        print("5. Make Sale")
        print("6. Generate Report")
        print("7. Save to File")
        print("8. Load from File")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            full_name = input("Enter full name: ")
            position = input("Enter position: ")
            contact_phone = input("Enter contact phone: ")
            email = input("Enter email: ")
            employee = EntityFactory.create_employee(full_name, position, contact_phone, email)
            bookstore.employee_manager.add_employee(employee)
        elif choice == '2':
            full_name = input("Enter full name of employee to remove: ")
            employee = next((e for e in bookstore.employee_manager.employees if e.full_name == full_name), None)
            if employee:
                bookstore.employee_manager.remove_employee(employee)
            else:
                print("Employee not found.")
        elif choice == '3':
            title = input("Enter book title: ")
            publication_year = int(input("Enter publication year: "))
            author = input("Enter author: ")
            genre = input("Enter genre: ")
            cost_price = float(input("Enter cost price: "))
            potential_sale_price = float(input("Enter potential sale price: "))
            book = EntityFactory.create_book(title, publication_year, author, genre, cost_price, potential_sale_price)
            bookstore.book_manager.add_book(book)
        elif choice == '4':
            title = input("Enter book title to remove: ")
            book = next((b for b in bookstore.book_manager.books if b.title == title), None)
            if book:
                bookstore.book_manager.remove_book(book)
            else:
                print("Book not found.")
        elif choice == '5':
            emp_name = input("Enter employee name: ")
            employee = next((e for e in bookstore.employee_manager.employees if e.full_name == emp_name), None)
            if employee:
                book_title = input("Enter book title: ")
                book = next((b for b in bookstore.book_manager.books if b.title == book_title), None)
                if book:
                    sale_date = input("Enter sale date (YYYY-MM-DD): ")
                    sale_date = datetime.strptime(sale_date, "%Y-%m-%d").date()
                    actual_sale_price = float(input("Enter actual sale price: "))
                    bookstore.sale_manager.make_sale(employee, book, sale_date, actual_sale_price)
                else:
                    print("Book not found.")
            else:
                print("Employee not found.")
        elif choice == '6':
            print("\nGenerate Report")
            print("1. Full Information about Employees")
            print("2. Full Information about Books")
            print("3. Full Information about Sales")
            print("4. Sales by Date")
            print("5. Sales by Period")
            print("6. Sales by Employee")
            print("7. Bestseller Book by Period")
            print("8. Top Employee by Period")
            print("9. Total Profit by Period")
            print("10. Popular Author by Period")
            print("11. Popular Genre by Period")
            report_choice = input("Enter your choice: ")

            if report_choice == '1':
                bookstore.set_report_strategy(EmployeeReportStrategy())
                print(bookstore.generate_report())
            elif report_choice == '2':
                print(bookstore.get_book_report())
            elif report_choice == '3':
                print(bookstore.get_sale_report())
            elif report_choice == '4':
                sale_date = input("Enter sale date (YYYY-MM-DD): ")
                sale_date = datetime.strptime(sale_date, "%Y-%m-%d").date()
                print(bookstore.get_sales_by_date(sale_date))
            elif report_choice == '5':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                print(bookstore.get_sales_by_period(start_date, end_date))
            elif report_choice == '6':
                emp_name = input("Enter employee name: ")
                print(bookstore.get_sales_by_employee(emp_name))
            elif report_choice == '7':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                print(bookstore.get_bestseller_book(start_date, end_date))
            elif report_choice == '8':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%м-%d").date()
                print(bookstore.get_top_employee(start_date, end_date))
            elif report_choice == '9':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%м-%d").date()
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%м-%d").date()
                print(bookstore.get_total_profit(start_date, end_date))
            elif report_choice == '10':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%м-%d").date()
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%м-%d").date()
                print(bookstore.get_popular_author(start_date, end_date))
            elif report_choice == '11':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%м-%d").date()
                end_date = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(end_date, "%Y-%м-%d").date()
                print(bookstore.get_popular_genre(start_date, end_date))
            else:
                print("Invalid choice.")
        elif choice == '7':
            filename = input("Enter filename to save data: ")
            bookstore.save_to_file(filename)
        elif choice == '8':
            filename = input("Enter filename to load data: ")
            bookstore = Bookstore.load_from_file(filename)
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
