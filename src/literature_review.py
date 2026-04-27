from groq import Groq

class LiteratureReviewGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def generate_review(self, papers_text):
        prompt = f"""Generate a comprehensive literature review from these research papers.

Include:
1. Overview of the research area
2. Key themes and trends
3. Major findings and contributions
4. Research gaps
5. Future directions

Papers:
{papers_text[:10000]}

Write a structured literature review:"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_comparative_analysis(self, papers_text):
        prompt = f"""Compare and contrast the methodologies, findings, and contributions of these papers.

Papers:
{papers_text[:8000]}

Provide a comparative analysis:"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
