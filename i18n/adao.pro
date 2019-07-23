# Copy/paste the first lines to generate the list of source files
#
# clear ; echo ; echo -e "#\n# Debut des sources" ; echo ; \
# echo -e "TRANSLATIONS += adao_fr.ts\n\nCODECFORTR = utf-8\n" ; \
# find .. -name '*.ui' | sed 's#^\.#FORMS += .#g' | sort ; \
# find ../bin -name '*.py' | sed 's#^\.#SOURCES += .#g' | sort ; \
# find ../src -name '*.py' | grep -v tests/ | sed 's#^\.#SOURCES += .#g' ; \
# echo
#
# Creer ou remettre a jour les fichiers TS avec :
#   pylupdate5 adao.pro
#   geany adao_*.ts # Pour traiter si necessaire les "obsolete"
#   linguist adao_*.ts
#   lrelease adao.pro
#
# Pour refaire facilement les fichiers QM a partir des fichiers TS :
#   lrelease -qm adao_en.qm adao_en.ts
#   lrelease -qm adao_fr.qm adao_fr.ts
#
# Debut des sources

TRANSLATIONS += adao_en.ts
TRANSLATIONS += adao_fr.ts

CODECFORTR = utf-8
