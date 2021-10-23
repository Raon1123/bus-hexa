# Returns a list of elements in a request dictionary
# count : number of elements
# elements : index to element list
def element_list(count, element):
    if isinstance(count, str):
        count = int(count)

    l = []

    if count == 0:
        pass
    elif count == 1:
        l.append(element)
    else:
        l = element

    return l
