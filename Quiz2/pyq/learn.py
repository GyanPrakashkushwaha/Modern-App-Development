def modify(func):
    def wrapper(l):
        res = func(l)
        return res[::-1]
    return wrapper

def update(func):
    def wrapper(l):
        res = func(l)
        return list(map(lambda x: x/2, res))
    return wrapper

@modify
@update
def mylist(l):
    out_list = []
    for i in l:
        out_list.append(i**2)
    return out_list

# print(modify([2,4,1,7,5,9]))
print(mylist([2,4,1,7,5,9]))
