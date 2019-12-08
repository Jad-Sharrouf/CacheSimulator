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
