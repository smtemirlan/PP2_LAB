#Example 1
def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")

#Example 2
def my_function(name): # name is a parameter
  print("Hello", name)
my_function("Emil") # "Emil" is an argument

#Example 3
def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil", "Refsnes")

#Example 4
def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil")

#Example 5
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function(animal = "dog", name = "Buddy")

#Example 6
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("dog", "Buddy")

#Example 7
def my_function(fruits):
  for fruit in fruits:
    print(fruit)
my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

#Example 8
def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])
my_person = {"name": "Emil", "age": 25}
my_function(my_person)