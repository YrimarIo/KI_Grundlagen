#!/usr/bin/env python3
"""
Demo: Vector embeddings and simple analogy solving.
Loads a small word-vector dictionary from word_vectors.json,
performs vector arithmetic (king - man + woman) and finds the closest word.
"""

import json
import math
import os

def load_vectors(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    # Ensure all vectors are lists of floats
    return {word: [float(v) for v in vec] for word, vec in data.items()}

def cosine_similarity(vec_a, vec_b):
    dot = sum(a*b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a*a for a in vec_a))
    norm_b = math.sqrt(sum(b*b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def find_nearest(target_vec, vectors, exclude=None):
    if exclude is None:
        exclude = set()
    best_word = None
    best_score = -1.0
    for word, vec in vectors.items():
        if word in exclude:
            continue
        sim = cosine_similarity(target_vec, vec)
        if sim > best_score:
            best_score = sim
            best_word = word
    return best_word, best_score

def main():
    vec_file = os.path.join(os.path.dirname(__file__), 'word_vectors.json')
    vectors = load_vectors(vec_file)
    print("Loaded vectors for words:", list(vectors.keys()))

    # Example analogy: king - man + woman ≈ ?
    if all(w in vectors for w in ("king", "man", "woman")):
        king = vectors["king"]
        man = vectors["man"]
        woman = vectors["woman"]
        # Compute target vector
        target = [k - m + w for k, m, w in zip(king, man, woman)]
        print("\nAnalogy: king - man + woman =")
        print("  king  :", king)
        print("  man   :", man)
        print("  woman :", woman)
        print("  target:", target)
        # Find nearest neighbor
        exclude = {"king", "man", "woman"}
        nearest_word, score = find_nearest(target, vectors, exclude)
        print(f"\nNearest vector to target: '{nearest_word}' (similarity = {score:.4f})")
        if nearest_word == "queen":
            print("Success! The result matches 'queen'.")
        else:
            print("Note: The closest word is not 'queen' with this tiny random dataset.")
    else:
        print("Required words (king, man, woman) not found in vectors.")

    # Additional demo: compute similarity between some pairs
    print("\n--- Similarity examples ---")
    pairs = [("apple", "fruit"), ("car", "vehicle"), ("king", "queen"), ("apple", "car")]
    for w1, w2 in pairs:
        if w1 in vectors and w2 in vectors:
            sim = cosine_similarity(vectors[w1], vectors[w2])
            print(f"Similarity({w1}, {w2}) = {sim:.4f}")

if __name__ == "__main__":
    main()