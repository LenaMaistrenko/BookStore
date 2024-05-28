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