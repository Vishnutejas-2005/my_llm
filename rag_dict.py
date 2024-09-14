from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import numpy as np

class RAGDict:
    def __init__(self, data):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.sentence_transformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.data = data

    def __getitem__(self, key):
        query_embedding = self.sentence_transformer.encode(key)
        results = []
        for aliases, value in self.data.items():
            alias_embeddings = self.sentence_transformer.encode(aliases)
            max_similarity = np.max(np.dot(query_embedding, alias_embeddings.T))
            results.append((max_similarity, value))
        sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
        return [value for similarity, value in sorted_results]
    
# d = RAGDict(
#     {
#     ("car", "vehicle"): "Maruti",
#     ("scooter", "two wheeler"): "Bajaj"
#     }
# )

# print(d["scooty"])  # Should print ["Bajaj", "Maruti"]
# print(d["automobile"])  # Should print ["Maruti", "Bajaj"]
# d = RAGDict(
#     {
#         ("guitar", "stringed instrument"): "Acoustic Guitar",
#         ("piano", "keyboard instrument"): "Grand Piano",
#         ("drums", "percussion instrument"): "Drum Set"
#     }
# )

# print(d["six-stringed instrument"])  # Expected output: ["Acoustic Guitar"]
# print(d["keyboards"])  # Expected output: ["Grand Piano"]
# print(d["percussion"])  # Expected output: ["Drum Set"]
# d = RAGDict(
d = RAGDict(
    {
        ("apple", "fruit"): "Red Delicious",
        ("banana", "fruit"): "Yellow Banana",
        ("orange", "fruit"): "Navel Orange"
    }
)

print(d["red fruit"])  # Expected output: ["Red Delicious"]
print(d["yellow fruit"])  # Expected output: ["Yellow Banana"]
print(d["citrus fruit"])  # Expected output: ["Navel Orange"]