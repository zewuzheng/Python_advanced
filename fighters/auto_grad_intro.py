# Tensor torch.Tensor is the central class of the package. If you set its attribute .
# requires_grad as True, it starts to track all operations on it.
# When you finish your computation you can call .backward() and have all the gradients computed automatically.
# The gradient for this tensor will be accumulated into .grad attribute.

# To stop a tensor from tracking history, you can call .detach() to detach it from the computation history,
# and to prevent future computation from being tracked.

# To prevent tracking history (and using memory), you can also wrap the code block in with torch.no_grad():.
# This can be particularly helpful when evaluating a model because the model may have trainable parameters
# with requires_grad=True, but for which we don’t need the gradients.

# There’s one more class which is very important for autograd implementation - a Function.

# Tensor and Function are interconnected and build up an acyclic graph,
# that encodes a complete history of computation. Each tensor has a .grad_fn attribute that
# references a Function that has created the Tensor (except for Tensors created by the user - their grad_fn is None).

# If you want to compute the derivatives, you can call .backward() on a Tensor.
# If Tensor is a scalar (i.e. it holds a one element data), you don’t need to specify any arguments to backward(),
# however if it has more elements, you need to specify a gradient argument that is a tensor of matching shape.
#%%
import torch
import torchvision

x = torch.ones(5, 3, requires_grad=True)
print(x)
y = x+2
print(y)
print(y.grad_fn)

z = y*y*3
out = z.mean()
print(z, out)

# .requires_grad_( ... ) changes an existing Tensor’s requires_grad flag in-place.
# The input flag defaults to False if not given
a = torch.randn(2, 2)
a = ((a * 3) / (a - 1))
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)


#%%
# Gradients
# Let’s backprop now. Because out contains a single scalar,
# out.backward() is equivalent to out.backward(torch.tensor(1.)).
out.backward()
print(x.grad)


x = torch.randn(3, requires_grad=True)

y = x * 2
while y.data.norm() < 1000:
    y = y * 2

print(y)
# Now in this case y is no longer a scalar. torch.autograd could not compute the full Jacobian directly,
# but if we just want the vector-Jacobian product, simply pass the vector to backward as argument:
v = torch.tensor([1.0, 1.0, 1.0], dtype=torch.float)
y.backward(v)

print(x.grad)
# You can also stop autograd from tracking history on Tensors with
# .requires_grad=True either by wrapping the code block in with torch.no_grad():
print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
    print((x ** 2).requires_grad)

# Or by using .detach() to get a new Tensor with the same content but that does not require gradients:
print(x.requires_grad)
y = x.detach()
print(y.requires_grad)
print(x.eq(y).all())