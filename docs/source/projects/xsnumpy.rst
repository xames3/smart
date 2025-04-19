.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, March 01 2025
.. Last updated on: Friday, April 18 2025

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
    :about: National Louis University
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

This realisation hit me so hard, I challenged myself, "Could I build a dinky
version of NumPy from scratch?" Again, not to replace it, that'd be barking
mad, but to learn from it. If I really want to ace at teaching these stuff to
my students, I had to go deeper.

.. image:: ../assets/need-to-go-deeper-meme.png
    :alt: We need to go deeper meme from Inception

There were a few other reasons for writing xsNumPy besides my lack of
understanding about the NumPy internals. I essentially wanted to break free
from the **"Oh, Neural Networks are like black box"** rubbish. When I'm
teaching Machine Learning and Neural Networks, I often compare these scientific
computing libraries to a car. You can go places, sure, but what happens when
something breaks? What do you do then? So to get around this situation, I
thought of actually learning it by building.

xsNumPy isn't just for me. It's for anyone and everyone who's ever stared at a
piece of Machine Learning code and asked, "How in God's name does this bloody
thing works?"

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
primary |xp.ndarray|_ data structure.

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
    check out the full |xp.ndarray|_ class on GitHub.

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
called |xp._convert_dtype|_. Its job? To fetch the size of the given data type
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
another |xp.ndarray|_. If it was, it nabbed the base buffer. The buffer was
assigned to ``self._base``, and the strides were either given directly or
calculated. Before moving on, the constructor did a bit of housekeeping:

- Offset (starting point in the memory) had to be non-negative
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

Phew 😮‍💨 |dash| that was a fair bit, wasn't it?

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

I remember talking to myself one morning, "let's start with something dead
easy, perhaps just display the array." That couldn't be hard, right? All I
need to do is print the content of my array in a readable format how NumPy
does. Little did I know I was shooting myself in the foot. At its core, a
:py:func:`repr` is just an object's internal data representation. I started
with something like this...

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

    See |xp.ndarray.repr|_ for complete implementation details.

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

Well, after wrestling with the **"simple"** things, I naively thought th
hardest and, in all honesty, the boring part of xsNumPy was behind me. I was
chuffed and more excited than ever before for the **"fun"** stuff |dash|
element-wise arithmetics, broadcasting, and other random functions. What I
didn't realise was that my journey was about to get even more mental. If
implementing the |xp.ndarray|_ class was untangling a knot, matrix operations
felt like trying to weave my own thread from scratch. Not sure if that makes
sense.

But the point was, it was hard!

If you've read it till this point, you might've noticed a trend in my thought
process. I assume things to be quite simple, which they bloody aren't, and I
start small. This was nothing different. I started simple, at least that's
what I thought. Basic arithmetic operations like addition, subtraction, and
scalar multiplication seemed relatively straight. I figured I could just
iterate through my flattened data and perform operations element-wise. And it
worked... for the first few test cases.

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
``(3, 3)`` matrix? Could I add floats to ints? I mean, this lot works in
normal maths, right? Each new **"simple"** operation posed a challenge in
itself. I realised I wasn't just adding or multiplying numbers but recreating
NumPy's `broadcasting`_ rules.

Trust me, lads, nothing compared to the chaos caused by the matrix
multiplication. Whilst coding the initial draft of the |xp.ndarray.matmul|_, I
remember discussing this with my mate, :ref:`Sameer <cast-sameer-mathad>`. I
thought it'd be just a matter of looping through rows and columns, summing
them element-wise. Classic high school maths, if you ask me. And it worked as
well... until I tried with higher-dimensional arrays. This is where I realised
that matrix multiplication isn't just about rows and columns but about
correctly handling **batch** dimensions for higher-order tensors. I found
myself diving into NumPy's documentation, reading about the **Generalised
Matrix Multiplication (GEMM)** routines and how broadcasting affects the
output shapes.

.. note::

    You can check out the complete implementation of arithmetic operations on
    GitHub.

    `Learn more
    <https://github.com/xames3/xsnumpy/blob/main/xsnumpy/_core.py>`_ |chvrn|

.. _more-than-just-code:

-------------------------------------------------------------------------------
More than just code
-------------------------------------------------------------------------------

This happened during the winter break. I didn't have to attend uni and was
working full-time on this project. After days of debugging, I realised that
all of my vector operations weren't about **"getting the math right"**, but
they were about thinking like NumPy:

