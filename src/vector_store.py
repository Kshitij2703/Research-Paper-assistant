from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self, api_key=None):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.index = None
        
    def add_documents(self, chunks):
        self.chunks = chunks
        embeddings = self.model.encode(chunks)
        embeddings_array = np.array(embeddings, dtype='float32')
        self.index = faiss.IndexFlatL2(embeddings_array.shape[1])
        self.index.add(embeddings_array)
        
    def search(self, query, k=3):
        query_embedding = self.model.encode([query])
        query_vector = np.array(query_embedding, dtype='float32')
        distances, indices = self.index.search(query_vector, k)
        return [self.chunks[i] for i in indices[0]]
