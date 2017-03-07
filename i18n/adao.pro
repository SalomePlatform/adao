# Copy/paste the first lines to generate the list of source files
#
# clear ; echo ; echo -e "#\n# Debut des sources" ; echo ; \
# echo -e "TRANSLATIONS += adao_fr.ts\n\nCODECFORTR = utf-8\n" ; \
# find .. -name '*.ui' | sed 's#^\.#FORMS += .#g' ; \
# find ../bin -name '*.py' | sed 's#^\.#SOURCES += .#g' ; \
# find ../src -name '*.py' | grep -v tests/ | sed 's#^\.#SOURCES += .#g' ; \
# echo
#
# Create/update the .ts files with:
# pylupdate5 i18n/adao.pro
# geany i18n/adao_*.ts # Pour traiter si necessaire les "obsolete"
# linguist i18n/adao_*.ts
# lrelease i18n/adao.pro
#
# Debut des sources

TRANSLATIONS += adao_en.ts
TRANSLATIONS += adao_fr.ts

CODECFORTR = utf-8
