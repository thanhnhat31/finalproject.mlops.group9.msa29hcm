import os
import pypdf
import nltk
from nltk.tokenize import sent_tokenize

def extract_text_from_pdf(pdf_path):
    """
    Read and extract content from a PDF file.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
        
    reader = pypdf.PdfReader(pdf_path)
    full_text = []
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Remove leading and trailing spaces from the page text
            full_text.append(text.strip())
            
    # Join the text of all pages with double newlines
    return "\n\n".join(full_text)

def sliding_window_chunking(text, chunk_size=150, chunk_overlap=30):
    """
    Divide text into chunks using the sliding window method based on word count.
    
    Args:
        text (str): Raw input text.
        chunk_size (int): Maximum number of words in each chunk.
        chunk_overlap (int): Number of overlapping words between adjacent chunks.
        
    Returns:
        list of str: List of text chunks after chunking.
    """
    # Split text into a list of words
    words = text.split()
    chunks = []
    
    # Stride of the sliding window
    stride = chunk_size - chunk_overlap
    if stride <= 0:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
        
    for i in range(0, len(words), stride):
        # Get the chunk of words from position i to i + chunk_size
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        
        # Stop the loop if we have reached the end of the text
        if i + chunk_size >= len(words):
            break
            
    return chunks

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def semantic_chunking_by_sentence(text, target_word_count=150, overlap_sentences=1):
    """
    Split text into chunks based on sentence boundaries, 
    ensuring the length of each chunk is approximately target_word_count.
    
    Args:
        text (str): Raw input text.
        target_word_count (int): Target word count (estimated) for each chunk.
        overlap_sentences (int): Number of overlapping sentences between chunks.
        
    Returns:
        list of str: List of semantically complete chunks.
    """
    if not text or not text.strip():
        return []

    # 1. Split text into complete sentences
    sentences = sent_tokenize(text)
    
    chunks = []
    current_chunk_sentences = []
    current_word_count = 0
    
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        sentence_word_count = len(sentence.split())
        
        # Add current sentence to the accumulating chunk
        current_chunk_sentences.append(sentence)
        current_word_count += sentence_word_count
        
        # Check if the chunk has reached the target word count
        # Or force close the chunk if this is the last sentence in the text
        if current_word_count >= target_word_count or i == len(sentences) - 1:
            # Join sentences into a text chunk
            chunk_text = " ".join(current_chunk_sentences)
            chunks.append(chunk_text)
            
            # Prepare for the next chunk (handle sliding window overlap)
            if overlap_sentences > 0 and i < len(sentences) - 1:
                # Keep 'overlap_sentences' last sentences of the current chunk
                current_chunk_sentences = current_chunk_sentences[-overlap_sentences:]
                # Recalculate word count of the overlap part to add to the next chunk
                current_word_count = sum(len(s.split()) for s in current_chunk_sentences)
            else:
                current_chunk_sentences = []
                current_word_count = 0
                
        i += 1
        
    return chunks

def save_chunks_to_json(chunks, output_path, metadata=None):
    """
    Saves a list of text chunks to a JSON file, optionally adding metadata.
    
    Args:
        chunks (list of str): The text chunks to save.
        output_path (str): The path to the output JSON file.
        metadata (dict, optional): Additional metadata (e.g., source file name).
    """
    import json
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    data = {
        "metadata": metadata or {},
        "total_chunks": len(chunks),
        "chunks": [
            {
                "index": idx,
                "word_count": len(chunk.split()),
                "text": chunk
            }
            for idx, chunk in enumerate(chunks)
        ]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Successfully saved {len(chunks)} chunks to {output_path}")

def load_chunks_from_json(json_path):
    """
    Loads text chunks and metadata from a JSON file.
    
    Args:
        json_path (str): Path to the JSON file.
        
    Returns:
        tuple: (list of str, dict) -> (chunks, metadata)
    """
    import json
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chunks = [chunk_item["text"] for chunk_item in data["chunks"]]
    return chunks, data.get("metadata", {})

def two_stage_retrieval(query, corpus, stage1_retriever, stage2_model, stage1_top_k=10, stage2_top_k=3):
    """
    Two-Stage Retrieval Pipeline:
    - Stage 1: Fast retrieval (BM25 or Bi-Encoder) to get 'stage1_top_k' candidates.
    - Stage 2: Cross-Encoder to re-rank the candidates and return top 'stage2_top_k' results.
    
    Args:
        query (str): The search query.
        corpus (list of str): The entire corpus of text chunks.
        stage1_retriever: An instance of CustomBM25 or DenseRetriever.
        stage2_model: An initialized CrossEncoder model.
        stage1_top_k (int): Number of candidates to retrieve in Stage 1.
        stage2_top_k (int): Final number of results to return after re-ranking.
        
    Returns:
        tuple: (list of dict, dict) -> (reranked_results, latency_breakdown)
    """
    import time
    
    # --- STAGE 1: Fast Retrieval ---
    start_stage1 = time.time()
    candidates, stage1_time = stage1_retriever.retrieve(query, corpus, top_k=stage1_top_k)
    
    if not candidates:
        return [], {"stage1_seconds": stage1_time, "stage2_seconds": 0.0, "total_seconds": stage1_time}
        
    # --- STAGE 2: Cross-Encoder Re-ranking ---
    start_stage2 = time.time()
    
    # Format query-chunk pairs only for the retrieved candidates
    pairs = [[query, item["chunk_text"]] for item in candidates]
    
    # Run the Cross-Encoder model on the subset of candidates
    scores = stage2_model.predict(pairs)
    
    # Combine scores with original chunk index and text
    reranked_results = []
    for idx, (candidate, score) in enumerate(zip(candidates, scores)):
        reranked_results.append({
            "chunk_index": candidate["chunk_index"],
            "chunk_text": candidate["chunk_text"],
            "stage1_score": candidate["score"],
            "score": float(score)  # Re-ranked score
        })
        
    # Sort by the new Cross-Encoder score in descending order
    reranked_results = sorted(reranked_results, key=lambda x: x["score"], reverse=True)
    
    stage2_time = time.time() - start_stage2
    total_time = stage1_time + stage2_time
    
    latency_breakdown = {
        "stage1_seconds": stage1_time,
        "stage2_seconds": stage2_time,
        "total_seconds": total_time
    }
    
    return reranked_results[:stage2_top_k], latency_breakdown