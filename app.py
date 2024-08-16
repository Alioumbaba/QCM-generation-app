# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def testflask():
#     return "TEST FLASK"
#
#
#
# if __name__ == "__main__":
#     app.run()
#
# from flask import Flask, render_template, request
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/generate', methods=['POST'])
# def generate():
#     text = request.form['text']
#     num_questions = request.form['num_questions']
#     # Logique pour utiliser le modèle et générer des questions à partir du texte
#     # À compléter avec votre code spécifique
#     return f"Text received: {text[:100]}... (truncated), Number of questions: {num_questions}"
#
# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, render_template, request
# from app.mcq_generation import MCQGenerator
#
# app = Flask(__name__)

# Route pour afficher le formulaire HTML
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# # Route pour traiter le formulaire et générer les questions
# @app.route('/generate', methods=['POST'])
# def generate():
#     # Récupérer les données du formulaire
#     text = request.form['text']
#     num_questions = int(request.form['num_questions'])
#
#     # Initialiser votre générateur de QCM
#     mcq_generator = MCQGenerator()
#
#     # Générer les questions
#     questions = mcq_generator.generate_mcq_questions(text, num_questions)
#
#     # Afficher les résultats dans une nouvelle page
#     return render_template('result.html', questions=questions)
#
# if __name__ == '__main__':
#     app.run(debug=True)

import streamlit as st
import nltk
import os

# Ajouter le chemin où NLTK doit chercher les données
nltk.data.path.append('C:\\Users\\aliou\\PycharmProjects\\QCM-Local\\.venv\\nltk_data')


from app.mcq_generation import MCQGenerator
import gdown
import os

# insertion des fichiers Drive
# Fichier 1: race-distractors.ckpt
url1 = "https://drive.google.com/uc?id=1PzXhi6W2wxTVR-nOFTVV7O88CS9gBbY8"  # Remplacez FILE_ID1 par l'ID du fichier Google Drive
output1 = "./app/ml_models/distractor_generation/models/race-distractors.ckpt"
if not os.path.exists(output1):
    gdown.download(url1, output1, quiet=False)

# Fichier 2: multitask-qg-ag.ckpt
url2 = "https://drive.google.com/uc?id=1c9rw7rwWKUtQDIGOwC5yfy21DC5GekEt"  # Remplacez FILE_ID2 par l'ID du fichier Google Drive
output2 = "./app/ml_models/question_generation/models/multitask-qg-ag.ckpt"
if not os.path.exists(output2):
    gdown.download(url2, output2, quiet=False)

# Fichier 3: vectors
url3 = "https://drive.google.com/uc?id=1LUlf2STdxBg6BWcLQULFEn0o2FTMvHvj"  # Remplacez FILE_ID3 par l'ID du fichier Google Drive
output3 = "./app/ml_models/sense2vec_distractor_generation/data/s2v_old/vectors"
if not os.path.exists(output3):
    gdown.download(url3, output3, quiet=False)

# Titre de la page
# st.title("Cours A61 et A62 : Projet de synthèse\nRéalisé par : Alioum et Alpha Amadou Diallo\n\nSupervision : Hafed Benteftifa et Komi Sodoke\n\nGenerate Questions from Text")
st.markdown("**Cours A61 et A62 : Projet de synthèse**\n**Réalisé par : Alioum et Alpha Amadou Diallo**\n**Supervision : Hafed Benteftifa et Komi Sodoke**\n\n**Generate Questions from Text**")


# Formulaire pour entrer le texte
text = st.text_area("Enter your text (max 10,000 words):", max_chars=10000)
num_questions = st.number_input("Number of questions:", min_value=1, step=1)

# Bouton pour générer les questions
if st.button("Generate Questions"):
    # Initialiser votre générateur de QCM
    mcq_generator = MCQGenerator()

    # Générer les questions
    questions = mcq_generator.generate_mcq_questions(text, num_questions)

    # Afficher les résultats
    st.header("Generated Questions")
    for question in questions:
        st.subheader(f"Question: {question.questionText}")
        st.write(f"**Answer:** {question.answerText}")
        st.write("**Distractors:**")
        for distractor in question.distractors:
            st.write(f"- {distractor}")
    # # Afficher les résultats
    # st.header("Generated Questions")
    # for question in questions:
    #     st.subheader(f"Question: {question['questionText']}")
    #     st.write(f"**Answer:** {question['answerText']}")
    #     st.write("**Distractors:**")
    #     for distractor in question['distractors']:
    #         st.write(f"- {distractor}")
