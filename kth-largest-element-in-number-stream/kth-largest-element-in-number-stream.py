import random
import timeit
import heapq
import copy

from sortedcontainers import SortedList
from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt

def timer(func):

    def inner(*args, **kwargs):
        start_time = timeit.default_timer()
        return_output = func(*args)
        kwargs['runtimes'].append(timeit.default_timer() - start_time)
        return return_output

    return inner


class KthLargestElement:

    def __init__(self, initial_stream, k):

        self.runtimes_stupid = []
        self.runtimes_simple = []
        self.runtimes_bst = []
        self.runtimes_heap = []

        self.stream = initial_stream
        self.k = k

        # Create the sorted list for the simple method
        self.k_largest_elements_sorted_list = self._get_k_largest_elements(self.stream)[-self.k:]

        # Create the sorted container for the bst method
        self.k_largest_elements_bst = SortedList(self.k_largest_elements_sorted_list)

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

        if number > self.k_largest_elements_sorted_list[0]:
            self.k_largest_elements_sorted_list.append(number)
            self.k_largest_elements_sorted_list.pop(0)
            self.k_largest_elements_sorted_list.sort()
        return self.k_largest_elements_sorted_list[0]

    @timer
    def _add_bst_method(self, number, **kwargs):

        # BETTER SOLUTION
        # Keep the k biggest items in a BST tree

        if number > self.k_largest_elements_bst[0]:
            self.k_largest_elements_bst.add(number)
            self.k_largest_elements_bst.pop(0)
        return self.k_largest_elements_bst[0]

    @timer
    def _add_heap_method(self, number, **kwargs):

        # EFFICIENT SOLUTION
        # Keep the k biggest items in a heap
        if number > self.k_largest_elements_heap[0]:
            heapq.heappush(self.k_largest_elements_heap, number)
            heapq.heappop(self.k_largest_elements_heap)
        return self.k_largest_elements_heap[0]


    def add(self, number):

        self._add_stupid_method(number, runtimes=self.runtimes_stupid)
        self._add_simple_method(number, runtimes=self.runtimes_simple)
        self._add_bst_method(number, runtimes=self.runtimes_bst)
        self._add_heap_method(number, runtimes=self.runtimes_heap)


if __name__ == "__main__":

    sigma = 50

    N = 10000
    k = 5000

    initial_stream = [random.randrange(10) for i in range(k)]

    KthLargestElementObj = KthLargestElement(initial_stream=initial_stream, k=k)

    increment_options = [-1, 0, 1, 1]

    for i in range(N):

        last_number = KthLargestElementObj.stream[-1]
        new_number = last_number + random.choice(increment_options)

        KthLargestElementObj.add(new_number)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    ax1.plot(gaussian_filter1d(KthLargestElementObj.runtimes_stupid, sigma=sigma), label='Stupid')
    ax1.plot(gaussian_filter1d(KthLargestElementObj.runtimes_simple, sigma=sigma), label='Simple')
    ax1.plot(gaussian_filter1d(KthLargestElementObj.runtimes_bst, sigma=sigma), label='BST')
    ax1.plot(gaussian_filter1d(KthLargestElementObj.runtimes_heap, sigma=sigma), label='Heap')

    ax2.plot(gaussian_filter1d(KthLargestElementObj.runtimes_stupid, sigma=sigma), label='Stupid')
    ax2.plot(gaussian_filter1d(KthLargestElementObj.runtimes_simple, sigma=sigma), label='Simple')
    ax2.plot(gaussian_filter1d(KthLargestElementObj.runtimes_bst, sigma=sigma), label='BST')
    ax2.plot(gaussian_filter1d(KthLargestElementObj.runtimes_heap, sigma=sigma), label='Heap')

    ax1.set_ylim(.0003, .0006)  # outliers only
    ax2.set_ylim(0, .00003)  # most of the data

    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    plt.legend()

    plt.show()
