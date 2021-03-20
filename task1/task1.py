def slice_less(my_list, lesser):
    res = list()
    for el in my_list:
        if el >= lesser:
            res.append(el)
    res.sort()
    return res


if __name__ == '__main__':
    print(slice_less([3, 2, 1, 0, 4], 2))

