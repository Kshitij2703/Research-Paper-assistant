from groq import Groq

class RAGSystem:
    def __init__(self, api_key, vector_store):
        self.client = Groq(api_key=api_key)
        self.vector_store = vector_store
        
    def query(self, question):
        relevant_chunks = self.vector_store.search(question, k=3)
        context = "\n\n".join(relevant_chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer based on the context:"
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
