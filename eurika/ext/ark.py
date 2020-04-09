'''
Scripts for Arknights
'''

from itertools import chain, combinations

def powerset(iterable):
    '''powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)'''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def recruit(args):
    res = set()
    res = set(powerset(args))
    return list(res)


print(recruit(['A','B','C']))
