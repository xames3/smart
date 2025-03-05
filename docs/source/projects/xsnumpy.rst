.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, March 01 2025
.. Last updated on: Wednesday, March 05 2025

:og:title: Building xsNumpy
:og:description: Journey of building a lightweight, pure-python implementation
    of NumPy's core features
:og:type: article

.. _project-building-xsnumpy:

===============================================================================
Building xsNumpy
===============================================================================

.. author::
    :name: Akshay Mestry
    :email: xa@mes3.dev
    :about: DePaul University
    :avatar: https://avatars.githubusercontent.com/u/90549089?v=4
    :github: https://github.com/xames3
    :linkedin: https://linkedin.com/in/xames3
    :timestamp: Mar 01, 2025

.. rst-class:: lead

    Learning doesn't stop at using libraries, it starts when you build your
    own one line at a time

So it all kicked off in mid-November of 2024. Like usual, I was knee-deep in a
Machine Learning project, tinkering with `NumPy`_ every single day. I was
slicing and dicing arrays, `multiplying matrices`_, and running complex
mathematical operations, all with just a line or two of code. It was working a
treat, like pure magic. But, just like any magic trick, I had no idea
whatsoever how in the world it actually worked!

I remember starting with a simple bit of code, nothing fancy.

.. code-block:: python
    :linenos:

    import numpy as np

    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    c = np.dot(a, b)

The result popped out instantly, no errors, no fuss. But this time, instead of
just taking the output at face value, I asked myself, how the hell did
:func:`numpy.dot` know how to multiply those matrices? And hang on, I was doing
matrix multiplication right, then why the heck am I doing :func:`numpy.dot`
when I could've done something like ``a @ b`` which is more explicit?

What's going on here? If :func:`numpy.dot` does matrix multiplication, then
what in the blazes does :py:data:`numpy.matmul` or ``a @ b`` do? Why are there
two different ways to do the same thing? Is NumPy broken, or am I just missing
something dead obvious?

I couldn't let this slide. That's when I decided to learn more about these and
thought of building `xsNumPy`_.

.. _reasons-behind-xsnumpy:

-------------------------------------------------------------------------------
Reasons behind xsNumPy
-------------------------------------------------------------------------------

Now that I was motivated to learn the nitty-gritty implementation details of
NumPy, I was ready to build my own scrappy version of it. I mean, I didn't set
out to create something to rival NumPy. Because let's be real, NumPy is a
bloody powerhouse, built over decades of work and backed by incredible mad lads
in math and science, plus tons of optimisations in place. I possibly can't
compete with that!

Nonetheless, I realised something quite important. Just because its dense and
complicated, it doesn't mean I can't try to understand it. I realised I'd been
treating NumPy like a black box. I was chucking numbers at it, calling its
functions and underlying APIs without truly understanding how they worked! I
was gutted and felt a massive gap in my understanding. Sure, I was smashing
out Machine Learning models, fiddling with arrays, tensors, and pulling off
all sorts of matrix wizardry. But every time I used something like
:func:`numpy.linalg.inv` or :func:`numpy.einsum`, there was this nagging
feeling: I was just trusting the library to do its thing, without knowing why
it worked.

This realisation hit me so hard, I challenged myself, *Could I build a dinky
version of NumPy from scratch?* Again, not to replace it, that'd be barking
mad, but to learn from it. If I really want to ace at teaching these stuff to
my students, I had to go deeper.

.. image:: ../assets/need-to-go-deeper-meme.png
    :alt: We need to go deeper meme from Inception

There were a few other reasons for writing xsNumPy besides my lack of
understanding about the NumPy internals. I essentially wanted to break free
from the *"Oh, Neural Networks are like black box"* rubbish. When I'm teaching
Machine Learning and Neural Networks, I often compare these scientific
computing libraries to a car. You can go places, sure, but what happens when
something breaks? What do you do then? So to get around this situation, I
thought of actually learning it by building.

xsNumPy isn't just for me. It's for anyone and everyone who's ever stared at a
piece of Machine Learning code and asked, *"How in God's name does this bloody
thing works?"*

.. _building-process:

-------------------------------------------------------------------------------
Building Process
-------------------------------------------------------------------------------

