.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, March 01 2025
.. Last updated on: Monday, March 03 2025

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

So it all started in mid-November of 2024. Like usual, I was knee-deep in a
Machine Learning project, working with `NumPy`_ literally every single day. I
was slicing and dicing arrays, `multiplying matrices`_, and running complex
mathematical operations with just a line or two of code. Everything was
working great, like magic. But like all magic tricks, I had no idea whatsoever
how in the world it actually worked!

I remember starting with a simple code example, something like

.. code-block:: python
    :linenos:

    import numpy as np

    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    c = np.dot(a, b)

Since there was nothing wrong with the code, the result popped out instantly,
but this time, instead of accepting the result at face value, I asked myself,
how did :func:`numpy.dot` know how to multiply those matrices? But wait, I was
doing matrix multiplication right, then why the heck am I doing
:func:`numpy.dot` when I could've done something like ``a @ b`` which is more
explicit?

What is going on here? If :func:`numpy.dot` does matrix multiplication, then
what does :py:data:`numpy.matmul` or ``a @ b`` do? Why are there two different
methods to do the same thing? Is NumPy broken, or am I not understanding
something simple here?

That's when I decided to learn more about these and thought of building
`xsNumPy`_.

.. _the-why-behind-xsnumpy:

-------------------------------------------------------------------------------
The why behind xsNumPy
-------------------------------------------------------------------------------

Now that I was motivated to learn the nitty-gritty implementation details of
NumPy, I was ready to build my own version of it. I mean, I didn't set out to
create something to rival NumPy. Because let's be real, NumPy is a bloody
powerhouse, built over and backed by decades of work by incredible chaps in
math and science, plus tons of optimizations in place. I possibly can't
compete with that!

Nonetheless, I realized something quite important. Just because its dense and
complicated, it doesn't mean I can't try to understand it. I was literally
relying on it like a black box. I was using its functions and underlying APIs
without truly understanding how they worked! I was gutted and felt an enormous
gap in my understanding. Like I mentioned, I was writing models, manipulating
arrays, tensors, and performing all sorts of operations effortlessly. For
instance, whenever I was using functions like :func:`numpy.linalg.inv` or
:func:`numpy.einsum`, I couldn't shake the feeling that I was just
**"trusting"** the library to work, without understanding why it worked in the
first place.

This realization hit me so hard, I challenged myself, *Could I build a dinky
version of NumPy from scratch?* Again, not to replace it but to learn from it.
If I really want to ace at teaching these stuff to my students, I had to go
deeper.

.. image:: ../assets/need-to-go-deeper-meme.png
    :alt: We need to go deeper meme from Inception

There were a few other reasons for writing xsNumPy besides my lack of
understanding about the NumPy internals. I essentially wanted to break free
from the *"Oh, Neural Networks are like black box"* mindset. While teaching
Machine Learning and Neural Networks, I often compare these scientific
computing libraries to a car. You can go places, sure, but what happens when
something breaks? What do you do then? So to get around this situation, I
thought of actually learning it by building.

xsNumPy isn't just for me, it's for anyone and everyone who's ever asked,
*"How in the god's name this thing bloody works?"*

.. _building-process:

-------------------------------------------------------------------------------
Building Process
-------------------------------------------------------------------------------

So with the "whys" being explained, I'll explain the "hows". I was ready to
build my small version of NumPy, but I didn't know where to start. I began
scrutinizing and poking at various NumPy functions and methods. Soon I
realized that most of NumPy APIs rely on one core construct, the
:func:`numpy.array` function, which is a cheeky little wrapper for
:class:`numpy.ndarray`. That's where I decided to start, implementing my
primary ``xsnumpy.ndarray`` data structure.

To be honest, it seemed simple and fairly straightforward in my head |dash| a
collection of numbers arranged in rows and columns. I mean, what else could be
there in an array? Wrong! The more I dove deep into the implementation, more
things started poking their heads up. I had to think about
`memory allocation and management`_, calculations for `shape`_ (size),
`strides`_, and how to store the data more efficiently.

A few weeks in, I somehow got around implementing a barebones version of
:class:`numpy.ndarray` using :py:mod:`ctypes`.

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
            """Initialize an `ndarray` object from the provided shape."""
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

    This is not the complete implementation. For brevity, many details have
    been abstracted away. To see the complete implementation of the
    ``xsnumpy.ndarray`` class, check out the
    `code <https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L183>`_ on
    GitHub.

.. _deconstructing-ndarray:

Deconstructing ndarray
===============================================================================

Alright, let me break this down in a way that makes sense. First, I start with
checking if the shape is an :py:class:`collections.abc.Iterable` (a sequence
like a :py:class:`tuple` or :py:class:`list`). If it's not, I'm wrapping it
into a tuple to ensure that the shape is always represented as a tuple. The
shape is then converted into a tuple of integers, ensuring the dimensions are
valid.

.. code-block:: python
    :linenos:

        if not isinstance(shape, Iterable):
            shape = (shape,)
        self._shape = tuple(int(dim) for dim in shape)

