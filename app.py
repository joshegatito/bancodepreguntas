import streamlit as st
import json
import random
import time

# --- CONFIGURACIÓN Y FUNCIONES AUXILIARES ---

# Nombre del archivo donde se guardarán las preguntas
QUESTIONS_FILE = 'preguntas.json'

# --- NUEVO: CONTRASEÑA DE ACCESO PARA DOCENTES ---
# ¡IMPORTANTE! Cambia esta contraseña por una más segura.
TEACHER_PASSWORD = "docente123"

def load_questions():
    """Carga las preguntas desde el archivo JSON."""
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_questions(questions):
    """Guarda la lista de preguntas en el archivo JSON."""
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

# Cargar la base de datos de preguntas al iniciar la app
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = load_questions()

# --- INTERFAZ PRINCIPAL ---

st.set_page_config(page_title="App de Exámenes", layout="wide")

st.sidebar.title("🎓 App de Exámenes")
st.sidebar.markdown("Creada con Streamlit")

# --- NUEVO: LÓGICA DE AUTENTICACIÓN ---

# Inicializar el estado de autenticación
if 'teacher_authenticated' not in st.session_state:
    st.session_state.teacher_authenticated = False

# Mostrar formulario de login si no está autenticado
if not st.session_state.teacher_authenticated:
    with st.sidebar.expander("Acceso para Docentes", expanded=True):
        password_input = st.text_input("Contraseña:", type="password", key="login_password")
        if st.sidebar.button("Ingresar"):
            if password_input == TEACHER_PASSWORD:
                st.session_state.teacher_authenticated = True
                st.sidebar.success("¡Acceso concedido!")
                st.rerun()
            else:
                st.sidebar.error("Contraseña incorrecta.")
else:
    # Si está autenticado, mostrar botón de cerrar sesión
    st.sidebar.success("Sesión de Docente Activada")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.teacher_authenticated
        st.rerun()

# --- NUEVO: CONTROL DE NAVEGACIÓN ---
# Las opciones de navegación dependen del estado de autenticación
page_options = ["👨‍🎓 Examen para Estudiantes"]
if st.session_state.teacher_authenticated:
    page_options.insert(0, "👨‍🏫 Panel para Docentes")

page = st.sidebar.radio("Ir a:", page_options)


# --- SECCIÓN 1: PANEL PARA DOCENTES (AHORA PROTEGIDA) ---

if page == "👨‍🏫 Panel para Docentes":
    # Esta sección solo es visible si teacher_authenticated es True
    st.header("👨‍🏫 Panel para Docentes")
    st.markdown("Aquí puedes agregar nuevas preguntas al banco de datos.")

    with st.expander("➕ Agregar Nueva Pregunta"):
        with st.form("add_question_form"):
            st.subheader("Detalles de la Pregunta")
            
            question_text = st.text_area("Texto de la pregunta:", height=100)
            category = st.text_input("Categoría (ej: Matemáticas, Historia):")
            
            st.subheader("Opciones de Respuesta")
            option_a = st.text_input("Opción A")
            option_b = st.text_input("Opción B")
            option_c = st.text_input("Opción C")
            option_d = st.text_input("Opción D")
            
            correct_answer = st.radio("¿Cuál es la respuesta correcta?", ['A', 'B', 'C', 'D'])
            
            submit_button = st.form_submit_button("Agregar Pregunta")

            if submit_button:
                if question_text and category and option_a and option_b and option_c and option_d:
                    new_question = {
                        "question": question_text,
                        "category": category,
                        "options": {
                            "A": option_a,
                            "B": option_b,
                            "C": option_c,
                            "D": option_d
                        },
                        "correct": correct_answer
                    }
                    st.session_state.questions_db.append(new_question)
                    save_questions(st.session_state.questions_db)
                    st.success("¡Pregunta agregada exitosamente!")
                    st.rerun()
                else:
                    st.error("Por favor, completa todos los campos.")

    st.divider()
    st.subheader("📋 Preguntas Existentes")

    if not st.session_state.questions_db:
        st.info("Aún no hay preguntas. ¡Agrega algunas usando el formulario de arriba!")
    else:
        for i, q in enumerate(st.session_state.questions_db):
            with st.expander(f"{i+1}. {q['question']} ({q['category']})"):
                st.write(f"**A:** {q['options']['A']}")
                st.write(f"**B:** {q['options']['B']}")
                st.write(f"**C:** {q['options']['C']}")
                st.write(f"**D:** {q['options']['D']}")
                st.success(f"**Respuesta Correcta:** {q['correct']}")


# --- SECCIÓN 2: EXAMEN PARA ESTUDIANTES (SIEMPRE PÚBLICA) ---