So with the "whys" being explained, I'll explain the "hows". I was ready to
build my scrappy little version of NumPy, but I didn't know where to start. So,
like any sensible person, I did what we all do when we're lost |dash| I started
poking and prodding at various NumPy functions and methods, trying to suss out
what made them tick. It didn't take long to twig that most of NumPy's APIs
lean heavily on one core construct, the :func:`numpy.array` function. But
here's the kicker, it's just a cheeky little wrapper for the mighty
:class:`numpy.ndarray`. Aha! That's where I decided to start, implementing my
primary ``xsnumpy.ndarray`` data structure.

Now, I'll be straight with you, it all seemed dead simple in my head at first.
I mean, what's an array, really? A bunch of numbers neatly arranged in some
orientations like rows and columns, right?

Wrong.

The deeper I dug, the more worms came wriggling out. `Memory allocation`_,
`shape`_ (size) calculations, `strides`_, and optimising how the data's stored,
it was like opening Pandora's box. Turns out, building even a barebones
version of :class:`numpy.ndarray` is a bit of a faff. Still, after a few weeks
of head-scratching, I managed to cobble together a working, albeit minimal,
version using :py:mod:`ctypes`.

.. code-block:: python
    :linenos:

    class ndarray:
        """Simplified implementation of a multi-dimensional array.

        An array object represents a multidimensional, homogeneous
        collection or list of fixed-size items. An associated data-type
        property describes the format of each element in the array.

        :param shape: The desired shape of the array. Can be an int for
            1D arrays or a sequence of ints for multidimensional arrays.
        :param dtype: The desired data type of the array, defaults to
            `None` if not specified.
        :param buffer: Object used to fill the array with data, defaults to
            `None`.
        :param offset: Offset of array data in buffer, defaults to `0`.
        :param strides: Strides of data in memory, defaults to `None`.
        :param order: The memory layout of the array, defaults to `None`.
        :raises RuntimeError: If an unsupported order is specified.
        :raises ValueError: If invalid strides or offsets are provided.
        """

        def __init__(
            self,
            shape: _ShapeLike | int,
            dtype: None | DTypeLike | _BaseDType = None,
            buffer: None | t.Any = None,
            offset: t.SupportsIndex = 0,
            strides: None | _ShapeLike = None,
            order: None | _OrderKACF = None,
        ) -> None:
            """Initialise an `ndarray` object from the provided shape."""
            if order is not None:
                raise RuntimeError(
                    f"{type(self).__qualname__} supports only C-order arrays;"
                    " 'order' must be None"
                )
            if not isinstance(shape, Iterable):
                shape = (shape,)
            self._shape = tuple(int(dim) for dim in shape)
            if dtype is None:
                dtype = float64
            elif isinstance(dtype, type):
                dtype = globals()[
                    f"{dtype.__name__}{'32' if dtype != builtins.bool else ''}"
                ]
            else:
                dtype = globals()[dtype]
            self._dtype = dtype
            self._itemsize = int(_convert_dtype(dtype, "short")[-1])
            self._offset = int(offset)
            if buffer is None:
                self._base = None
                if self._offset != 0:
                    raise ValueError("Offset must be 0 when buffer is None")
                if strides is not None:
                    raise ValueError("Buffer is None; strides must be None")
                self._strides = calc_strides(self._shape, self.itemsize)
            else:
                if isinstance(buffer, ndarray) and buffer.base is not None:
                    buffer = buffer.base
                self._base = buffer
                if isinstance(buffer, ndarray):
                    buffer = buffer.data
                if self._offset < 0:
                    raise ValueError("Offset must be non-negative")
                if strides is None:
                    strides = calc_strides(self._shape, self.itemsize)
                elif not (
                    isinstance(strides, tuple)
                    and all(isinstance(stride, int) for stride in strides)
                    and len(strides) == len(self._shape)
                ):
                    raise ValueError("Invalid strides provided")
                self._strides = tuple(strides)
            buffersize = self._strides[0] * self._shape[0] // self._itemsize
            buffersize += self._offset
            Buffer = _convert_dtype(dtype, "ctypes") * buffersize
            if buffer is None:
                if not isinstance(Buffer, str):
                    self._data = Buffer()
            elif isinstance(buffer, ctypes.Array):
                self._data = Buffer.from_address(ctypes.addressof(buffer))
            else:
                self._data = Buffer.from_buffer(buffer)

