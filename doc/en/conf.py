# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2022 EDF R&D
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

import sys, os, time, sphinx, logging
# logging.getLogger().setLevel(logging.DEBUG)

# -- Module version information --------------------------------------------------

try:
    sys.path.append(os.path.abspath("../../bin"))
    import module_version
    logging.debug('Using "module_version" that was found from "bin"...')
except:
    pass
try:
    sys.path.append(os.path.abspath("../../adao/adao/daCore"))
    import version as module_version
    logging.debug('Using "module_version" that was found from "daCore"...')
except:
    pass
if "module_version" not in locals():
    module_version = lambda : None
    module_version.name    = "ADAO"
    module_version.year    = "%s"%(time.localtime()[0],)
    module_version.version = ""
    logging.warning('Using fallback "module_version" because none was found')

# -- Project information -------------------------------------------------------

project   = u'%s'%module_version.name
author    = u'Jean-Philippe ARGAUD'
copyright = u'2008-%s, EDF R&D, %s'%(module_version.year,author)
version   = '%s'%module_version.version
release   = '%s'%module_version.version
doctitle  = u"%s documentation"%module_version.name
docfull   = u"Aiding for Data Assimilation and Optimization"

# -- General configuration -----------------------------------------------------

from distutils.version import LooseVersion #, StrictVersion
__lv = LooseVersion(sphinx.__version__)
if __lv < LooseVersion("1.4.0"):
    extensions = ['sphinx.ext.pngmath']
    logging.debug('Using "%s" extensions'%(extensions,))
else:
    extensions = ['sphinx.ext.imgmath']
    logging.debug('Using "%s" extensions'%(extensions,))
try:
    import sphinx_rtd_theme
    extensions += ['sphinx_rtd_theme']
    use_rtd_theme = True
    logging.debug('Using "sphinx_rtd_theme" that was found')
except:
    use_rtd_theme = False
    logging.debug('Not using "sphinx_rtd_theme" because none was found')
#
source_suffix    = '.rst'
source_encoding  = 'utf-8'
master_doc       = 'index'
language         = 'en'
exclude_patterns = [
    'snippets',
    'scripts',
    'resources',
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'Grenier',
    ]
pygments_style   = None
templates_path   = ['_templates']
exclude_trees    = ['snippets',]
numfig           = True

# -- Options for HTML output ---------------------------------------------------

if use_rtd_theme:
    html_theme       = "sphinx_rtd_theme"
else:
    html_theme       = 'default' if __lv < LooseVersion("1.3.0") else 'classic'
#
html_title           = doctitle
html_static_path     = ['_static']
html_show_sourcelink = False
html_search_language = language
html_favicon         = 'resources/ADAO_favicon.ico'

# -- Options for HTMLHelp output -----------------------------------------------

htmlhelp_basename    = module_version.name+'doc'

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'figure_align': 'htbp',
}
latex_documents = [
  ('index', '%s.tex'%module_version.name, doctitle,
   author, 'manual'),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    (master_doc, '%s'%module_version.name, doctitle,
     [author], 1)
]

# -- Options for Texinfo output ------------------------------------------------

texinfo_documents = [
    (master_doc, '%s'%module_version.name, doctitle,
     author, '%s'%module_version.name, docfull,
     'Miscellaneous'),
]

# -- Options for Epub output ---------------------------------------------------

epub_title         = doctitle
epub_author        = author
epub_publisher     = author
epub_copyright     = copyright
epub_exclude_files = ['search.html']

# -- Options for PDF output ----------------------------------------------------

pdf_documents = [(
    'contents',
    u'%s'%module_version.name,
    u'%s'%module_version.name,
    author,
    dict(pdf_compressed = True),
),]
pdf_stylesheets = ['sphinx','kerning','a4']
pdf_compressed = True
pdf_inline_footnotes = True

# -- Extension configuration ---------------------------------------------------
