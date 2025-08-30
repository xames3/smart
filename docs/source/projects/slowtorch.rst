.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Friday, April 18 2025
.. Last updated on: Saturday, 30 August 2025

:og:title: PyTorch... But Slower
:og:description: PyTorch taught me how to build while SlowTorch taught me how
    it's built!
:og:type: article
:og:image: https://raw.githubusercontent.com/xames3/smart/main/docs/source/
    assets/media/slowtorch-meme.jpg

.. _project-slow-burning-torch:

===============================================================================
PyTorch... But Slower
===============================================================================

.. author::
    :name: Akshay Mestry
    :email: xa@mes3.dev
    :about: National Louis University
    :avatar: https://avatars.githubusercontent.com/u/90549089?v=4
    :github: https://github.com/xames3
    :linkedin: https://linkedin.com/in/xames3
    :timestamp: 15 Aug, 2025

.. rst-class:: lead

    What speed is to the machines... slowness is to the mind

There's some weird joy in those quiet moments after finishing a project. That
was exactly me in January of 2025, reflecting on xsNumPy. I had spent weeks
understanding the mysteries of arrays, memory buffers, and `broadcasting`_.
Like I mentioned in :doc:`that story <./xsnumpy>`, it felt like baking a cake
from scratch, where every ingredient and step mattered.

And yet, as I sat back gloating over my freshly baked xsNumPy, I found myself
hungry for something more. I wanted to feel that high again and explore
something new. Why not another library that had been a staple in my toolkit
since 2018, `PyTorch`_? It was time to show some love to it. I wondered if I
could build my own version of a simple `autograd`_ (automatic gradient) engine
or an `automatic differentiation`_ (autodiff, for short) library, slowly to
truly grasp its inner workings.

I mean, I've used PyTorch for years, but I had never really understood how it
worked under the hood, so why not? Thus, it all began...

.. _lessons-from-xsnumpy:

-------------------------------------------------------------------------------
Lessons from xsNumPy
-------------------------------------------------------------------------------

Before starting off with SlowTorch, I took a moment to reflect on the lessons I
learned while writing xsNumPy. It became super clear that the most valuable
insights came from the process of building it and not the results. Sure, the
results were important, but this reminded me that sometimes, the journey is
more important than the destination. xsNumPy taught me that **slowness can be a
gift** when you understand the fundamentals. When you're not chasing
performance, you can afford to be curious, experiment, make mistakes, and most
importantly, learn!

Much like my approach to xsNumPy, I wanted to take my time with SlowTorch too.
I wanted to build it slowly, understanding each component and appreciating the
complexity of the system. I had the same three rules...

.. admonition:: Rules of engagement

    - No LLMs or AI assistance. Every line of code and every solution had to
      come from my own understanding and experimentation.
    - Pure Python only. No external dependencies, just the standard library.
    - Clean, statically typed, and well-documented code that mirrored PyTorch's
      public APIs (mostly used ones), aiming to be a drop-in replacement where
      sensible.

.. _from-arrays-to-tensors:

-------------------------------------------------------------------------------
From arrays to tensors
-------------------------------------------------------------------------------

So, I started off with building SlowTorch. The first step was to understand the
core data structure of PyTorch, the :py:class:`tensor <torch.Tensor>` class.
It's basically the :class:`ndarray <numpy.ndarray>` equivalent of PyTorch. Much
of the initial work in building the tensor class was similar to what I had done
with xsNumPy, as :ref:`discussed here <crafting-my-first-array>`.

.. admonition:: :fas:`sparkles;sd-text-warning` Quick analogy

    To put it simply, if arrays were like egg cartons, tensors were like egg
    trays. Stacked in a way that you could easily access any egg (element) in
    the tray (tensor) without worrying about the carton (array) structure.

But this time, I had to add a few more things to make my tensor work like
PyTorch's. I needed to implement a way to save the node and operation history
for autodiff, which was a new concept for me. I also had to learn how to track
operations, gradients, and compute them efficiently.

