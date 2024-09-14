from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from scipy.spatial.distance import cosine

class RAGDict:
    def __init__(self, data):
        tagged_data = [TaggedDocument(words=aliases, tags=[i]) for i, aliases in enumerate(data.keys())]
        self.doc2vec_model = Doc2Vec(tagged_data, vector_size=20, min_count=1, epochs=20)
        self.data = data

    def __getitem__(self, key):
        query_vector = self.doc2vec_model.infer_vector(key.split())
        results = []
        for aliases, value in self.data.items():
            alias_vectors = [self.doc2vec_model.infer_vector(alias.split()) for alias in aliases]
            max_similarity = max(1 - cosine(query_vector, alias_vector) for alias_vector in alias_vectors)
            results.append((max_similarity, value))
        sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
        return [value for similarity, value in sorted_results]
    

d = RAGDict(
    {
        ("dog", "canine"): "Golden Retriever",
        ("cat", "feline"): "Persian",
        ("bird", "avian"): "Parrot"
    }
)

print(d["puppy"])  # Expected output: ["Golden Retriever"]
print(d["kitty"])  # Expected output: ["Persian"]
print(d["feathery friend"])  # Expected output: ["Parrot"]