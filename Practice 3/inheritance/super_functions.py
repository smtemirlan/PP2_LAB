#Example 1
class Student('Person'):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
#Example 2
class Student('Person'):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year
x = Student("Mike", "Olsen", 2019)