- **Shape manipulation.** How do I infer the correct output shape?
- **Broadcasting.** How can I extend the smaller arrays to fit the larger ones?
- **Efficiency.** How can I minimise unnecessary data duplication?

At this stage, I wasn't just rebuilding some scrappy numerical computing
doppelgänger but rather a flexible and extensible system that could handle both
the intuitive use cases and the weird edge cases. As I started thinking more
along the lines of NumPy developers, I began coming up with broader and more
general solutions. I realised for knotty problems, xsNumPy was slow... perhaps
painfully slow. But it was mine. Unlike NumPy, which runs like `The Flash`_
which I can't bloody see or understand, I **understood** every line of code.
And with each iteration, every commit I made, I explored even more ways to
optimise it, reducing redundant calculations, improving "pseudo-cache"
locality.

Every bug, every unexpected result, and every small achievement taught me
something new about NumPy and how it might be doing its magic behind the
scenes. As time went by, xsNumPy became more than a project and a scrappy
experiment. It became a mindset. It taught me to stop treating libraries as
mysterious tools and start seeing them as collections of smartly packed
algorithms and data structures waiting to be explored. Now, after countless
late nights and endless debugging sessions, I finally reached a point where
xsNumPy wasn't just a dinky implementation but it had proper shape, form, and
most importantly, it worked! What kicked off as a way to demystify NumPy had
grown into something far bigger. A project that taught me more than I could've
ever imagined about numerical computing.

So, what can xsNumPy actually do?

