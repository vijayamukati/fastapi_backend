from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load a pre-trained SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(content: str):
    return model.encode(content, convert_to_tensor=True)

def find_relevant_content(content: str, question: str) -> str:
    content_embeddings = generate_embeddings(content)
    question_embedding = generate_embeddings(question)

    # Compute cosine similarity
    similarity = cosine_similarity([question_embedding], [content_embeddings])
    
    # Return the response with the highest similarity
    if similarity[0][0] > 0.5:  # Example threshold
        return content
    else:
        return "Sorry, I couldn't find relevant information."

