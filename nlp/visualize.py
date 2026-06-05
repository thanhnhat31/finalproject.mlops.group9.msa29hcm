import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shutil

def load_overall_summaries(data_dir="nlp/data/evaluation_results"):
    """
    Loads and compiles the overall summary CSV files for paragraph, semantic, and sliding chunking.
    
    Args:
        data_dir (str): Path to directory containing evaluation results.
        
    Returns:
        pd.DataFrame: Merged dataframe with overall results.
    """
    methods = ["paragraph", "semantic", "sliding"]
    overall_dfs = []

    for method in methods:
        file_path = os.path.join(data_dir, f"overall_summary_{method}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["Chunking Method"] = method.capitalize()
            # Rename columns for consistency
            df = df.rename(columns={
                "Mean Reciprocal Rank (MRR)": "MRR",
                "Accuracy@1 (Hit Rate)": "Accuracy@1"
            })
            overall_dfs.append(df)

    if not overall_dfs:
        raise FileNotFoundError(f"No overall summary CSV files found in {data_dir}")

    df_overall = pd.concat(overall_dfs, ignore_index=True)

    # Clean names
    df_overall["Model"] = df_overall["Model"].str.replace(" (Sparse)", "", regex=False)
    df_overall["Model"] = df_overall["Model"].str.replace(" (Dense)", "", regex=False)
    df_overall["Model"] = df_overall["Model"].str.replace(" (Context)", "", regex=False)
    df_overall["Model"] = df_overall["Model"].str.replace(" (Dense + CE)", "", regex=False)
    
    return df_overall

def plot_overall_quality(df_overall, save_path=None, show=True):
    """
    Plots the MRR and Accuracy@1 comparisons (Grouped Bar Chart).
    
    Args:
        df_overall (pd.DataFrame): Dataframe returned by load_overall_summaries.
        save_path (str, optional): Path to save the generated plot.
        show (bool): Whether to display the plot inline (useful in notebook).
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    models = df_overall["Model"].unique()
    chunk_methods = ["Paragraph", "Semantic", "Sliding"]
    colors = {"Paragraph": "#3B82F6", "Semantic": "#10B981", "Sliding": "#EF4444"} # Blue, Green, Red

    x = np.arange(len(models))
    width = 0.25

    # Left Plot: MRR
    for idx, method in enumerate(chunk_methods):
        subset = df_overall[df_overall["Chunking Method"] == method]
        subset = subset.set_index("Model").reindex(models).reset_index()
        mrr_vals = subset["MRR"].fillna(0).tolist()
        bars = axes[0].bar(x + (idx - 1) * width, mrr_vals, width, label=method, color=colors[method], alpha=0.9, edgecolor="grey", linewidth=0.5)
        
        # Add values on top of bars
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                axes[0].text(bar.get_x() + bar.get_width()/2.0, h + 0.01, f"{h:.3f}", ha='center', va='bottom', fontsize=9, fontweight='semibold')

    axes[0].set_title("Mean Reciprocal Rank (MRR) Comparison", fontsize=14, fontweight='bold', pad=15)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models, fontsize=11)
    axes[0].set_ylabel("MRR Score", fontsize=12)
    axes[0].set_ylim(0, 0.75)
    axes[0].grid(axis='y', linestyle='--', alpha=0.3)
    axes[0].legend(title="Chunking Method", fontsize=10)

    # Right Plot: Accuracy@1
    for idx, method in enumerate(chunk_methods):
        subset = df_overall[df_overall["Chunking Method"] == method]
        subset = subset.set_index("Model").reindex(models).reset_index()
        acc_vals = subset["Accuracy@1"].fillna(0).tolist()
        bars = axes[1].bar(x + (idx - 1) * width, acc_vals, width, label=method, color=colors[method], alpha=0.9, edgecolor="grey", linewidth=0.5)
        
        # Add values on top of bars
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                axes[1].text(bar.get_x() + bar.get_width()/2.0, h + 0.01, f"{h:.3f}", ha='center', va='bottom', fontsize=9, fontweight='semibold')

    axes[1].set_title("Accuracy@1 (Hit Rate) Comparison", fontsize=14, fontweight='bold', pad=15)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(models, fontsize=11)
    axes[1].set_ylabel("Accuracy@1 Score", fontsize=12)
    axes[1].set_ylim(0, 0.75)
    axes[1].grid(axis='y', linestyle='--', alpha=0.3)
    axes[1].legend(title="Chunking Method", fontsize=10)

    # Styling
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cccccc')
        ax.spines['bottom'].set_color('#cccccc')

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()
    else:
        plt.close()

def plot_latency_vs_quality(df_overall, save_path=None, show=True):
    """
    Plots the Latency vs Quality (MRR) Trade-off (Pareto Frontier).
    
    Args:
        df_overall (pd.DataFrame): Dataframe returned by load_overall_summaries.
        save_path (str, optional): Path to save the generated plot.
        show (bool): Whether to display the plot inline (useful in notebook).
    """
    plt.figure(figsize=(10, 7))

    markers = {"Paragraph": "o", "Semantic": "s", "Sliding": "^"}
    model_colors = {
        "BM25": "#6B7280",          # Gray
        "Bi-Encoder": "#3B82F6",    # Blue
        "Cross-Encoder": "#F59E0B", # Orange
        "Two-Stage": "#8B5CF6"      # Purple
    }

    for _, row in df_overall.iterrows():
        model = row["Model"]
        method = row["Chunking Method"]
        latency = row["Average Latency (ms)"]
        mrr = row["MRR"]
        
        plt.scatter(
            latency, mrr, 
            s=150, 
            color=model_colors[model], 
            marker=markers[method], 
            alpha=0.85, 
            edgecolors="black", 
            linewidths=1.0,
            label=f"{model} ({method})"
        )
        
        # Add label next to point
        plt.annotate(
            f"{model}\n({method})", 
            (latency, mrr),
            textcoords="offset points", 
            xytext=(0, 10), 
            ha='center', 
            fontsize=8, 
            fontweight='semibold',
            bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.1, ec="gray", lw=0.5)
        )

    plt.xscale("log")
    plt.xlabel("Average Latency in ms (Log Scale)", fontsize=12)
    plt.ylabel("Mean Reciprocal Rank (MRR)", fontsize=12)
    plt.title("RAG Retrieval: Latency vs. Retrieval Quality (MRR) Trade-off", fontsize=14, fontweight='bold', pad=15)
    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.ylim(0.15, 0.7)
    plt.xlim(0.03, 700.0)

    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#6B7280', markersize=10, label='BM25 (Sparse)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#3B82F6', markersize=10, label='Bi-Encoder (Dense)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#F59E0B', markersize=10, label='Cross-Encoder (Context)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#8B5CF6', markersize=10, label='Two-Stage (Dense + CE)'),
        Line2D([0], [0], marker='none', color='w', label=''), # Spacer
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Paragraph Chunking', linestyle='None'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='black', markersize=8, label='Semantic Chunking', linestyle='None'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='black', markersize=8, label='Sliding Window Chunking', linestyle='None')
    ]
    plt.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.9)

    # Clean spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()
    else:
        plt.close()

def plot_category_breakdown(data_dir="nlp/data/evaluation_results", save_path=None, show=True):
    """
    Plots the performance (MRR) of all models across categories and chunking methods
    in a 2x2 subplot grid.
    
    Args:
        data_dir (str): Path to directory containing evaluation results.
        save_path (str, optional): Path to save the generated plot.
        show (bool): Whether to display the plot inline (useful in notebook).
    """
    methods = ["paragraph", "semantic", "sliding"]
    categories = ["Contextual Trap", "Exact Keyword", "Synonyms", "Typo Robustness"]
    models = ["BM25", "Bi-Encoder", "Cross-Encoder", "Two-Stage"]
    model_columns = {
        "BM25": "BM25 (Sparse)",
        "Bi-Encoder": "Bi-Encoder (Dense)",
        "Cross-Encoder": "Cross-Encoder (Context)",
        "Two-Stage": "Two-Stage (Dense + CE)"
    }
    
    cat_data = []

    for method in methods:
        file_path = os.path.join(data_dir, f"category_breakdown_{method}.csv")
        if os.path.exists(file_path):
            df_cat = pd.read_csv(file_path, header=[0, 1], index_col=0)
            df_cat = df_cat.dropna(how='all')
            df_cat = df_cat.drop('Category', errors='ignore')
            
            for cat in categories:
                if cat in df_cat.index:
                    for model_name, col_name in model_columns.items():
                        if ("MRR", col_name) in df_cat.columns:
                            mrr_val = df_cat.loc[cat, ("MRR", col_name)]
                            try:
                                mrr_val = float(mrr_val)
                            except:
                                mrr_val = np.nan
                            cat_data.append({
                                "Category": cat,
                                "Model": model_name,
                                "Chunking Method": method.capitalize(),
                                "MRR": mrr_val
                            })

    if not cat_data:
        print(f"No category breakdown data found in {data_dir}")
        return

    df_cat_all = pd.DataFrame(cat_data)
    
    # Setup a 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), sharey=True)
    axes = axes.flatten()
    
    chunk_methods = ["Paragraph", "Semantic", "Sliding"]
    model_colors = {
        "BM25": "#6B7280",          # Gray
        "Bi-Encoder": "#3B82F6",    # Blue
        "Cross-Encoder": "#F59E0B", # Orange
        "Two-Stage": "#8B5CF6"      # Purple
    }
    
    x = np.arange(len(chunk_methods))
    width = 0.18
    
    for ax_idx, cat in enumerate(categories):
        ax = axes[ax_idx]
        cat_df = df_cat_all[df_cat_all["Category"] == cat]
        
        for m_idx, model in enumerate(models):
            model_subset = cat_df[cat_df["Model"] == model]
            model_subset = model_subset.set_index("Chunking Method").reindex(chunk_methods).reset_index()
            mrr_vals = model_subset["MRR"].fillna(0).tolist()
            
            pos = x + (m_idx - 1.5) * width
            
            bars = ax.bar(
                pos, 
                mrr_vals, 
                width, 
                label=model if ax_idx == 0 else "", 
                color=model_colors[model], 
                alpha=0.9, 
                edgecolor="grey", 
                linewidth=0.5
            )
            
            for bar in bars:
                h = bar.get_height()
                if h > 0:
                    ax.text(
                        bar.get_x() + bar.get_width()/2.0, 
                        h + 0.01, 
                        f"{h:.2f}", 
                        ha='center', 
                        va='bottom', 
                        fontsize=8, 
                        fontweight='semibold'
                    )
                    
        ax.set_title(f"Category: {cat}", fontsize=12, fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(chunk_methods, fontsize=10)
        ax.set_ylabel("MRR Score", fontsize=10)
        ax.set_ylim(0, 1.1)
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cccccc')
        ax.spines['bottom'].set_color('#cccccc')
        
    fig.suptitle("Retrieval Performance (MRR) by Category, Model & Chunking Method", fontsize=16, fontweight='bold', y=0.97)
    fig.legend(title="Model", loc='lower center', bbox_to_anchor=(0.5, 0.01), ncol=4, fontsize=11, title_fontsize=12)
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.94])
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()
    else:
        plt.close()

def generate_all_plots(data_dir="nlp/data/evaluation_results", output_dir="nlp/data/evaluation_results/plots", copy_to_artifacts=True):
    """
    Generates and saves all three evaluation plots, and optionally copies them to the artifact folder.
    
    Args:
        data_dir (str): Directory containing the CSV result files.
        output_dir (str): Directory where the generated plots will be saved.
        copy_to_artifacts (bool): Whether to copy the plots to the project's artifact directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    df_overall = load_overall_summaries(data_dir)
    
    plot_1 = os.path.join(output_dir, "overall_quality_comparison.png")
    plot_2 = os.path.join(output_dir, "latency_vs_quality_tradeoff.png")
    plot_3 = os.path.join(output_dir, "category_breakdown_comparison.png")
    
    print("Generating overall quality comparison plot...")
    plot_overall_quality(df_overall, save_path=plot_1, show=False)
    
    print("Generating latency vs quality trade-off plot...")
    plot_latency_vs_quality(df_overall, save_path=plot_2, show=False)
    
    print("Generating category breakdown plot...")
    plot_category_breakdown(data_dir, save_path=plot_3, show=False)
    
    print(f"All plots saved to {output_dir}")
    
    if copy_to_artifacts:
        artifact_dir = r"C:\Users\thanh\.gemini\antigravity-ide\brain\a087aeb0-eb06-4801-b545-d20cc4c9d429"
        if os.path.exists(artifact_dir):
            shutil.copy(plot_1, os.path.join(artifact_dir, "overall_quality_comparison.png"))
            shutil.copy(plot_2, os.path.join(artifact_dir, "latency_vs_quality_tradeoff.png"))
            shutil.copy(plot_3, os.path.join(artifact_dir, "category_breakdown_comparison.png"))
            print(f"Successfully copied plots to artifact directory: {artifact_dir}")
        else:
            print(f"Artifact directory {artifact_dir} does not exist. Skipping copy.")

def display_overall_summary(data_dir="nlp/data/evaluation_results"):
    """
    Loads, formats, and styles the overall summary of all models
    to match the desired visual style exactly.
    """
    methods = ["paragraph", "semantic", "sliding"]
    method_labels = {
        "paragraph": "Paragraph Chunking",
        "semantic": "Semantic Chunking",
        "sliding": "Sliding Window"
    }
    
    dfs = []
    for method in methods:
        file_path = os.path.join(data_dir, f"overall_summary_{method}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["Phương pháp Chunking"] = method_labels[method]
            dfs.append(df)
            
    if not dfs:
        raise FileNotFoundError(f"No overall summary CSV files found in {data_dir}")
        
    df_all = pd.concat(dfs, ignore_index=True)
    
    # Rename columns to match the Vietnamese headers
    df_all = df_all.rename(columns={
        "Model": "Mô hình (Retriever)",
        "Average Latency (ms)": "Latency trung bình (ms)",
        "Mean Reciprocal Rank (MRR)": "Mean Reciprocal Rank (MRR)",
        "Accuracy@1 (Hit Rate)": "Accuracy@1 (Hit Rate)"
    })
    
    # Define exact columns order
    cols = [
        "Phương pháp Chunking", 
        "Mô hình (Retriever)", 
        "Latency trung bình (ms)", 
        "Mean Reciprocal Rank (MRR)", 
        "Accuracy@1 (Hit Rate)"
    ]
    df_all = df_all[cols]
    
    # Ensure correct sorting order for chunking methods and model types
    method_order = {"Paragraph Chunking": 0, "Semantic Chunking": 1, "Sliding Window": 2}
    model_order = {
        "BM25 (Sparse)": 0,
        "Bi-Encoder (Dense)": 1,
        "Cross-Encoder (Context)": 2,
        "Two-Stage (Dense + CE)": 3
    }
    
    df_all["_c_order"] = df_all["Phương pháp Chunking"].map(method_order)
    df_all["_m_order"] = df_all["Mô hình (Retriever)"].map(model_order)
    df_all = df_all.sort_values(by=["_c_order", "_m_order"]).drop(columns=["_c_order", "_m_order"]).reset_index(drop=True)
    
    # Create copy for display/formatting
    df_disp = df_all.copy()
    
    # Format columns exactly as shown in the template
    df_disp["Latency trung bình (ms)"] = df_disp["Latency trung bình (ms)"].map(lambda x: f"{x:.2f} ms")
    df_disp["Mean Reciprocal Rank (MRR)"] = df_disp["Mean Reciprocal Rank (MRR)"].map(lambda x: f"{x:.3f}")
    df_disp["Accuracy@1 (Hit Rate)"] = df_disp["Accuracy@1 (Hit Rate)"].map(lambda x: f"{x:.3f} ({x:.1%})")
    
    # Set MultiIndex to merge duplicate chunking method labels visually
    df_disp = df_disp.set_index(["Phương pháp Chunking", "Mô hình (Retriever)"])
    
    # Style styling (bolding the Two-Stage rows)
    def highlight_rows(row):
        model = row.name[1]
        if "Two-Stage" in model:
            return ["font-weight: bold;"] * len(row)
        return [""] * len(row)
        
    styled = df_disp.style.apply(highlight_rows, axis=1)
    
    # Bold the index labels for Two-Stage as well
    def highlight_index(idx_val):
        styles = []
        for val in idx_val:
            if "Two-Stage" in str(val):
                styles.append("font-weight: bold;")
            else:
                styles.append("")
        return styles

    try:
        styled = styled.apply_index(highlight_index, axis=0, level=1)
    except:
        pass  # Fail-safe for older pandas versions without apply_index
        
    # Apply table CSS styling for neat borders and alignment
    styled = styled.set_table_styles([
        {"selector": "th", "props": [("font-weight", "bold"), ("text-align", "left"), ("padding", "10px"), ("border-bottom", "1px solid #555")]},
        {"selector": "td", "props": [("padding", "8px 10px"), ("text-align", "left"), ("border-bottom", "1px solid #333")]},
    ])
    
    # try:
    #     from IPython.display import display
    #     display(styled)
    # except ImportError:
    #     print("\n=== OVERALL RETRIEVAL PERFORMANCE SUMMARY ===")
    #     print(df_disp.to_string())
        
    return styled

if __name__ == "__main__":
    generate_all_plots()
