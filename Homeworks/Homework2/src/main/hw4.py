"""
Create classes to track homeworks.

1. Homework - accepts howework text and deadline (datetime.timedelta)
Homework has a method, that tells if deadline has passed.

2. Student - can solve homework with `do_homework` method.
Raises DeadlineError with "You are late" message if deadline has passed

3. Teacher - can create homework with `create_homework`; check homework with `check_homework`.
Any teacher can create or check any homework (even if it was created by one of colleagues).

Homework are cached in dict-like structure named `homework_done`. Key is homework, values are 
solutions. Each student can only have one homework solution.

Teacher can `reset_results` - with argument it will reset results for specific homework, without - 
it clears the cache.

Homework is solved if solution has more than 5 symbols.

-------------------
Check file with tests to see how all these classes are used. You can create any additional classes 
you want.
"""
import datetime
from collections import defaultdict


# Custom exception
class DeadlineError(Exception):
    pass


# Homework class
class Homework:
    def __init__(self, text: str, deadline: datetime.timedelta):
        self.text = text
        self.deadline = deadline
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        return datetime.datetime.now() < self.created + self.deadline


# Base Person class
class Person:
    def __init__(self, last_name: str, first_name: str):
        self.last_name = last_name
        self.first_name = first_name


# Student class
class Student(Person):
    def do_homework(self, homework: Homework, solution: str):
        if not homework.is_active():
            raise DeadlineError("You are late")
        return HomeworkResult(self, homework, solution)


# Teacher class
class Teacher(Person):
    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text: str, days: int) -> Homework:
        return Homework(text, datetime.timedelta(days=days))

    @classmethod
    def check_homework(cls, hw_result) -> bool:
        if len(hw_result.solution) > 5:
            cls.homework_done[hw_result.homework].add(hw_result)
            return True
        return False

    @classmethod
    def reset_results(cls, homework=None):
        if homework:
            cls.homework_done.pop(homework, None)
        else:
            cls.homework_done.clear()


# HomeworkResult class
class HomeworkResult:
    def __init__(self, author: Student, homework: Homework, solution: str):
        if not isinstance(homework, Homework):
            raise TypeError("You gave not a Homework object")
        self.author = author
        self.homework = homework
        self.solution = solution
