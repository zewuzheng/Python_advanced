# What is pytorch
# Tensors are similar to NumPy’s ndarrays, with the addition being
# that Tensors can also be used on a GPU to accelerate computing.

from __future__ import print_function
import torch

# %%
# construct an uninitialize matrix
# An uninitialized matrix is declared, but does not contain definite known values before it is used.
# When an uninitialized matrix is created, whatever values were in the
# allocated memory at the time will appear as the initial values.
x = torch.empty(5, 3)
print(x)
x = torch.rand(5, 3)
print(x)
x = torch.zeros(5, 3, dtype=torch.long)
print(x)
x = torch.tensor([5.5, 3])
print(x)

# create a tensor based on an existing tensor. These methods will reuse properties
# of the input tensor, e.g. dtype, unless new values are provided by user
x = x.new_ones(5, 3, dtype=torch.double)      # new_* methods take in sizes
print(x)
x = torch.randn_like(x, dtype=torch.float)    # override dtype!
print(x)                                      # result has the same size

#%%
# Operations
y = torch.rand(5, 3)
print(x + y)
print(torch.add(x, y))

result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)

# adds x to y
y.add_(x)
print(y)

# Any operation that mutates a tensor in-place is post-fixed with an _.
# For example: x.copy_(y), x.t_(), will change x.
# You can use standard NumPy-like indexing with all bells and whistles!
print(x[:, 1])
print(x[1, :].size())

# Resizing: If you want to resize/reshape tensor, you can use torch.view:
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
print(x.size(), y.size(), z.size())

# If you have a one element tensor, use .item() to get the value as a Python number
x = torch.randn(1)
print(x)
print(x.item())

#%%
# Converting a Torch Tensor to a NumPy array and vice versa is a breeze.
#
# The Torch Tensor and NumPy array will share their underlying memory locations
# (if the Torch Tensor is on CPU), and changing one will change the other.
a = torch.ones(5)
print(a)
b = a.numpy()
print(b)

# See how the numpy array changed in value.
a.add_(1)
print(a)
print(b)

# Converting NumPy Array to Torch Tensor
# See how changing the np array changed the Torch Tensor automatically
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)

#%%
# CUDA Tensors
# Tensors can be moved onto any device using the .to method.
# let us run this cell only if CUDA is available
# We will use ``torch.device`` objects to move tensors in and out of GPU
if torch.cuda.is_available():
    device = torch.device("cuda")          # a CUDA device object
    y = torch.ones_like(x, device=device)  # directly create a tensor on GPU
    x = x.to(device)                       # or just use strings ``.to("cuda")``
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))       # ``.to`` can also change dtype together!

