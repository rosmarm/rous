"""
Rous — AI Career Agent for Rosmar Mendoza
Streamlit Web Application (Bilingual: Spanish / English)
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

    st.markdown("### 👤 " + ("Candidata" if lang == "es" else "Candidate"))
    st.markdown("**Rosmar Alejandra Mendoza**")
    st.caption("Desarrolladora Backend Semi-Senior (Golang & Python)" if lang == "es" else "Mid-Level Backend Developer (Golang & Python)")
    st.markdown("📍 Colombia | ✉️ [mendozarosmar@gmail.com](mailto:mendozarosmar@gmail.com)")
    st.markdown("🔗 [LinkedIn](https://linkedin.com/in/rosmar-mendoza) | 🐙 [GitHub](https://github.com/rosmarm)")

    st.divider()
    if lang == "es":
        st.success("🟢 Modo Offline Activo\n\nMotor heurístico y base de conocimiento cargados.")
    else:
        st.success("🟢 Offline Mode Active\n\nHeuristic engine and knowledge base loaded.")

cv_data = load_cv_data(lang)

# Main Header
col_title, col_stat = st.columns([3, 1])
with col_title:
    title_text = "🤖 Rous — Asistente de Carrera Profesional" if lang == "es" else "🤖 Rous — AI Career Agent"
    sub_text = "Optimizador de postulaciones, análisis de vacantes y preparación técnica para Rosmar Mendoza." if lang == "es" else "Application optimizer, vacancy evaluator, and interview prep for Rosmar Mendoza."
    st.markdown(f"<div class='main-header'>{title_text}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>{sub_text}</div>", unsafe_allow_html=True)

tab_names = [
    "🎯 Evaluador de Vacantes (Job Fit)",
    "✉️ Materiales de Postulación (Pitches & Cartas)",
    "🎙️ Simulador STAR (Entrevistas)",
    "👤 Perfil & CV Base"
] if lang == "es" else [
    "🎯 Job Fit Evaluator",
    "✉️ Application Materials (Pitches & Letters)",
    "🎙️ STAR Interview Simulator",
    "👤 Candidate Profile & CV"
]

tab_match, tab_pitch, tab_star, tab_cv = st.tabs(tab_names)

# Sample Vacancies
SAMPLE_JDS = {
    "es": {
        "Personalizada (Escribe o pega la tuya)": "",
        "Golang Backend Developer (Semi-Senior / SSR)": """Buscamos un Desarrollador Backend Semi-Senior con experiencia en Golang para nuestro equipo de microservicios.
Requisitos:
- 2+ a 4 años de experiencia sólida en Golang.
- Diseño y desarrollo de microservicios y APIs RESTful de alto rendimiento.
- Bases de datos relacionales (PostgreSQL / MySQL) y optimización de consultas SQL.
- Experiencia en plataformas cloud (AWS) y contenedores Docker.
- Gestión de incidentes en producción, observabilidad y guardias On-Call bajo SLAs.
- Deseable: Nociones de Kubernetes o mensajería con Kafka."""
    },
    "en": {
        "Custom (Write or paste your own)": "",
        "Golang Backend Developer (Mid-Level / Semi-Senior)": """We are seeking a Mid-Level Backend Developer with hands-on Golang expertise to join our engineering team. 
