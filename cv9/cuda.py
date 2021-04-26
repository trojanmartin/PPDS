from __future__ import division
from numba import cuda
import numpy
import math


# CUDA kernel
@cuda.jit
def my_kernel(first_array, second_array):
    pos = cuda.grid(1)
    if pos < first_array.size:
        first_array[pos] += second_array[pos]  # do the computation


# Host code
first_array = numpy.ones(256)
second_array = numpy.ones(256) * 10
threadsperblock = 256
blockspergrid = math.ceil(first_array.shape[0] / threadsperblock)
my_kernel[blockspergrid, threadsperblock](first_array, second_array)
print(first_array)