.. tab-set::

    .. tab-item:: Creations

        When I first started adding array creation methods to xsNumPy, I
        thought, how hard could it be? Just slap together a few initialisers,
        right? But, as always, reality gave me a proper wake-up call. It
        wasn't just about making arrays appear; it was about ensuring they
        worked seamlessly with the whole system |dash| shapes, data types, and
        all.

        - **array()**

          The |xp.array|_ function is the bread and butter of xsNumPy, the most
          flexible way to create arrays from Python lists or tuples.

          .. code-block:: python

              >>> import xsnumpy as xp
              >>>
              >>> xp.array([1, 2, 3])
              array([1, 2, 3])
              >>> xp.array([[1, 2, 3], [4, 5, 6]])
              array([[1, 2, 3],
                     [4, 5, 6]])
              >>> xp.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
              array([[[1, 2],
                      [3, 4]],

                     [[5, 6],
                      [7, 8]]])
              >>> xp.array([1, 2, 3.0])
              array([1. , 2. , 3. ])
              >>> xp.array([1, 0, 2], dtype=xp.bool)
              array([True, False, True])

        - **zeros()** and **ones()**

          I added |xp.zeros|_ and |xp.ones|_ as the go-to methods for
          initialising arrays filled with, well, zeros and ones. Simple, yet
          essential.

          .. code-block:: python

              >>> xp.zeros(3)
              array([0. , 0. , 0. ])
              >>> xp.zeros([2, 2])
              array([[0. , 0. ],
                     [0. , 0. ]])
              >>> xp.ones([3, 2], dtype=xp.int32)
              array([[1, 1],
                     [1, 1],
                     [1, 1]])

        - **full()**

          For custom initialisation, |xp.full|_ lets you fill an array with any
          value you want.

          .. code-block:: python

              >>> xp.full(2, 3, fill_value=3.14)
              array([[3.14, 3.14, 3.14],
                     [3.14, 3.14, 3.14]])

          Here, I had to be mindful about handling scalars vs arrays, ensuring
          the ``fill_value`` was broadcastable when needed.

        - **arange()**

          Inspired by Python's :py:class:`range`, |xp.arange|_ generates arrays
          with evenly spaced values.

          .. code-block:: python

              >>> xp.arange(3)
              array([0, 1, 2])
              >>> xp.arange(3.0)
              array([0. , 1. , 2. ])
              >>> xp.arange(3, 7)
              array([3, 4, 5, 6])
              >>> xp.arange(3, 7, 2)
              array([3, 5])
              >>> xp.arange(0, 5, 0.5)
              array([0. , 0.5, 1. , 1.5, 2. , 2.5, 3. , 3.5, 4. , 4.5])

          The tricky part here? Making sure it worked with both integers and
          floats without rounding errors creeping in.

        .. seealso::

            Check out the complete list of
            `array creation <https://github.com/xames3/xsnumpy?
            tab=readme-ov-file#array-creation-routines>`_ methods which are
            supported by xsNumPy on GitHub.

    .. tab-item:: Operations

        Once I had array creation sorted, I quickly realised that the real
        meat of xsNumPy lay in the operations, the arithmetic, element-wise
        manipulations, and the fundamental maths that give NumPy its power. It
        wasn't just about adding two numbers or multiplying matrices; it was
        about making these operations flexible, intuitive, and most of all,
        consistent with how NumPy does it.

        In xsNumPy, I implemented a range of arithmetic operations, carefully
        adhering to NumPy's rules for broadcasting and type coercion.

        - **Basic arithmetic**

          You can perform element-wise addition, subtraction, multiplication,
          and division directly using xsNumPy arrays. Just like NumPy, these
          operations are broadcasted, so you can mix scalars, vectors, and
          matrices freely.

          .. code-block:: python

              >>> import xsnumpy as xp
              >>>
              >>> a = xp.array([[1, 0], [0, 1]])
              >>> b = xp.array([[4, 1], [2, 2]])
              >>>
              >>> a + b
              array([[5, 1],
                     [2, 3]])
              >>> a - b
              array([[-3, -1],
                     [-2, -1]])
              >>> a * b
              array([[4, 0],
                     [0, 2]])
              >>> a / b
              array([[0.25, 0.  ],
                     [0.  ,  0.5]])
              >>> a // b
              array([[0, 0],
                     [0, 0]])
              >>> a ** b
              array([[1, 0],
                     [0, 1]])
              >>> a % b
              array([[1, 0],
                     [0, 1]])
              >>> a @ b
              array([[4, 1],
                     [2, 2]])
              >>> a < b
              array([[True, True],
                     [True, True]])
              >>> a >= b
              array([[False, False],
                     [False, False]])

          The challenge here wasn't the simple cases, it was ensuring that
          these operations worked for higher-dimensional arrays, and correctly
          handled broadcasting.

        - **Broadcasting and arithmetic**

          I had to dive deep into the logic of broadcasting. If you've ever
          wondered why adding a ``(3, 1)`` array to a ``(3, 3)`` matrix just
          works in NumPy, it's all thanks to broadcasting rules. Implementing
          those rules was tricky, matching shapes, stretching smaller arrays,
          and making sure the output shape followed NumPy's exact logic.

          .. code-block:: python

              >>> matrix = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> column_vector = xp.array([[1], [2], [3]])
              >>> matrix + column_vector
              array([[ 2,  4,  6],
                     [ 5,  7,  9],
                     [ 8, 10, 12]])

        - **Linear algebraic helper functions**

          To mirror NumPy's API, I also implemented explicit arithmetic
          functions. These are useful when you want to be very clear about the
          operation being performed or when you need more control over the
          parameters.

          .. code-block:: python

              >>> xp.dot(3, 4)
              12
              >>> a = xp.array([[1, 0], [0, 1]])
              >>> b = xp.array([[4, 1], [2, 2]])
              >>> xp.dot(a, b)
              array([[4, 1],
                     [2, 2]])
              >>> xp.add(a, b)
              array([[5. , 1. ],
                     [2. , 3. ]])
              >>> xp.divide(a, b)
              array([[0.25, 0.  ],
                     [0.  ,  0.5]])
              >>> xp.power(3, 4)
              81

        - **Scalar operations**

          You're not just limited to array-to-array operations, scalars work
          too, just as you'd expect.

          .. code-block:: python

              >>> xp.array([3, 4]) + 10
              array([13, 14])

        .. seealso::

            Check out more examples of the
            `arithmetic operations <https://github.com/xames3/xsnumpy?
            tab=readme-ov-file#linear-algebra>`_ supported by xsNumPy on
            GitHub.

    .. tab-item:: Shape manipulations

        Once I had nailed down array creation and operations, the next beast
        to tackle was shape manipulation. If there's one thing I learned
        quickly, it's that reshaping arrays isn't just a matter of rearranging
        elements, it's about understanding how data is stored and accessed
        under the hood.

        In xsNumPy, I wanted to mirror NumPy's intuitive and flexible shape
        manipulation methods, while also reinforcing my grasp of concepts like
        `views`_, `strides`_, and contiguous arrays.

        .. tip::

            Read more about `NumPy internals`_ here.

        - **reshape()**

          The |xp.ndarray.reshape|_ method allows you to change an array's
          shape without altering its data. The key was ensuring the total
          number of elements remained consistent, a simple yet crucial check.

          .. code-block:: python

              >>> import xsnumpy as xp
              >>>
              >>> a = xp.array([1, 2, 3, 4, 5, 6])
              >>> a.reshape((2, 3))
              array([[1, 2, 3],
                     [4, 5, 6]])
              >>> a.reshape((2, 4))
              Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
              ...
              ValueError: New shape is incompatible with the current size

          The tricky bit was handling corner cases, reshaping empty arrays,
          adding singleton dimensions, and ensuring reshaped arrays remain
          views (not copies) where possible.

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

          The |xp.ndarray.flatten|_ method returns a copy. Implementing this
          pushed me to understand `memory alignment`_ and stride tricks.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.flatten()
              array([1, 2, 3, 4, 5, 6])

        These methods taught me the importance of shape manipulation, it's not
        just about rearranging numbers but respecting how arrays interact with
        memory and computation. Each feature made me peel back yet another
        layer of NumPy's magic, reinforcing my understanding while building
        xsNumPy piece by piece.

    .. tab-item:: Indexing

        Indexing and slicing were, without a doubt, one of the most
        head-scratching features to implement in xsNumPy. What seemed like a
        simple task of grabbing an element or a subset of an array turned into
        a proper rabbit hole of possibilities, single-element access, slice
        objects, fancy indexing, boolean masks, the lot.

        - **Basic indexing**

          At its core, basic indexing in xsNumPy works similarly to NumPy,
          using zero-based indices to access elements. You can fetch single
          elements or entire subarrays.

          .. code-block:: python

              >>> import xsnumpy as xp
              >>>
              >>> a = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> a[0, 1]
              2
              >>> a[1, 2]
              6

          You can also use negative indices to count from the end of an array.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> a[-1, -2]
              8

        - **Slicing**

          Slicing allows you to extract subarrays using a ``start:stop:step``
          format. Just like NumPy, xsNumPy supports all the classic slicing
          mechanics.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
              >>> a[1:2]
              array([[4, 5, 6]])
              >>> a[:2]
              array([[1, 2, 3],
                     [4, 5, 6]])
              >>> a[::2]
              array([[1, 2, 3],
                     [7, 8, 9]])
              >>> a[:2, 1:]
              array([[2, 3],
                     [5, 6]])
              >>> a[::2, ::2]
              array([[1, 3],
                     [7, 9]])

        - **Boolean masking**

          This was a added surprise. I honestly, didn't engineer this one but
          since, xsNumPy now functions more generally, it allows features like
          Boolean masking. Boolean masking lets you select elements based on a
          condition.

          .. code-block:: python

              >>> a[a % 2 == 0]
              array([1, 2, 3])

        Implementing indexing and slicing wasn't just about grabbing elements,
        it was about ensuring the shapes stayed correct, broadcasting rules
        were respected, and that corner cases (like empty slices or
        out-of-bounds indices) didn't cause the whole system to collapse. It
        took a lot of late nights and a fair bit of trial and error to make
        sure xsNumPy worked as closely as possible to NumPy.

        .. seealso::

            Indexing and slicing were implemented by overridding the standard
            ``__getitem__`` and ``__setitem__`` protocols. To see the complete
            implementation and other complementary methods, visit
            `here <https://github.com/xames3/xsnumpy/blob/
            69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L368>`_.

    .. tab-item:: Reductions

        After wrangling with array creation, operations, shape manipulation,
        and indexing, I found myself standing at the gates of reductions, those
        neat little methods that take an array and distil it down to a single
        value or a smaller array. Sounds straightforward, right? Well, not
        quite.

        Reductions in xsNumPy were a real eye-opener. They forced me to think
        deeply about axes, and handling empty arrays, all while ensuring my
        logic matched the intuitive elegance of NumPy.

        - **sum()**

          The |xp.sum|_ method computed the sum of elements along a given
          axis. The tricky part? Handling multi-dimensional arrays.

          .. code-block:: python

              >>> import xsnumpy as xp
              >>>
              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.sum()
              21
              >>> a.sum(axis=0)
              array([5, 7, 9])

        - **min()** and **max()**

          Finding minimum and maximum values sounds simple, but reducing along
          the axes with proper shape handling kept me busy for a while.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.min()
              1
              >>> a.max(axis=1)
              array([3, 6])

        - **mean()**

          Calculating the mean was more than just summing and dividing, I
          needed to ensure type consistency and careful shape adjustments.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.mean()
              3.5
              >>> a.mean(axis=1)
              array([2. , 5. ])

        - **prod()**

          The |xp.prod|_ (product) method computed the multiplication of
          elements along a given axis. Multiplying elements together was the
          final boss of reductions. As simple as it may sound, I had to think
          through the overflow errors and correct data types.

          .. code-block:: python

              >>> a = xp.array([[1, 2, 3], [4, 5, 6]])
              >>> a.prod()
              720
              >>> a.prod(axis=0)
              array([ 4, 10, 18])

        - **any()** and **all()**

          Logical reductions were their own beast. The |xp.all|_ method checks
          if all elements are ``True``, while |xp.any|_ checks if at least one
          is.

          .. code-block:: python

              >>> b = xp.array([[True, False, True], [True, True, False]])
              >>> b.all()
              False
              >>> b.any(axis=1)
              array([True, True])

        Building reductions in xsNumPy pushed me to think harder about how
        arrays collapse along dimensions and how NumPy seamlessly handles type
        promotion and shape consistency. It's not just about computing a value,
        it's about ensuring the result fits neatly into the broader array
        ecosystem.

        With reductions wrapped up, xsNumPy finally started to feel like a
        **real** numerical computing library. Every sum, min, and mean wasn't
        just a calculation, it was a carefully crafted operation built on a
        solid foundation.

