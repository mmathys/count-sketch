import hashlib
from statistics import median

class CountSketch:
    def __init__(self, t: int, b: int):
        # t x b array of counters
        self.t = t
        self.b = b
        self.C = [[0] * b for i in range(t)]
        self.hash = hashlib.sha256

    def sha256_salted_mod(self, obj: bytes, salt: int, mod: int):
        assert salt in range(0, 2 ** 16)
        payload = (salt).to_bytes(2, "big") + obj
        h = self.hash()
        h.update(payload)
        res = int.from_bytes(h.digest(), "big")
        return res % mod

    def hash_h(self, q: bytes, i: int) -> int:
        return self.sha256_salted_mod(q, i, self.b)

    def hash_s(self, q: bytes, i: int) -> int:
        res = self.sha256_salted_mod(q, i, 2)
        if res == 0:
            return -1
        else:
            return 1

    def add(self, q: bytes):
        for i in range(self.t):
            h = self.hash_h(q, i)
            s = self.hash_s(q, i)
            self.C[i][h] += s

    def estimate(self, q: bytes):
        # naive implementation. should actually be implemented with max heap.
        estimates = []
        for i in range(self.t):
            h = self.hash_h(q, i)
            s = self.hash_s(q, i)
            estimates.append(self.C[i][h] * s)
        return median(estimates)
