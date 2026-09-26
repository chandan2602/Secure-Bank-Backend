from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path = './chroma_db')

collection = client.get_or_create_collection("Database_Knowledge")

def retrive_data(question :str, top_k : int = 3):
    question_emb = model.encode(question).tolist()
    
    result = collection.query(query_embeddings=[question_emb], n_results= top_k)
    
    docs = result['documents'][0]       # taking the top  record out of the three document retrived
    
    context = "/n/n".join(docs)
    
    return context
    