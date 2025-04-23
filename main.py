import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from advanced_retrieval import retrieve_chunks,rerank_with_gpt
from generation import  generate_multiple_answers, compare_answers

# Example question
question = "How do commercial banks incorporate ESG factors into their credit analysis?"
print("actual question:", question)
# Retrieve chunks using advanced method
print("Retrieving relevant chunks...")
top_chunks = retrieve_chunks(question)

#Re-rank chunks with GPT for more relevance
print("Re-ranking chunks with GPT...")
reranked_chunks = rerank_with_gpt(question, top_chunks[:10])

#Generate final answer
print("Generating final answer...")
final_answer = generate_multiple_answers(question, reranked_chunks[:3])
evaluation = compare_answers(question, final_answer)

#Output
print("\n================== SOURCES ==================\n")
for i, chunk in enumerate(reranked_chunks[:3], 1):
    print(f"Chunk {i} from {chunk['source_file']}")
    print(chunk['text'][:300])
    print("---")
print("\n================== FINAL ANSWER ==================\n")
for i, ans in enumerate(final_answer, 1):
    print(f"Answer {i}:\n{ans}\n")
print("\nGPT Evaluation:\n", evaluation)