.. note::

    This isn't the full-fat version of the implementation. I've skimmed over a
    lot of the gory details for brevity. If you want to get into the weeds,
    check out the full ``xsnumpy.ndarray`` class on GitHub.

    `See here <https://github.com/xames3/xsnumpy/blob/main/xsnumpy/_core.py>`_
    |right|

.. _deconstructing-ndarray:

Deconstructing ndarray
===============================================================================

Alright, let me break this down in a way that makes sense. First up, the shape
of the array. I started by checking if the shape was an instance of
:py:class:`collections.abc.Iterable`. Basically, if it was a :py:class:`tuple`
or a :py:class:`list`. If it wasn't, I wrapped it in a tuple, making sure the
shape always looked like a tuple. Then, I converted the shape into a tuple of
integers, because let's face it, you can't have non-integer dimensions knocking
about in an array.

.. code-block:: python
    :linenos:

        if not isinstance(shape, Iterable):
            shape = (shape,)
        self._shape = tuple(int(dim) for dim in shape)

Next up, the ``dtype`` (data type). If you didn't provide a ``dtype``, the
constructor would default it to ``None``. If a :py:class:`type` (such as
:py:class:`int` or a :py:class:`float`) is provided, it dynamically retrieves
the appropriate data type from the global namespace using :func:`globals`. This
nifty trick meant I could dynamically fetch whatever data type you fancied.

Once resolved, the data type was assigned to ``self._dtype``.

.. code-block:: python
    :linenos:

        if dtype is None:
            dtype = float64
        elif isinstance(dtype, type):
            dtype = globals()[
                f"{dtype.__name__}{'32' if dtype != builtins.bool else ''}"
            ]
        else:
            dtype = globals()[dtype]
        self._dtype = dtype

Now, the size of each element in the array. I wrote a neat little function
called ``_convert_dtype``. Its job? To fetch the size of the given data type
in its shortest format. This is super important for calculating memory layout
and strides.

.. code-block:: python
    :linenos:

        self._itemsize = int(_convert_dtype(dtype, "short")[-1])

Right, on to the ``buffer``. If no ``buffer`` was provided, the array was
initialised without an external memory buffer. In this case:

- The offset must be zero
- Strides must also be ``None``

The constructor would then calculate the strides, which, put simply, are just
the number of bytes between consecutive elements in memory.

.. code-block:: python
    :linenos:

        if buffer is None:
            self._base = None
            if self._offset != 0:
                raise ValueError("Offset must be 0 when buffer is None")
            if strides is not None:
                raise ValueError("Buffer is None; strides must be None")
            self._strides = calc_strides(self._shape, self.itemsize)


But what if a buffer was provided?

Well, then it got a bit trickier. The constructor checked if the buffer was
another ``ndarray``. If it was, it nabbed the base buffer. The buffer was
assigned to ``self._base``, and the strides were either given directly or
calculated. Before moving on, the constructor did a bit of housekeeping:

- Offset had to be non-negative (you can't have a negative starting point in
  memory!)
- Strides had to be a tuple of integers matching the shape's dimensions
  otherwise, the whole thing would fall apart

.. code-block:: python
    :linenos:
    :emphasize-lines: 7-10

        else:
            if isinstance(buffer, ndarray) and buffer.base is not None:
                buffer = buffer.base
            self._base = buffer
            if isinstance(buffer, ndarray):
                buffer = buffer.data
            if self._offset < 0:
                raise ValueError("Offset must be non-negative")
            if strides is None:
                strides = calc_strides(self._shape, self.itemsize)
            elif not (
                isinstance(strides, tuple)
                and all(isinstance(stride, int) for stride in strides)
                and len(strides) == len(self._shape)
            ):
                raise ValueError("Invalid strides provided")
            self._strides = tuple(strides)

Finally, calculating the total buffer size. This was worked out using the
strides, shape, and item size. The ``buffer`` itself was a type derived from
the data type (dtype) and its size. Depending on whether a buffer was passed
or not, the constructor handled it like so:

- If no buffer is provided, a new buffer is created
- If the buffer is a :py:class:`ctypes.Array`, the address of the buffer
  is used to initialise the data. Basically, we use its address like a map
- If it's any other type of buffer, the buffer is used directly

Phew |dash| that was a fair bit, wasn't it?

