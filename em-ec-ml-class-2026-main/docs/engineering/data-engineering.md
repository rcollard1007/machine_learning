# Data Engineering

The purpose of a data engineering project is to deliver data artifacts that are stored in a secure, reliable and scalable way. This necessitates strict access management, and traceability of the data and the execution events.

## Principles

- A Data Engineering project is a software project, and thus must follow good software engineering practices.
- It is best handled as a standalone object, decoupled from any Machine Learning or dashboarding logic.
- In essence an data engineering project is a `data factory`, producing clean data based on raw data. Therefore it has 2 deliverables: 1) a, Extract-Transform-Load (ETL) pipeline (as source code), 2) a lineage of data produced using this pipeline.
- The project establishes the data contract, consumed by downstream ML projects, dashboards or other processes. It must sets what is quality data, and handle out-of-distribution situations (missing data, extraordinary values, wrong behavior of upstream processing).
- The execution of a Data Engineering project consumes input artifacts (rows in a database, logs, files), apply transformations on it and generates output artifacts (rows in a database, live stream). All inputs, outputs and events must be versioned and have identifiers allowing to audit and troubleshoot.
- The execution must be resilient: it should fulfils idempotent execution, retry mechanism, bad records flagging. 
- The execution is best set as background tasks with scheduling, alerting in case of execution warning/failure.
