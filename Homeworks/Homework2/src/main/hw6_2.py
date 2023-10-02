# 2. Implement a map-like function that returns an iterator (generator function)
# extra functionality: if arg function can't be applied, return element as is + text exception
#
# def map_like(fun, *elems):
#     pass
#
# # example input
# a = [1, 2, 3]
# b = 6
# c = 'zhaba'
# d = True
# fun = lambda x: x[0]
#
# for _ in map_like(fun, a, b, c, d):
#     print(_)

# output:
# 1
# 6: 'int' object is not subscriptable
# z
# True: 'bool' object is not subscriptable

def map_like(fun, *elems):
    for elem in elems:
        try:
            yield fun(elem)
        except Exception as e:
            yield f"{elem}: {str(e)}"

# example input
if __name__ == "__main__":
    a = [1, 2, 3]
    b = 6
    c = 'zhaba'
    d = True
    fun = lambda x: x[0]

for _ in map_like(fun, a, b, c, d):
    print(_)
