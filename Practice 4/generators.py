#Example 1
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1
ctr = fun(5)
for n in ctr:
    print(n)

#Example 2
def fun():
    return 1 + 2 + 3
res = fun()
print(res)

#Example 2
sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)

#Example 3
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)
print(next(myit))
print(next(myit))
print(next(myit))

#Example 4
mystr = "banana"
myit = iter(mystr)
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#Example 5 (with cycle for)
mytuple = ("apple", "banana", "cherry")
for x in mytuple:
  print(x)

#Example 6 (also cycle for)
mystr = "banana"
for x in mystr:
  print(x)

#Example 7 (_next_())
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
  def __next__(self):
    x = self.a
    self.a += 1
    return x
myclass = MyNumbers()
myiter = iter(myclass)
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

#Example 8
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration
myclass = MyNumbers()
myiter = iter(myclass)
for x in myiter:
  print(x)