

def remove_dublicate(key, queryset):
    """
    Убирает дубликаты из queryset
    :param queryset: получает queryset
    :return: {'categories': [cat1, cat2, cat3, ... cat_n]}
    """
    lst = []
    for dct in queryset:
        if len(dct.get(key)):
            for el in dct.get(key):
                if el not in lst:
                    lst.append(el)
    lst_out = list(map(lambda x: {key: x}, lst))
    return lst_out

