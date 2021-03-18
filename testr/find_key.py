# find_key.py
def find_key(key, targ, path=[]):
    """ Search an aribitarily deep nested dict `targ` for key `key`.
        Return its value(s) together with the path(s) of ancestor keys.
    """
    if key == targ:
        yield v, path
    if isinstance(targ, dict):
        for k, v in targ.items():
            if k == key:
                yield v, path
            else:
                path.append(k)
                find_key(key, v, path)
                path.pop()

# test code
targ_1 = {'a': 1, 'b': {'b': 2, 'c': 3}, 'd': {'e': {'f': 4}}}
tests = {'test_a': {'key' : 'a', 'targ': targ_1, 'expect': [(1, [])]},
         'test_b': {'key' : 'b', 'targ': targ_1, 'expect': [({'b': 2, 'c': 3}, []), (2, ['b'])]},
         'test_c': {'key' : 'c', 'targ': targ_1, 'expect': [(3, ['b'])]},
         'test_d': {'key' : 'd', 'targ': targ_1, 'expect': [({'e': {'f': 4}}, [])]},
         'test_e': {'key' : 'e', 'targ': targ_1, 'expect': [({'f': 4}, ['d'])]},
         'test_f': {'key' : 'f', 'targ': targ_1, 'expect': [(4, ['d', 'e'])]}}
for k, v in tests.items():
    if list(find_key(v['key'], v['targ'])) == v['expect']:
        print(k, 'OK')
    else:
        print(k, 'actual:', list(find_key(v['key'], v['targ'])))
        print(k, 'expected:', v['expect'])

