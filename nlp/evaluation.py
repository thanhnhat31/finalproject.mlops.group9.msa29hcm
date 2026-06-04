import time
import pandas as pd
import matplotlib.pyplot as plt

def calculate_metrics(retrieved_indices, expected_indices):
    """
    Calculate Reciprocal Rank (RR) and Hit@1 (Accuracy@1) for a query.
    Returns (None, None) if expected_indices is empty (Out of Domain query).
    
    Args:
        retrieved_indices (list of int): Ordered list of retrieved chunk indices.
        expected_indices (list of int): List of ground truth chunk indices.
        
    Returns:
        tuple: (rr, hit_at_1)
    """
    if not expected_indices:
        return None, None
        
    hit_at_1 = 1.0 if retrieved_indices and retrieved_indices[0] in expected_indices else 0.0
    
    rr = 0.0
    for rank, idx in enumerate(retrieved_indices):
        if idx in expected_indices:
            rr = 1.0 / (rank + 1)
            break
            
    return rr, hit_at_1

def evaluate_bm25(dataset, chunks, bm25_index, top_k=3):
    """
    Evaluate the Custom BM25 Sparse retriever.
    """
    results = []
    for item in dataset:
        query_text = item["query"]
        expected = item.get("expected_chunk_id", [])
        
        retrieved, duration = bm25_index.retrieve(query_text, chunks, top_k=top_k)
        retrieved_indices = [r["chunk_index"] for r in retrieved]
        
        rr, hit = calculate_metrics(retrieved_indices, expected)
        results.append({
            "id": item["id"],
            "category": item["category"],
            "query": query_text,
            "expected_chunk_id": expected,
            "retrieved_index": retrieved_indices[0] if retrieved_indices else -1,
            "latency_ms": duration * 1000,
            "rr": rr,
            "hit": hit
        })
    return results

def evaluate_dense(dataset, chunks, dense_retriever, top_k=3):
    """
    Evaluate the Bi-Encoder Dense retriever.
    """
    results = []
    for item in dataset:
        query_text = item["query"]
        expected = item.get("expected_chunk_id", [])
        
        retrieved, duration = dense_retriever.retrieve(query_text, chunks, top_k=top_k)
        retrieved_indices = [r["chunk_index"] for r in retrieved]
        
        rr, hit = calculate_metrics(retrieved_indices, expected)
        results.append({
            "id": item["id"],
            "category": item["category"],
            "query": query_text,
            "expected_chunk_id": expected,
            "retrieved_index": retrieved_indices[0] if retrieved_indices else -1,
            "latency_ms": duration * 1000,
            "rr": rr,
            "hit": hit
        })
    return results

def evaluate_cross_encoder_single_stage(dataset, chunks, ce_model, single_stage_fn, top_k=3):
    """
    Evaluate the Single-Stage Cross-Encoder model.
    """
    results = []
    for item in dataset:
        query_text = item["query"]
        expected = item.get("expected_chunk_id", [])
        
        retrieved, duration = single_stage_fn(query_text, chunks, ce_model, top_k=top_k)
        retrieved_indices = [r["chunk_index"] for r in retrieved]
        
        rr, hit = calculate_metrics(retrieved_indices, expected)
        results.append({
            "id": item["id"],
            "category": item["category"],
            "query": query_text,
            "expected_chunk_id": expected,
            "retrieved_index": retrieved_indices[0] if retrieved_indices else -1,
            "latency_ms": duration * 1000,
            "rr": rr,
            "hit": hit
        })
    return results

def evaluate_two_stage(dataset, chunks, dense_retriever, ce_model, two_stage_fn, stage1_top_k=5, stage2_top_k=3):
    """
    Evaluate the Two-Stage Cross-Encoder retriever.
    """
    results = []
    for item in dataset:
        query_text = item["query"]
        expected = item.get("expected_chunk_id", [])
        
        retrieved, latency_breakdown = two_stage_fn(
            query=query_text,
            corpus=chunks,
            stage1_retriever=dense_retriever,
            stage2_model=ce_model,
            stage1_top_k=stage1_top_k,
            stage2_top_k=stage2_top_k
        )
        retrieved_indices = [r["chunk_index"] for r in retrieved]
        
        rr, hit = calculate_metrics(retrieved_indices, expected)
        results.append({
            "id": item["id"],
            "category": item["category"],
            "query": query_text,
            "expected_chunk_id": expected,
            "retrieved_index": retrieved_indices[0] if retrieved_indices else -1,
            "latency_ms": latency_breakdown["total_seconds"] * 1000,
            "rr": rr,
            "hit": hit
        })
    return results

