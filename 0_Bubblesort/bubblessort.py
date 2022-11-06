# Author: Alexander Schwaighofer

import random, time

def shuffle(l: list):
    # Shuffle the list using Fisher-Yates algorithm
    for x in range(len(l)-1, 0, -1):
        # Generate a pseudo-random index from 0 to x
        y = random.randint(0, x+1)
        # Swap the current loop item with the random generated index
        l[x], l[y] = l[y], l[x]
    return l

def sort(l: list):
    for i in range(len(l)):
        for j in range(len(l)-1):
            if (l[j] > l[j+1]):
                l[j], l[j+1] = l[j+1], l[j]
    return l

if __name__ == "__main__":
    print("--- This program will sort a randomly sorted and generated list of integers with the bubblesort algorithm ---")
    
    # Get number of list entries from user
    item_cnt = int(input("Please enter the number of items the generated list should contain: "))
    # Fill a sample list with values from 0 to item_cnt
    sample_list = [i for i in range(item_cnt)]
    unsorted_list = shuffle(sample_list)
    print("\n... A shuffled input dataset was successfully created")

    # Start the timer for algorithm runtime measurement
    tic = time.perf_counter()
    sorted_list = sort(unsorted_list)
    toc = time.perf_counter()
    print(f"... The list was successfully sorted. The operation completed in: {toc - tic:0.4f} sec.\n")