Requirements:
- 2+ to 4 years building high-throughput microservices and RESTful APIs in Golang.
- Strong experience with relational databases (PostgreSQL / MySQL) and SQL query optimization.
- Familiarity with cloud platforms (AWS), containerization with Docker, and CI/CD pipelines.
- Experience handling production incidents, monitoring, and On-Call rotations.
- Familiarity with Kubernetes (K8s) or message queues (Kafka) is a plus."""
    }
}

samples_dict = SAMPLE_JDS[lang]

# ----------------- TAB 1: JOB MATCH EVALUATOR -----------------
with tab_match:
    st.subheader("1. " + ("Analizar compatibilidad con una oferta de empleo" if lang == "es" else "Analyze Job Description Fit"))
    st.caption("Pega los requisitos de la vacante para calcular el match, identificar fortalezas y mitigar brechas." if lang == "es" else "Paste job requirements to compute match score, identify strengths, and bridge skill gaps.")

    sample_key = st.selectbox(
        "Seleccionar vacante de ejemplo o personalizada:" if lang == "es" else "Select sample or custom job description:",
        list(samples_dict.keys())
    )
    default_text = samples_dict[sample_key]

    jd_input = st.text_area(
        "Descripción del puesto (Job Description):" if lang == "es" else "Job Description:",
        value=default_text,
        height=200,
        placeholder="Pega aquí los requisitos..." if lang == "es" else "Paste requirements here..."
    )

    btn_text = "🚀 Analizar Compatibilidad con Rous" if lang == "es" else "🚀 Analyze Job Fit with Rous"
    if st.button(btn_text, type="primary"):
        if not jd_input.strip():
            st.warning("Por favor, ingresa o pega una descripción de empleo primero." if lang == "es" else "Please paste a job description first.")
        else:
            with st.spinner("Analizando..." if lang == "es" else "Analyzing..."):
                analysis = analyze_job_description(jd_input, cv_data, lang=lang)
                st.session_state["last_analysis"] = analysis

    if "last_analysis" in st.session_state:
        analysis = st.session_state["last_analysis"]

        st.divider()
        col_score, col_details = st.columns([1, 2])

        with col_score:
            st.metric(
                label="Índice de Compatibilidad (Match Score)" if lang == "es" else "Compatibility Match Score",
                value=f"{analysis['score']}%",
                delta=analysis['match_tier']
            )
            st.progress(analysis['score'] / 100)

        with col_details:
            st.markdown("#### " + ("✅ Habilidades Coincidentes Identificadas:" if lang == "es" else "✅ Matched Technical Skills:"))
            if analysis["matched_skills"]:
                chips = " ".join([f"<span class='skill-badge'>{skill}</span>" for skill in analysis["matched_skills"]])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.info("No se identificaron coincidencias directas." if lang == "es" else "No direct matches identified.")

            if analysis["gaps_with_mitigation"]:
                st.markdown("#### " + ("💡 Estrategia para Requisitos Adicionales (Mitigación):" if lang == "es" else "💡 Mitigation Strategy for Additional Requirements:"))
                for gap in analysis["gaps_with_mitigation"]:
                    st.markdown(f"- **{gap['technology']}**: {gap['mitigation']}")

        st.markdown("#### " + ("📌 Puntos clave a destacar en tu postulación:" if lang == "es" else "📌 Key Strategic Highlights for Your Application:"))
        for bullet in analysis["key_highlights"]:
            st.markdown(f"- {bullet}")

# ----------------- TAB 2: APPLICATION GENERATOR -----------------
with tab_pitch:
    st.subheader("2. " + ("Materiales de Postulación Generados" if lang == "es" else "Generated Application Materials"))
    st.caption("Copia y personaliza estos textos para contactar reclutadores." if lang == "es" else "Copy and tailor these materials to reach out to recruiters.")

    if "last_analysis" in st.session_state:
        materials = st.session_state["last_analysis"]["generated_materials"]

        sub_tab_names = [
            "💬 Mensaje para Reclutador (LinkedIn)",
            "📝 Carta de Presentación (Cover Letter ATS)",
            "📌 Bullets para Encabezado de CV"
        ] if lang == "es" else [
            "💬 Recruiter Outreach (LinkedIn)",
            "📝 Cover Letter (ATS Optimized)",
            "📌 Tailored CV Bullets"
        ]

        subtab_li, subtab_cl, subtab_sum = st.tabs(sub_tab_names)

        with subtab_li:
            st.markdown("##### " + ("Mensaje directo para conectar en LinkedIn:" if lang == "es" else "Direct message for LinkedIn outreach:"))
            st.text_area("Texto / Text:", value=materials["linkedin_pitch"], height=220)

        with subtab_cl:
            st.markdown("##### " + ("Carta de presentación formal (Cover Letter):" if lang == "es" else "Formal Cover Letter:"))
            st.text_area("Carta / Letter:", value=materials["cover_letter"], height=320)

        with subtab_sum:
            st.markdown("##### " + ("Bullets recomendados para tu encabezado:" if lang == "es" else "Recommended bullets for your header:"))
            for b in st.session_state["last_analysis"]["key_highlights"]:
                st.markdown(f"• {b}")
    else:
        st.info("💡 Haz clic en 'Analizar Compatibilidad' primero." if lang == "es" else "💡 Please run 'Analyze Job Fit' first.")

# ----------------- TAB 3: STAR INTERVIEW PREP -----------------
with tab_star:
    st.subheader("3. " + ("Simulador de Entrevistas (Formato STAR)" if lang == "es" else "STAR Interview Simulator"))
    st.caption("Situación -> Tarea -> Acción -> Resultado basada en la experiencia de Rosmar." if lang == "es" else "Situation -> Task -> Action -> Result based on Rosmar's engineering track record.")

    star_scenarios = st.session_state.get("last_analysis", {}).get("generated_materials", {}).get("star_prep")
    if not star_scenarios:
        from analyzer import generate_star_scenarios
        star_scenarios = generate_star_scenarios(["Golang", "Microservicios", "AI-Assisted Development"], lang)

    for i, s in enumerate(star_scenarios, 1):
        case_title = f"{'Caso' if lang == 'es' else 'Case'} {i}: {s['topic']} — {s['question']}"
        with st.expander(case_title, expanded=True):
            st.markdown(f"**{'Pregunta' if lang == 'es' else 'Question'}:** *\"{s['question']}\"*")
            col_s, col_t = st.columns(2)
            with col_s:
                st.markdown(f"**{'📍 Situación' if lang == 'es' else '📍 Situation'}:**")
                st.write(s["situation"])
            with col_t:
                st.markdown(f"**{'🎯 Tarea' if lang == 'es' else '🎯 Task'}:**")
                st.write(s["task"])
            
            st.markdown(f"**{'⚡ Acción' if lang == 'es' else '⚡ Action'}:**")
            st.write(s["action"])
            st.markdown(f"**{'🏆 Resultado' if lang == 'es' else '🏆 Result'}:**")
            st.success(s["result"])

# ----------------- TAB 4: GROUND TRUTH PROFILE -----------------
with tab_cv:
    st.subheader("4. " + ("Perfil Profesional & CV Base" if lang == "es" else "Professional Profile & Base CV"))
    st.caption("Datos estructurados del perfil de Rosmar." if lang == "es" else "Structured candidate profile data.")

    st.markdown(f"### {cv_data.get('nombre', cv_data.get('name'))}")
    st.markdown(f"**{cv_data.get('titulo', cv_data.get('title'))}**")
    st.write(cv_data.get("perfil_profesional", cv_data.get("professional_summary", "")))

    col_exp, col_skills = st.columns([3, 2])

    with col_exp:
        st.markdown("#### " + ("💼 Experiencia Laboral" if lang == "es" else "💼 Work Experience"))
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
        st.markdown("#### " + ("🛠️ Habilidades Técnicas" if lang == "es" else "🛠️ Technical Skills"))
        skills = cv_data.get("habilidades_tecnicas", cv_data.get("technical_skills", {}))
        for cat, item_list in skills.items():
            st.markdown(f"**{cat.replace('_', ' ').title()}:**")
            if isinstance(item_list, list):
                chips = " ".join([f"<span class='skill-badge'>{item}</span>" for item in item_list])
                st.markdown(chips, unsafe_allow_html=True)
            st.write("")

        st.markdown("#### " + ("🎓 Educación" if lang == "es" else "🎓 Education"))
        for edu in cv_data.get("educacion", cv_data.get("education", [])):
            st.markdown(f"- {edu}")

        st.markdown("#### " + ("🌐 Idiomas" if lang == "es" else "🌐 Languages"))
        langs = cv_data.get("idiomas", cv_data.get("languages", {}))
        for k, v in langs.items():
            st.markdown(f"- **{k.title()}:** {v}")
