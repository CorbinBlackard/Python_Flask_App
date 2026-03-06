from flask import Flask, render_template, request, redirect, url_for
from models import books, users, current_user, Book, User

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', current_user=current_user)

@app.route('/books')
def list_books():
	book_total = len(books)
	return render_template('books.html', books=books, current_user=current_user, book_total=book_total)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
	book = next((b for b in books if b.id == book_id), None)
	if book:
		return render_template('book_detail.html', book=book, current_user=current_user)
	else:
		return "Book not found", 404

@app.route('/check_out/<int:book_id>')
def check_out(book_id):
	print(f'Checking out book {book_id}')
	book = next((b for b in books if b.id == book_id), None)
	if book and book.available:
		current_user.check_out_book(book)
		print(f'{current_user.name} checked out {book.title}')
	else:
		print('Book not available')
	return redirect(url_for('book_detail', book_id=book_id))

@app.route('/return_book/<int:book_id>')
def return_book(book_id):
	print(f'Returned {book_id}')
	book = next((b for b in books if b.id == book_id), None)
	if book and not book.available and book.borrower == current_user:
		current_user.return_book(book)
		print(f'{current_user.name} returned {book.title}')
	else:
		print('Cannot return this book')
	return redirect(url_for('book_detail', book_id=book_id))

@app.route('/switch_user/<int:user_index>')
def switch_user(user_index):
	global current_user
	if 0 <= user_index < len(users):
		current_user = users[user_index]
	return redirect(url_for('index', current_user=current_user))

@app.route('/user_dash/<string:user_id>')
def user_dash(user_id):
	user = next((u for u in users if u.user_id == user_id), None)
	most_checked_out = max(books, key=lambda book: book.times_checked_out)
	if user:
		return render_template('user_dash.html', user=user, most_checked_out=most_checked_out, current_user=current_user)
	else:
		return "User not found", 404



if __name__ == '__main__':
	app.run(debug=True, port=5001)
