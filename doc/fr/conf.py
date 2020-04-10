# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
#
# This file is part of SALOME ADAO module
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import sys, os, sphinx
import sphinx_rtd_theme

try:
    sys.path.append(os.path.abspath("../../bin"))
    import module_version
    print("Import du module_version de bin...")
except:
    pass
try:
    sys.path.append(os.path.abspath("../../adao/adao/daCore"))
    import version as module_version
    print("Import du module_version de daCore...")
except:
    pass

# -- Project information -----------------------------------------------------

project   = u'%s'%module_version.name
author    = u'Jean-Philippe ARGAUD'
copyright = u'2008-%s, EDF R&D, %s'%(module_version.year,author)
version   = '%s'%module_version.version
release   = '%s'%module_version.version
doctitle  = u"Documentation %s"%module_version.name
docfull   = u"Assimilation de Données et Aide à l'Optimisation"

# -- General configuration ---------------------------------------------------

from distutils.version import LooseVersion #, StrictVersion
if LooseVersion(sphinx.__version__) < LooseVersion("1.4.0"):
    extensions = [
        'sphinx.ext.pngmath',
        'sphinx_rtd_theme',
    ]
else:
    extensions = [
        'sphinx.ext.imgmath',
        'sphinx_rtd_theme',
        ]
#
source_suffix    = '.rst'
source_encoding  = 'utf-8'
master_doc       = 'index'
language         = 'fr'
exclude_patterns = ['snippets', 'scripts', 'resources', '_build', 'Thumbs.db', '.DS_Store', 'Grenier']
pygments_style   = None
templates_path   = ['_templates']
exclude_trees    = ['snippets',]

# -- Options for HTML output -------------------------------------------------

html_theme       = "sphinx_rtd_theme"
# html_theme     = 'default'
# html_theme     = 'alabaster'
html_title       = doctitle
html_static_path = ['_static']
html_show_sourcelink = False

# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'ADAOdoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'figure_align': 'htbp',
}
latex_documents = [
  ('index', 'ADAO.tex', doctitle,
   author, 'manual'),
]

# -- Options for manual page output ------------------------------------------

man_pages = [
    (master_doc, 'adao', doctitle,
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'ADAO', doctitle,
     author, 'ADAO', docfull,
     'Miscellaneous'),
]
# -- Options for Epub output -------------------------------------------------

epub_title         = doctitle
epub_author        = author
epub_publisher     = author
epub_copyright     = copyright
epub_exclude_files = ['search.html']

# -- Options for PDF output --------------------------------------------------

pdf_documents = [
    ('contents', u'ADAO', u'ADAO', author, dict(pdf_compressed = True)),
]
pdf_stylesheets = ['sphinx','kerning','a4']
pdf_compressed = True
pdf_inline_footnotes = True

# -- Extension configuration -------------------------------------------------
