"""
Rous — AI Career Agent for Rosmar Mendoza
Streamlit Web Application
"""

import json
from pathlib import Path
import streamlit as st

from analyzer import (
    analyze_job_description,
    SKILL_TAXONOMY,
    MITIGATION_STRATEGIES
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="Rous — AI Career Agent | Rosmar Mendoza",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #1E293B;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .skill-badge {
        display: inline-block;
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .gap-badge {
        display: inline-block;
        background-color: #FEF3C7;
        color: #B45309;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_cv_data(lang: str = "es"):
    filename = "cv_rosmar_es.json" if lang == "es" else "cv_rosmar_en.json"
    file_path = DATA_DIR / filename
    if not file_path.exists():
        file_path = DATA_DIR / "cv_rosmar_es.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/laptop-coding.png", width=110)
    st.title("🤖 Rous Agent")
    st.caption("AI Career Agent & Technical Advocate")

    lang_choice = st.radio("Idioma / Language", ["Español 🇪🇸", "English 🇺🇸"], index=0)
    lang = "es" if "Español" in lang_choice else "en"

    st.divider()

    st.markdown("### 👤 Candidata")
    st.markdown("**Rosmar Alejandra Mendoza**")
    st.caption("Backend Software Developer (Golang & Python)")
    st.markdown("📍 Colombia | ✉️ [mendozarosmar@gmail.com](mailto:mendozarosmar@gmail.com)")
    st.markdown("🔗 [LinkedIn](https://linkedin.com/in/rosmar-mendoza) | 🐙 [GitHub](https://github.com/rosmarm)")

    st.divider()
    st.success("🟢 Modo Offline Activo\n\nMotor heurístico y base de conocimiento cargados.")

cv_data = load_cv_data(lang)

# Main Header
col_title, col_stat = st.columns([3, 1])
with col_title:
    st.markdown("<div class='main-header'>🤖 Rous — Asistente de Carrera Profesional</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Optimizador de postulaciones, análisis de vacantes y preparación técnica para Rosmar Mendoza.</div>", unsafe_allow_html=True)

tab_match, tab_pitch, tab_star, tab_cv = st.tabs([
    "🎯 Evaluador de Vacantes (Job Fit)",
    "✉️ Generador de Postulaciones (Pitches & Cartas)",
    "🎙️ Simulador STAR (Entrevistas)",
    "👤 Perfil & CV Base"
])

# Sample Vacancies
SAMPLE_JDS = {
    "Personalizada (Escribe o pega la tuya)": "",
    "Senior Golang Backend Engineer (Microservicios & Cloud)": """We are looking for a Senior Golang Backend Engineer to join our high-scale engineering team. 
Requirements:
- 3+ years of software development experience with Golang (Go).
- Strong experience with microservices architecture and high-throughput REST APIs.
- Experience with relational databases (PostgreSQL / MySQL) and SQL query optimization.
- Familiarity with cloud platforms (AWS), containerization with Docker, and CI/CD pipelines.
- Experience handling production incidents, monitoring, and On-Call rotations.
- Familiarity with Kubernetes (K8s) or message queues (Kafka) is a plus.""",
    "Python / FastAPI Backend Developer (Fintech)": """We are seeking a Python Backend Developer for our fintech credit platform.
Requirements:
- Strong experience with Python 3, FastAPI and/or Django.
- Experience building RESTful APIs, data validation, and third-party integrations.
- Solid knowledge of PostgreSQL, relational data modeling, and performance tuning.
- Experience working with AWS services (S3, RDS, Lambda).
- Experience working under Agile/Scrum methodologies.
- Bonus: Knowledge of AI-assisted productivity tools and microservices."""
}

# ----------------- TAB 1: JOB MATCH EVALUATOR -----------------
with tab_match:
    st.subheader("1. Analizar compatibilidad con una oferta de empleo")
    st.caption("Pega la descripción de la vacante (Job Description) para calcular el match, identificar fortalezas y mitigar posibles brechas.")

    sample_key = st.selectbox("Seleccionar vacante de ejemplo o personalizada:", list(SAMPLE_JDS.keys()))
    default_text = SAMPLE_JDS[sample_key]

    jd_input = st.text_area(
        "Descripción del puesto (Job Description):",
        value=default_text,
        height=200,
        placeholder="Pega aquí los requisitos, stack tecnológico y responsabilidades de la oferta..."
    )

    if st.button("🚀 Analizar Compatibilidad con Rous", type="primary"):
        if not jd_input.strip():
            st.warning("Por favor, ingresa o pega una descripción de empleo primero.")
        else:
            with st.spinner("Analizando requerimientos y comparando contra el perfil de Rosmar..."):
                analysis = analyze_job_description(jd_input, cv_data, lang=lang)
                st.session_state["last_analysis"] = analysis

    if "last_analysis" in st.session_state:
        analysis = st.session_state["last_analysis"]

        st.divider()
        col_score, col_details = st.columns([1, 2])

        with col_score:
            st.metric(
                label="Índice de Compatibilidad (Match Score)",
                value=f"{analysis['score']}%",
                delta=analysis['match_tier']
            )
            st.progress(analysis['score'] / 100)

        with col_details:
            st.markdown("#### ✅ Habilidades Coincidentes Identificadas:")
            if analysis["matched_skills"]:
                chips = " ".join([f"<span class='skill-badge'>{skill}</span>" for skill in analysis["matched_skills"]])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.info("No se identificaron coincidencias directas con el stack principal.")

            if analysis["gaps_with_mitigation"]:
                st.markdown("#### 💡 Estrategia para Requisitos Adicionales (Mitigación):")
                for gap in analysis["gaps_with_mitigation"]:
                    st.markdown(f"- **{gap['technology']}**: {gap['mitigation']}")

        st.markdown("#### 📌 Puntos clave a destacar en tu postulación:")
        for bullet in analysis["key_highlights"]:
            st.markdown(f"- {bullet}")

# ----------------- TAB 2: APPLICATION GENERATOR -----------------
with tab_pitch:
    st.subheader("2. Materiales de Postulación Generados")
    st.caption("Copia y personaliza estos textos para contactar reclutadores y aplicar con ventaja.")

    if "last_analysis" in st.session_state:
        materials = st.session_state["last_analysis"]["generated_materials"]

        subtab_li, subtab_cl, subtab_sum = st.tabs([
            "💬 Mensaje para Reclutador (LinkedIn)",
            "📝 Carta de Presentación (Cover Letter ATS)",
            "📌 Bullets para Encabezado de CV"
        ])

        with subtab_li:
            st.markdown("##### Mensaje directo y personalizado para conectar en LinkedIn:")
            st.text_area("Copia el texto:", value=materials["linkedin_pitch"], height=220)

        with subtab_cl:
            st.markdown("##### Carta de presentación formal (Cover Letter):")
            st.text_area("Copia la carta:", value=materials["cover_letter"], height=320)

        with subtab_sum:
            st.markdown("##### Bullets recomendados para colocar debajo de tu título profesional:")
            for b in st.session_state["last_analysis"]["key_highlights"]:
                st.markdown(f"• {b}")
    else:
        st.info("💡 Ve a la pestaña **'Evaluador de Vacantes'** y haz clic en **'Analizar Compatibilidad'** para generar estos materiales automáticamente adaptados a la vacante.")

# ----------------- TAB 3: STAR INTERVIEW PREP -----------------
with tab_star:
    st.subheader("3. Simulador de Entrevistas (Formato STAR)")
    st.caption("Estructura: **S**ituación | **T**area | **A**cción | **R**esultado basada en la experiencia real de Rosmar.")

    star_scenarios = st.session_state.get("last_analysis", {}).get("generated_materials", {}).get("star_prep")
    if not star_scenarios:
        from analyzer import generate_star_scenarios
        star_scenarios = generate_star_scenarios(["Golang", "Microservicios", "AI-Assisted Development"], lang)

    for i, s in enumerate(star_scenarios, 1):
        with st.expander(f"Caso {i}: {s['topic']} — {s['question']}", expanded=True):
            st.markdown(f"**Pregunta:** *\"{s['question']}\"*")
            col_s, col_t = st.columns(2)
            with col_s:
                st.markdown("**📍 Situación (Situation):**")
                st.write(s["situation"])
            with col_t:
                st.markdown("**🎯 Tarea (Task):**")
                st.write(s["task"])
            
            st.markdown("**⚡ Acción (Action):**")
            st.write(s["action"])
            st.markdown("**🏆 Resultado (Result):**")
            st.success(s["result"])

# ----------------- TAB 4: GROUND TRUTH PROFILE -----------------
with tab_cv:
    st.subheader("4. Perfil Profesional & CV Base")
    st.caption("Datos estructurados que Rous utiliza como fuente de verdad.")

    st.markdown(f"### {cv_data.get('nombre', cv_data.get('name'))}")
    st.markdown(f"**{cv_data.get('titulo', cv_data.get('title'))}**")
    st.write(cv_data.get("perfil_profesional", cv_data.get("professional_summary", "")))

    col_exp, col_skills = st.columns([3, 2])

    with col_exp:
        st.markdown("#### 💼 Experiencia Laboral")
        for exp in cv_data.get("experiencia_laboral", cv_data.get("work_experience", [])):
            company = exp.get("empresa", exp.get("company"))
            role = exp.get("cargo", exp.get("role"))
            period = exp.get("periodo", exp.get("period"))
            achievements = exp.get("logros", exp.get("achievements", []))
            
            with st.container():
                st.markdown(f"**{role}** — *{company}* ({period})")
                for ach in achievements:
                    st.markdown(f"- {ach}")
                st.write("")

    with col_skills:
        st.markdown("#### 🛠️ Habilidades Técnicas")
        skills = cv_data.get("habilidades_tecnicas", cv_data.get("technical_skills", {}))
        for cat, item_list in skills.items():
            st.markdown(f"**{cat.replace('_', ' ').title()}:**")
            if isinstance(item_list, list):
                chips = " ".join([f"<span class='skill-badge'>{item}</span>" for item in item_list])
                st.markdown(chips, unsafe_allow_html=True)
            st.write("")

        st.markdown("#### 🎓 Educación")
        for edu in cv_data.get("educacion", cv_data.get("education", [])):
            st.markdown(f"- {edu}")

        st.markdown("#### 🌐 Idiomas")
        langs = cv_data.get("idiomas", cv_data.get("languages", {}))
        for k, v in langs.items():
            st.markdown(f"- **{k.title()}:** {v}")
