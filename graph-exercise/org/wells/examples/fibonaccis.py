import itertools


def fibo(count):
    if count <= 0:
        raise "Count should be positive."
    elif count == 1:
        return [1]
    else:
        lst = [1]
        i = 1
        last_1 = 0
        last_2 = 1
        while i < count:
            i += 1
            current = last_1 + last_2
            lst.append(current)
            last_1 = last_2
            last_2 = current
        return lst


def fibo2():
    last_1 = 0
    last_2 = 0
    current = 0
    while True:
        if current == 0:
            current = 1
        else:
            current = last_1 + last_2
        last_1 = last_2
        last_2 = current
        yield current


# print(list(i*i for i in fibo(10)))
# print(list(itertools.islice(fibo2(), 10)))
print([x for _, x in zip(range(10), fibo2())])

even_fibo = (item for item in fibo2() if item % 2 == 0)
print(list(itertools.takewhile(lambda x: x < 100, even_fibo)))
