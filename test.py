from CountSketch.CountSketch import CountSketch
import random
import numpy as np

cs = CountSketch(100, 100)
s = np.random.normal(10, 1, 1000)
rng = [0, 20]

for num in s:
    num = round(num)
    if num in range(rng[0], rng[1]):
        cs.add(num.to_bytes(2, "big"))

estimates = []
for i in range(rng[0], rng[1]):
    q = i.to_bytes(2, "big")
    estimates.append(cs.estimate(q))

print(f"sum: {np.sum(estimates)}")
print(estimates)