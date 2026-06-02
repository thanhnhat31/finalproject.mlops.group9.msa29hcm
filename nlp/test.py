import time
import json
from sentence_transformers import CrossEncoder

def evaluate_cross_encoder(dataset, chunks, model, top_k=5):
    """
    Evaluate the Cross-Encoder model on a dataset of test queries against a corpus of chunks.
    Focuses purely on testing, calculating scores, and recording execution time.
    
    Args:
        dataset (list of dict): List of query dicts, e.g., [{"id": "TC01", "category": "Exact Keyword", "query": "..."}]
        chunks (list of str): Pre-loaded list of document chunks.
        model (CrossEncoder): Pre-initialized Cross-Encoder model instance.
        top_k (int): Number of top retrieval results to record.
        
    Returns:
        list of dict: Detailed evaluation logs for each query.
        dict: Aggregated summary stats (total queries, avg latency, latency by category).
    """
    evaluation_logs = []
    category_stats = {}
    total_latency = 0.0
    
    for idx, item in enumerate(dataset):
        query_id = item.get("id", f"Q{idx}")
        category = item.get("category", "General")
        query_text = item.get("query")
        
        # Build dynamic query-chunk pairs for Cross-Encoder ranking
        pairs = [[query_text, chunk] for chunk in chunks]
        
        # Run inference and measure execution time (latency)
        start_time = time.time()
        scores = model.predict(pairs)
        latency = time.time() - start_time
        
        total_latency += latency
        
        # Keep track of latency metrics by category
        if category not in category_stats:
            category_stats[category] = {"count": 0, "total_latency": 0.0}
        category_stats[category]["count"] += 1
        category_stats[category]["total_latency"] += latency
        
        # Rank and extract top results
        ranked_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        top_results = []
        for rank in range(min(top_k, len(ranked_indices))):
            orig_idx = ranked_indices[rank]
            top_results.append({
                "rank": rank + 1,
                "chunk_index": orig_idx,
                "score": float(scores[orig_idx]),
                "text": chunks[orig_idx]
            })
            
        evaluation_logs.append({
            "id": query_id,
            "category": category,
            "query": query_text,
            "latency_seconds": latency,
            "top_matches": top_results
        })
        
    # Build final stats report dict
    summary_report = {
        "total_queries": len(dataset),
        "total_time_seconds": total_latency,
        "average_latency_seconds": total_latency / len(dataset) if dataset else 0.0,
        "latency_by_category": {
            cat: stats["total_latency"] / stats["count"]
            for cat, stats in category_stats.items()
        }
    }
    
    return evaluation_logs, summary_report
