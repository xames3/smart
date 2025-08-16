.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, 1 March 2025
.. Last updated on: Friday, 15 August 2025

:og:title: Building xsNumPy
:og:description: Journey of building a lightweight, pure-python implementation
    of NumPy's core features
:og:type: article

.. _project-building-xsnumpy:

===============================================================================
Building xsNumPy
===============================================================================

.. author::
    :name: Akshay Mestry
    :email: xa@mes3.dev
    :about: National Louis University
    :avatar: https://avatars.githubusercontent.com/u/90549089?v=4
    :github: https://github.com/xames3
    :linkedin: https://linkedin.com/in/xames3
    :timestamp: 4 Apr, 2025

.. rst-class:: lead

    Learning really begins when you build your own tools, one line at a time

It all started in mid-November 2024. I was working on a project where I had to
use NumPy. Arrays were being indexed, `matrices multiplied`_, and NumPy
effortlessly made complex tasks appear simple. However, beneath this
simplicity, a few questions began to gnaw at me.

So, I found myself experimenting with a simple code, nothing fancy.

.. code-block:: python
    :linenos:

    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.dot(a, b)

The result popped out instantly, with no errors. But this time, instead of
accepting the answer, I found myself asking why I was using
:func:`np.dot <numpy.dot>` when I could use
:py:data:`np.matmul <numpy.matmul>`, which feels more correct. And if
:func:`np.dot <numpy.dot>` indeed performs matrix multiplication, then what
does the :meth:`@ <object.__matmul__>` operator do? Why are there two
different ways to perform matrix multiplication, and which is the best?

.. _building-with-a-purpose:

-------------------------------------------------------------------------------
Building with a purpose
-------------------------------------------------------------------------------

Once I was motivated enough to learn the implementation details of NumPy, I was
ready to build my own scrappy version. I didn't set out to create something to
rival NumPy, it's a bloody powerhouse, built over decades of work by incredible
minds in maths and science, plus countless optimisations. I wanted to break
free from treating these libraries as black boxes and truly understand the
**whys** and **hows**.

This realisation hit me so hard that I challenged myself. Could I build a dinky
version of NumPy from scratch? If I really wanted to ace teaching these
concepts, I had to go deeper...

.. image:: ../assets/need-to-go-deeper-meme.jpg
    :alt: We need to go deeper meme from Inception

It felt a wee bit like baking a cake from scratch. Every ingredient, every
step, had to be understood and chosen deliberately. If I was going to learn
this properly, I needed discipline and some rules to follow.

.. admonition:: Rules of engagement

    - No LLMs or AI assistance. Every line of code and every solution had to
      come from my own understanding and experimentation.
    - Pure Python only. No external dependencies, just the standard library.
    - PEP8, mypy, and documentation. Clean, typed, well-documented code that
      mirrored NumPy's public APIs, aiming to be a drop-in replacement where
      sensible.

.. _crafting-my-first-array:

-------------------------------------------------------------------------------
Crafting my first array
-------------------------------------------------------------------------------

With my rules set, I started experimenting with NumPy's functions, trying to
understand their functionality. It quickly became evident that most of NumPy's
APIs heavily rely on a single core construct, the
:func:`np.array <numpy.array>` function. However, it's worth noting that this
function is a cheeky little wrapper for the
:class:`np.ndarray <numpy.ndarray>` class. That's where I decided to start,
implementing my own |xp.ndarray|_ data structure.

I had a simple understanding of an array as a collection of numbers neatly
organised in rows and columns. However, as I delved deeper, I discovered a
complex web of concepts, including `memory allocation`_, `shape`_
calculations, `strides`_, and various optimisation techniques for data storage.
It felt like opening Pandora's box!

.. admonition:: :fas:`sparkles;sd-text-warning` Quick analogy

    If you're new to arrays, think of them as egg cartons, each slot holds an
    egg, and the shape of the carton tells you how many eggs you've got. Where
    your hand moves from one slot to the next are the strides; the type of
    eggs is the dtype; the carton itself is the buffer.

After weeks of head-scratching, I managed to create a basic, albeit minimal,
working version using Python's built-in :py:mod:`ctypes` module. It wasn't
pretty, but it worked.

.. code-block:: python
    :caption: :octicon:`file-code` `xsnumpy/_core.py`_
    :linenos:

    class ndarray:

        def __init__(
            self, shape, dtype=None, buffer=None, offset=0, strides=None
        ):
            if not isinstance(shape, Iterable):
                shape = (shape,)
            self._shape = tuple(int(dim) for dim in shape)
            if dtype is None:
                dtype = globals()[dtype]
            self._dtype = dtype
            self._itemsize = int(_convert_dtype(dtype, "short")[-1])
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

    This section intentionally has removed a lot of details to keep things
    simple. Check out the complete implementation of |xp.ndarray|_ on GitHub.

