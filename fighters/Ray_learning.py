# %%
import ray

# %%
ray.init()

@ray.remote
def f(x):
    return x * x

futures = [f.remote(i) for i in range(4)]
print(ray.get(futures))  # [0, 1, 4, 9]
#%%
# Parallelizing Python Classes with Ray Actors
# Ray provides actors to allow you to parallelize an instance of a class in Python.
# When you instantiate a class that is a Ray actor, Ray will start a remote instance of that class in the cluster.
# This actor can then execute remote method calls and maintain its own internal state.

@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0

    def increment(self):
        self.n += 1

    def read(self):
        return self.n

counters = [Counter.remote() for i in range(4)]
[c.increment.remote() for c in counters]
futures = [c.read.remote() for c in counters]
print(ray.get(futures)) # [1, 1, 1, 1]