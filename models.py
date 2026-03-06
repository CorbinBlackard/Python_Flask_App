import datetime

class Book:
	def __init__(self, id, title, author):
		self.id = id
		self.title = title
		self.author = author
		self.available = True
		self.due_date = None
		self.borrower = None
		self.times_checked_out = 0

	def check_out(self, user , days=14):
		self.borrower = user
		self.available = False
		self.due_date = datetime.datetime.now() + datetime.timedelta(days=days)
		self.times_checked_out += 1

	def return_book(self, user):
		self.borrower = None
		self.available = True
		self.due_date = None

	def __str__(self):
		return f'{self.title} by {self.author}'

class User:
	id_counter = 1
	def __init__(self, name):
		self.name = name
		self.checked_out_books = []
		self.user_id = f"USER{User.id_counter:03d}"
		User.id_counter += 1

	def check_out_book(self, book, days=14):
		self.checked_out_books.append(book)
		book.check_out(self, days)
	
	def return_book(self, book):
		self.checked_out_books.remove(book)
		book.return_book(self)


books = [
	Book(1, "The Hobbit", "J.R.R. Tolkien"),
	Book(2, "1984", "George Orwell"),
	Book(3, "Dune", "Frank Herbert"),
	Book(4, "Python Crash Course", "Eric Matthes"),
	Book(5, "Clean Code", "Robert Martin")
]

users = [
	User("Alice"),
	User("Bob"),
	User("Charlie")
]
current_user = users[0]