`PyTorch's docs`_ and `community boards`_ were super helpful in understanding
the various properties and methods of the :py:class:`tensor <torch.Tensor>`
class. I started off with creating various :py:class:`dtypes <torch.dtype>`
like ``float64``, ``float32``, ``int64``, etc. alongside a simple
:py:attr:`device <torch.Tensor.device>`. But my devices were just strings, like
"cpu" or "gpu", with no actual hardware acceleration. The
:meth:`__repr__ <object.__repr__>` method was pretty similar to what I had in
xsNumPy, but I had to add a few more details to reflect the tensor's properties
like :py:attr:`shape <torch.Tensor.shape>`,
:py:attr:`device <torch.Tensor.device>`, :py:class:`dtype <torch.dtype>`, and
whether it :py:attr:`requires gradients <torch.Tensor.requires_grad>` or not.

.. note::

    Complete implementation of SlowTorch's |storch.tensor|_ with helper
    functions.

.. _walking-backwards:

-------------------------------------------------------------------------------
Walking backwards
-------------------------------------------------------------------------------

I was happy with my minimal implementation of the |storch.tensor|_ class, but
then I realised I needed to implement autodiff logic. `Autodiff`_ is arguably
the most important feature of PyTorch. It allows you to compute the gradients
of tensors with respect to a loss function, which is basically the backbone of
training a neural network. In more simple terms, it's a glorified version of
calculating `the chain rule`_ from calculus.

In PyTorch, calling :py:meth:`.backward() <torch.Tensor.backward>` on a tensor
magically tells every parameter (tensor) how it should change. But... how? What
does it truly mean for a tensor to change based on its history? How does it
know the appropriate path when asked to reverse its operations? To be super
duper honest, my initial attempts were a complete mess. I attempted to
meticulously track every operation, parent, and child tensor, resulting in a
code resembling a family tree. But Andrej's video made me realise that I was
overcomplicating things and I reworked on my implementation... slowly.

.. admonition:: :fas:`sparkles;sd-text-warning` Inspiration

    My guru, `Andrej Karpathy <https://karpathy.ai>`_, had explained this
    concept in much detail in his video where he builds
    `micrograd <https://github.com/karpathy/micrograd>`_, a simple autograd
    engine, from scratch. This video is perhaps the best introduction and
    explanation and the only thing you need to know about how autograd works,
    and it helped me a ton in understanding the core concepts. I highly
    recommend watching it!

.. youtube:: https://www.youtube.com/watch?v=VMj-3S1tku0

As I rewatched the video again and again, I realised that each operation could
be represented as a node, and each node could carry a little function, a recipe
for how to compute its own gradient. The real breakthrough came when I stopped
thinking of the graph as a static structure and started seeing it as a living,
breathing thing, growing with every operation. Thus, I created a ``Node`` class
that represented each operation, and each tensor would have a reference to its
parent nodes. This way, I could traverse the graph and compute gradients in a
more structured way.

.. code-block:: python
    :caption: :octicon:`file-code` `slowtorch/internal/tensor.py`_
    :emphasize-lines: 19-21

    class Tensor:

        def backward(self, inputs=None, retain_graph=False):
            if not self.requires_grad:
                raise RuntimeError("Tensors does not require grad")
            graph = []
            seen = set()
            self.grad = 1.0

            def iter_graph(inputs):
                if isinstance(inputs, Tensor) and inputs not in seen:
                    seen.add(inputs)
                    if hasattr(inputs.grad_fn, "inputs"):
                        for input in inputs.grad_fn.inputs:
                            iter_graph(input)
                    graph.append(inputs)

            iter_graph(inputs if inputs else self)
            for node in reversed(graph):
                if node.grad_fn is not None and callable(node.grad_fn):
                    node.grad_fn()
            self.grad = None
            if not retain_graph:
                self.grad_fn = None

Every tensor (node) carried a ``grad_fn`` node in the computation graph. When
you call ``backward``, the tensor does not just look at itself; it traces its
lineage, visiting every ancestor, and calls their gradient functions in reverse
order. It is a wee bit like walking back through your own footsteps after a
long hike, pausing at each fork to remember which way you came.

.. figure:: ../assets/media/shawshank-success-meme.gif
    :alt: Shawshank Redemption escape scene meme

    This was me when I finally got my backward pass working and could compute
    gradients for tensors

