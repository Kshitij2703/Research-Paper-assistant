from groq import Groq

class DomainClassifier:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def classify(self, text):
        prompt = f"""Classify this research paper into ONE primary domain and list 2-3 sub-domains.

Domains: AI/ML, Computer Science, Biology, Physics, Chemistry, Medicine, Mathematics, Engineering, Social Sciences, Other

Text: {text[:3000]}

Return in format:
Primary Domain: [domain]
Sub-domains: [sub1, sub2, sub3]
Confidence: [High/Medium/Low]"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
