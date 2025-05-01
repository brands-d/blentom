# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

print(sys.path)
project = "blentom"
copyright = "2024, Dominik Brandstetter"
author = "Dominik Brandstetter"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

autodoc_mock_imports = [
    "numpy",
    "bpy",
    "bmesh",
    "ase",
    "skimage",
    "math",
    "mathutils",
    "bpy_extras",
    "console_python",
]
autodoc_typehints = "none"
autodoc_member_order = "groupwise"

html_sidebars = {
    "**": [
        "globaltoc.html",
        "relations.html",  # Show previous and next files
        "sourcelink.html",  # Show a link to the source on GitHub/GitLab/etc.
        "searchbox.html",  # Show a search box
    ]
}
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
