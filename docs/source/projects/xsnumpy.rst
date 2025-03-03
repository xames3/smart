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
pretty obvious that there were some significant flaws in my logic.

.. image:: ../assets/sigh-meme.jpg
    :alt: Deep sigh meme

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
