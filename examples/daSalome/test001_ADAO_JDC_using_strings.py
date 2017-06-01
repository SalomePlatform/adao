# -*- coding: utf-8 -*-
study_config = {} 
study_config['StudyType'] = 'ASSIMILATION_STUDY'
study_config['Name'] = 'Test'
study_config['Debug'] = '0'
study_config['Algorithm'] = 'Blue'
Background_config = {}
Background_config['Type'] = 'Vector'
Background_config['From'] = 'String'
Background_config['Data'] = '0 0 0'
study_config['Background'] = Background_config
BackgroundError_config = {}
BackgroundError_config['Type'] = 'Matrix'
BackgroundError_config['From'] = 'String'
BackgroundError_config['Data'] = '1 0 0 ; 0 1 0 ; 0 0 1'
study_config['BackgroundError'] = BackgroundError_config
Observation_config = {}
Observation_config['Type'] = 'Vector'
Observation_config['From'] = 'String'
Observation_config['Data'] = '1 1 1'
study_config['Observation'] = Observation_config
ObservationError_config = {}
ObservationError_config['Type'] = 'Matrix'
ObservationError_config['From'] = 'String'
ObservationError_config['Data'] = '1 0 0 ; 0 1 0 ; 0 0 1'
study_config['ObservationError'] = ObservationError_config
ObservationOperator_config = {}
ObservationOperator_config['Type'] = 'Matrix'
ObservationOperator_config['From'] = 'String'
ObservationOperator_config['Data'] = '1 0 0 ; 0 1 0 ; 0 0 1'
study_config['ObservationOperator'] = ObservationOperator_config
inputvariables_config = {}
inputvariables_config['Order'] =['adao_default']
inputvariables_config['adao_default'] = -1
study_config['InputVariables'] = inputvariables_config
outputvariables_config = {}
outputvariables_config['Order'] = ['adao_default']
outputvariables_config['adao_default'] = -1
study_config['OutputVariables'] = outputvariables_config
Analysis_config = {}
Analysis_config['From'] = 'String'
Analysis_config['Data'] = """import numpy
xa=numpy.ravel(ADD.get('Analysis')[-1])
print 'Analysis:',xa"""
study_config['UserPostAnalysis'] = Analysis_config
