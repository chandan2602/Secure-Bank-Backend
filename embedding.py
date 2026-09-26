from sentence_transformers import SentenceTransformer
import chromadb
from knowledgebase import documents

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient('./chroma_db')

collection = client.get_or_create_collection(name='Database_Knowledge')

for i,d in enumerate(documents):
    model_embbeding = model.encode(d).tolist()
    collection.upsert(ids= f"documents_{i}",
                      documents=[d],
                      embeddings=[model_embbeding],
                      metadatas= [{
                          "sourse" : f"documents_{i}",
                          "type" : "Database_Schema"
                      }])
    
    
print(f"documents embedded sucessfully : {len(documents)}")
    
