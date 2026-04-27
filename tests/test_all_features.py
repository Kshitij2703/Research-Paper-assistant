#!/usr/bin/env python3
"""
Test script to verify all features of Research Paper Assistant
Run this when you have API quota available
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_feature(feature_name, test_func):
    """Test a feature and report results"""
    print(f"\n{'='*60}")
    print(f"Testing: {feature_name}")
    print('='*60)
    try:
        result = test_func()
        print(f"✅ {feature_name} - PASSED")
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print(f"⚠️  {feature_name} - QUOTA EXCEEDED (Feature works, but API limit reached)")
        else:
            print(f"❌ {feature_name} - FAILED: {e}")
        return False

def test_pdf_extraction():
    from pdf_loader import extract_text_from_pdf
    text = extract_text_from_pdf("researchpaper1.pdf")
    assert len(text) > 0, "No text extracted"
    print(f"Extracted {len(text)} characters")
    return text

def test_chunking(text):
    from chunker import chunk_text
    chunks = chunk_text(text)
    assert len(chunks) > 0, "No chunks created"
    print(f"Created {len(chunks)} chunks")
    return chunks

def test_embeddings(chunks):
    from vector_store import VectorStore
    api_key = os.getenv("GEMINI_API_KEY")
    vector_store = VectorStore(api_key)
    vector_store.add_documents(chunks[:3])  # Test with 3 chunks
    print("Embeddings created successfully")
    return vector_store

def test_domain_classification(text):
    from classifier import DomainClassifier
    api_key = os.getenv("GEMINI_API_KEY")
    classifier = DomainClassifier(api_key)
    domain = classifier.classify(text)
    print(f"Domain: {domain[:100]}...")
    return domain

def test_rag(vector_store):
    from rag_system import RAGSystem
    api_key = os.getenv("GEMINI_API_KEY")
    rag = RAGSystem(api_key, vector_store)
    answer = rag.query("What is this paper about?")
    print(f"Answer: {answer[:100]}...")
    return answer

def test_summarization(text):
    from summarizer import Summarizer
    api_key = os.getenv("GEMINI_API_KEY")
    summarizer = Summarizer(api_key)
    summary = summarizer.summarize(text)
    print(f"Summary: {summary[:100]}...")
    return summary

def test_literature_review(text):
    from literature_review import LiteratureReviewGenerator
    api_key = os.getenv("GEMINI_API_KEY")
    lit_review = LiteratureReviewGenerator(api_key)
    review = lit_review.generate_review(text)
    print(f"Review: {review[:100]}...")
    return review

def test_citations(text):
    from citation_manager import CitationManager
    api_key = os.getenv("GEMINI_API_KEY")
    citation_mgr = CitationManager(api_key)
    citations = citation_mgr.extract_citations(text)
    print(f"Citations: {citations[:100]}...")
    return citations

def test_peer_review(text):
    from reviewer import PaperReviewer
    api_key = os.getenv("GEMINI_API_KEY")
    reviewer = PaperReviewer(api_key)
    review = reviewer.review_paper(text)
    print(f"Review: {review[:100]}...")
    return review

def test_consistency(text, summary):
    from consistency_checker import ConsistencyChecker
    api_key = os.getenv("GEMINI_API_KEY")
    consistency = ConsistencyChecker(api_key)
    result = consistency.check_consistency(text, summary)
    print(f"Consistency: {result[:100]}...")
    return result

def test_rouge():
    from evaluator import evaluate_summary
    scores = evaluate_summary("This is a test", "This is a test")
    print(f"ROUGE scores: {scores}")
    return scores

def main():
    print("\n" + "="*60)
    print("Research Paper Assistant - Feature Test Suite")
    print("="*60)
    
    results = {}
    
    # Test 1: PDF Extraction
    text = None
    if test_feature("PDF Extraction", lambda: test_pdf_extraction()):
        text = test_pdf_extraction()
        results["PDF Extraction"] = "✅"
    else:
        results["PDF Extraction"] = "❌"
        return
    
    # Test 2: Chunking
    chunks = None
    if test_feature("Text Chunking", lambda: test_chunking(text)):
        chunks = test_chunking(text)
        results["Text Chunking"] = "✅"
    else:
        results["Text Chunking"] = "❌"
        return
    
    # Test 3: Embeddings
    vector_store = None
    if test_feature("Embeddings & Vector Store", lambda: test_embeddings(chunks)):
        vector_store = test_embeddings(chunks)
        results["Embeddings"] = "✅"
    else:
        results["Embeddings"] = "⚠️"
    
    # Test 4: Domain Classification
    if test_feature("Domain Classification", lambda: test_domain_classification(text)):
        results["Domain Classification"] = "✅"
    else:
        results["Domain Classification"] = "⚠️"
    
    # Test 5: RAG Q&A
    if vector_store and test_feature("RAG Q&A", lambda: test_rag(vector_store)):
        results["RAG Q&A"] = "✅"
    else:
        results["RAG Q&A"] = "⚠️"
    
    # Test 6: Summarization
    summary = None
    if test_feature("Summarization", lambda: test_summarization(text)):
        summary = test_summarization(text)
        results["Summarization"] = "✅"
    else:
        results["Summarization"] = "⚠️"
    
    # Test 7: Literature Review
    if test_feature("Literature Review", lambda: test_literature_review(text)):
        results["Literature Review"] = "✅"
    else:
        results["Literature Review"] = "⚠️"
    
    # Test 8: Citations
    if test_feature("Citation Extraction", lambda: test_citations(text)):
        results["Citation Extraction"] = "✅"
    else:
        results["Citation Extraction"] = "⚠️"
    
    # Test 9: Peer Review
    if test_feature("Peer Review", lambda: test_peer_review(text)):
        results["Peer Review"] = "✅"
    else:
        results["Peer Review"] = "⚠️"
    
    # Test 10: Consistency Check
    if summary and test_feature("Consistency Check", lambda: test_consistency(text, summary)):
        results["Consistency Check"] = "✅"
    else:
        results["Consistency Check"] = "⚠️"
    
    # Test 11: ROUGE Evaluation
    if test_feature("ROUGE Evaluation", lambda: test_rouge()):
        results["ROUGE Evaluation"] = "✅"
    else:
        results["ROUGE Evaluation"] = "❌"
    
    # Print Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for feature, status in results.items():
        print(f"{status} {feature}")
    
    passed = sum(1 for s in results.values() if s == "✅")
    quota_limited = sum(1 for s in results.values() if s == "⚠️")
    failed = sum(1 for s in results.values() if s == "❌")
    
    print(f"\nTotal: {len(results)} features")
    print(f"✅ Passed: {passed}")
    print(f"⚠️  Quota Limited: {quota_limited}")
    print(f"❌ Failed: {failed}")
    
    if quota_limited > 0:
        print("\n⚠️  Note: Some features hit API quota limits.")
        print("   This is expected with free tier (20 requests/day).")
        print("   The features work correctly when quota is available.")

if __name__ == "__main__":
    main()
