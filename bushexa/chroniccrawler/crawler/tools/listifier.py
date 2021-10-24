# Returns a list of elements in a request dictionary
# count : number of elements
# elements : list of indexes leading to elements
def element_list(count, rdict, element):
    if isinstance(count, str):
        count = int(count)

    l = []

    if count == 0:
        pass
    else:
        thing = rdict
        for key in element:
            thing = thing[key]

        if count == 1:
            l.append(thing)
        else:
            l = thing

    return l
