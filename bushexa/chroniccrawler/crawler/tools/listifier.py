# Returns a list of elements in a request dictionary
# count : list of indexes leading to number of elements
# elements : list of indexes leading to elements
def element_list(count, rdict, element):
    cnt = rdict
    for key in count:
        if cnt == None:
            raise Exception("Wrong response!")
        else:
            cnt = cnt[key]

    if isinstance(cnt, str):
        cnt = int(cnt)

    l = []

    if cnt == 0:
        pass
    else:
        thing = rdict
        for key in element:
            thing = thing[key]

        if cnt == 1:
            l.append(thing)
        else:
            l = thing

    return l
