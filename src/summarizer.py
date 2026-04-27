from groq import Groq

class Summarizer:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def summarize(self, text, max_length=500):
        prompt = f"Summarize the following research paper in {max_length} words or less:\n\n{text[:15000]}"
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
