# run.py
import sys
import os

from adapters import CSVAdapter
from stages import InputStage, TransformStage, OutputStage
from pipelines import DefaultPipeline
from manager import NexusManager


def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py <csv-file>")
        return

    path = sys.argv[1]

    if not (path.endswith(".csv") or path.endswith(".json")):
        print("Error: unsupported file type. Only .csv and .json files are allowed.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            csv_text = f.read()

        pipeline = DefaultPipeline()
        pipeline.add_stage(InputStage())
        pipeline.add_stage(TransformStage())
        pipeline.add_stage(OutputStage())

        manager = NexusManager()
        manager.add_pipeline("clean_csv", pipeline)

        adapter = CSVAdapter("clean_csv")
        result = adapter.process(csv_text, manager)

        os.makedirs("out", exist_ok=True)

        with open("out/clean.csv", "w", encoding="utf-8") as f:
            f.write(result)

        print("Clean CSV written to: out/clean.csv")

    except FileNotFoundError:
        print(f"Error: file not found → {path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