But now you can see how all the pieces fit together. From handling shapes and
data types to calculating strides and buffers. It's all a bit mad when you
first dive in, but once you get the hang of it, it starts clicking into place.

.. _the-easy-peasy-stuff:

The "easy peasy" stuff
===============================================================================

Like I said before, I wanted to build a tiny version of NumPy. It was my clear
and straightforward goal. Start small, build arrays, and then add the fancy
operations like matrix multiplication, `broadcasting`_, and so on. What took me
by surprise was the fact that how challenging things were, which I thought to
be **"easy peasy"**. Things like writing a :py:func:`repr` or overriding the
built-in methods.

I remember talking to myself one morning, *"let's start with something dead
easy, perhaps just display the array."* That couldn't be hard, right? All I
need to do is print the content of my array in a readable format how NumPy
does. Little did I know I was shooting myself in the foot. At its core, a
``repr`` is just an object's internal data representation. I started with
something like this...

.. code-block:: python
    :linenos:

    def __repr__(self) -> str:
        return f"array({self._data}, dtype={self.dtype.__str__()})"

Sure, it worked for a scalar. But what about vectors? With some adjustments, I
got it working for 1D arrays. Feeling chuffed, I tried a 2D array. Suddenly, it
printed everything as a flat list. I realised that I hadn't accounted rows and
columns in my initial implementation. No problem, I updated the code slightly
to make it work and after some initial struggles, I got it working... just
about!

Then the 3D arrays... and it broke again.

That's when it hit me, this wasn't just about formatting strings. I needed a
proper solution that would work with **any** number of dimensions. A few days
later, I found myself deep into recursive logic and multi-dimensional indexing,
all for what I believed was a **"easy peasy"** print function. Now the problem
wasn't just getting this thing to work but rather making sure it worked
consistently across all the possible array shapes. What I thought would take
an hour or two dragged on for days.

But finally, I cracked it!

.. note::

    You can read about the complete implementation of the
    ``xsnumpy.ndarray.__repr__`` on GitHub.

    `See this <https://github.com/xames3/xsnumpy/blob/main/xsnumpy/_core.py>`_
    |right|

Just when I thought the hard part was done and dusted, I moved on to array
indexing which is perhaps one of the biggest superpowers of NumPy. At first, I
assumed this would be easy too, and it worked... partly.

.. code-block:: python
    :linenos:

    def __getitem__(self, index) -> t.Any:
        row, column = index
        flat = row * self.shape[1] + column
        return self.data[flat]

When I tried a slice like ``array[:, 1]``, it broke. When I tried with
higher-dimensional arrays, it fell apart! With each new test case, it became
pretty obvious that there were some significant flaws in my logic. I wasn't
just building some way to access data, I was constructing a flexible system
needed to mirror NumPy's powerful, intuitive `indexing`_.

.. image:: ../assets/sigh-meme.jpg
    :alt: Deep sigh meme

After days of trial and error, I finally realised, these so-called **"easy
peasy"** methods were actually sly little gateways into NumPy's deeper design
philosophies:

- **Consistency.** Whether you're tinkering with 1D, 2D, or N-D arrays, the
  operations should behave like clockwork, no surprises, Sherlock!
- **Efficiency.** Slices and views shouldn't faff about copying data
  willy-nilly, they ought to create references, keeping things lean and mean.
- **Extensibility.** Indexing had to be nimble enough to handle both the
  simple stuff (``array[1, 2]``) and the proper head-scratchers (
  ``array[1:3, ...]``).

What kicked off as a laid-back attempt to rework :py:func:`repr` and
other important methods ended up being a right masterclass in designing for
generality. I wasn't just sorting out the easy bits, I had to step back and
think like a "library designer", anticipating edge cases and making sure the
whole thing didn't crumble the moment someone tried something a tad clever.
As of writing about xsNumPy, a couple of months later, this struggle taught me
something profound, what seems super duper simple on the surface often hides
massive complexity underneath.

And that's exactly why building xsNumpy has been so powerful for my learning.

.. _illusion-of-simplicity:

Illusion of simplicity
===============================================================================

Well, after wrestling with the **"simple"** things, I naively thought the
hardest and in all honesty, the boring part of xsNumPy was behind me. I was
chuffed and excited than ever before for the **"fun"** stuff |dash|
element-wise arithmetics, broadcasting, and other random functions. What I
didn't realise was that my journey was about to get even more mental. If
implementing the ``ndarray`` class was untangling a knot, matrix operations
felt like trying to weave my own thread from scratch. Not sure, if that makes
sense.

