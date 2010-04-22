study_config = {}
study_config["Name"] = "test000_Blue"
study_config["Algorithm"] = "Blue"

Background_config = {}
Background_config["Data"] = "0,1,2"
Background_config["Type"] = "Vector"
Background_config["From"] = "string"
study_config["Background"] = Background_config

BackgroundError_config = {}
BackgroundError_config["Data"] = "1 0 0;0 1 0;0 0 1"
BackgroundError_config["Type"] = "Matrix"
BackgroundError_config["From"] = "string"
study_config["BackgroundError"] = BackgroundError_config

Observation_config = {}
Observation_config["Data"] = "0.5,1.5,2.5"
Observation_config["Type"] = "Vector"
Observation_config["From"] = "string"
study_config["Observation"] = Observation_config

ObservationError_config = {}
ObservationError_config["Data"] = "1 0 0;0 1 0;0 0 1"
ObservationError_config["Type"] = "Matrix"
ObservationError_config["From"] = "string"
study_config["ObservationError"] = ObservationError_config

ObservationOperator_config = {}
ObservationOperator_config["Data"] = "1 0 0;0 1 0;0 0 1"
ObservationOperator_config["Type"] = "Matrix"
ObservationOperator_config["From"] = "string"
study_config["ObservationOperator"] = ObservationOperator_config