.. _making-sense-of-shapes:

-------------------------------------------------------------------------------
Making sense of shapes
-------------------------------------------------------------------------------

I started by checking if the provided shape can be
:py:class:`iterated <collections.abc.Iterable>`. If it wasn't, I wrapped it in
a :py:class:`tuple`. Then, I converted the shape into a tuple of
:py:class:`integers <int>`, because you can't have non-integer dimensions
knocking about in an array.

.. code-block:: python
    :linenos:

        if not isinstance(shape, Iterable):
            shape = (shape,)
        self._shape = tuple(int(dim) for dim in shape)

Next up, the ``dtype`` (short for data type). If you didn't provide it, the
constructor would default it to :py:obj:`None`. If a :py:class:`float` or an
:py:class:`int` is provided, it dynamically retrieves the appropriate data
type from the global namespace using :func:`globals`. This nifty trick meant I
could dynamically fetch whatever data type you fancied.

Right, on to the ``buffer``. If no ``buffer`` was provided, the array was
initialised without an external memory buffer. In this case the offset must be
zero and strides must be :py:obj:`None`. The constructor would then calculate
the `strides`_, which, put simply, are just the number of bytes between
consecutive elements in memory.

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

Well, then it got a bit trickier. It used the base buffer and the strides were
either given directly or calculated.

.. code-block:: python
    :linenos:
    :emphasize-lines: 8

        else:
            if isinstance(buffer, ndarray) and buffer.base is not None:
                buffer = buffer.base
            self._base = buffer
            if isinstance(buffer, ndarray):
                buffer = buffer.data
            if strides is None:
                strides = calc_strides(self._shape, self.itemsize)
            self._strides = tuple(strides)

Finally, calculating the total buffer size. This was worked out using the
strides, shape, and item size. The ``buffer`` itself was a type derived from
the data type and its size. Depending on whether a buffer was passed or not,
the constructor handled it accordingly, either creating a new buffer or
using the existing one.

Phew... that was a fair bit, wasn't it?

.. _illusion-of-simplicity:

-------------------------------------------------------------------------------
Illusion of simplicity
-------------------------------------------------------------------------------

After all that hard work, I thought of giving myself a break. I remembered
telling myself, "Let's start with something dead easy... perhaps just display
the array." I thought, "That couldn't be hard, right? All I need to do is
print the content of my array in a readable format, just like NumPy does."

Little did I know, I was shooting myself in the foot. At its core,
:meth:`__repr__ <object.__repr__>` is an object's internal data
representation. I started with something simple, and it worked for scalars and
1D arrays.

.. code-block:: python
    :linenos:

    def __repr__(self):
        return f"array({self._data}, dtype={str(self.dtype)})"

Feeling quite pleased, I tried a 2D array, but it unexpectedly printed
everything as a flat list. I realised I hadn't accounted for the rows and
columns. No problem, I updated the code and it worked!

.. code-block:: python
    :linenos:

    def __repr__(self):
        if self.ndim == 1:
            return f"array({self._data}, dtype={str(self.dtype)})"
        elif self.ndim > 1:
            rows = ",\n       ".join(
                [f"[{', '.join(map(str, row))}]" for row in self._data]
            )
            return f"array([{rows}], dtype={str(self.dtype)})"

Then the 3D arrays... and it broke again.

That's when it hit me, this wasn't just about formatting strings. I needed a
proper solution that would work with any number of dimensions. A few days
later, I found myself deep into recursive logic and multi-dimensional
`indexing`_, all for what I believed was an "easy peasy" print function.

What started as a laid-back attempt to rework
:meth:`__repr__ <object.__repr__>`  turned out to be a masterclass in designing
for generality. This struggle taught me something profound, what seems super
simple on the surface often hides massive complexity underneath.

Printing a NumPy array from scratch was a rabbit hole!!!

.. seealso::

    Complete implementation of |xp.ndarray.repr|_ with helper functions.

.. _more-than-meets-the-eye:

-------------------------------------------------------------------------------
More than meets the eye
-------------------------------------------------------------------------------

After wrestling with the "simple" things, I naively believed the hardest part
was behind me. I was excited for the "fun" stuff, like element-wise arithmetic,
`broadcasting`_, and other random functions. However, I didn't realise my
journey was about to get even more challenging.

