# -*- coding: utf-8 -*-

# --------------------------------------------------
# debut entete
# --------------------------------------------------

import Accas
from Accas import *

JdC = JDC_CATA (code = 'DATASSIM',
                execmodul = None,
                regles = ( AU_MOINS_UN ('ASSIM_STUDY')),
               )

def F_VECTOR(statut) : return FACT(statut = statut,
                                   FROM = SIMP(statut = "o", typ = "TXM", into=("String")),
                                   DATA = SIMP(statut = "o", typ = "TXM"),
                                  )

def F_MATRIX(statut) : return FACT(statut = statut,
                                   FROM = SIMP(statut = "o", typ = "TXM", into=("String")),
                                   DATA = SIMP(statut = "o", typ = "TXM"),
                                  )

def F_BACKGROUND(statut) : return FACT(statut=statut,
                                       regles = ( UN_PARMI ("VECTOR")),
                                       VECTOR = F_VECTOR("o"),
                                      )

def F_BACKGROUND_ERROR(statut) : return FACT(statut=statut,
                                             regles = ( UN_PARMI ("MATRIX")),
                                             MATRIX = F_MATRIX("o"),
                                            )

def F_OBSERVATION(statut) : return FACT(statut=statut,
                                        regles = ( UN_PARMI ("VECTOR")),
                                        VECTOR = F_VECTOR("o"),
                                       )

def F_OBSERVATION_ERROR(statut) : return FACT(statut=statut,
                                              regles = ( UN_PARMI ("MATRIX")),
                                              MATRIX = F_MATRIX("o"),
                                             )

def F_OBSERVATION_OPERATOR(statut) : return FACT(statut=statut,
                                                 regles = ( UN_PARMI ("MATRIX", "FUNCTION")),
                                                 MATRIX = F_MATRIX("o"),
                                                )

def F_ANALYSIS(statut) : return FACT(statut = statut,
                                     FROM = SIMP(statut = "o", typ = "TXM", into=("String", "File")),
                                     STRING_DATA = BLOC ( condition = " FROM in ( 'String', ) ",

                                                  STRING = SIMP(statut = "o", typ = "TXM"),
                                                 ),
                                     FILE_DATA = BLOC ( condition = " FROM in ( 'File', ) ",

                                                  FILE = SIMP(statut = "o", typ = "Fichier"),
                                                 ),
                                    )


ASSIM_STUDY = PROC(nom="ASSIM_STUDY",
                   op=None,
                   repetable = "n",
                   STUDY_NAME = SIMP(statut="o", typ = "TXM"),
                   ALGORITHM  = FACT(statut='o',
                                     regles = ( UN_PARMI ("Blue", "ENSEMBLEBLUE"),),

                                     Blue = FACT(regles = ( ENSEMBLE ("Background", "BackgroundError", 
                                                                      "Observation", "ObservationError",
                                                                      "ObservationOperator")),
                                                 Background = F_BACKGROUND("o"),
                                                 BackgroundError = F_BACKGROUND_ERROR("o"),
                                                 Observation = F_OBSERVATION("o"),
                                                 ObservationError = F_OBSERVATION_ERROR("o"),
                                                 ObservationOperator = F_OBSERVATION_OPERATOR("o"),
                                                 Analysis = F_ANALYSIS("f"),
                                                ),
                                     ENSEMBLEBLUE = FACT(BACKGROUND = F_BACKGROUND("o"),
                                                        ),
                                    ),
                  )