elif page == "👨‍🎓 Examen para Estudiantes":
    st.header("👨‍🎓 Examen para Estudiantes")
    
    if not st.session_state.questions_db:
        st.warning("El banco de preguntas está vacío. Por favor, contacta a un docente.")
        st.stop()

    # --- LÓGICA DEL EXAMEN (sin cambios en esta parte) ---
    
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_finished' not in st.session_state:
        st.session_state.quiz_finished = False
    if 'score' not in st.session_state:
        st.session_state.score = 0

    if not st.session_state.quiz_started and not st.session_state.quiz_finished:
        st.subheader("Configura tu examen")
        
        with st.form("quiz_config_form"):
            name = st.text_input("Tu Nombre Completo:")
            grade = st.text_input("Tu Grado/Sección:")
            
            num_questions = st.slider(
                "Número de preguntas a responder:",
                min_value=1,
                max_value=len(st.session_state.questions_db),
                value=min(5, len(st.session_state.questions_db))
            )
            time_limit = st.number_input("Límite de tiempo (minutos):", min_value=1, value=5)
            randomize_questions = st.checkbox("Aleatorizar el orden de las preguntas", value=True)
            randomize_options = st.checkbox("Aleatorizar el orden de las opciones", value=True)
            
            start_button = st.form_submit_button("Comenzar Examen")
            
            if start_button and name and grade:
                questions_for_quiz = st.session_state.questions_db.copy()
                if randomize_questions:
                    random.shuffle(questions_for_quiz)
                questions_for_quiz = questions_for_quiz[:num_questions]
                
                st.session_state.quiz_config = {
                    'name': name,
                    'grade': grade,
                    'time_limit': time_limit * 60,
                    'randomize_options': randomize_options
                }
                st.session_state.questions_for_quiz = questions_for_quiz
                st.session_state.current_question_index = 0
                st.session_state.answers = {}
                st.session_state.score = 0
                st.session_state.quiz_started = True
                st.session_state.start_time = time.time()
                st.rerun()

    if st.session_state.quiz_started and not st.session_state.quiz_finished:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = st.session_state.quiz_config['time_limit'] - elapsed_time
        
        if remaining_time <= 0:
            st.session_state.quiz_finished = True
            st.error("¡Tiempo agotado!")
            st.rerun()
        
        st.info(f"Tiempo restante: {int(remaining_time // 60):02d}:{int(remaining_time % 60):02d}")
        
        current_q_data = st.session_state.questions_for_quiz[st.session_state.current_question_index]
        question_index = st.session_state.current_question_index + 1
        
        st.subheader(f"Pregunta {question_index} de {len(st.session_state.questions_for_quiz)}")
        st.write(current_q_data['question'])
        
        options = current_q_data['options']
        correct_key = current_q_data['correct']
        
        if st.session_state.quiz_config['randomize_options']:
            items = list(options.items())
            random.shuffle(items)
            options = dict(items)
            for key, value in options.items():
                if value == current_q_data['options'][correct_key]:
                    correct_key = key
                    break
        
        answer = st.radio("Selecciona una respuesta:", list(options.values()), key=f"q_{question_index}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Anterior", disabled=(st.session_state.current_question_index == 0)):
                st.session_state.current_question_index -= 1
                st.rerun()
        with col2:
            button_text = "Siguiente" if question_index < len(st.session_state.questions_for_quiz) else "Finalizar Examen"
            if st.button(button_text):
                selected_key = None
                for key, value in options.items():
                    if value == answer:
                        selected_key = key
                        break
                
                st.session_state.answers[st.session_state.current_question_index] = answer # Guardamos el valor, no la clave
                
                if question_index >= len(st.session_state.questions_for_quiz):
                    st.session_state.quiz_finished = True
                else:
                    st.session_state.current_question_index += 1
                st.rerun()

    if st.session_state.quiz_finished:
        st.header("🎉 Examen Finalizado")
        
        final_score = 0
        for i, q_data in enumerate(st.session_state.questions_for_quiz):
            correct_answer_text = q_data['options'][q_data['correct']]
            user_answer_text = st.session_state.answers.get(i)
            if user_answer_text == correct_answer_text:
                final_score += 1
        
        st.session_state.score = final_score
        total_questions = len(st.session_state.questions_for_quiz)
        percentage = (st.session_state.score / total_questions) * 100

        st.balloons()
        st.markdown(f"### 🏆 Resultados para: **{st.session_state.quiz_config['name']}**")
        st.write(f"**Grado:** {st.session_state.quiz_config['grade']}")
        st.write(f"**Puntuación Final:** {st.session_state.score} / {total_questions}")
        st.write(f"**Porcentaje de Aciertos:** {percentage:.2f}%")

        st.subheader("Revisión de Respuestas")
        for i, q_data in enumerate(st.session_state.questions_for_quiz):
            user_answer_text = st.session_state.answers.get(i, "No respondida")
            correct_answer_text = q_data['options'][q_data['correct']]
            
            is_correct = (user_answer_text == correct_answer_text)
            
            with st.expander(f"Pregunta {i+1}: {q_data['question'][:50]}..."):
                st.write(f"**Tu respuesta:** {user_answer_text}")
                st.write(f"**Respuesta correcta:** {correct_answer_text}")
                if is_correct:
                    st.success("✅ Correcto")
                else:
                    st.error("❌ Incorrecto")

        if st.button("Realizar otro examen"):
            for key in ['quiz_started', 'quiz_finished', 'score', 'questions_for_quiz', 'current_question_index', 'answers', 'quiz_config', 'start_time']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()