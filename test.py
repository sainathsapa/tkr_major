import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

studnt_Submitted_Files = [doc for doc in os.listdir("assignments/newAssign") if doc.endswith('.html')]
studnt_Submitted_Files_DT =[open("assignments/newAssign/"+File).read() for File in  studnt_Submitted_Files]


# Getting Data from FIles
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()

# Findinnging Similarity
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
# creating a array
vectors = vectorize(studnt_Submitted_Files_DT)

s_vectors = list(zip(studnt_Submitted_Files, vectors))

# Similarity Checking Function
def check_plagiarism():

    plagiarism_results = set()
    global s_vectors

    for student_a, text_vector_a in s_vectors:
        new_vectors =s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b , text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1] * 100
            
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1],sim_score)
            plagiarism_results.add(score)
    return plagiarism_results
    
for data in check_plagiarism():
    print(data)