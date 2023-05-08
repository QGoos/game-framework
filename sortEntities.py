import entity

def sortByHitbox(ents) -> entity.Entity:
    num_zs = [0,0,0]
    for e in ents:
        num_zs[e.getZ()] += 1

    sortByZ(0, len(ents)-1, ents)
    
    return ents

def sortByZ(start, end, entities):
    '''A quicksort for entities by their Z axis value'''
    if (start < end):

        p = partitionZ(start, end, entities)

        sortByZ(start, p-1, entities)
        sortByZ(p+1, end, entities)

def partitionZ(start, end, entities) -> int:
    pivot_index = start
    pivot = entities[pivot_index].getZ()

    while start < end:
        while start < len(entities) and entities[start].getZ() <= pivot:
            start += 1

        while entities[end].getZ() > pivot:
            end -= 1
        
        if(start < end):
            entities[start], entities[end] = entities[end], entities[start]

    entities[end], entities[pivot_index] = entities[pivot_index], entities[end]

    return end