.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, March 01 2025
.. Last updated on: Saturday, March 01 2025

:og:title: Building xsNumpy
:og:description: Building a lightweight, pure-python implementation of NumPy's
    core features
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

Now that I was motivated to learn the nitty-gritty implementation details of
NumPy, I was ready to build my own version of it.

.. _NumPy: https://numpy.org/
.. _xsNumPy: https://github.com/xames3/xsnumpy
