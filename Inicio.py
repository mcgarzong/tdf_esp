import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from nltk.stem import SnowballStemmer

st.title("🔍 Demo TF-IDF en Español")

image = Image.open('vacaciones.jpeg') 
st.image(image,width=300)
# Documentos de ejemplo
default_docs = """La familia viajó a la playa para disfrutar del sol y el mar.
Los amigos acamparon en la montaña durante el fin de semana.
En el pueblo, los turistas probaron platos típicos y compraron recuerdos.
Los niños construyeron castillos de arena en la orilla.
En la noche, todos observaron las estrellas junto a una fogata."""

# Stemmer en español
stemmer = SnowballStemmer("spanish")

def tokenize_and_stem(text):
    # Minúsculas
    text = text.lower()
    # Solo letras españolas y espacios
    text = re.sub(r'[^a-záéíóúüñ\s]', ' ', text)
    # Tokenizar
    tokens = [t for t in text.split() if len(t) > 1]
    # Aplicar stemming
    stems = [stemmer.stem(t) for t in tokens]
    return stems

# Layout en dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area("📝 Documentos (uno por línea):", default_docs, height=150)
    question = st.text_input("❓ Escribe tu pregunta:", "¿Dónde viajó la familia de vacaciones?")

with col2:
    st.markdown("### 💡 Preguntas sugeridas:")
    
    # NUEVAS preguntas optimizadas para mayor similitud
    if st.button("¿Dónde viajó la familia de vacaciones?", use_container_width=True):
        st.session_state.question = "¿Dónde viajó la familia de vacaciones?"
        st.rerun()
    
    if st.button("¿Qué hicieron los amigos durante el fin de semana?", use_container_width=True):
        st.session_state.question = "¿Qué hicieron los amigos durante el fin de semana?"
        st.rerun()
        
    if st.button("¿Qué compraron los turistas en el pueblo?", use_container_width=True):
        st.session_state.question = "¿Qué compraron los turistas en el pueblo?"
        st.rerun()
        
    if st.button("¿Qué construyeron los niños en la orilla?", use_container_width=True):
        st.session_state.question = "¿Qué construyeron los niños en la orilla?"
        st.rerun()
        
    if st.button("¿Qué hicieron todos durante la noche?", use_container_width=True):
        st.session_state.question = "¿Qué hicieron todos durante la noche?"
        st.rerun()

# Actualizar pregunta si se seleccionó una sugerida
if 'question' in st.session_state:
    question = st.session_state.question

if st.button("🔍 Analizar", type="primary"):
    documents = [d.strip() for d in text_input.split("\n") if d.strip()]
    
    if len(documents) < 1:
        st.error("⚠️ Ingresa al menos un documento.")
    elif not question.strip():
        st.error("⚠️ Escribe una pregunta.")
    else:
        # Crear vectorizador TF-IDF
        vectorizer = TfidfVectorizer(
            tokenizer=tokenize_and_stem,
            min_df=1  # Incluir todas las palabras
        )
        
        # Ajustar con documentos
        X = vectorizer.fit_transform(documents)
        
        # Mostrar matriz TF-IDF
        st.markdown("### 📊 Matriz TF-IDF")
        df_tfidf = pd.DataFrame(
            X.toarray(),
            columns=vectorizer.get_feature_names_out(),
            index=[f"Doc {i+1}" for i in range(len(documents))]
        )
        st.dataframe(df_tfidf.round(3), use_container_width=True)
        
        # Calcular similitud con la pregunta
        question_vec = vectorizer.transform([question])
        similarities = cosine_similarity(question_vec, X).flatten()
        
        # Encontrar mejor respuesta
        best_idx = similarities.argmax()
        best_doc = documents[best_idx]
        best_score = similarities[best_idx]
        
        # Mostrar respuesta
        st.markdown("### 🎯 Respuesta")
        st.markdown(f"**Tu pregunta:** {question}")
        
        if best_score > 0.01:  # Umbral muy bajo
            st.success(f"**Respuesta:** {best_doc}")
            st.info(f"📈 Similitud: {best_score:.3f}")
        else:
            st.warning(f"**Respuesta (baja confianza):** {best_doc}")
            st.info(f"📉 Similitud: {best_score:.3f}")
