from typing import TypeVar, Generic, Optional, Callable

K = TypeVar('K')  # Generic type
V = TypeVar('V')  # Generic type

class _Node(Generic[K,V]):
    def __init__(self,key:K, value: V):
        self.key = key
        self.value: V = value
        self._height: int = 1
        self._left: Optional['_Node[K,V]'] = None
        self._right: Optional['_Node[K,V]'] = None

    def _update_height(self) -> None:
        self._height = max(\
            self.left.height if self.left else 0, \
            self.right.height if self.right else 0 \
        ) + 1
    
    @property
    def height(self):
        return self._height
    
    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right
    
    @left.setter
    def left(self, node):
        self._left = node
        self._update_height()

    @right.setter
    def right(self, node):
        self._right = node
        self._update_height()

class AVLTree(Generic[K,V]):
    def __init__(self, ascendant=True):
        self._root: Optional[_Node[K,V]] = None
        self.ascendant = ascendant
        self._size = 0

    def _calc_priority(self, key: K):
        return key if self.ascendant else -key

    def _balance_factor(self, node: Optional[_Node[K,V]]) -> int:
        return (node.left.height if node.left else 0) - (node.right.height if node.right else 0) \
                if node else 0

    def _rotate_right(self, z: _Node[K,V]) -> _Node[K,V]:
        y = z.left
        z.left = y.right
        y.right = z
        return y

    def _rotate_left(self, z: _Node[K,V]) -> _Node[K,V]:
        y = z.right
        z.right = y.left
        y.left = z
        return y

    def _balance(self, node: _Node[K,V]) -> _Node[K,V]:
        balance = self._balance_factor(node)
        
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node

    def _insert(self, node: Optional[_Node[K,V]], key: K, value: V) -> _Node[K,V]:
        if not node:
            self._size+=1
            return _Node(key, value)

        if self._calc_priority(key) == self._calc_priority(node.key):
            node.value = value
            return node

        if self._calc_priority(key) < self._calc_priority(node.key):
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)
        
        return self._balance(node)

    def __setitem__(self, key: K, value: V) -> None:
        self._root = self._insert(self._root, key, value)

    def __contains__(self, key: K) -> bool:
        """ Check if the key is in the tree. """
        return self[key] != None
    
    def __getitem__(self, key:K) -> V:
        """ Returns the value asociated with the key """
        node = self._root
        while node:
            if key == node.key:
                return node.value
            node = node.left if self._calc_priority(key) < self._calc_priority(node.key) else node.right
        return None


    def __len__(self) -> int:
        """ Return the number of elements in the tree. """
        return self._size
    
    def range(self, low: Optional[K] = None, high: Optional[K] = None):
        """ An iterable between [low, high] inclusive. """
        yield from self._iter_range(self._root, low, high)

    def __iter__(self, low: Optional[K] = None, high: Optional[K] = None):
        yield from self._iter_range(self._root, low, high)

    def _iter_range(self, node: Optional[_Node[K,V]], low: Optional[K], high: Optional[K]):
        if not node:
            return
        if low is None or self._calc_priority(low) < self._calc_priority(node.key):
            yield from self._iter_range(node.left, low, high)
        if (low is None or self._calc_priority(low) <= self._calc_priority(node.key)) and \
              (high is None or self._calc_priority(node.key) <= self._calc_priority(high)):
            yield (node.key, node.value)
        if high is None or self._calc_priority(node.key) < self._calc_priority(high):
            yield from self._iter_range(node.right, low, high)

    def _min_value_node(self, node: _Node[K, V]) -> _Node[K, V]:
        """ Returns the node with the minimal key """
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node: Optional[_Node[K, V]], key: K) -> Optional[_Node[K, V]]:
        if not node:
            return None
        
        if self._calc_priority(key) < self._calc_priority(node.key):
            node.left = self._delete(node.left, key)
        elif self._calc_priority(key) > self._calc_priority(node.key):
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                self._size-=1
                return node.right
            elif not node.right:
                self._size-=1
                return node.left
            
            temp = self._min_value_node(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete(node.right, temp.key)

        return self._balance(node)

    def __delitem__(self, key: K) -> None:
        if key is not None:
            self._root = self._delete(self._root, key)

    def __len(self):
        return self._size