def compute_summary_report(bm25_res, dense_res, ce_res, two_stage_res=None):
    """
    Compute average statistics (latency, MRR, hit rate) for all models.
    """
    models = ["BM25 (Sparse)", "Bi-Encoder (Dense)", "Cross-Encoder (Context)"]
    results_list = [bm25_res, dense_res, ce_res]
    
    if two_stage_res is not None:
        models.append("Two-Stage (Dense + CE)")
        results_list.append(two_stage_res)
        
    summary_data = []
    
    for model_name, res in zip(models, results_list):
        df = pd.DataFrame(res)
        # Filter out Out of Domain queries for MRR/Accuracy calculations
        df_valid = df[df["expected_chunk_id"].map(len) > 0]
        
        avg_latency = df["latency_ms"].mean()
        mrr = df_valid["rr"].mean() if not df_valid.empty else 0.0
        accuracy = df_valid["hit"].mean() if not df_valid.empty else 0.0
        
        summary_data.append({
            "Model": model_name,
            "Average Latency (ms)": avg_latency,
            "Mean Reciprocal Rank (MRR)": mrr,
            "Accuracy@1 (Hit Rate)": accuracy
        })
        
    return pd.DataFrame(summary_data)



def compute_category_report(bm25_res, dense_res, ce_res, two_stage_res=None):
    """
    Computes performance statistics (latency, MRR, hit rate) grouped by Category for all models.
    Pivots the resulting dataframe for a cleaner side-by-side comparison matrix.
    """
    models = ["BM25 (Sparse)", "Bi-Encoder (Dense)", "Cross-Encoder (Context)"]
    results_list = [bm25_res, dense_res, ce_res]
    
    if two_stage_res is not None:
        models.append("Two-Stage (Dense + CE)")
        results_list.append(two_stage_res)
        
    category_data = []
    
    for model_name, res in zip(models, results_list):
        df = pd.DataFrame(res)
        
        # Group by category
        for category, group in df.groupby("category"):
            is_out_of_domain = (category == "Out of Domain")
            
            avg_latency = group["latency_ms"].mean()
            
            if is_out_of_domain:
                mrr = None
                accuracy = None
            else:
                mrr = group["rr"].mean() if "rr" in group else 0.0
                accuracy = group["hit"].mean() if "hit" in group else 0.0
                
            category_data.append({
                "Category": category,
                "Model": model_name,
                "Average Latency (ms)": avg_latency,
                "MRR": mrr,
                "Accuracy@1": accuracy
            })
            
    df_cat = pd.DataFrame(category_data)
    
    # Pivot for clean comparison format
    df_pivot = df_cat.pivot(index="Category", columns="Model", values=["Average Latency (ms)", "MRR", "Accuracy@1"])
    return df_pivot

def plot_comparisons(df_summary):
    """
    Plots the latency and quality comparisons from the summary report dataframe.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    models = df_summary["Model"].tolist()
    latencies = df_summary["Average Latency (ms)"].tolist()
    mrr_scores = df_summary["Mean Reciprocal Rank (MRR)"].tolist()
    acc_scores = df_summary["Accuracy@1 (Hit Rate)"].tolist()
    
    # Custom color palette for 3 or 4 models
    colors = ['#FFA07A', '#5E64FF', '#FF5E7E', '#20B2AA'][:len(models)]
    
    # Latency Chart
    bars1 = axes[0].bar(models, latencies, color=colors, width=0.45)
    axes[0].set_title("Average Latency Comparison", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Latency (milliseconds)")
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    axes[0].set_xticklabels(models, rotation=15, ha='right')
    
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + (max(latencies) * 0.02), f"{yval:.2f} ms", ha='center', va='bottom', fontweight='bold')
        
    # Quality Metrics Chart (grouped bars)
    x = range(len(models))
    width = 0.3
    
    bars_mrr = axes[1].bar([i - width/2 for i in x], mrr_scores, width, label='MRR', color='#4682B4')
    bars_acc = axes[1].bar([i + width/2 for i in x], acc_scores, width, label='Accuracy@1', color='#8FBC8F')
    
    axes[1].set_title("Retrieval Quality Comparison (MRR vs Accuracy@1)", fontsize=12, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(models, rotation=15, ha='right')
    axes[1].set_ylabel("Score (0.0 to 1.0)")
    axes[1].set_ylim(0, 1.15)
    axes[1].legend()
    axes[1].grid(axis='y', linestyle='--', alpha=0.3)
    
    for bar in bars_mrr:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval*100:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
    for bar in bars_acc:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval*100:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
    plt.tight_layout()
    plt.show()
