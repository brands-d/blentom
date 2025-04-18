Blentom
=======

Blentom is a Blender addon to allow for simple import, scene setup, and rendering of files common in the electronic structure simulation community. Currently, it supports molecule-like atomic structures in all ASE supported files (e.g., ``.cube``, ``POSCAR``, ``.xyz``, ``.pdb``, etc.). Furthermore, wavefunction densities can additionally be loaded from ``.cube`` files and charge densities from ``CHGCAR`` files.

.. image:: https://github.com/brands-d/blentom/blob/main/demo/output/Ag-NiTCNB2.png?raw=true
   :alt: Ag-NiTCNB2

Installation
------------

1. **Download the Addon**: Download the ``blentom.zip`` file from the `GitHub Page <https://github.com/brands-d/blentom/>`_.
2. **Install in Blender**: Open Blender and navigate to ``Edit > Preferences > Add-ons > Install...``, then select the ``blentom.zip`` file [1]_.
3. **Enable the Addon**: Search for 'Blentom' in the Add-ons tab and enable it if not already automatically enabled [2]_.

.. [1] On Windows Blender sometimes has to be executed in administrator mode.
.. [2] The activation takes some time the first time because external dependencies are installed.

Usage
-----

**Navigate to the Scripting page inside Blender. There you find a console or you can load .py scripts or create new ones.**

Quickstart
~~~~~~~~~~

If you just want to import common files use the appropriate entry under ``File > Import``.

.. code-block:: python

   from blentom import Atoms, Camera

   Atoms.read("path/to/input")
   camera = Camera()
   camera.render("path/to/output.png")

Demo Files
~~~~~~~~~~

Inside the ``blentom/demo/scripts`` you can find a couple of demo scripts that highlight certain features.

Documentation
~~~~~~~~~~~~~
https://blentom.readthedocs.io/latest/index.html