Implementing the |xp.ndarray|_ class felt like untangling a knot, while matrix
operations were like trying to weave my own thread from scratch. Basic
arithmetic operations like addition, subtraction, and scalar multiplication
seemed straightforward. I figured I could just iterate through my flattened
data and perform operations element-wise. And it worked... for the first few
test cases. But, as always, the system collapsed almost immediately for
higher-dimensional vectors.

.. code-block:: python
    :linenos:
    :emphasize-lines: 4,11

    def __add__(self, other):
        arr = ndarray(self.shape, self.dtype)
        if isinstance(other, (int, float)):
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

What if I added a scalar to a matrix, or a ``(3,)`` array to a ``(3, 3)``
matrix? Could I add a :py:class:`float` to an :py:class:`int`? Each new
"simple" operation posed a challenge in itself. I realised I wasn't just adding
or multiplying numbers, but learning and recreating NumPy's broadcasting rules.

Matrix multiplication was another beast entirely. I thought it would be just a
matter of looping through rows and columns, summing them element-wise, classic
high school mathematics, if you ask me. And it worked as well... until I tried
with higher-dimensional arrays. This is where I realised that matrix
multiplication isn't just about rows and columns, but about correctly handling
batch dimensions for higher-order tensors. I found myself diving into NumPy's
documentation, reading about the **Generalised Matrix Multiplication (GEMM)**
routines and how broadcasting affects the output shapes.

.. seealso::

    Complete implementation of `arithmetic operations
    <https://github.com/xames3/xsnumpy/blob/main/xsnumpy/_core.py>`_ on GitHub.

.. _small-victories-big-lessons:

-------------------------------------------------------------------------------
Small victories, big lessons
-------------------------------------------------------------------------------

By this time, I was in my winter break. I was fully committed to this project
because I didn't have to attend school. After days of debugging, I realised
that my vector operations weren't just about getting the "maths" right. They
were about thinking like NumPy:

- **Shape manipulation.** How do I infer the correct output shape?
- **Broadcasting.** How can I extend the smaller arrays to fit the larger ones?
- **Efficiency.** How can I minimise unnecessary data duplication?

At this stage, I wasn't just rebuilding a scrappy numerical computing
doppelganger. I was creating a flexible and extensible system that could handle
both intuitive and weird edge cases. With each iteration, every commit I made,
I explored even more ways to optimise it, reducing redundant calculations and
improving speed (not really).

Every bug, every unexpected result, and every small achievement taught me
something new about NumPy. I started speculating about the magic behind the
scenes. As time went by, xsNumPy became more than just a project and a scrappy
experiment. It became a mindset, a belief that the best way to learn is by
rolling up your sleeves, breaking it, and then putting it back together, piece
by piece.

.. _what-can-xsnumpy-do:

-------------------------------------------------------------------------------
What can xsNumPy do?
-------------------------------------------------------------------------------

xsNumPy started off as a learning exercise and has since grown into a small but
reliable companion. It was not about speed but about clarity. Here's a brief
tour, without the scaffolding, to show what it already does well.