Long story short... I had built a simple autograd engine that could handle
basic operations like addition, multiplication, and even more complex ones like
matrix multiplication and broadcasting. I was able to compute gradients for
tensors with respect to a loss function, and it felt like I had finally
understood the magic behind PyTorch's autodiff and my small autograd engine was
working!!

.. admonition:: :octicon:`heart-fill;1em;sd-text-danger` Special shoutout

    I want to give a special shoutout to my colleague,
    :ref:`Fatemeh Taghvaei <cast-fatemeh-taghvaei>` for her patience and late
    night meetings. She helped me fix my broadcasting logic and brought a fresh
    perspective to my understanding and implementation of broadcasting in
    SlowTorch. I can't thank her enough for her support and guidance during
    this phase of the project.

.. _building-the-building-blocks:

-------------------------------------------------------------------------------
Building the building blocks
-------------------------------------------------------------------------------

Once my tensor with autodiff support was in place, I turned my attention to
the neural networks. PyTorch's :py:mod:`torch.nn` module is a marvel of
abstractions, and I wanted to recreate it from scratch. I began by defining
`Module`_, a base class that could hold parameters and submodules. This class
was responsible for managing the state of the model, including saving and
loading weights, switching between training and evaluation modes, and handling
parameter updates.

I was pacing through my development. Things were much clearer now. As more time
passed, I implemented many things. The layers, activations, losses, and
transforms were all implemented in their functional forms initially and later
wrapped around classes much like PyTorch.

