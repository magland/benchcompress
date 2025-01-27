import numpy as np
from zia_benchmark.algorithms.simple_ans.markov import markov_predict, markov_reconstruct
from zia_benchmark.algorithms.simple_ans.markov_reconstruct_wrapper import markov_reconstruct as markov_reconstruct_cpp

coeffs = np.array([1, 2, 3], dtype=np.float32)
initial = np.array([7, 5], dtype=np.int16)
resid = np.array([6, 7], dtype=np.int16)
a = markov_reconstruct(coeffs, initial, resid)

b = markov_reconstruct_cpp(coeffs, initial, resid)

print(a)
print(b)
print(type(b))
print(b.shape)
print(b.dtype)