.. tab-set::

    .. tab-item:: :octicon:`duplicate;1em;sd-text-success` Creations

        xsNumPy provides familiar ways to create arrays. These creation
        routines are consistent, predictable, and designed to slot neatly into
        later operations.

        - **array()**

          Like NumPy, the |xp.array|_ function is the bread and butter of
          xsNumPy as well. It's the most flexible way to create arrays from
          Python lists or tuples with sensible ``dtype`` inference and the
          option to set one explicitly.

          .. code-block:: python

              >>> import xsnumpy as xp
              >>> xp.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
              array([[[1, 2],
                      [3, 4]],

                     [[5, 6],
                      [7, 8]]])
              >>> xp.array([1, 0, 2], dtype=xp.bool)
              array([True, False, True])

        - **zeros()**, **ones()**, and **full()**

          xsNumPy support |xp.zeros|_, |xp.ones|_, and |xp.full|_ functions for
          repeatable initialisation of arrays filled with, zeros, ones, and any
          ``fill_value`` respectively.

          .. code-block:: python

              >>> xp.zeros(3)
              array([0. , 0. , 0. ])
              >>> xp.ones([3, 2], dtype=xp.int32)
              array([[1, 1],
                     [1, 1],
                     [1, 1]])
              >>> xp.full(2, 3, fill_value=3.14159)
              array([[3.14159, 3.14159, 3.14159],
                     [3.14159, 3.14159, 3.14159]])

        - **arange()**

          Inspired by Python's :py:class:`range`, |xp.arange|_ generates arrays
          with evenly spaced values.

          .. code-block:: python

              >>> xp.arange(0, 5, 0.5)
              array([0. , 0.5, 1. , 1.5, 2. , 2.5, 3. , 3.5, 4. , 4.5])

        .. seealso::

            Check out the complete list of array
            `creation <https://github.com/xames3/xsnumpy?
            tab=readme-ov-file#array-creation-routines>`_ methods supported by
            xsNumPy on GitHub.

    .. tab-item:: :octicon:`diff;1em;sd-text-warning` Operations

        xsNumPy provides a range of arithmetic operations, carefully adhering
        to NumPy's rules for broadcasting and type coercion. The emphasis is on
        correctness and clear behaviour across dimensions.

        - **Element-wise arithmetic**

          xsNumPy supports element-wise addition, subtraction, multiplication,
          and division along with other basic arithmetics.

          .. code-block:: python

              >>> a = xp.array([[1, 0], [0, 1]])
              >>> b = xp.array([[4, 1], [2, 2]])
              >>> a + b
              array([[5, 1],
                     [2, 3]])

        - **Broadcasting arithmetic**

          xsNumPy matches shapes, stretches smaller arrays, and makes sure the
          output shape followed NumPy's exact logic. Just like NumPy, these
          operations are broadcasted.

          .. code-block:: python

              >>> matrix = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> vector = xp.array([[1], [2], [3]])
              >>> matrix + vector
              array([[ 2,  4,  6],
                     [ 5,  7,  9],
                     [ 8, 10, 12]])

        - **Linear algebraic helper functions**

          To mirror NumPy's API, xsNumPy supports explicit arithmetic
          functions. These are useful when you want to be very clear about the
          operation being performed or when you need more control over the
          parameters.

          .. code-block:: python

              >>> a = xp.array([[1, 0], [0, 1]])
              >>> b = xp.array([[4, 1], [2, 2]])
              >>> xp.dot(a, b)
              array([[4, 1],
                     [2, 2]])

        - **Scalar operations**

          xsNumPy supports scalar operations as well so you're not just
          limited to array-to-array operations.

          .. code-block:: python

              >>> xp.array([3, 4]) + 10
              array([13, 14])

        .. seealso::

            Check out more examples of the arithmetic
            `operations <https://github.com/xames3/xsnumpy?
            tab=readme-ov-file#linear-algebra>`_ supported by xsNumPy on
            GitHub.

    .. tab-item:: :octicon:`pivot-column;1em;sd-text-primary` Transforms

        xsNumPy provides essential shape manipulation APIs that are predictable
        and memory-aware. The emphasis is on clarity of intent and avoiding
        unnecessary data duplication. Think of this as learning to fold and
        unfold the same fabric without tearing it.

        .. tip::

            Read more about `NumPy internals`_ here.

        - **reshape()**

          The |xp.ndarray.reshape|_ method changes the view of data when
          possible, preserving the total element count.

          .. code-block:: python

              >>> a = xp.array([1, 2, 3, 4, 5, 6])
              >>> a.reshape((2, 3))
              array([[1, 2, 3],
                     [4, 5, 6]])

        - **transpose()**

          Transposing is more than just flipping rows and columns; for
          higher-dimensional arrays, it's about permuting the axes. The
          |xp.ndarray.transpose|_ method does just that.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.transpose()
              array([[1, 4],
                     [2, 5],
                     [3, 6]])

        - **flatten()**

          The |xp.ndarray.flatten|_ method returns a tidy 1D copy.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.flatten()
              array([1, 2, 3, 4, 5, 6])

    .. tab-item:: :octicon:`multi-select;1em;sd-text-info` Indexing

        Indexing is expressive and disciplined in xsNumPy, just like NumPy. The
        goal is to provide intuitive access to elements and subarrays while
        maintaining clarity about the underlying data structure.

        - **Basic indexing**

          At its core, basic indexing in xsNumPy works similarly to NumPy,
          using zero-based indices to access elements. You can fetch single
          elements or entire subarrays. You can also use negative indices to
          count from the end of an array.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> a[1, 2]
              6
              >>> a[-1, -2]
              8

        - **Slicing**

          Slicing allows you to extract subarrays using a ``start:stop:step``
          format. Just like NumPy, xsNumPy supports all the classic slicing
          mechanics.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> a[::2]
              array([[1, 2, 3],
                     [7, 8, 9]])
              >>> a[:2, 1:]
              array([[2, 3],
                     [5, 6]])

        - **Boolean masking**

          Boolean masking lets you select elements based on a condition.

          .. code-block:: python

              >>> a[a % 2 == 0]
              array([1, 2, 3])

        .. seealso::

            Indexing and slicing were implemented by overridding the standard
            :meth:`__getitem__ <object.__getitem__>`  and
            :meth:`__setitem__ <object.__setitem__>`  protocols. Check out the
            complete implementation and other complementary methods
            `here <https://github.com/xames3/xsnumpy/blob/
            69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L368>`_
            on GitHub.

    .. tab-item:: :octicon:`sort-desc;1em;sd-text-danger` Reductions

        Reductions condense information carefully, preserving the essence of
        the data. xsNumPy provides a few key reduction operations that are
        predictable and consistent.

        - **sum()**

          The |xp.sum|_ method computed the sum of elements along a given
          axis.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.sum()
              21
              >>> a.sum(axis=0)
              array([5, 7, 9])

        - **prod()**

          The |xp.prod|_ (product) method computed the multiplication of
          elements along a given axis.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.prod()
              720
              >>> a.prod(axis=0)
              array([ 4, 10, 18])

        - **any()** and **all()**

          The |xp.all|_ method checks if all elements are :py:obj:`True`, while
          |xp.any|_ checks if at least one is.

          .. code-block:: python

              >>> b = xp.array([[True, False, True], [True, True, False]])
              >>> b.all()
              False
              >>> b.any(axis=1)
              array([True, True])

