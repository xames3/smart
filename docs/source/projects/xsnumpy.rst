.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, March 01 2025
.. Last updated on: Sunday, March 02 2025

:og:title: Building xsNumpy
:og:description: A lightweight, pure-python implementation of NumPy's core
    features
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
was slicing and dicing arrays, multiplying matrices, and running complex
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
powerhouse, built over and backed by decades of work by incredible minds in
math and science, plus tons of optimizations in place. I possibly can't
compete with that!

But still... I realized something quite important. Just because its dense and
complicated, it doesn't mean I can't try to understand it. I was literally
relying on it like a black box. I was using its functions and underlying APIs
without truly understanding how they worked!

So, I challenged myself, *Could I build a dinky version of NumPy from
scratch?* Again, not to replace it but to learn from it.

.. _building-process:

-------------------------------------------------------------------------------
Building Process
-------------------------------------------------------------------------------

I was ready to build my small version of NumPy, but I didn't know where to
start. I began scrutinizing and poking at various NumPy functions and methods.
Soon I realized that most of NumPy APIs rely on one core construct, the
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

.. dropdown:: Code explanation
    :animate: fade-in

    Alright, let me break this down in a way that makes sense. First, I start
    with checking if the shape is an :py:class:`collections.abc.Iterable`
    (a sequence like a :py:class:`tuple` or :py:class:`list`). If it's not,
    I'm wrapping it into a tuple to ensure that the shape is always
    represented as a tuple. The shape is then converted into a tuple of
    integers, ensuring the dimensions are valid.

    .. code-block:: python
        :linenos:

            if not isinstance(shape, Iterable):
                shape = (shape,)
            self._shape = tuple(int(dim) for dim in shape)

    Next up, the ``dtype`` (data type). If ``dtype`` is not provided, the
    constructor sets the default data type to ``None``. If a :py:class:`type`
    (such as :py:class:`int`, :py:class:`float`, etc.) is provided, it
    dynamically retrieves the appropriate data type from the global namespace
    using :func:`globals`. This allows flexibility in handling various types.
    Finally, the resolved data type is assigned to ``self._dtype``.

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

    The size of each element in the array is calculated based on the provided
    data type. I wrote a handy function, ``_convert_dtype`` to fetch the
    appropriate size of the data type (in a ``short`` format), and the last
    value is used to determine the item size.

    This is super important for calculating memory layout and strides!

    .. code-block:: python
        :linenos:

            self._itemsize = int(_convert_dtype(dtype, "short")[-1])

    Now, if ``buffer`` is ``None``, the array is initialized without an
    external memory buffer. In this case:

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

    If a ``buffer`` is provided, the constructor handles it by checking if
    it's another ``ndarray``. If the ``ndarray`` has a base buffer, it uses
    that. The buffer is assigned to ``self._base``, and strides are either
    provided or calculated.

    The constructor validates the offset (it must be non-negative) and the
    strides (it must be a tuple of integers matching the shape's dimensions).

    .. code-block:: python
        :linenos:

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

    Finally, the constructor calculates the total buffer size based on the
    strides, shape, and item size. The ``Buffer`` is a type derived from the
    data type (dtype) and its size. Depending on whether the buffer is provided
    or not, it initializes ``self._data`` using different methods:

    - If no buffer is provided, a new buffer is created
    - If the buffer is a :py:class:`ctypes.Array`, the address of the buffer
      is used to initialize the data. Basically, we use its address like a map
    - If it's any other type of buffer, the buffer is used directly

    Phew, that was a lot, but now you can see how it's all orchestrated!

.. _NumPy: https://numpy.org/
.. _xsNumPy: https://github.com/xames3/xsnumpy
.. _memory allocation and management: https://numpy.org/doc/stable/reference/
    c-api/data_memory.html
.. _shape: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    shape.html
.. _strides: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.
    strides.html
