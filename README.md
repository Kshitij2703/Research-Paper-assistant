# Research Paper Assistant - Complete Pipeline

A comprehensive NLP/LLM system for research paper analysis with full pipeline capabilities.

## Features

### Core Features
- **PDF Processing**: Extract text from research papers using PyMuPDF
- **Text Chunking**: Split documents into ~500 word segments with overlap
- **Vector Embeddings**: Use SentenceTransformer (all-MiniLM-L6-v2) for local embeddings
- **Semantic Search**: FAISS vector database for efficient retrieval
- **RAG Q&A**: Context-aware answers using Llama 3.3 70B via Groq

### Advanced Features
- **Domain Classification**: Automatically classify papers into research domains (AI, Biology, Physics, etc.)
- **Literature Review Generation**: Generate comprehensive literature reviews from multiple papers
- **Citation Management**: Extract citations, generate formatted citations (APA, MLA, etc.), create bibliographies
- **Peer Review Agent**: Automated paper review with scoring and detailed feedback
- **Factual Consistency Checking**: Verify generated content against source material
- **arXiv Integration**: Search and retrieve papers from arXiv database
- **Summarization**: Generate concise paper summaries
- **Evaluation**: ROUGE metrics for quality assessment

## Quick Start

### 1. Setup
```bash
./setup.sh
source venv/bin/activate
```

### 2. Configure API Key
Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```
Get your free API key: https://console.groq.com/keys

### 3. Run

**Web UI (Recommended):**
```bash
python server.py
# Open http://localhost:8080
```

**CLI:**
```bash
python src/main.py
```

## Usage

### Web UI
1. Start the server: `python server.py`
2. Open http://localhost:8080 in your browser
3. Upload a PDF using drag & drop or file picker
4. Choose from 7 analysis features:
   - **Ask Questions** - Interactive Q&A with conversation history
   - **Domain Classification** - Identify research domain
   - **Summarization** - Generate concise summaries
   - **Literature Review** - Comprehensive review generation
   - **Citation Extraction** - Extract and format citations
   - **Peer Review** - Automated review with scoring
   - **Consistency Check** - Verify factual accuracy

### CLI
Simply run the application and provide a PDF path:

```bash
python src/main.py
```

## Project Structure

```
.
├── server.py                    # HTTP backend (Python built-in server)
├── static/
│   └── index.html              # Web UI (HTML/CSS/JS)
├── src/
│   ├── main.py                 # CLI application
│   ├── pdf_loader.py           # PDF text extraction
│   ├── chunker.py              # Text chunking
│   ├── vector_store.py         # FAISS + embeddings
│   ├── rag_system.py           # RAG query pipeline
│   ├── summarizer.py           # Summarization
│   ├── classifier.py           # Domain classification
│   ├── literature_review.py    # Literature review generation
│   ├── citation_manager.py     # Citation extraction/generation
│   ├── reviewer.py             # Peer review agent
│   ├── consistency_checker.py  # Factual consistency checking
│   ├── arxiv_integration.py    # arXiv API integration
│   └── evaluator.py            # ROUGE metrics
├── data/                       # Sample PDFs (gitignored)
├── docs/                       # Documentation and reports
├── tests/                      # Test scripts
├── requirements.txt            # Dependencies
└── .env                        # API key
```

## Requirements

- Python 3.8+
- Groq API key (free tier available)

## License

MIT
