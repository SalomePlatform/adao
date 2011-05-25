include $(top_srcdir)/adm_local/make_common_starter.am

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = $(top_builddir)/doc/build
SRCDIR        = $(top_srcdir)/doc

EXTRA_DIST = conf.py advanced.rst  examples.rst  index.rst  intro.rst  theory.rst  using.rst \
	     resources/ADAO.png \
	     resources/ADAO_small.png \
	     resources/ADAO_small_rouge.png \
	     resources/ADAO_small_vert.png \
	     images/adao_activate.png \
	     images/adao_jdcexample01.png \
	     images/adao_scriptentry01.png \
	     images/adao_viewer.png \
	     images/eficas_new.png \
	     images/eficas_save.png \
	     images/eficas_yacs.png \
	     images/yacs_generatedscheme.png \
	     images/adao_exporttoyacs.png \
	     images/adao_jdcexample02.png \
	     images/adao_scriptentry02.png \
	     images/eficas_close.png \
	     images/eficas_open.png \
	     images/eficas_saveas.png \
	     images/yacs_containerlog.png

install-data-local:
	make html
	${mkinstalldirs} $(DESTDIR)$(docdir)
	${mkinstalldirs} $(DESTDIR)$(salomeresdir)
	cp -R $(BUILDDIR)/html/* $(DESTDIR)$(docdir)
	cp $(SRCDIR)/resources/*.png $(DESTDIR)$(salomeresdir)
	cp $(SRCDIR)/images/eficas_*.png $(DESTDIR)$(salomeresdir)

uninstall-local:
	chmod -R +w $(DESTDIR)$(docdir)
	rm -rf $(DESTDIR)$(docdir)
	rm -f $(DESTDIR)$(salomeresdir)/*.png

clean-local:
	-rm -rf $(top_builddir)/doc/build


# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(top_srcdir)/doc

.PHONY: help clean html dirhtml pickle json htmlhelp qthelp latex changes linkcheck doctest

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  dirhtml   to make HTML files named index.html in directories"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  qthelp    to make HTML files and a qthelp project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  doctest   to run all doctests embedded in the documentation (if enabled)"

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/ADAO.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/ADAO.qhc"

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."
