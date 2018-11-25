DROP TABLE IF EXISTS LibraryUser;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Note;
DROP TABLE IF EXISTS BookList;
DROP TABLE IF EXISTS BookListToBook;
DROP TABLE IF EXISTS Loan;

CREATE TABLE LibraryUser (
	id SERIAL PRIMARY KEY,
	user_name varchar(32) not null unique,
	password varchar(32) not null
);

CREATE TABLE Book (
	id SERIAL PRIMARY KEY,
	author varchar(255) not null,
	title varchar(255) not null,
	year int not null,
	genre varchar(255) not null
);

CREATE TABLE Note (
	id SERIAL PRIMARY KEY,
	book_id int,
	user_id int,
	content text,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	foreign key (book_id) references Book(id) ON DELETE SET NULL,
	foreign key (user_id) references LibraryUser(id) ON DELETE SET NULL
);

CREATE TABLE BookList (
	id SERIAL PRIMARY KEY,
	user_id int,
	name varchar(255) not null,
	description text,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	foreign key (user_id) references LibraryUser(id) ON DELETE SET NULL
);

CREATE TABLE BookListToBook (
	id SERIAL PRIMARY KEY,
	book_list_id int,
	book_id int,
	foreign key (book_id) references Book(id) ON DELETE SET NULL,
	foreign key (book_list_id) references BookList(id) ON DELETE SET NULL
);

CREATE TABLE Loan (
	id SERIAL PRIMARY KEY,
	user_id int,
	book_id int,
	due date not null,
	return_date date,
	foreign key (user_id) references LibraryUser(id) ON DELETE SET NULL,
	foreign key (book_id) references Book(id) ON DELETE SET NULL
);



