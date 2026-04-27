from groq import Groq

class AbstractSimplifier:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def simplify_abstract(self, text):
        """Simplify abstract for non-expert audience"""
        prompt = f"""Simplify this research paper abstract for a general audience (high school level).

Rules:
- Use simple, everyday language
- Avoid jargon and technical terms
- Explain concepts in plain English
- Keep it concise (3-5 sentences)
- Make it engaging and accessible

Paper text (first part):
{text[:5000]}

Write a simplified abstract:"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
