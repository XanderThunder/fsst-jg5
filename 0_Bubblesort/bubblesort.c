/*
    Author: Alexander Schwaighofer
*/

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

// #define DEBUG

void shuffle(int *arr, int len) {
    int i, j, tmp;

    for (i = 0; i < len; i++) {
        j = rand() / (RAND_MAX / (len - 1) + 1);
        tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}

void sort(int *arr, int len) {
    int i, j, tmp;

    for (i = 1; i < len; i++) {
        for (j = 0; j < len - i; j++) {
            if (arr[j] > arr [j+1]) {
                tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;
            }
        }
    }
}

int main() {
    int item_cnt;

    printf("--- This program will sort a randomly sorted and generated list of integers with the bubblesort algorithm ---\n");
    
    // Get number of list entries from user
    printf("Please enter the number of items the generated list should contain: ");
    scanf("%d", &item_cnt);
    // Fill a sample list with values from 0 to item_cnt
    int array[item_cnt];
    for (int i = 0; i < item_cnt; i++) { array[i] = i; }
    shuffle(array, item_cnt);
    printf("\n\n... A shuffled input dataset was successfully created\n");
    
    // Start the timer for algorithm runtime measurement
    clock_t tic = clock();
    sort(array, item_cnt);
    clock_t toc = clock();
    double time_taken = ((double) toc - tic) / CLOCKS_PER_SEC;
    printf("... The list was successfully sorted. The operation completed in: %lf sec.\n", time_taken);

    #ifdef DEBUG
    for(int i = 0; i < item_cnt; i++) {
        printf("%d ", array[i]);
    }
    #endif

    return EXIT_SUCCESS;
}