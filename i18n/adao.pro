# Copy/paste the first lines to generate the list of source files
#
# clear ; echo ; echo -e "#\n# Debut des sources" ; echo ; \
# echo -e "TRANSLATIONS += adao_fr.ts\n\nCODECFORTR = utf-8\n" ; \
# find .. -name '*.ui' | sed 's#^\.#FORMS += .#g' | sort ; \
# find ../bin -name '*.py' | sed 's#^\.#SOURCES += .#g' | sort ; \
# find ../src -name '*.py' | grep -v tests/ | sed 's#^\.#SOURCES += .#g' ; \
# echo
#
# Create/update the .ts files with:
# pylupdate5 adao.pro
# geany adao_*.ts # Pour traiter si necessaire les "obsolete"
# linguist adao_*.ts
# lrelease adao.pro
#
# Debut des sources

TRANSLATIONS += adao_en.ts
TRANSLATIONS += adao_fr.ts

CODECFORTR = utf-8