Next up, the ``dtype`` (data type). If ``dtype`` is not provided, the
constructor sets the default data type to ``None``. If a :py:class:`type`
(such as :py:class:`int`, :py:class:`float`, etc.) is provided, it dynamically
retrieves the appropriate data type from the global namespace using
:func:`globals`. This allows flexibility in handling various types. Finally,
the resolved data type is assigned to ``self._dtype``.

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

The size of each element in the array is calculated based on the provided data
type. I wrote a handy function, ``_convert_dtype`` to fetch the appropriate
size of the data type (in a ``short`` format), and the last value is used to
determine the item size.

This is super important for calculating memory layout and strides!

.. code-block:: python
    :linenos:

        self._itemsize = int(_convert_dtype(dtype, "short")[-1])

Now, if ``buffer`` is ``None``, the array is initialized without an external
memory buffer. In this case:

- The offset must be zero
- Strides must also be ``None``

The constructor calculates the strides. The strides is nothing but steps
between consecutive elements in memory.

.. code-block:: python
    :linenos:

        if buffer is None:
            self._base = None
            if self._offset != 0:
                raise ValueError("Offset must be 0 when buffer is None")
            if strides is not None:
                raise ValueError("Buffer is None; strides must be None")
            self._strides = calc_strides(self._shape, self.itemsize)

If a ``buffer`` is provided, the constructor handles it by checking if it's
another ``ndarray``. If the ``ndarray`` has a base buffer, it uses that. The
buffer is assigned to ``self._base``, and strides are either provided or
calculated.

The constructor validates the offset (it must be non-negative) and the strides
(it must be a tuple of integers matching the shape's dimensions).

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

Finally, the constructor calculates the total buffer size based on the strides,
shape, and item size. The ``Buffer`` is a type derived from the data type
(dtype) and its size. Depending on whether the buffer is provided or not, it
initializes ``self._data`` using different methods:

- If no buffer is provided, a new buffer is created
- If the buffer is a :py:class:`ctypes.Array`, the address of the buffer
  is used to initialize the data. Basically, we use its address like a map
- If it's any other type of buffer, the buffer is used directly

Phew, that was a lot, but now you can see how it's all orchestrated!

.. _the-easy-peasy-stuff:

The "easy peasy" stuff
===============================================================================

Like I said before, I wanted to build a tiny version of NumPy. It was my clear
and straightforward goal. Start small, build arrays, and then add the fancy
operations like matrix multiplication, `broadcasting`_, and so on. What took me
by surprise was the fact that how challenging things were, which I thought to
be **"easy peasy"**. Things like writing a :py:func:`repr` or overriding the
built-in methods.

I remember talking to myself one morning, *"let's start with something bloody
easy, perhaps just display the array."* That couldn't be hard, right? All I
need to do is print the content of my array in a readable format how NumPy
does. Little did I know I was shooting myself in the foot. At its core, a
``repr`` is just an object's internal data representation. I started with
something like...

.. code-block:: python
    :linenos:

    def __repr__(self) -> str:
        return f"array({self._data}, dtype={self.dtype.__str__()})"

Sure, it worked for a scalar. But what about vectors? With some adjustments, I
got it working for 1D arrays. Being chuffed, I tried a 2D array. Suddenly, it
printed everything as a flat list. I realized that I had not accounted my
implementation for rows and columns. No problem, I updated the code slightly
to make it work and after some initial struggles, I got it working... barely!

Then the 3D arrays... and it broke again.

That's when it struck me, this wasn't merely about formatting strings. I needed
a generic solution that would work with **any** number of dimensions. A few
days later, I found myself deep into recursive logic and multi-dimensional
indexing, all for what I believed was a **"easy peasy"** print function. Now
the problem wasn't just getting this thing to work but rather make sure it
worked consistently across all the possible array shapes. What I thought would
take an hour or two took days.

But finally, I got it working!

.. note::

    You can read about the `complete <https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L275C1-L327C27>`_
    implementation of the ``xsnumpy.ndarray.__repr__`` on GitHub.

Just when I thought the hard part was over, I moved on to array indexing which
is perhaps one of the superpowers of NumPy. At first, I assumed this would be
easy too and it worked, partly.

.. code-block:: python
    :linenos:

    def __getitem__(self, index) -> t.Any:
        row, column = index
        flat = row * self.shape[1] + column
        return self.data[flat]

When I tried a slice like ``array[:, 1]``, it broke. When I tried with higher
dimensional arrays, it collapsed! With each new test case, it was pretty
evident that there were significant flows in my logic.

.. image:: ../assets/sigh-meme.jpg
    :alt: Deep sigh meme

.. _NumPy: https://numpy.org/
.. _multiplying matrices: https://www.mathsisfun.com/algebra/
    matrix-multiplying.html
.. _xsNumPy: https://github.com/xames3/xsnumpy
.. _memory allocation and management: https://numpy.org/doc/stable/reference/
    c-api/data_memory.html
.. _shape: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    shape.html
.. _strides: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    strides.html
.. _broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