.. tab-set::

    .. tab-item:: :octicon:`stack;1em;sd-text-primary` Layers

        `Layers`_ were implemented as functions that took tensors as ``input``
        and returned new tensors with the layer transformation applied (forward
        pass). Each layer function also had a backward pass that computed the
        gradient with respect to the input tensors.

        .. list-table::
            :header-rows: 1

            * - SlowTorch supports
              - Forward
              - Backward
            * - Linear (Fully Connected/Dense)
              - :math:`f(x) = xW^T + b`
              - :math:`f'(x) = \begin{cases} W &
                \text{for } x \\ x &
                \text{for } W \\ 1 &
                \text{for } b \end{cases}`
            * - Embedding
              - :math:`f(x) = W[x]`
              - :math:`f'(x) = \begin{cases} 1 &
                \; \; \text{for } W[x] \\ 0 &
                \; \; \text{for } W[j], j \neq x \end{cases}`

        For example, below is a minimal implementation of the linear layer in
        its functional form with its backward pass.

        .. code-block:: python
            :caption: :octicon:`file-code` `slowtorch/nn/functional/layer.py`_
            :emphasize-lines: 2,9-10

            def linear(input, weight, bias=None):
                new_tensor = input @ weight.T
                if bias is not None:
                    if bias._shape != (new_tensor._shape[-1],):
                        raise ValueError("Bias incompatible with output shape")
                    new_tensor += bias

                def AddmmBackward0():
                    input.grad += new_tensor.grad @ weight
                    weight.grad += new_tensor.grad.T @ input
                    if bias is not None:
                        bias.grad += new_tensor.grad.sum(dim=0)

                new_tensor.grad_fn = Node(AddmmBackward0)
                new_tensor.grad_fn.inputs = (input, weight, bias)
                return new_tensor

    .. tab-item:: :octicon:`graph;1em;sd-text-warning` Activations

        `Activation functions`_ were implemented as simple functions that took
        a tensor as ``input`` and returned a new tensor with the activation
        (forward pass) applied. Each activation function also had a backward
        pass that computed the gradient with respect to the input tensor.

        .. list-table::
            :header-rows: 1

            * - SlowTorch supports
              - Forward
              - Backward
            * - `Tanh`_
              - :math:`f(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}`
              - :math:`f'(x) = 1 - f(x)^2`
            * - `Sigmoid`_
              - :math:`f(x) = \frac{1}{1 + e^{-x}}`
              - :math:`f'(x) = f(x)(1 - f(x))`
            * - `ReLU`_
              - :math:`f(x) = \max(0, x)`
              - :math:`\:f'(x) = \begin{cases} 0 &
                \qquad \qquad \qquad \; \; \text{if } x < 0 \\ 1 &
                \qquad \qquad \qquad \; \; \text{if } x > 0 \end{cases}`
            * - `ELU`_
              - :math:`f(x) = \begin{cases} x &
                \text{if } x > 0 \\ \alpha(e^x - 1) &
                \text{if } x \leq 0 \end{cases}`
              - :math:`\:f'(x) = \begin{cases} 1 &
                \qquad \qquad \quad \; \; \text{if } x > 0 \\ \alpha e^x &
                \qquad \qquad \quad \; \; \text{if } x \leq 0 \end{cases}`
            * - `Softmax`_
              - :math:`f(x_i) = \frac{e^{x_i}}{\sum_{j} e^{x_j}}`
              - :math:`f'(x_i) = \begin{cases} f(x_i)(1 - f(x_i)) &
                \text{if } i = j \\ -f(x_i)f(x_j) &
                \text{if } i \neq j \end{cases}`
            * - Log Softmax
              - :math:`f(x_i) = \log\left(\frac{e^{x_i}}{\sum_{j} e^{x_j}}
                \right)`
              - :math:`f'(x_i) = \begin{cases} 1 - f(x_i) &
                \qquad \quad \text{if } i = j \\ -f(x_j) &
                \qquad \quad \text{if } i \neq j \end{cases}`

        For example, below is a minimal implementation of the sigmoid function
        with its backward pass.

        .. code-block:: python
            :caption: :octicon:`file-code`
                `slowtorch/nn/functional/pointwise.py`_
            :emphasize-lines: 10,13,19

            def sigmoid(input):
                new_tensor = Tensor(input._shape, input.dtype)
                storage = []
                if len(input._shape) == 1:
                    it = range(input._shape[0])
                else:
                    it = product(*[range(index) for index in input._shape])
                for index in it:
                    try:
                        storage.append(1.0 / (1.0 + math.exp(-input[index])))
                    except IndexError:
                        continue
                new_tensor[:] = storage

                def SigmoidBackward0():
                    if input.grad is None:
                        input.grad = Tensor(input._shape, input.dtype)
                    grad = new_tensor.grad
                    input.grad -= (new_tensor * (1 - new_tensor)) * grad

                new_tensor.grad_fn = Node(SigmoidBackward0)
                new_tensor.grad_fn.inputs = (input,)
                return new_tensor

    .. tab-item:: :octicon:`issue-reopened;1em;sd-text-danger` Losses

        `Loss functions`_ were implemented as functions that took two tensors,
        ``input`` and ``target``, and returned a new tensor representing the
        calculated loss (forward pass). Each loss function also had a backward
        pass that computed the gradient with respect to the input and target
        tensors.

        .. list-table::
            :header-rows: 1

            * - SlowTorch supports
              - Forward
              - Backward
            * - `Mean Squared Error (MSE)`_
              - :math:`f(x, y) = \frac{1}{n} \sum_{i=1}^{n} (x_i - y_i)^2`
              - :math:`f'(x, y) = \begin{cases} 2(x_i - y_i) / n &
                \text{mean} \\ 2(x_i - y_i) &
                \text{sum} \\ 2(x_i - y_i) &
                \text{none} \end{cases}`
            * - `L1 Loss`_
              - :math:`f(x, y) = \frac{1}{n} \sum_{i=1}^{n} |x_i - y_i|`
              - :math:`f'(x, y) = \begin{cases} |(x_i - y_i) / n| &
                \text{mean} \\ |(x_i - y_i)| &
                \text{sum} \\ |(x_i - y_i)| &
                \text{none} \end{cases}`
            * - `Cross Entropy`_
              - :math:`f(x, y) = -\sum_{i=1}^{n} y_i \log(x_i)`
              - :math:`f'(x, y) = \begin{cases} -\frac{y_i}{x_i} &
                \qquad \quad \; \; \text{mean} \\ -y_i &
                \qquad \quad \; \; \text{sum} \\ -y_i &
                \qquad \quad \; \; \text{none} \end{cases}`
            * - `Negative Log Likelihood (NLL)`_
              - :math:`f(x, y) = -\sum_{i=1}^{n} y_i \log(x_i)`
              - :math:`f'(x, y) = \begin{cases} -\frac{y_i}{x_i} &
                \qquad \quad \; \; \text{mean} \\ -y_i &
                \qquad \quad \; \; \text{sum} \\ -y_i &
                \qquad \quad \; \; \text{none} \end{cases}`

        For example, below is a minimal implementation of the mean squared
        error (MSE) loss function with its backward pass.

        .. code-block:: python
            :caption: :octicon:`file-code` `slowtorch/nn/functional/loss.py`_
            :emphasize-lines: 2,14-16

            def mse_loss(input, target, reduction="mean"):
                loss = (input - target) ** 2
                if reduction == "mean":
                    new_tensor = loss.sum() / loss.nelement()
                elif reduction == "sum":
                    new_tensor = loss.sum()
                elif reduction == "none":
                    new_tensor = loss

                def MseLossBackward0():
                    if None in (input.grad, target.grad):
                        input.grad = Tensor(input._shape, input.dtype)
                        target.grad = Tensor(target._shape, target.dtype)
                    grad = 2.0 / loss.nelement() if reduction == "mean" else 2.
                    input.grad += grad * (input - target)
                    target.grad -= grad * (input - target)

                new_tensor.grad_fn = Node(MseLossBackward0)
                new_tensor.grad_fn.inputs = (input, target)
                return new_tensor

    .. tab-item:: :octicon:`pivot-column;1em;sd-text-success` Transforms

        `Transformations`_ were implemented as functions that took a tensor as
        ``input`` and returned a new tensor with the transformation applied
        (forward pass). Each transform function also had a backward pass that
        computed the gradient with respect to the input tensor.

        .. list-table::
            :header-rows: 1

            * - SlowTorch supports
              - Forward
              - Backward
            * - Clone (Copy)
              - :math:`f(x) = x.clone()`
              - :math:`f'(x) = \begin{cases} 1 &
                \text{for } x \\ 0 & \text{for } x[j], j \neq i \end{cases}`
            * - Ravel (Flatten)
              - :math:`f(x) = x.ravel()`
              - :math:`f'(x) = \begin{cases} 1 &
                \text{for } x \\ 0 & \text{for } x[j], j \neq i \end{cases}`
            * - Transpose (T)
              - :math:`f(x) = x.transpose(dim_0, dim_1)`
              - :math:`f'(x) = \begin{cases} 1 &
                \text{for } x[dim_0] \\ 1 & \text{for } x[dim_1] \\ 0 &
                \text{for } x[j], j \neq dim_0, dim_1 \end{cases}`
            * - Reshape (View)
              - :math:`f(x) = x.reshape(shape)`
              - N/A (no backward pass implemented)
            * - Unsqueeze
              - :math:`f(x) = x.unsqueeze(dim)`
              - N/A (no backward pass implemented)
            * - One Hot Encoding
              - :math:`f(x) = \text{one_hot}(x, classes)`
              - N/A (no backward pass implemented)

        For example, below is a minimal implementation of the ravel (flatten)
        function with its backward pass.

        .. code-block:: python
            :caption: :octicon:`file-code`
                `slowtorch/nn/functional/mutation.py`_
            :emphasize-lines: 3,7

            def ravel(input):
                new_tensor = Tensor(input.nelement(), input.dtype)
                new_tensor[:] = input

                def ViewBackward0():
                    if input.grad is None:
                        input.grad = new_tensor.grad

                new_tensor.grad_fn = Node(ViewBackward0)
                new_tensor.grad_fn.inputs = (input,)
                return new_tensor

    .. tab-item:: :octicon:`sliders;1em;sd-text-info` Parameter

        `Parameters`_ were just tensors with a flag indicating whether they
        required gradients. For example, below is a minimal implementation of a
        SlowTorch parameter.

        .. code-block:: python
            :caption: :octicon:`file-code` `slowtorch/nn/modules/parameter.py`_

            class Parameter(Tensor):

                def __init__(self, data=None, requires_grad=True):
                    if data is None:
                        data = slowtorch.randn(1, requires_grad=requires_grad)
                    else:
                        data = data.clone()
                    data.requires_grad = requires_grad
                    for key, value in data.__dict__.items():
                        setattr(self, key, value)

                def __repr__(self):
                    return f"Parameter containing:\n{super().__repr__()}"

                @property
                def data(self):
                    return self

                @data.setter
                def data(self, value):
                    if not isinstance(value, Tensor):
                        raise TypeError("Parameter data must be a tensor")
                    self.storage[:] = value.storage

