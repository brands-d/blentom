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

.. [1] Organic molecule database from Prof. Peter Puschnig from the University of Graz
.. [2] File format from `RIIGID <https://github.com/siegfriedkaidisch/RIIGID>`_

Installation
------------

Please note that the installation of Blentom will install dependencies directly with Blender's bundled Python interpreter and modify the system path.

#. **Download the Addon**: Download the ``blentom.zip`` file from the `GitHub Page <https://github.com/brands-d/blentom/>`_.
#. **Allow internet access**: Blentom depends on external dependencies that will automatically install if not installed already. Make sure to allow internet access ("Preferences -> System -> Network -> Allow Online Access") or install them ourself manually. Internet access can be turned off after successfull installation.
#. **Install in Blender**: Open Blender and navigate to ``Edit > Preferences > Add-ons > Install...``, then select the ``blentom.zip`` file [1,2].
#. **Enable the Addon**: Search for 'Blentom' in the Add-ons tab and enable it if not already automatically enabled [3].
#. **Restart Blender**: If there is an error when enabling, restart Blender and try to enable it again.

.. [1] On Windows Blender sometimes has to be executed in administrator mode.
.. [2] Tested on Blender 4.4.1, 4.1 and 3.6.0 on Windows, Linux and MacOS.
.. [3] The activation takes some time the first time because external dependencies are installed. Please be patient until Blender gets responsive again and you see blentom in the addon list. 

Usage
-----

Import
~~~~~~

"File -> Import" 

Script
~~~~~~
**Navigate to the Scripting page inside Blender. There you find a console or you can load .py scripts or create new ones.**

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
