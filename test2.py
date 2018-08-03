def ifRepeat(L):
    if len(L) == 0 or len(L) == 1:
        return False
    L_copy= []
    for item in L:
        L_copy.append(item)
    for item in L_copy:
        L.pop(0)
        try:
            L.index(item) 
        except ValueError:
            continue
        else:
            return True
    return False



print(ifRepeat([]))
print(ifRepeat([1]))
print(ifRepeat([1,1]))
print(ifRepeat([1,2,3]))
print(ifRepeat([1,1,3]))