.. admonition:: :octicon:`heart-fill;1em;sd-text-danger` Massive thanks

    I want to thank my friends, :ref:`Sameer <cast-sameer-g-mathad>` and
    `Lucas Yong <https://www.linkedin.com/in/lucas-yong>`_ for their invaluable
    insights while implementing the `Softmax function`_'s backward pass. Lucas
    derived the gradients for Softmax and
    :download:`shared <../assets/docs/softmax_jacobian_lucas.pdf>` them via
    email, while Sameer helped me implement a crude version of second-order
    derivatives. Both were game-changers for me, helping me understand the core
    concepts of autodiff in a way that no documentation or blog post ever
    could.

Recreating neural networks from first principles reminded me of learning to
ride a bicycle without training wheels. I fell off a ton!! But each time I
got back on, I understood a little more. I was, in a way, backpropagating my
mistakes, learning from them, and adjusting my gradients...

.. _joy-of-manual-optimisation:

-------------------------------------------------------------------------------
Joy of manual optimisation
-------------------------------------------------------------------------------

With some of my neural network modules in place, I moved on to building my
optimiser, which presented another challenge. PyTorch's optimisers are elegant
and efficient, but I wanted to understand their mechanics. I implemented a
simple optimiser, manually updating its parameters step by step. Once I was
happy with my optimiser, I wrote a basic |storch.optim.Optimiser|_ class that
took a list of parameters and a learning rate, and it had an :python:`.step()`
method that updated the parameters based on their gradients.

