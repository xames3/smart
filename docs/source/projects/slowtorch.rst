.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Friday, April 18 2025
.. Last updated on: Saturday, April 19 2025

:og:title: Slow Burning Torch
:og:description: PyTorch taught me how to build while SlowTorch taught me how
    it's built.
:og:type: article

.. _project-slow-burning-torch:

===============================================================================
Slow Burning Torch
===============================================================================

.. author::
    :name: Akshay Mestry
    :email: xa@mes3.dev
    :about: National Louis University
    :avatar: https://avatars.githubusercontent.com/u/90549089?v=4
    :github: https://github.com/xames3
    :linkedin: https://linkedin.com/in/xames3
    :timestamp: Apr 18, 2025

.. rst-class:: lead

    Speed is for production, serving machines while slowness is for humans,
    for understanding

So, it all started on a quiet afternoon in early January of 2025, just after I
wrapped up :doc:`xsNumPy <./xsnumpy>`. I was still basking in the glow of
having finally built `NumPy`_ (at least a fraction of it) from scratch to
demystify how array operations worked. It was a project born out of curiosity.
I didn't want performance, nor did I care. I just wanted to understand. And as
I was pushing the final commit to the repository, I felt two things very
clearly:

- Relief, because rewriting |xp.ndarray|_ and debugging the broadcasting logic
  from first principles is as mentally taxing as it is rewarding
- Restlessness, because once you've peeled back the curtain on one big library,
  you start seeing others in a whole new light

Rewriting NumPy had shown me the power of writing slow code to understand fast
abstractions. Now, I wanted to take that same approach to something I'd been
using for over half a decade, `PyTorch`_.

.. _rewriting-pytorch-badly-on-purpose:

-------------------------------------------------------------------------------
Rewriting PyTorch Badly, On Purpose
-------------------------------------------------------------------------------

Now, I've been working with PyTorch since 2018, back when
:py:class:`torch.nn.Sequential` felt like magic and
:py:meth:`torch.Tensor.backward` method seemed to compute gradients by
sorcery.

.. _NumPy: https://numpy.org/
.. |xp.ndarray| replace:: ``xsnumpy.ndarray``
.. _xp.ndarray: https://github.com/xames3/xsnumpy/blob/
    69c302ccdd594f1d8f0c51dbe16346232c39047f/xsnumpy/_core.py#L183
.. _PyTorch: https://pytorch.org/
