from typing import TypeVar, Generic
import heapq

# Define a type variable for generics
T = TypeVar('T')

class Reversed:
    def __init__(self, value):
        self.value = value
    
    def __lt__(self, other):
        return self.value > other.value  # Invertimos el comparador

class Heap(Generic[T]):
    def __init__(self, ascendant=True):
        self.heap = []
        self.ascendant = ascendant
    
    def insert(self, item: T):
        """Inserts an item with a given priority."""
        heapq.heappush(self.heap, item if self.ascendant else Reversed(item))
    
    def extract(self) -> T:
        """Extracts the item with the highest priority."""
        if self.not_empty():
            item = heapq.heappop(self.heap)
            return item if self.ascendant else item.value
        raise IndexError("The heap is empty")
    
    def peek(self) -> T:
        """Looks at the the item with the highest priority."""
        if self.not_empty():
            item = self.heap[0]
            return item if self.ascendant else item.value
        raise IndexError("The heap is empty")
    
    def empty(self) -> bool:
        """Checks if the heap is empty."""
        return len(self.heap) == 0
    
    def not_empty(self) -> bool:
        """Checks if the heap is not empty."""
        return not self.empty()