.. code-block:: python
    :caption: :octicon:`file-code` `slowtorch/optim/optimiser.py`_

    class Optimiser:

        def __init__(self, params, lr=0.01):
            self.params = list(params)
            self.lr = lr

        def step(self):
            for param in self.params:
                if param.grad is None:
                    continue
                param -= self.lr * param.grad

It was slow and clunky, but I could see every calculation, update, and mistake.
I had to understand how each parameter was updated, how the learning rate
(:math:`\mu`) affected the updates, and how momentum (:math:`\mu`) could help
smooth out the learning process. With time, I learnt techniques that improved
the training process. Finally, I implemented my own version of the
`SGD <https://stackoverflow.com/a/48597579>`_ (Stochastic Gradient Descent)
optimiser, which was a simple yet effective way to update parameters based on
their gradients.

.. note::

    Check out SlowTorch's |storch.optim.Optimiser|_ and |storch.optim.SGD|_ for
    proper implementation details.

.. _embracing-slowness-as-a-virtue:

-------------------------------------------------------------------------------
Embracing slowness as a virtue
-------------------------------------------------------------------------------

As more time passed while building SlowTorch, I realised the hardest part
wasn't the code or maths, but the mindset. I knew I couldn't compete with
PyTorch's raw speed, so I had to let go of my desire for speed, elegance, and
perfection I always strived for as a Software Engineer. Instead, I embraced the
slowness, curiosity, and experimentation of a child. Every bug I encountered
was a lesson, and every unexpected result was an opportunity to recuperate and
learn. I quite often found myself talking to my code, asking it questions,
coaxing it to reveal its secrets.

While SlowTorch isn't a replacement for PyTorch, it's a learning tool for those
interested in understanding the inner workings of deep learning. It can perform
basic tasks like training a simple neural network, but it's not intended for
production use... if that's not obvious already.

.. figure:: ../assets/media/slowtorch-meme.jpg
    :alt: SlowTorch, embrace the journey, not the race meme
    :figclass: zoom

    By the end, this was me realising the true meaning of "slow" in SlowTorch
    and began embracing the slowness for understanding, over speed.

For me, personally, SlowTorch serves as a reminder that true understanding and
mastery come not from speed but from experience, attention, and care. It taught
me that sometimes, the slowest path is the fastest way to learn.

