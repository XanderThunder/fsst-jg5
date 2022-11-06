
# Project: An object-oriented implementation of Dijkstra's infamous Smoothsort comparison-based sorting algorithm in Python 3.10
# Author: Alexander Schwaighofer

import random, time

# user facing module export
def smooth_sort(arr: list) -> list:
    heap = LeonardoHeap(arr, len(arr))
    return heap.dequeue()


# Note: leonardo numbers must fulfill the following sequence:
# L(0) = 1
# L(1) = 1
# L(n) = L(n-2) + L(n-1) + 1

# hold a cache of leonardo numbers in a list
_L_cache = [1, 1, 3, 5, 9, 15, 25, 41, 67, 109,
    177, 287, 465, 753, 1219, 1973, 3193, 5167, 8361, 13529, 21891,
    35421, 57313, 92735, 150049, 242785, 392835, 635621, 1028457,
    1664079, 2692537, 4356617, 7049155, 11405773, 18454929, 29860703,
    48315633, 78176337, 126491971, 204668309, 331160281, 535828591,
    866988873]  # the next number is > 31 bits.

# return the n-th leonardo number
def _get_L(n):
    try:
        return _L_cache[n]
    # handle cache miss
    except IndexError:
        while len(_L_cache) <= n:
            _L_cache.append(_L_cache[-2] + _L_cache[-1] + 1)
        return _L_cache[n]


class LeonardoHeap():
    # arr -> input data set to be sorted in ascending order
    # size -> size of data set
    def __init__(self, arr, size) -> None:
        self.__arr = arr
        self.__size = size
        # store sizes of leonardo trees in forest in format [n] where n is the n-th leonardo number
        # -> very important for efficient traversal through heap
        self.__tree_sizes = []
        
        # create leonardo heap from arr
        self.__heapify()
    
    def __heapify(self):
        # fill heap until heap_end == size of input array
        for heap_end in range(self.__size):
            self.__push()
            self.__fix_roots(heap_end, len(self.__tree_sizes) - 1)

    def dequeue(self):
        #  decrease heap size when popping nodes
        for heap_size in reversed(range(self.__size)):
            self.__pop(heap_size)
        return self.__arr

    # left child located at arr[i - L(n-2) - 1]
    def __get_left_child(self, idx, n):
        return idx - _get_L(n - 2) - 1
    
    # right child located at arr[i - 1]
    def __get_right_child(self, idx):
        return idx - 1

    # pushes new node onto heap
    def __push(self):
        # current number of trees in forest
        nro_trees = len(self.__tree_sizes)

        # * there are essentially 3 cases to cover when adding a node to a leonardo heap
        # case 1: the two right most trees differ in leonardo order by just one
            # -> merge trees (seen left to right) L(n) and L(n-1) under a new root node of size L(n+1) 
        # * INFO: list[-1] means get the last, list[-2] second to last element
        if nro_trees > 1 and self.__tree_sizes[-2] == self.__tree_sizes[-1] + 1:
            self.__tree_sizes[-2] += 1
            del self.__tree_sizes[-1]
            return

        # case 2: last tree in forest is L(1) -> Add new tree of L(0)
        if nro_trees >= 1 and self.__tree_sizes[-1] == 1:
            self.__tree_sizes.append(0)
            return

        # case 3: forest is empty or no L(1) in forest -> add tree of L(1)
        self.__tree_sizes.append(1)

    # pops largest node from heap
    def __pop(self, heap_size):
        # pop rightmost tree size
        removed_size = self.__tree_sizes.pop()
        
        # * 2 cases to cover
        # case 1: popped single node tree
        if removed_size == 0 or removed_size == 1:
            return

        # case 2: popped tree has children
        # add exposed children back with their respective tree sizes
        self.__tree_sizes.append(removed_size - 1)
        self.__tree_sizes.append(removed_size - 2)
        right_child_idx = heap_size - 1
        left_child_idx = right_child_idx - _get_L(self.__tree_sizes[-1])
        # calculate indices in tree_sizes for exposed children
        right_size_idx = len(self.__tree_sizes) - 1
        left_size_idx = len(self.__tree_sizes) - 2
        # fix left and then fix right children
        self.__fix_roots(left_child_idx, left_size_idx)
        self.__fix_roots(right_child_idx, right_size_idx)


    # swaps root nodes if ordering violates rule of ascending root node values in heap
    # * Variables in this method refer to indices !
    def __fix_roots(self, start_heap_idx, start_size_idx):
        # start_size_idx refers to starting position index in tree_sizes list
        # start_heap_idx refers to starting position index in the entire heap
        cur_root = start_heap_idx
        cur_size = start_size_idx

        # keep swapping roots until correct sequence restored (extreme position: leftmost root of heap)
        while cur_size > 0:
            # travel L(n) elements back in the heap (i.e. jump to beginning of left tree/root) 
            next_root = cur_root - _get_L(self.__tree_sizes[cur_size])
            
            # break if roots are equal
            if self.__arr[next_root] <= self.__arr[cur_root]:
                break
            
            # break if next root is lesser than both children of current root
            if self.__tree_sizes[cur_size] > 1:
                right_child = self.__get_right_child(cur_root)
                left_child = self.__get_left_child(cur_root, self.__tree_sizes[cur_size])
                if self.__arr[next_root] <= self.__arr[right_child] or self.__arr[next_root] <= self.__arr[left_child]:
                    break

            # swap current root with next root
            self.__arr[cur_root], self.__arr[next_root] = self.__arr[next_root], self.__arr[cur_root]
            
            # next root becomes current root
            cur_size -= 1
            cur_root = next_root

        self.__sift_down(cur_root, self.__tree_sizes[cur_size])

    # sifts down node in tree
    # * Variables in this method refer to indices !
    def __sift_down(self, root_idx, tree_size):
        cur_node = root_idx

        # trickle down cur_node
        # tree_size will be set to subtree size of the subtree rooted at cur_node
        while tree_size > 1:
            right_child = self.__get_right_child(cur_node)
            left_child = self.__get_left_child(cur_node, tree_size)
            
            # do not swap
            if self.__arr[cur_node] >= self.__arr[left_child] and self.__arr[cur_node] >= self.__arr[right_child]:
                break

            # swap cur_node with right_child
            if self.__arr[right_child] >= self.__arr[left_child]:
                self.__arr[cur_node], self.__arr[right_child] = self.__arr[right_child], self.__arr[cur_node]
                cur_node = right_child
                tree_size -= 2
                continue

            # swap cur_node with left_child
            self.__arr[cur_node], self.__arr[left_child] = self.__arr[left_child], self.__arr[cur_node]
            cur_node = left_child
            tree_size -= 1



# manual testing case
if __name__ == "__main__":
    test_size = 100000
    # generate random data set
    arr = list(range(test_size))
    random.shuffle(arr)

    print(f"executing: smooth_sort({len(arr)})")
    t_start = time.perf_counter()
    sorted_arr = smooth_sort(arr)
    t_exec = time.perf_counter() - t_start
    print(f"exec time: {t_exec} sec")
    
    # assert sorting done correctly
    correct = all(a <= b for a, b in zip(sorted_arr, sorted_arr[1:]))
    if not correct:
        print("***** Sorting incorrect! *****")
        print(sorted_arr)
