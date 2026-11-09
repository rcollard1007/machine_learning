# Machine Learning Engineering

The purpose of a machine learning project is to deliver a lineage of machine learning models, used to perform a task automatically, in a target production environment, with a reliable estimation of its ability to perform this task.

## Principles

- An ML project is a software project, and thus must follow good software engineering practices: version control, code quality, unit and integration testing, CICD. In particular, all exploration, analysis and documentation material must be dissociated from the project source code.
- It is best handled as a standalone object, decoupled from any production service logic, scheduled raw data ingestion, or user interfaces.
- In essence an ML project is a `model factory`, producing models based on a snapshot of data. Therefore it has 3 deliverables: 1) a model factory pipeline (as source code), 2) a model instance produced using this pipeline (as a runnable object), 3) a quality evaluation pipeline.
- There must be a strict separation between train, validation and test data, and the splitting must be appropriate given the use case (split by time, or by group with a balance mimicking real stats). Compare models on validation data only, as model selection based on the test data gives an overestimation of a model's true quality.
- Acceptance levels must be clarified asap, and a baseline rule or model should be delivered first to establish the standard to beat.
- The execution of an ML project must generate metadata for each experiment, with identifiers of the input artifacts (data, configuration, source code version) and output artifacts (model, metrics), which is necessary for reproducibility and traceability.
- Input data evolves over time, hence model quality must be monitored, so that as the data evolves, the model also evolves.

## Execution

The execution of a Machine Learning project produces artifacts: models, metrics, metadatas.
This execution depends on the echosystem it lives in:

- Data is often stored in a remote storage solution with access management, in which case no data streams through your laptop. It is often the code that goes next to the data, not the other way around.
- Training jobs can necessitate specific compute hardware, so can run on a virtual machine or docker container running on a remote cluster. Therefore, code development happens locally while execution happens remotely. It is critical that the code behaves the same on the different platforms it runs on (this holds for collaboration as well, as all contributors may not have identical machines of operative systems).
- Training runs produce metadatas that are handled by dedicated tools. These metadata must carry all informations regading the source code version, the data version, and the configuration content (random seeds, train and eval params) in order to guarantee reproducibility.
- Models are artifacts that must be compatible with a production echosystem. An artifact produced by python code must be loadable in the target language (c++, rust, java ... or python itself), and a parity test must pass: the model behavior across train/prod environments must be the same on a representative test sample.
