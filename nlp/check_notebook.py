import json

notebook_path = r"e:/GitHub/finalproject.mlops.group9.msa29hcm/nlp/VSM_RAG-demo_Group_3.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for idx, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source_str = "".join(cell["source"])
        if any(term in source_str for term in ["plot_overall_quality", "plot_latency_vs_quality", "plot_category_breakdown", "display_overall_summary", "load_overall_summaries"]):
            print(f"Cell index {idx}:")
            print(source_str)
            print("-" * 40)
