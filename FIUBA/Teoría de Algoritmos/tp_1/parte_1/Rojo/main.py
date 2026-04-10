import sys
from collections import deque

def main(file):
    with open (file) as f:
        stacks = []
        for linea in f:
            acomodar(stacks, int(linea))
        print (len(stacks))

def acomodar(stacks, num):
    topes = []
    for stack in stacks:
        topes.append(stack[-1])
    index = busqueda_binaria(topes, num)
    if index < len(stacks):
        stacks[index].append(num)
    else:
        nuevo_stack = deque()
        nuevo_stack.append(num)
        stacks.append(nuevo_stack)



def busqueda_binaria(topes, num):
    min, max = 0, len(topes)
    while max > min:
        mid = (min + max) // 2
        if topes[mid] > num:
            max = mid
        else:
            min = mid + 1
    return min

if __name__ == "__main__":
    main(sys.argv[1])