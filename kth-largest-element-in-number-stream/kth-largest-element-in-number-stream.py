import random
import timeit
import heapq
import copy
import logging

from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt

logger = logging.getLogger()


def timer(func):
    """Time a function. 'runtimes'-list needs to be passed to the function as kwarg."""

    def inner(*args, **kwargs):
        start_time = timeit.default_timer()
        return_output = func(*args)
        kwargs['runtimes'].append(timeit.default_timer() - start_time)
        return return_output

    return inner


class KthLargestElement:
    """Class to process a stream with integer and return the kth largest element."""

    def __init__(self, initial_stream, k):

        self.runtimes_stupid = []
        self.runtimes_simple = []
        self.runtimes_heap = []

        self.k = k

        # Keep track of the whole stream for the stupid method
        self.stream = initial_stream

        # Create the sorted list for the simple method
        self.k_largest_elements_sorted_list = self._get_k_largest_elements(self.stream)[-self.k:]

        # Create the heap for the heap method
        self.k_largest_elements_heap = copy.deepcopy(self.k_largest_elements_sorted_list)
        heapq.heapify(self.k_largest_elements_heap)

    def _get_k_largest_elements(self, stream):
        return sorted(stream)[-self.k:]

    def _get_kth_largest_element(self, stream):
        return self._get_k_largest_elements(stream)[0]

    @timer
    def _add_stupid_method(self, number, **kwargs):

        # DUMB SOLUTION
        # Processing new number: O(1) - very simple append
        # Retrieving kth largest number: O(N) - need to go over all elements in the stream

        self.stream.append(number)
        return self._get_kth_largest_element(self.stream)

    @timer
    def _add_simple_method(self, number, **kwargs):

        # SIMPLE SOLUTION
        # Keep the k biggest items in a sorted shortlist
        # Processing new number: O(k) - need to resort the list with biggest numbers
        # Retrieving kth largest number: O(1) - kth largest element is the root of the shortlist

        # ASSUMPTION: self.k_largest_elements_sorted_list already contains k items
        if number > self.k_largest_elements_sorted_list[0]:
            self.k_largest_elements_sorted_list.append(number)
            self.k_largest_elements_sorted_list.pop(0)
            self.k_largest_elements_sorted_list.sort()
        return self.k_largest_elements_sorted_list[0]

    @timer
    def _add_heap_method(self, number, **kwargs):

        # EFFICIENT SOLUTION
        # Keep the k biggest items in a heap
        # Processing new number: O(log(k)) - need to smartly update part of the heap data structure
        # Retrieving kth largest number: O(1) - kth largest element is the root of the heap
        if number > self.k_largest_elements_heap[0]:
            # ASSUMPTION: self.k_largest_elements_heap already contains k items
            heapq.heappushpop(self.k_largest_elements_heap, number)
        return self.k_largest_elements_heap[0]

    def run_stream(self, number):
        """Add a number to the stream and get the kth largest number in three different ways."""

        assert (self._add_stupid_method(number, runtimes=self.runtimes_stupid) ==
                self._add_simple_method(number, runtimes=self.runtimes_simple) ==
                self._add_heap_method(number, runtimes=self.runtimes_heap))


if __name__ == "__main__":

    # Define the amount of numbers before the stream ends (N), k
    # and a smoothener for the plots (sigma)
    N = 100000
    k = 500
    sigma = 100

    # Generate an initial stream
    initial_stream = [random.randrange(10) for i in range(k)]

    # Initialize the class
    KthLargestElementObj = KthLargestElement(initial_stream=initial_stream, k=k)

    for i in range(N):

        # Generate a new number
        last_number = KthLargestElementObj.stream[-1]
        new_number = last_number + random.choice([-1, 0, 1, 1])

        # Print progress
        if i % 1000 == 0:
            print(f"{i}/{N} ({int(i / N * 100)}%) numbers processed.")

        # Add the new number to the stream
        KthLargestElementObj.run_stream(new_number)

    # Plot the results
    plt.plot(gaussian_filter1d(KthLargestElementObj.runtimes_stupid, sigma=sigma), label='Stupid')
    plt.plot(gaussian_filter1d(KthLargestElementObj.runtimes_simple, sigma=sigma), label='Simple')
    plt.plot(gaussian_filter1d(KthLargestElementObj.runtimes_heap, sigma=sigma), label='Heap')

    plt.yscale('log')

    plt.legend()

    plt.show()
