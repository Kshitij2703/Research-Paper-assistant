from groq import Groq

class PaperReviewer:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def review_paper(self, text):
        prompt = f"""Provide a comprehensive peer review of this research paper.

Evaluate:
1. Novelty and Significance (1-5)
2. Technical Quality (1-5)
3. Clarity and Presentation (1-5)
4. Experimental Validation (1-5)

Provide:
- Summary
- Strengths (3-5 points)
- Weaknesses (3-5 points)
- Detailed Comments
- Questions for Authors
- Recommendation (Accept/Minor Revision/Major Revision/Reject)

Paper:
{text[:12000]}

Review:"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def check_methodology(self, text):
        prompt = f"""Analyze the methodology of this paper. Identify:
1. Research methods used
2. Strengths of the approach
3. Potential limitations
4. Suggestions for improvement

Paper: {text[:8000]}"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
