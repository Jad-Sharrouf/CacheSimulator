# Cache Simulator in Python

This is an implementation of a cache simulator that simulates Direct-Mapped, Fully-Associative, and Set-Associative caches using an LRU replacement policy.

## Testing

I've provided a couple of memory trace files for you to test with:

- 1KB_64B is a synthetic trace of accessing 1KB memory with a 64B block size (repeated for 2 iterations), using a 16-way 1KB cache, the simulator should produce a 50% miss rate.

- 4MB_4B is a synthetic trace of accessing 4MB memory with a 4B block size, using a 16-way 4MB cache, the simulator should produce a 2.08% miss rate.

- gcc.trace is a partial memory trace of a gcc compilation, using a 16-way 32KB cache, the simulator should produce a 1.89% miss rate.

- ls.trace is a partial memory trace of an ls invocation, using a 16-way 32KB cache, the simulator should produce a 2.17% miss rate.

- naive_dgemm.trace is a partial memory trace of a naive matrix multiplication of two 256x256 matrices with double-precision floats, using a 16-way 256KB cache, the simulator should produce a 50.24% miss rate.

You can also play around with the cacheSize, lineSize and ways variables in the code to experiment and see which produces the optimal cache miss rate.


## Results

Given a memory trace file, the simulator will output the cache miss rate and a filled table containing the set, slot, tag, data, and LRU (queue position).

Output Example:

   set  slot     tag                         data  LRU
   
0     0     0  000000  64 bytes from @000000000000  -15   
1     0     1  000001  64 bytes from @000001000000  -14   
2     0     2  000010  64 bytes from @000010000000  -13   
3     0     3  000011  64 bytes from @000011000000  -12   
4     0     4  000100  64 bytes from @000100000000  -11   
5     0     5  000101  64 bytes from @000101000000  -10   
6     0     6  000110  64 bytes from @000110000000   -9   
7     0     7  000111  64 bytes from @000111000000   -8

8     0     8  001000  64 bytes from @001000000000   -7

9     0     9  001001  64 bytes from @001001000000   -6

10    0    10  001010  64 bytes from @001010000000   -5

11    0    11  001011  64 bytes from @001011000000   -4

12    0    12  001100  64 bytes from @001100000000   -3

13    0    13  001101  64 bytes from @001101000000   -2

14    0    14  001110  64 bytes from @001110000000   -1

15    0    15  001111  64 bytes from @001111000000    0

Cache miss rate = 50.0% using a Fully-Associative cache.
