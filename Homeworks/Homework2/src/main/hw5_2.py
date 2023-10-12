""""
Homework 5_2:
============

Preamble
========

We have a database file (example.sqlite) in sqlite3 format with some tables and data.
All tables have 'author' column and maybe some additional ones.

Data retrieval and modifications are done with sqlite3 module by issuing SQL statements.
For example, to get all data from TABLE1::

    import sqlite3
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from TABLE1')
    data = cursor.fetchall()   # will be a list with data.

instead of getting all data at once, you can use .fetchone() calls and named expressions::

    while row:=cursor.fetchone():
        print(row)

To get a row with specific author equal to some value::

    import sqlite3
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from books where author=:author', {author:'Bradbury'})
    data = cursor.fetchall()  # will get all records with this name. You can also use .fetchone() to get one record.

in order to get record with author (sorted alphabetically) use SQL expression `SELECT * from books order by author asc limit 1`
in order to get record after specified (sorted alphabetically) use SQL expression `SELECT * from books where author > :author order by author limit`.
To get amount of records in table TABLE1, use `select count(*) from TABLE1` query.


Please refer to this documents for more information about how to retrieve data from sqlite database:
DBAPI: https://www.python.org/dev/peps/pep-0249/
sqlite3 module: https://docs.python.org/3/library/sqlite3.html


Task
====

Write a wrapper class TableData for database table, that when initialized with database name
and table acts as collection object (implements Collection protocol).
Assume all data has unique values in 'author' column.
So, if books = TableData(database_name='example.sqlite', table_name='books')

then
 -  `len(books)` will give current amount of rows in books table in database
 -  `books['Bradbury']` should return single data row for book with author Bradbury
 -  `'Yeltsin' in books` should return if book with same author exists in table
 -  object implements iteration protocol. i.e. you could use it in for loops::
       for book in books:
           print(book['author'])
 - all above mentioned calls should reflect most recent data.
 If data in table changed after you created collection instance, your calls should return updated data.

Avoid reading entire table into memory. When iterating through records, start reading the first record,
then go to the next one, until records are exhausted.
When writing tests, it's not always neccessary to mock database calls completely.
Use supplied example.sqlite file as database fixture file.
"""

import sqlite3
from collections.abc import Collection, Iterable


class TableData(Collection, Iterable):
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def __len__(self):
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM {self.table_name}')
            return cursor.fetchone()[0]

    def __getitem__(self, author: str):
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name} WHERE author=?', (author,))
            row = cursor.fetchone()
            if row:
                return {description[0]: value for description, value in zip(cursor.description, row)}
            return None

    def __contains__(self, author: str):
        return self.__getitem__(author) is not None

    def __iter__(self):
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name}')
            for row in cursor.fetchall():
                yield {description[0]: value for description, value in zip(cursor.description, row)}


# Testing the implementation with the provided database
books = TableData(database_name='example.sqlite', table_name='books')

# Printing the total number of books
print(len(books))

# Printing information about a book with a specific author
print(books['Bradbury'])

# Checking if a book by a specific author exists
print('Yeltsin' in books)

# Iterating through the books and printing the authors
for book in books:
    print(book['author'])
