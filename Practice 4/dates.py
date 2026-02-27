#Example 1
import datetime

x = datetime.datetime.now()
print(x)

#Example 2
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#Example 3
import datetime

x = datetime.datetime(2020, 5, 17)

print(x)

#Example 4 ("strtime()")
import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

#Example 5