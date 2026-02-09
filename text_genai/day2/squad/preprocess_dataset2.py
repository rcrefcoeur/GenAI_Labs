import os
import json
import pandas as pd
from collections import defaultdict
import sys
from pathlib import Path

# Make "day2/" importable no matter where you run from
DAY2_DIR = Path(__file__).resolve().parents[1]  # .../day2
sys.path.append(str(DAY2_DIR))

from RAG.I_constants import source_path  # can be str or Path

SCRIPT_DIR = Path(__file__).resolve().parent  # .../day2/squad

# Input parquet is expected to be in the same folder as this script
squad_path = SCRIPT_DIR / "train-00000-of-00001.parquet"

# All outputs go into day2/output/
output_dir = DAY2_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# JSON output file
json_out_path = output_dir / "squad_multiple_contexts.json"

# Ensure source_path folder exists (convert to Path safely)
source_path = Path(source_path)
source_path.mkdir(parents=True, exist_ok=True)


def extract_questions_and_answers(squad_parquet_path):
    df_org = pd.read_parquet(squad_parquet_path)
    question_context_map = defaultdict(set)

    for context, question in zip(df_org["context"], df_org["question"]):
        question_context_map[question].add(context)

    questions = []
    for n, q in enumerate(question_context_map):
        if len(question_context_map[q]) > 1:
            new_question = {"text": q, "sources": []}

            for m, c in enumerate(question_context_map[q]):
                new_id = "Q%d_C%d.txt" % (n, m)
                new_question["sources"].append(new_id)

                out_txt = source_path / new_id
                out_txt.write_text(c, encoding="utf-8")

            questions.append(new_question)

    json_out_path.write_text(
        json.dumps(questions, indent=1, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Read parquet:", squad_parquet_path)
    print("Wrote texts to:", source_path)
    print("Wrote json to:", json_out_path)


if __name__ == "__main__":
    if not squad_path.exists():
        raise FileNotFoundError(f"Parquet not found: {squad_path}")
    extract_questions_and_answers(squad_path)