But the point was, it was hard!

If you've read it till this point, you might've noticed a trend in my thought
process. I assume things to be quite simple, which they bloody aren't and I
start small. This was nothing different. I started simple, at least that's what
I thought. Basic arithmetic operations like addition, subtraction, and scalar
multiplication seemed relatively straight. I figured I could just iterate
through my flattened data and perform operations element-wise. And it worked...
for the first few test cases.

.. code-block:: python
    :linenos:
    :emphasize-lines: 20,27

    def __add__(self, other: ndarray | int | builtins.float) -> ndarray:
        """Perform element-wise addition of the ndarray with a scalar or
        another ndarray.

        This method supports addition with scalars (int or float) and
        other ndarrays of the same shape. The resulting array is of the
        same shape and dtype as the input.

        :param other: The operand for addition. Can be a scalar or an
            ndarray of the same shape.
        :return: A new ndarray containing the result of the element-wise
            addition.
        :raises TypeError: If `other` is neither a scalar nor an
            ndarray.
        :raises ValueError: If `other` is an ndarray but its shape
            doesn't match `self.shape`.
        """
        arr = ndarray(self.shape, self.dtype)
        if isinstance(other, (int, builtins.float)):
            arr[:] = [x + other for x in self._data]
        elif isinstance(other, ndarray):
            if self.shape != other.shape:
                raise ValueError(
                    "Operands couldn't broadcast together with shapes "
                    f"{self.shape} {other.shape}"
                )
            arr[:] = [x + y for x, y in zip(self.flat, other.flat)]
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: {type(self).__name__!r} "
                f"and {type(other).__name__!r}"
            )
        return arr

But, as always, the system collapsed almost immediately for higher-dimensional
vectors. What if I added a scalar to a matrix? Or a ``(3,)`` array to a
``(3, 3)`` matrix? Could I add floats to ints? I mean this lot works in normal
math, right? Each new **"simple"** operation posed a challenge in itself. I
realised I wasn't just adding or multiplying numbers but recreating NumPy's
`broadcasting`_ rules.

Trust me lads, nothing compared to the chaos caused by the matrix
multiplication. Whilst coding the initial draft of the ``__matmul__``, I
remember discussing this with my friend, :ref:`cast-sameer-mathad`. I thought
it'd be just a matter of looping through rows and columns, summing them
element-wise. Classic high school math, if you ask me. And it worked as well...
until I tried with higher-dimensional arrays. This is where I realised that
matrix multiplication isn't just about rows and columns but about correctly
handling **batch dimensions** for higher-order tensors. I found myself diving
into NumPy's documentation, reading about the **Generalised Matrix
Multiplication (GEMM)** routines and how broadcasting affects the output
shapes.

.. note::

    You can check out the complete implementation of arithmetic operations on
    GitHub.

    `Learn more
    <https://github.com/xames3/xsnumpy/blob/main/xsnumpy/_core.py>`_ |right|

.. _aha-moment:

"Aha!" moment
===============================================================================

This happened during the winter break. I didn't have to attend my uni and was
working full-time on this project. After days of debugging, I realised that
all of my vector operations weren't about **"getting the math right"**, but
they were about thinking like NumPy:

- **Shape manipulation.** How do I infer the correct output shape?
- **Broadcasting.** How can I extend the smaller arrays to fit the larger ones?
- **Efficiency.** How can I minimise unnecessary data duplication?

At this stage, I wasn't just rebuilding some scrappy numerical computing
doppleganger but rather a flexible and extensible system that could handle both
the intuitive use cases and the weird edge cases. As I started more along the
lines of NumPy developers, I started coming up with more broader and general
solutions.

.. _NumPy: https://numpy.org/
.. _multiplying matrices: https://www.mathsisfun.com/algebra/
    matrix-multiplying.html
.. _xsNumPy: https://github.com/xames3/xsnumpy
.. _Memory allocation: https://numpy.org/doc/stable/reference/
    c-api/data_memory.html
.. _shape: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    shape.html
.. _strides: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    strides.html
.. _broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
.. _indexing: https://numpy.org/doc/stable/user/basics.indexing.html
