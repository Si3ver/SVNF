def ifRepeat(L):
    if len(L) == 0 or len(L) == 1:
        return False
    L_copy1, L_copy2= [], []
    
    for item in L:
        L_copy1.append(item)
        L_copy2.append(item)
    print(L_copy1, L_copy2)
    
    for item in L_copy1:
        L_copy2.pop(0)
        # print(item, L_copy2)
        try:
            L_copy2.index(item) 
        except ValueError:
            continue
        else:
            return True
    return False

servList = [58, 60, 61, 62, 59, 57, 65, 62, 93]
if ifRepeat(servList):
    print('wrong place!', servList)



