import os, sys, json, tempfile, traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from dotenv import load_dotenv
load_dotenv()

from pdf_loader import extract_text_from_pdf
from chunker import chunk_text
from vector_store import VectorStore
from rag_system import RAGSystem
from summarizer import Summarizer
from classifier import DomainClassifier
from literature_review import LiteratureReviewGenerator
from citation_manager import CitationManager
from reviewer import PaperReviewer
from consistency_checker import ConsistencyChecker
from arxiv_integration import ArxivIntegration
from abstract_simplifier import AbstractSimplifier

API_KEY = os.getenv("GROQ_API_KEY")
session = {}
conversation_history = []
arxiv = ArxivIntegration()

def init_session(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    vs = VectorStore()
    vs.add_documents(chunks)
    session.update({
        "text": text,
        "rag": RAGSystem(API_KEY, vs),
        "summarizer": Summarizer(API_KEY),
        "lit_review": LiteratureReviewGenerator(API_KEY),
        "citations": CitationManager(API_KEY),
        "reviewer": PaperReviewer(API_KEY),
        "consistency": ConsistencyChecker(API_KEY),
        "classifier": DomainClassifier(API_KEY),
        "simplifier": AbstractSimplifier(API_KEY),
    })
    return len(chunks)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if urlparse(self.path).path in ("/", "/index.html"):
            fp = os.path.join(os.path.dirname(__file__), "static", "index.html")
            body = open(fp, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            if path == "/upload":
                self._upload(body)
            elif path == "/action":
                self._action(json.loads(body))
            elif path == "/stream":
                self._stream(json.loads(body))
            elif path == "/export":
                self._export(json.loads(body))
            elif path == "/history/save":
                self._save_history()
            elif path == "/history/load":
                self._load_history()
            elif path == "/arxiv/search":
                self._arxiv_search(json.loads(body))
            elif path == "/arxiv/download":
                self._arxiv_download(json.loads(body))
            else:
                self.send_json({"error": "not found"}, 404)
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def _upload(self, body):
        ct = self.headers.get("Content-Type", "")
        boundary = ct.split("boundary=")[-1].encode()
        for part in body.split(b"--" + boundary):
            if b"filename=" in part:
                pdf_bytes = part.split(b"\r\n\r\n", 1)[1].rstrip(b"\r\n--")
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                    f.write(pdf_bytes); tmp = f.name
                try:
                    n = init_session(tmp)
                    self.send_json({"status": "ok", "chunks": n, "preview": session["text"][:400]})
                finally:
                    os.unlink(tmp)
                return
        self.send_json({"error": "No PDF found"}, 400)

    def _action(self, data):
        if not session:
            self.send_json({"error": "Upload a PDF first."}, 400); return
        action = data.get("action")
        text = session["text"]
        if action == "classify":
            r = session["classifier"].classify(text)
        elif action == "summarize":
            r = session["summarizer"].summarize(text)
        elif action == "simplify":
            r = session["simplifier"].simplify_abstract(text)
        elif action == "literature_review":
            r = session["lit_review"].generate_review(text)
        elif action == "citations":
            r = session["citations"].extract_citations(text)
        elif action == "peer_review":
            r = session["reviewer"].review_paper(text)
        elif action == "consistency":
            s = session["summarizer"].summarize(text)
            r = session["consistency"].check_consistency(text, s)
        elif action == "evaluate":
            from rouge_score import rouge_scorer
            s = session["summarizer"].summarize(text)
            # Generate reference summary from first 3000 chars
            ref_summary = text[:3000]
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
            scores = scorer.score(ref_summary, s)
            r = f"""ROUGE Evaluation Metrics:

ROUGE-1 (Unigram Overlap):
  Precision: {scores['rouge1'].precision:.3f}
  Recall: {scores['rouge1'].recall:.3f}
  F1-Score: {scores['rouge1'].fmeasure:.3f}

ROUGE-2 (Bigram Overlap):
  Precision: {scores['rouge2'].precision:.3f}
  Recall: {scores['rouge2'].recall:.3f}
  F1-Score: {scores['rouge2'].fmeasure:.3f}

ROUGE-L (Longest Common Subsequence):
  Precision: {scores['rougeL'].precision:.3f}
  Recall: {scores['rougeL'].recall:.3f}
  F1-Score: {scores['rougeL'].fmeasure:.3f}

Interpretation:
- Precision: How much of the summary is relevant
- Recall: How much of the reference is covered
- F1-Score: Harmonic mean of precision and recall
- Higher scores (closer to 1.0) indicate better quality"""
        elif action == "insights":
            r = self._extract_insights(text)
        elif action == "custom_prompt":
            prompt = data.get("prompt", "").strip()
            if not prompt: self.send_json({"error": "No prompt provided"}); return
            r = self._run_custom_prompt(text, prompt)
        elif action == "ask":
            q = data.get("question", "").strip()
            if not q: self.send_json({"error": "No question"}); return
            r = session["rag"].query(q)
            conversation_history.append({"role": "user", "content": q})
            conversation_history.append({"role": "assistant", "content": r})
        else:
            self.send_json({"error": f"Unknown action: {action}"}); return
        self.send_json({"result": r})

    def _stream(self, data):
        if not session:
            self.send_json({"error": "Upload a PDF first."}, 400); return
        action = data.get("action")
        q = data.get("question", "").strip()
        if action == "ask" and q:
            relevant = session["rag"].vector_store.search(q, k=3)
            context = "\n\n".join(relevant)
            prompt = f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer based on the context:"
            
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                stream = session["rag"].client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                full_response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        token = chunk.choices[0].delta.content
                        full_response += token
                        self.wfile.write(f"data: {json.dumps({'token': token})}\n\n".encode())
                        self.wfile.flush()
                self.wfile.write(b"data: [DONE]\n\n")
                conversation_history.append({"role": "user", "content": q})
                conversation_history.append({"role": "assistant", "content": full_response})
            except:
                self.wfile.write(b"data: [ERROR]\n\n")
        else:
            self.send_json({"error": "Invalid stream request"}, 400)

    def _extract_insights(self, text):
        prompt = f"""Extract key insights from this research paper in bullet points:

1. Main Contribution (1-2 sentences)
2. Novel Approach (1-2 sentences)
3. Key Results (2-3 bullet points)
4. Limitations (1-2 points)
5. Future Work (1-2 points)

Paper: {text[:10000]}

Format as clear bullet points."""
        response = session["rag"].client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def _export(self, data):
        format_type = data.get("format", "txt")
        content = data.get("content", "")
        filename = data.get("filename", "export")
        
        if format_type == "md":
            body = content.encode()
            ct = "text/markdown"
            ext = ".md"
        else:
            body = content.encode()
            ct = "text/plain"
            ext = ".txt"
        
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Disposition", f'attachment; filename="{filename}{ext}"')
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _save_history(self):
        data = json.dumps(conversation_history, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Disposition", 'attachment; filename="conversation_history.json"')
        self.send_header("Content-Length", len(data))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _load_history(self):
        global conversation_history
        conversation_history = []
        self.send_json({"history": conversation_history})

    def _run_custom_prompt(self, text, prompt):
        full_prompt = f"{prompt}\n\nPaper text:\n{text[:12000]}"
        response = session["rag"].client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content

    def _arxiv_search(self, data):
        query = data.get("query", "")
        max_results = data.get("max_results", 10)
        papers = arxiv.search_papers(query, max_results)
        if isinstance(papers, str):
            self.send_json({"error": papers}, 500)
        else:
            self.send_json({"papers": papers})

    def _arxiv_download(self, data):
        import urllib.request
        url = data.get("url", "")
        if not url:
            self.send_json({"error": "No URL provided"}, 400)
            return
        try:
            with urllib.request.urlopen(url) as response:
                pdf_data = response.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", 'attachment; filename="paper.pdf"')
            self.send_header("Content-Length", len(pdf_data))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(pdf_data)
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

if __name__ == "__main__":
    port = 8080
    print(f"🚀  http://localhost:{port}")
    HTTPServer(("", port), Handler).serve_forever()