.. _xsNumPy: https://github.com/xames3/xsnumpy
.. _PyTorch: https://pytorch.org/
.. _broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
.. _automatic differentiation: https://www.reddit.com/r/learnprogramming/
   comments/u5nl1q/comment/i5333ru/?utm_source=share&utm_medium=web3x&
   utm_name=web3xcss&utm_term=1&utm_content=share_button
.. _Autodiff: https://pytorch.org/blog/overview-of-pytorch-autograd-engine/
.. _autograd: https://docs.pytorch.org/tutorials/beginner/introyt/
    autogradyt_tutorial.html
.. _the chain rule: https://www.mathcentre.ac.uk/resources/uploaded/
    mc-ty-chain-2009-1.pdf
.. _Module: https://github.com/xames3/slowtorch/tree/main/slowtorch/nn/modules/
    module.py
.. _Layers: https://github.com/xames3/slowtorch/blob/main/slowtorch/nn/
    functional/layer.py
.. _Activation functions: https://github.com/xames3/slowtorch/blob/main/
    slowtorch/nn/functional/pointwise.py
.. _Loss functions: https://github.com/xames3/slowtorch/blob/main/slowtorch/nn/
    functional/loss.py
.. _Transformations: https://github.com/xames3/slowtorch/blob/main/slowtorch/
    nn/functional/mutation.py
.. _Parameters: https://github.com/xames3/slowtorch/blob/main/slowtorch/nn/
    modules/parameter.py
.. _ReLU: https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.
    html#relu
.. _ELU: https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.
    html#elu
.. _Tanh: https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.
    html#tanh
.. _Sigmoid: https://ml-cheatsheet.readthedocs.io/en/latest/
    activation_functions.html#sigmoid
.. _Softmax: https://eli.thegreenplace.net/2016/the-softmax-function-and-its
    -derivative/
.. _Mean Squared Error (MSE): https://docs.pytorch.org/docs/stable/
    generated/torch.nn.MSELoss.html
.. _Cross Entropy: https://docs.pytorch.org/docs/stable/generated/
    torch.nn.CrossEntropyLoss.html
.. _Negative Log Likelihood (NLL): https://docs.pytorch.org/docs/stable/
    generated/torch.nn.NLLLoss.html
.. _L1 Loss: https://docs.pytorch.org/docs/stable/generated/
    torch.nn.L1Loss.html
.. _PyTorch's docs: https://docs.pytorch.org/docs/stable/
.. _community boards: https://discuss.pytorch.org/
.. _Softmax function: https://medium.com/@sue_nlp/
    what-is-the-softmax-function-used-in-deep-learning-illustrated-in-an-easy
    -to-understand-way-8b937fe13d49

.. _slowtorch/internal/tensor.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/internal/tensor.py
.. _slowtorch/optim/optimiser.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/optim/optimiser.py
.. _slowtorch/nn/modules/parameter.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/nn/modules/parameter.py
.. _slowtorch/nn/functional/mutation.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/nn/functional/mutation.py
.. _slowtorch/nn/functional/layer.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/nn/functional/layer.py
.. _slowtorch/nn/functional/pointwise.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/nn/functional/pointwise.py
.. _slowtorch/nn/functional/loss.py: https://github.com/xames3/slowtorch/
    blob/main/slowtorch/nn/functional/loss.py

.. |storch.tensor| replace:: ``tensor``
.. _storch.tensor: https://github.com/xames3/slowtorch/blob/main/slowtorch/
    internal/tensor.py
.. |storch.tensor.repr| replace:: ``tensor.__repr__``
.. _storch.tensor.repr: https://github.com/xames3/slowtorch/blob/main/
    slowtorch/internal/tensor.py
.. |storch.optim.Optimiser| replace:: ``Optimiser``
.. _storch.optim.Optimiser: https://github.com/xames3/slowtorch/blob/main/
    slowtorch/optim/optimiser.py
.. |storch.optim.SGD| replace:: ``SGD``
.. _storch.optim.SGD: https://github.com/xames3/slowtorch/blob/main/
    slowtorch/optim/optimiser.py
