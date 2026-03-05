n=int(input())
def to_zero(n):
    for i in range(n,-1,-1):
        yield i
for nums in to_zero(n):
    print(nums)