.. _from-notes-to-community:

-------------------------------------------------------------------------------
From notes to community
-------------------------------------------------------------------------------

This project was as much a conversation as it was code. I shared the story at
`ChiPy`_ in a talk titled **"xsNumPy: Curiosity to Code"**, walking through
the decisions, the missteps, and the insights that stayed with me.

The presentation covers the technical challenges, mathematical discoveries,
and most importantly, the mindset shift from viewing libraries as opaque
entities to understanding them as collections of elegant algorithms waiting to
be explored.

.. youtube:: https://www.youtube.com/watch?v=QIhyix3oEns

.. _looking-back-moving-forward:

-------------------------------------------------------------------------------
Looking back, moving forward
-------------------------------------------------------------------------------

xsNumPy didn't aim for speed, that wasn't the plan anyway. It aimed for
understanding. It taught me to replace awe with attention, trust libraries
while still learn and understand their concepts with care. Most importantly,
it reminded me that building is a generous teaching and learning experience.
When we step beyond the black box, the work slows down, and in the quiet,
ideas speak more clearly.

I will keep refining the library in small, respectful steps. However, the
larger work is already done. I re-learnt the essentials by making them, and
that learning will travel with me far beyond this code.

.. _matrices multiplied: https://www.mathsisfun.com/algebra/
    matrix-multiplying.html
.. _memory allocation: https://numpy.org/doc/stable/reference/
    c-api/data_memory.html
.. _shape: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    shape.html
.. _strides: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    strides.html
.. _broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
.. _indexing: https://numpy.org/doc/stable/user/basics.indexing.html
.. _NumPy internals: https://numpy.org/doc/stable/dev/internals.html
.. _ChiPy: https://chipy.org/

.. _xsnumpy/_core.py: https://github.com/xames3/xsnumpy/blob/main/xsnumpy/
    _core.py

.. |xp.ndarray| replace:: ``ndarray``
.. _xp.ndarray: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L183
.. |xp.ndarray.repr| replace:: ``ndarray.__repr__``
.. _xp.ndarray.repr: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L275C1-L327C27
.. |xp.array| replace:: ``array``
.. _xp.array: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L75
.. |xp.zeros| replace:: ``zeros``
.. _xp.zeros: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L171
.. |xp.ones| replace:: ``ones``
.. _xp.ones: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L229
.. |xp.full| replace:: ``full``
.. _xp.full: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L289
.. |xp.arange| replace:: ``arange``
.. _xp.arange: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L437
.. |xp.ndarray.reshape| replace:: ``ndarray.reshape``
.. _xp.ndarray.reshape: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L1571
.. |xp.ndarray.transpose| replace:: ``ndarray.transpose``
.. _xp.ndarray.transpose: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L1609
.. |xp.ndarray.flatten| replace:: ``ndarray.flatten``
.. _xp.ndarray.flatten: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L1386
.. |xp.sum| replace:: ``sum``
.. _xp.sum: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1518
.. |xp.prod| replace:: ``prod``
.. _xp.prod: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1536
.. |xp.all| replace:: ``all``
.. _xp.all: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1237
.. |xp.any| replace:: ``any``
.. _xp.any: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1254
