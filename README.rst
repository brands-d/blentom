Blentom
=======

Blentom is a Blender addon built on top of ASE designed to ease the production of high quality render of molecules, periodic interfaces, wavefunctions and more. It features both quick and easy import of numerous file formats common in the surface science community as well as a interface between ASE and Blender to allow for a potential automatic scripting approach to import, scene setup and even render process. 

.. image:: https://github.com/brands-d/blentom/blob/main/demo/output/Ag-NiTCNB2.png?raw=true
   :alt: Ag-NiTCNB2

Features
--------

* Import: Many ASE supported file formats for atomic structure and 3D scalar fields like wavefunctions and charge densities (e.g. ``.cube``, ``POSCAR``, ``.xyz``, ``.pdb``, ...) can be imported in a render ready state. For import a GUI interface well integrated with Blender's UI is available that makes this process simple and requires no coding. Additionally, frontier orbitals and molecular structures for hundreds of common organic molecules can be imported directly from an (`online database <physikmdb.uni-graz.at:5001>`_) [1].
* Comprehensive coding interface between ASE, Blender and Python allows for everything from import, modification, materials selection, camera/lighting setup up to rendering to be done in a script, potentially automated even from the command line.
* Available material and render presets for all elements in various different designs. Possibility to integrate a custom material or asset library.
* Periodic structure are possible with seamless transition between unit cell boundaries.
* Animation of atomic structures and import of geometry optimization files (VASP: ``XDATCAR``, ``.traj`` [2]).
* Dynamic bonding including double and triple bonds.

.. [1] Organic molecule database from Prof. Peter Puschnig from the University of Graz
.. [2] File format from `RIIGID <https://github.com/siegfriedkaidisch/RIIGID>`_

Installation
------------

Clone the lastest version of this repository and run the build.py script to create a zip file that can be installed in Blender. If the Blender version or the Python version inside Blenders differs update the blentom/blender_manifest.toml file accordingly.

Usage
-----

Import
~~~~~~

"File -> Import" 

Script
~~~~~~
**Navigate to the Scripting page inside Blender. There you find a console or you can load .py scripts or create new ones.**

.. code-block:: python

   from bl_ext.user_default.blentom import Atoms, Camera

   Atoms.read("path/to/input")
   camera = Camera()
   camera.render("path/to/output.png")


Demo Files
~~~~~~~~~~

Inside the ``blentom/demo/scripts`` you can find a couple of demo scripts that highlight certain features.

Documentation
~~~~~~~~~~~~~
https://blentom.readthedocs.io/latest/index.html
