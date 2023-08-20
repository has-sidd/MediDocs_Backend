# from gensim.models import Word2Vec
# from contour_detection import *
# import spacy

# nlp = spacy.load("en_core_web_sm")
# # print(nlp.pipe_names)

# doc = nlp("haemoglobin: 0.7")
# for ent in doc.ents:
#     print(ent.text, "|", spacy.explain(ent.label_))


# # Load the model
# # model = Word2Vec.load('W2V_100/w2v_OA_CR_100d.bin')

# # print(model.wv.most_similar('haemoglobin'))

# # # Generate word embeddings for words in medical reports
# # words = scanned_img()
# # word_embeddings = []  # List to store word embeddings

# # # Iterate through words and get their corresponding word embeddings
# # for word in words:
# #     try:
# #         word_embedding = model.wv.get_vector(word)  # Get word embedding
# #         word_embeddings.append(word_embedding)
# #     except KeyError:
# #         print(f"Word '{word}' not found in Word2Vec model's vocabulary")

# # # Calculate similarity for each word with a reference term
# # reference_term = "haemoglobin"  # Example reference term for similarity comparison
# # similarity_threshold = 0.8  # Example similarity threshold for similarity comparison

# # for i in range(len(words)):
# #     try:
# #         similarity = model.wv.similarity(words[i], reference_term)
# #         if similarity > similarity_threshold:
# #             print(f"Word '{words[i]}' is similar to '{reference_term}' with similarity score: {similarity}")
# #             # Perform further processing or retrieval based on the similarity score
# #         else:
# #             print(f"Word '{words[i]}' is not similar to '{reference_term}' with similarity score: {similarity}")
# #     except KeyError:
# #         print(f"Word '{words[i]}' not found in Word2Vec model's vocabulary")











# # ========================NOT USING THIS, JUST FOR REFERENCE============================



# # Iterate through words and get their corresponding word embeddings
# # for word in words:
# #     if word in model.wv.key_to_index.keys():  # Check if word is in Word2Vec model's vocabulary
# #         word_embedding = model.wv.get_vector(word)  # Get word embedding
# #         word_embeddings.append(word_embedding)

# # print(word_embeddings)

# # Perform NLP operations using word embeddings
# # For example, calculate similarity between word embeddings
# # and a reference medical terminology
# # reference_term = "haemoglobin"
# # similarity_threshold = 0.8

# # for i in range(len(words)):
# #     similarity = model.wv.similarity(words[i], reference_term)
# #     if similarity > similarity_threshold:
# #         print(f"Word '{words[i]}' is similar to '{reference_term}' with similarity score: {similarity}")
# #         # Perform further processing or retrieval based on the similarity score
# #     else:
# #         print(f"Word '{words[i]}' is not similar to '{reference_term}' with similarity score: {similarity}")











# # # Return 100-dimensional vector representations of each word
# # model.wv.get_vector('diabetes')
# # model.wv.get_vector('cardiac_arrest')
# # model.wv.get_vector('lymphangioleiomyomatosis')

# # # Try out cosine similarity
# # # print(model.wv.similarity('copd', 'chronic_obstructive_pulmonary_disease'))
# # # print(model.wv.similarity('myocardial_infarction', 'heart_attack'))
# # # print(model.wv.similarity('lymphangioleiomyomatosis', 'lam'))

# # word_embedding = model.wv['copd']
# # print(word_embedding)