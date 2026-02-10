# Code Nexus

Code Nexus is a minimal data-processing framework written in Python that demonstrates how real-world data pipelines are designed, orchestrated, and used.

The project focuses on **clean architecture**, **separation of concerns**, and **practical data cleaning**, using a CSV cleaning pipeline as a concrete example.

---

## What this project does

Given a messy CSV file, the pipeline:

- Parses raw input into structured records
- Cleans and normalizes the data
- Outputs a clean, machine-readable CSV file

The same pipeline logic can be reused with different input formats (CSV, JSON, streams) without changing the core processing logic.

---

## Project structure

.
- ├── adapters/
- │ ├── csv_adapter.py
- │ ├── json_adapter.py
- │ └── stream_adapter.py
- ├── stages/
- │ ├── base.py
- │ ├── input_stage.py
- │ ├── transform_stage.py
- │ └── output_stage.py
- ├── pipelines/
- │ └── default_pipeline.py
- ├── manager.py
- ├── pipeline.py
- ├── run.py
- ├── create_sample_data.py


---

## Architecture overview

### Adapters
Adapters handle **format translation only**.

- Convert external formats (CSV, JSON, stream) into Python records
- Do not clean data
- Do not contain business logic

---

### Stages
Stages are small, focused processing steps:

- **InputStage**  
  Normalizes input into a stable internal structure
- **TransformStage**  
  Cleans and transforms records
- **OutputStage**  
  Serializes cleaned records into CSV output

Each stage follows the same contract:


---

### Pipeline
A pipeline orchestrates stages.

- Defines execution order
- Passes data between stages
- Handles execution flow

Stages define *what* happens.  
The pipeline defines *how it runs*.

---

### NexusManager
The manager routes data to pipelines.

- Registers pipelines by name
- Dispatches parsed data to the correct pipeline
- Keeps adapters decoupled from pipeline logic

Even with a single pipeline, it enforces a clean architectural boundary.

---

## Usage

### 1. Generate sample data

Create a messy CSV file for testing:

```bash
python3 create_sample_data.py

This creates:

data/messy.csv

2. Run the pipeline
python3 run.py data/messy.csv


Output:

out/clean.csv

```

## Error handling

- Only `.csv` and `.json` files are accepted
- Invalid file paths are rejected with clear messages
- The program never crashes with raw Python tracebacks
- Errors are handled at the entrypoint, not inside the pipeline

---

## Skills demonstrated

- Clean separation of concerns
- Adapter pattern for format isolation
- Pipeline and stage orchestration
- Protocol-based polymorphism (duck typing)
- Data serialization and validation
- Writing reusable framework code
- Designing software that is easy to explain and extend

---

## Purpose

This project is intentionally minimal.

Its goal is to demonstrate:

- how data pipelines are structured  
- how responsibilities are clearly divided  
- how clean design improves readability and maintainability  

rather than to build a large production system.
