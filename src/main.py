import os
from dotenv import load_dotenv
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

load_dotenv()

def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env file")
        return
    
    pdf_path = input("\n📄 Enter PDF path: ").strip()
    if not os.path.exists(pdf_path):
        print("Error: PDF file not found")
        return
    
    print("\n[1/5] Extracting text from PDF...")
    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        return
    
    print("[2/5] Classifying domain...")
    try:
        classifier = DomainClassifier(api_key)
        domain = classifier.classify(text)
        print(f"\n{domain}\n")
    except Exception as e:
        print(f"⚠️ Domain classification failed: {e}")
        print("Continuing without classification...\n")
    
    print("[3/5] Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    print("[4/5] Creating embeddings and vector store...")
    try:
        vector_store = VectorStore(api_key)
        vector_store.add_documents(chunks)
    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
        return
    
    print("[5/5] Initializing all systems...")
    rag = RAGSystem(api_key, vector_store)
    summarizer = Summarizer(api_key)
    lit_review = LiteratureReviewGenerator(api_key)
    citation_mgr = CitationManager(api_key)
    reviewer = PaperReviewer(api_key)
    consistency = ConsistencyChecker(api_key)
    
    print("\n✓ System ready!\n")
    
    while True:
        print("\n🔬 Research Paper Assistant - Features:")
        print("1. Ask a question (RAG)")
        print("2. Get summary")
        print("3. Generate literature review")
        print("4. Extract citations")
        print("5. Get peer review")
        print("6. Check consistency")
        print("7. Exit")
        
        choice = input("\nChoice: ").strip()
        
        try:
            if choice == "1":
                question = input("Question: ").strip()
                if question:
                    print("\nAnswer:", rag.query(question))
            
            elif choice == "2":
                print("\nGenerating summary...")
                print(summarizer.summarize(text))
            
            elif choice == "3":
                print("\nGenerating literature review...")
                print(lit_review.generate_review(text))
            
            elif choice == "4":
                print("\nExtracting citations...")
                print(citation_mgr.extract_citations(text))
            
            elif choice == "5":
                print("\nGenerating peer review...")
                print(reviewer.review_paper(text))
            
            elif choice == "6":
                summary = summarizer.summarize(text)
                print("\nChecking consistency...")
                print(consistency.check_consistency(text, summary))
            
            elif choice == "7":
                break
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print("\n❌ API Quota Exceeded!")
                print("You've reached the free tier limit (20 requests/day).")
                print("Please wait 24 hours or upgrade your API plan.")
                print("Visit: https://ai.google.dev/pricing")
            elif "404" in error_msg:
                print("\n❌ Model not found. Please check your API configuration.")
            else:
                print(f"\n❌ Error: {error_msg}")
            print("\nContinuing with other features...")

if __name__ == "__main__":
    main()
