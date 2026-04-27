from groq import Groq

class ConsistencyChecker:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def check_consistency(self, source_text, generated_text):
        prompt = f"""Check if the generated text is factually consistent with the source.

Source: {source_text[:5000]}

Generated: {generated_text[:2000]}

Analyze:
1. Factual accuracy (are facts correct?)
2. Hallucinations (any made-up information?)
3. Consistency score (0-100)
4. Issues found

Return structured analysis."""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def verify_claims(self, text, claims):
        prompt = f"""Verify if these claims are supported by the text:

Text: {text[:6000]}

Claims to verify:
{claims}

For each claim, state: Supported/Partially Supported/Not Supported"""
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
