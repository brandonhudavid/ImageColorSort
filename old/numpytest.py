import numpy as np

#def test():
#    indices = np.array([8])
#    indices = np.concatenate(((indices, np.array([0, 1]))))
#    indices = np.concatenate(((indices, np.array([5, 8]))))
    #indices = np.concatenate(((np.array([0, 1])), np.array([5, 8])))
#    return indices

#counter = [0, 0]
#a = test()
#if 5 in a:
#    print("True")
#print(a)

#for elem in a:
#    counter[int(elem)] += 1
#print(counter)

#x = np.array([0, 0, 0])
#y = np.concatenate((x, np.array([2, 3, 4])))
#y[1] += 1
#print(y)

#lst = [(1,2), (3,4)]
#counter = [0, 0, 0, 0, 0]
#a = (1, 3)
#if a in lst:
#    print("True")
#else:
#    lst += [a]
#lst_array = np.array(lst)
#print(lst_array)

#lst1 = [(1,2,3), (4,5,6), (7,8,9)]
#lst2 = [1, 3, 5]
#a = np.insert((np.array(lst1)), 3, lst2, axis=1)
#print(a)s
result = {(0,1,2): 20, (1,2,3): 30, (3,4,5): 50}

names = ['str','str2']
formats = ['f8','f8']
dtype = dict(names = names, formats=formats)
a = np.fromiter(result.items(), dtype=dtype)
print(a)
