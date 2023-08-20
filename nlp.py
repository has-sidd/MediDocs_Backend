# import gensim
# from gensim.models import Word2Vec, FastText
# from sklearn.metrics.pairwise import cosine_similarity

# # Load pre-trained Word2Vec model
# # word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('path/to/word2vec/model.bin', binary=True)
# word2vec_model = Word2Vec.load('W2V_100/w2v_OA_CR_100d.bin')

# # Define a function to calculate word embeddings
# def get_word_embedding(word):
#     try:
#         return word2vec_model.wv[word]
#     except KeyError:
#         return None

# # Example dataset of medical terms and values
# medical_terms = {
#         "basophil_ree": 0.7,
#         "eosinophil": 4.5,
#         "haematocrit": 25.9,
#         "haemoglobin": 8.3,
#         "lymphocyte_ted": 14.4,
#         "m.c.h": 22.7,
#         "m.c.h.c": 32.0,
#         "m.c.v": 70.8,
#         "monocyte": 9.3,
#         "neutrophil_lymphocyte_ratio": 4.9,
#         "neutrophil": 71.1,
#         "platelet": 256.0,
#         "r.b.c": 2.0,
#         "r.d.w_se_ar": 16.6,
#         "specimen_id": 18092020.0,
#         "w.b.c": 7.4
#     }

# # Preprocess the user-provided term (you may need to modify this based on your specific preprocessing needs)
# # user_term = preprocess_text(user_provided_term)

# # Calculate the embedding for the user-provided term
# user_embedding = get_word_embedding("neutrophil")

# if user_embedding is None:
#     print("User-provided term not found in the dataset.")
# else:
#     # Calculate similarity between user-provided term and all medical terms
#     similarity_scores = {}
#     for term, value in medical_terms.items():
#         term_embedding = get_word_embedding(term)
#         if term_embedding is not None:
#             similarity_scores[term] = cosine_similarity([user_embedding], [term_embedding])[0][0]

#     # Sort the medical terms based on similarity score (descending order)
#     sorted_terms = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

#     # Print the most similar medical term
#     most_similar_term, similarity_score = sorted_terms[0]
#     print(f"The most similar term to", most_similar_term, similarity_score)