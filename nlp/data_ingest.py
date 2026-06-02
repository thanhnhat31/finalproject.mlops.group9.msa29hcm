import os
import pypdf

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