.. _concluding-xsnumpy:

-------------------------------------------------------------------------------
Concluding xsNumPy
-------------------------------------------------------------------------------

Now, I won't pull the wool over your eyes, xsNumPy isn't a blazing-fast,
industrial-strength library, nor was it ever meant to be. But every line of
code carries the weight of a battle fought, a bug squashed, a concept
unravelled, a little victory earned. It's a project born out of pure curiosity
and a stubborn desire to lift the bonnet on a tool I use daily. More than just
its features, xsNumPy reflects a mindset, the belief that the best way to
learn is by rolling up your sleeves, building something from scratch, breaking
it, then putting it back together, piece by piece.

.. image:: ../assets/victory-shall-be-mine-meme.gif
    :alt: Victory shall be mine meme from Family Guy

This experience taught me to stop seeing libraries as mystical black boxes and
start recognising them for what they are. And for me, that's the real win of
demystifying complex libraries one line at a time!

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
.. _The Flash: https://www.dc.com/characters/the-flash
.. _views: https://numpy.org/doc/stable/user/basics.copies.html
.. _NumPy internals: https://numpy.org/doc/stable/dev/internals.html
.. _memory alignment: https://numpy.org/doc/stable/dev/alignment.html

.. |xp.ndarray| replace:: ``xsnumpy.ndarray``
.. _xp.ndarray: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L183
.. |xp._convert_dtype| replace:: ``_convert_dtype``
.. _xp._convert_dtype: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L150
.. |xp.ndarray.repr| replace:: ``__repr__``
.. _xp.ndarray.repr: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L275C1-L327C27
.. |xp.ndarray.matmul| replace:: ``__matmul__``
.. _xp.ndarray.matmul: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L831
.. |xp.array| replace:: ``xsnumpy.array()``
.. _xp.array: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L75
.. |xp.zeros| replace:: ``xsnumpy.zeros()``
.. _xp.zeros: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L171
.. |xp.ones| replace:: ``xsnumpy.ones()``
.. _xp.ones: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L229
.. |xp.full| replace:: ``xsnumpy.full()``
.. _xp.full: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L289
.. |xp.arange| replace:: ``xsnumpy.arange()``
.. _xp.arange: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L437
.. |xp.ndarray.reshape| replace:: ``xsnumpy.ndarray.reshape()``
.. _xp.ndarray.reshape: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L1571
.. |xp.ndarray.transpose| replace:: ``xsnumpy.ndarray.transpose()``
.. _xp.ndarray.transpose: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L1609
.. |xp.ndarray.flatten| replace:: ``xsnumpy.ndarray.flatten()``
.. _xp.ndarray.flatten: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L1386
.. |xp.sum| replace:: ``xsnumpy.sum()``
.. _xp.sum: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1518
.. |xp.prod| replace:: ``xsnumpy.prod()``
.. _xp.prod: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1536
.. |xp.all| replace:: ``xsnumpy.all()``
.. _xp.all: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1237
.. |xp.any| replace:: ``xsnumpy.any()``
.. _xp.any: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_numeric.py#L1254
