#!/usr/bin/env python3
"""
Zero-dependency Web UI Server for Rous - AI Career Agent
Runs a local, interactive web dashboard using Python's standard library.
Includes full instant bilingual switching (Spanish / English).
"""

import sys
import json
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Add src to path
SRC_DIR = Path(__file__).resolve().parent
BASE_DIR = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))

from analyzer import analyze_job_description

DATA_DIR = BASE_DIR / "data"

def get_profile(lang="es"):
    filename = "cv_rosmar_es.json" if lang == "es" else "cv_rosmar_en.json"
    file_path = DATA_DIR / filename
    if not file_path.exists():
        file_path = DATA_DIR / "cv_rosmar_es.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

HTML_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rous — AI Career Agent | Rosmar Mendoza</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col">

    <!-- Top Navbar -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white font-bold text-xl shadow-md">
                    🤖
                </div>
                <div>
                    <h1 class="text-lg font-bold text-slate-900 leading-tight">
                        Rous <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 ml-1">AI Career Agent</span>
                    </h1>
                    <p class="text-xs text-slate-500" id="ui-subtitle">Rosmar Mendoza &bull; Backend Engineer (Golang &bull; Python)</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-4">
                <!-- Language Selector -->
                <div class="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200">
                    <button onclick="changeLang('es')" id="btn-lang-es" class="text-xs font-bold px-2.5 py-1 rounded-lg transition bg-white text-indigo-700 shadow-sm">
                        🇪🇸 Español
                    </button>
                    <button onclick="changeLang('en')" id="btn-lang-en" class="text-xs font-medium px-2.5 py-1 rounded-lg transition text-slate-600 hover:text-slate-900">
                        🇺🇸 English
                    </button>
                </div>

                <!-- Profile Links -->
                <a href="https://linkedin.com/in/rosmar-mendoza" target="_blank" class="hidden sm:flex text-xs font-semibold text-blue-600 hover:text-blue-800 items-center gap-1">
                    LinkedIn &rarr;
                </a>
                <a href="https://github.com/rosmarm" target="_blank" class="hidden sm:flex text-xs font-semibold text-slate-700 hover:text-slate-900 items-center gap-1">
                    GitHub &rarr;
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        
        <!-- Navigation Tabs -->
        <div class="flex border-b border-slate-200 mb-8 space-x-2 sm:space-x-8 overflow-x-auto">
            <button onclick="switchTab('tab-match')" id="btn-tab-match" class="tab-btn py-3 px-1 border-b-2 border-indigo-600 font-semibold text-indigo-600 text-sm whitespace-nowrap flex items-center gap-2">
                🎯 <span id="lbl-tab-match">Evaluador de Vacantes</span>
            </button>
            <button onclick="switchTab('tab-pitch')" id="btn-tab-pitch" class="tab-btn py-3 px-1 border-b-2 border-transparent font-medium text-slate-500 hover:text-slate-700 text-sm whitespace-nowrap flex items-center gap-2">
                ✉️ <span id="lbl-tab-pitch">Materiales de Postulación</span>
            </button>
            <button onclick="switchTab('tab-star')" id="btn-tab-star" class="tab-btn py-3 px-1 border-b-2 border-transparent font-medium text-slate-500 hover:text-slate-700 text-sm whitespace-nowrap flex items-center gap-2">
                🎙️ <span id="lbl-tab-star">Simulador STAR (Entrevistas)</span>
            </button>
            <button onclick="switchTab('tab-cv')" id="btn-tab-cv" class="tab-btn py-3 px-1 border-b-2 border-transparent font-medium text-slate-500 hover:text-slate-700 text-sm whitespace-nowrap flex items-center gap-2">
                👤 <span id="lbl-tab-cv">Perfil &amp; CV Base</span>
            </button>
        </div>

        <!-- TAB 1: EVALUADOR DE VACANTES -->
        <section id="tab-match" class="tab-content block">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <!-- Left: Input Area -->
                <div class="lg:col-span-6 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <h2 class="text-base font-bold text-slate-900" id="lbl-input-title">Pegar Oferta de Empleo (Job Description)</h2>
                        <button onclick="loadSampleJD()" id="btn-load-sample" class="text-xs font-semibold text-indigo-600 hover:text-indigo-800 bg-indigo-50 px-2.5 py-1 rounded-md transition">
                            Cargar ejemplo Golang / MercadoLibre
                        </button>
                    </div>
                    <textarea id="jdInput" rows="12" placeholder="Pega aquí los requisitos, stack tecnológico y responsabilidades de la oferta..." class="w-full text-sm p-4 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-slate-800 font-mono leading-relaxed resize-y"></textarea>
                    
                    <button onclick="runAnalysis()" id="btnAnalyze" class="mt-4 w-full bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 text-white font-semibold py-3 px-4 rounded-xl shadow-md hover:shadow-lg transition flex items-center justify-center gap-2">
                        🚀 <span id="lbl-btn-analyze">Analizar Compatibilidad con Rous</span>
                    </button>
                </div>

                <!-- Right: Results Card -->
                <div class="lg:col-span-6 flex flex-col space-y-6">
                    <!-- Score Banner Placeholder -->
                    <div id="resultPlaceholder" class="bg-white p-8 rounded-2xl border border-dashed border-slate-300 flex flex-col items-center justify-center text-center h-full min-h-[350px]">
                        <div class="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center text-3xl mb-4">
                            📊
                        </div>
                        <h3 class="text-base font-bold text-slate-700 mb-1" id="lbl-placeholder-title">Ninguna vacante analizada aún</h3>
                        <p class="text-xs text-slate-500 max-w-sm" id="lbl-placeholder-sub">Pega una descripción de empleo a la izquierda y presiona "Analizar Compatibilidad" para ver el score y recomendaciones.</p>
                    </div>

                    <div id="resultContent" class="hidden space-y-6">
                        <!-- Score Display -->
                        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <div class="flex items-center justify-between">
                                <div>
                                    <span class="text-xs font-bold text-slate-400 uppercase tracking-wider" id="lbl-score-title">Score de Compatibilidad</span>
                                    <div class="text-4xl font-extrabold text-indigo-600 mt-1" id="resScore">--%</div>
                                </div>
                                <div id="resTierBadge" class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-green-50 text-green-700 border border-green-200">
                                    --
                                </div>
                            </div>
                            <!-- Progress Bar -->
                            <div class="w-full bg-slate-100 rounded-full h-3 mt-4 overflow-hidden">
                                <div id="resProgressBar" class="bg-indigo-600 h-3 rounded-full transition-all duration-700" style="width: 0%"></div>
                            </div>
                        </div>

                        <!-- Matched Skills -->
                        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h4 class="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                                ✅ <span id="lbl-skills-matched">Habilidades Coincidentes Identificadas:</span>
                            </h4>
                            <div id="resMatchedSkills" class="flex flex-wrap gap-2"></div>
                        </div>

                        <!-- Gaps & Mitigation -->
                        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h4 class="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                                💡 <span id="lbl-gaps-title">Estrategia para Requisitos Adicionales (Mitigación):</span>
                            </h4>
                            <div id="resGaps" class="space-y-2.5 text-xs text-slate-600"></div>
                        </div>

                        <!-- Header Bullets -->
                        <div class="bg-indigo-50/70 p-6 rounded-2xl border border-indigo-100 shadow-sm">
                            <h4 class="text-sm font-bold text-indigo-950 mb-3 flex items-center gap-2">
                                📌 <span id="lbl-highlights-title">Puntos Clave para tu Postulación:</span>
                            </h4>
                            <ul id="resHighlights" class="space-y-2 text-xs text-indigo-900 list-disc list-inside"></ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 2: PITCHES & CARTAS -->
        <section id="tab-pitch" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- LinkedIn Pitch -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="text-base font-bold text-slate-900 flex items-center gap-2" id="lbl-li-title">
                                💬 Mensaje Directo para Reclutador (LinkedIn)
                            </h3>
                            <button onclick="copyToClipboard('txtLinkedIn')" class="btn-copy text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-2.5 py-1 rounded-md transition">
                                📋 <span class="lbl-copy-btn">Copiar</span>
                            </button>
                        </div>
                        <p class="text-xs text-slate-500 mb-3" id="lbl-li-sub">Mensaje conciso, cordial y de alto impacto para enviar junto a la solicitud de conexión.</p>
                        <textarea id="txtLinkedIn" rows="9" class="w-full text-xs p-3.5 bg-slate-50 border border-slate-200 rounded-xl font-mono text-slate-700 resize-none leading-relaxed"></textarea>
                    </div>
                </div>

                <!-- Cover Letter -->
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3">
                            <h3 class="text-base font-bold text-slate-900 flex items-center gap-2" id="lbl-cl-title">
                                📝 Carta de Presentación (Cover Letter ATS)
                            </h3>
                            <button onclick="copyToClipboard('txtCoverLetter')" class="btn-copy text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-2.5 py-1 rounded-md transition">
                                📋 <span class="lbl-copy-btn">Copiar</span>
                            </button>
                        </div>
                        <p class="text-xs text-slate-500 mb-3" id="lbl-cl-sub">Redactada con énfasis en escalabilidad, experiencia en MercadoLibre y metodologías modernas.</p>
                        <textarea id="txtCoverLetter" rows="14" class="w-full text-xs p-3.5 bg-slate-50 border border-slate-200 rounded-xl font-mono text-slate-700 resize-none leading-relaxed"></textarea>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: STAR INTERVIEW PREP -->
        <section id="tab-star" class="tab-content hidden space-y-6">
            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm mb-6">
                <h3 class="text-base font-bold text-slate-900 mb-1" id="lbl-star-header">🎙️ Respuestas Estructuradas en Formato STAR</h3>
                <p class="text-xs text-slate-500" id="lbl-star-sub">
                    Estructura: <strong>Situación</strong> &rarr; <strong>Tarea</strong> &rarr; <strong>Acción</strong> &rarr; <strong>Resultado</strong>, extraídas de la trayectoria técnica de Rosmar.
                </p>
            </div>

            <div id="starContainer" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
        </section>

        <!-- TAB 4: PROFILE & CV -->
        <section id="tab-cv" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <!-- Left: Work Experience -->
                <div class="lg:col-span-7 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-6 flex items-center gap-2" id="lbl-cv-exp-title">
                        💼 Trayectoria Laboral
                    </h3>
                    <div id="cvExperienceList" class="space-y-6 relative border-l-2 border-indigo-100 ml-3 pl-6"></div>
                </div>

                <!-- Right: Skills & Education -->
                <div class="lg:col-span-5 space-y-6">
                    <!-- Skills -->
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 class="text-base font-bold text-slate-900 mb-4 flex items-center gap-2" id="lbl-cv-skills-title">
                            🛠️ Stack Tecnológico
                        </h3>
                        <div id="cvSkillsContainer" class="space-y-4 text-xs"></div>
                    </div>

                    <!-- Education -->
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 class="text-base font-bold text-slate-900 mb-3 flex items-center gap-2" id="lbl-cv-edu-title">
                            🎓 Educación &amp; Certificaciones
                        </h3>
                        <ul id="cvEducationList" class="space-y-2 text-xs text-slate-700"></ul>
                    </div>

                    <!-- Languages -->
                    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 class="text-base font-bold text-slate-900 mb-3 flex items-center gap-2" id="lbl-cv-lang-title">
                            🌐 Idiomas
                        </h3>
                        <ul id="cvLangList" class="space-y-1.5 text-xs text-slate-700"></ul>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
        Rous &bull; AI Career Agent &bull; Rosmar Mendoza &bull; GitHub: <a href="https://github.com/rosmarm/rous" class="text-indigo-600 underline">rosmarm/rous</a>
    </footer>

    <!-- App JavaScript with Complete Bilingual Translation Dictionary -->
    <script>
        let currentLang = 'es';
        let profileData = null;
        let lastAnalysis = null;

        const SAMPLE_JDS = {
            es: `Senior Golang Backend Engineer
Buscamos un Ingeniero Backend apasionado con experiencia sólida en Golang para nuestro equipo de ingeniería.
Requisitos:
- 3+ años de experiencia construyendo microservicios y APIs RESTful de alto rendimiento en Golang.
- Dominio de bases de datos relacionales (PostgreSQL, MySQL) y optimización de consultas SQL.
- Experiencia con plataformas cloud (AWS), contenedores Docker y despliegues CI/CD.
- Experiencia en soporte a producción, guardias On-Call y cumplimiento estricto de SLAs.
- Deseable: Conocimiento en Kubernetes (K8s) o sistemas de mensajería asíncrona como Kafka.`,
            en: `Senior Golang Backend Engineer
We are seeking an experienced Backend Engineer with strong Golang expertise to join our engineering team.
Requirements:
- 3+ years building high-throughput microservices and RESTful APIs in Golang.
- Deep familiarity with relational databases (PostgreSQL, MySQL) and SQL query optimization.
- Solid background in cloud architectures (AWS), Docker containerization, and CI/CD pipelines.
- Experience managing production incidents, On-Call support rotations, and SLA compliance.
- Nice to have: Knowledge of Kubernetes (K8s) or message streaming (Kafka / RabbitMQ).`
        };

        const I18N = {
            es: {
                subtitle: "Rosmar Mendoza • Backend Engineer (Golang • Python)",
                tab_match: "Evaluador de Vacantes",
                tab_pitch: "Materiales de Postulación",
                tab_star: "Simulador STAR (Entrevistas)",
                tab_cv: "Perfil & CV Base",
                input_title: "Pegar Oferta de Empleo (Job Description)",
                btn_sample: "Cargar ejemplo Golang / MercadoLibre",
                input_placeholder: "Pega aquí los requisitos, stack tecnológico y responsabilidades de la oferta...",
                btn_analyze: "Analizar Compatibilidad con Rous",
                placeholder_title: "Ninguna vacante analizada aún",
                placeholder_sub: "Pega una descripción de empleo a la izquierda y presiona 'Analizar Compatibilidad' para ver el score y recomendaciones.",
                score_title: "Score de Compatibilidad",
                skills_matched: "Habilidades Coincidentes Identificadas:",
                gaps_title: "Estrategia para Requisitos Adicionales (Mitigación):",
                highlights_title: "Puntos Clave para tu Postulación:",
                li_title: "💬 Mensaje Directo para Reclutador (LinkedIn)",
                li_sub: "Mensaje conciso, cordial y de alto impacto para enviar junto a la solicitud de conexión.",
                cl_title: "📝 Carta de Presentación (Cover Letter ATS)",
                cl_sub: "Redactada con énfasis en escalabilidad, experiencia en MercadoLibre y metodologías modernas.",
                copy_btn: "Copiar",
                copied_alert: "¡Copiado al portapapeles!",
                star_header: "🎙️ Respuestas Estructuradas en Formato STAR",
                star_sub: "Estructura: <strong>Situación</strong> &rarr; <strong>Tarea</strong> &rarr; <strong>Acción</strong> &rarr; <strong>Resultado</strong>, extraídas de la trayectoria técnica de Rosmar.",
                star_case: "Caso",
                star_situation: "📍 Situación:",
                star_task: "🎯 Tarea:",
                star_action: "⚡ Acción:",
                star_result: "🏆 Resultado:",
                cv_exp_title: "💼 Trayectoria Laboral",
                cv_skills_title: "🛠️ Stack Tecnológico",
                cv_edu_title: "🎓 Educación & Certificaciones",
                cv_lang_title: "🌐 Idiomas"
            },
            en: {
                subtitle: "Rosmar Mendoza • Backend Engineer (Golang • Python)",
                tab_match: "Job Fit Evaluator",
                tab_pitch: "Application Materials",
                tab_star: "STAR Interview Prep",
                tab_cv: "Profile & CV",
                input_title: "Paste Job Description",
                btn_sample: "Load Golang / Microservices Sample",
                input_placeholder: "Paste job requirements, tech stack, and responsibilities here...",
                btn_analyze: "Analyze Job Fit with Rous",
                placeholder_title: "No job analyzed yet",
                placeholder_sub: "Paste a job description on the left and click 'Analyze Job Fit' to see your score and recommendations.",
                score_title: "Compatibility Match Score",
                skills_matched: "Matched Technical Skills:",
                gaps_title: "Mitigation Strategy for Additional Requirements:",
                highlights_title: "Key Strategic Highlights for Your Application:",
                li_title: "💬 Direct Recruiter Pitch (LinkedIn)",
                li_sub: "Concise, high-impact message to accompany your connection request.",
                cl_title: "📝 ATS-Optimized Cover Letter",
                cl_sub: "Tailored with focus on scalability, MercadoLibre experience, and engineering excellence.",
                copy_btn: "Copy",
                copied_alert: "Copied to clipboard!",
                star_header: "🎙️ STAR Method Interview Responses",
                star_sub: "Structure: <strong>Situation</strong> &rarr; <strong>Task</strong> &rarr; <strong>Action</strong> &rarr; <strong>Result</strong>, drawn from Rosmar's engineering track record.",
                star_case: "Case",
                star_situation: "📍 Situation:",
                star_task: "🎯 Task:",
                star_action: "⚡ Action:",
                star_result: "🏆 Result:",
                cv_exp_title: "💼 Professional Experience",
                cv_skills_title: "🛠️ Technical Stack",
                cv_edu_title: "🎓 Education & Certifications",
                cv_lang_title: "🌐 Languages"
            }
        };

        async function init() {
            changeLang('es', true);
        }

        async function changeLang(lang, isInitial = false) {
            currentLang = lang;

            // Update Language Toggle Buttons Style
            const btnEs = document.getElementById('btn-lang-es');
            const btnEn = document.getElementById('btn-lang-en');
            if (lang === 'es') {
                btnEs.className = "text-xs font-bold px-2.5 py-1 rounded-lg transition bg-white text-indigo-700 shadow-sm";
                btnEn.className = "text-xs font-medium px-2.5 py-1 rounded-lg transition text-slate-600 hover:text-slate-900";
            } else {
                btnEn.className = "text-xs font-bold px-2.5 py-1 rounded-lg transition bg-white text-indigo-700 shadow-sm";
                btnEs.className = "text-xs font-medium px-2.5 py-1 rounded-lg transition text-slate-600 hover:text-slate-900";
            }

            // Apply all UI translations
            const t = I18N[lang];
            document.getElementById('ui-subtitle').innerHTML = t.subtitle;
            document.getElementById('lbl-tab-match').innerText = t.tab_match;
            document.getElementById('lbl-tab-pitch').innerText = t.tab_pitch;
            document.getElementById('lbl-tab-star').innerText = t.tab_star;
            document.getElementById('lbl-tab-cv').innerText = t.tab_cv;
            document.getElementById('lbl-input-title').innerText = t.input_title;
            document.getElementById('btn-load-sample').innerText = t.btn_sample;
            document.getElementById('jdInput').placeholder = t.input_placeholder;
            document.getElementById('lbl-btn-analyze').innerText = t.btn_analyze;
            document.getElementById('lbl-placeholder-title').innerText = t.placeholder_title;
            document.getElementById('lbl-placeholder-sub').innerText = t.placeholder_sub;
            document.getElementById('lbl-score-title').innerText = t.score_title;
            document.getElementById('lbl-skills-matched').innerText = t.skills_matched;
            document.getElementById('lbl-gaps-title').innerText = t.gaps_title;
            document.getElementById('lbl-highlights-title').innerText = t.highlights_title;
            document.getElementById('lbl-li-title').innerText = t.li_title;
            document.getElementById('lbl-li-sub').innerText = t.li_sub;
            document.getElementById('lbl-cl-title').innerText = t.cl_title;
            document.getElementById('lbl-cl-sub').innerText = t.cl_sub;
            document.querySelectorAll('.lbl-copy-btn').forEach(el => el.innerText = t.copy_btn);
            document.getElementById('lbl-star-header').innerText = t.star_header;
            document.getElementById('lbl-star-sub').innerHTML = t.star_sub;
            document.getElementById('lbl-cv-exp-title').innerText = t.cv_exp_title;
            document.getElementById('lbl-cv-skills-title').innerText = t.cv_skills_title;
            document.getElementById('lbl-cv-edu-title').innerText = t.cv_edu_title;
            document.getElementById('lbl-cv-lang-title').innerText = t.cv_lang_title;

            // If textarea has sample or is empty, adapt to the new language's sample
            const currentJdVal = document.getElementById('jdInput').value.trim();
            if (!currentJdVal || currentJdVal === SAMPLE_JDS.es.trim() || currentJdVal === SAMPLE_JDS.en.trim()) {
                document.getElementById('jdInput').value = SAMPLE_JDS[lang];
            }

            // Fetch profile data in selected language and render CV
            await fetchProfile();
            renderProfile();

            // Run analysis with new language
            await runAnalysis(true);
        }

        async function fetchProfile() {
            try {
                const res = await fetch(`/api/profile?lang=${currentLang}`);
                profileData = await res.json();
            } catch (e) {
                console.error("Error fetching profile", e);
            }
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('border-indigo-600', 'text-indigo-600', 'font-semibold');
                btn.classList.add('border-transparent', 'text-slate-500', 'font-medium');
            });

            document.getElementById(tabId).classList.remove('hidden');
            const activeBtn = document.getElementById('btn-' + tabId);
            activeBtn.classList.add('border-indigo-600', 'text-indigo-600', 'font-semibold');
            activeBtn.classList.remove('border-transparent', 'text-slate-500', 'font-medium');
        }

        function loadSampleJD() {
            document.getElementById('jdInput').value = SAMPLE_JDS[currentLang];
            runAnalysis();
        }

        async function runAnalysis(silent = false) {
            let jd = document.getElementById('jdInput').value.trim();
            if (!jd) {
                if (silent) jd = SAMPLE_JDS[currentLang];
                else {
                    alert(currentLang === 'es' ? "Por favor ingresa o pega el texto de la vacante." : "Please paste a job description first.");
                    return;
                }
            }

            try {
                const res = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ jd: jd, lang: currentLang })
                });
                lastAnalysis = await res.json();
                renderResults(lastAnalysis);
            } catch (err) {
                console.error("Analysis error:", err);
            }
        }

        function renderResults(data) {
            document.getElementById('resultPlaceholder').classList.add('hidden');
            document.getElementById('resultContent').classList.remove('hidden');

            document.getElementById('resScore').innerText = `${data.score}%`;
            document.getElementById('resProgressBar').style.width = `${data.score}%`;
            
            const tierBadge = document.getElementById('resTierBadge');
            tierBadge.innerText = data.match_tier;
            if (data.score >= 85) {
                tierBadge.className = 'px-3.5 py-1.5 rounded-full text-xs font-bold bg-green-50 text-green-700 border border-green-200';
            } else if (data.score >= 70) {
                tierBadge.className = 'px-3.5 py-1.5 rounded-full text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200';
            } else {
                tierBadge.className = 'px-3.5 py-1.5 rounded-full text-xs font-bold bg-amber-50 text-amber-700 border border-amber-200';
            }

            // Skills
            const skillsDiv = document.getElementById('resMatchedSkills');
            skillsDiv.innerHTML = '';
            data.matched_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'inline-block bg-indigo-50 text-indigo-700 border border-indigo-200 px-3 py-1 rounded-full text-xs font-semibold';
                span.innerText = skill;
                skillsDiv.appendChild(span);
            });

            // Gaps
            const gapsDiv = document.getElementById('resGaps');
            gapsDiv.innerHTML = '';
            if (data.gaps_with_mitigation && data.gaps_with_mitigation.length > 0) {
                data.gaps_with_mitigation.forEach(gap => {
                    const p = document.createElement('div');
                    p.className = 'p-3 bg-amber-50/70 border border-amber-200/80 rounded-xl';
                    p.innerHTML = `<span class="font-bold text-amber-900">${gap.technology}:</span> <span class="text-amber-800">${gap.mitigation}</span>`;
                    gapsDiv.appendChild(p);
                });
            } else {
                gapsDiv.innerHTML = `<p class="text-xs text-slate-500 italic">${currentLang === 'es' ? 'No se detectaron brechas tecnológicas críticas frente al stack evaluado.' : 'No critical technical gaps identified against core stack.'}</p>`;
            }

            // Highlights
            const hlList = document.getElementById('resHighlights');
            hlList.innerHTML = '';
            data.key_highlights.forEach(h => {
                const li = document.createElement('li');
                li.innerText = h;
                hlList.appendChild(li);
            });

            // Outreach Materials
            document.getElementById('txtLinkedIn').value = data.generated_materials.linkedin_pitch;
            document.getElementById('txtCoverLetter').value = data.generated_materials.cover_letter;

            // Render STAR
            renderStar(data.generated_materials.star_prep);
        }

        function renderStar(scenarios) {
            const container = document.getElementById('starContainer');
            container.innerHTML = '';
            const t = I18N[currentLang];
            
            scenarios.forEach((s, idx) => {
                const card = document.createElement('div');
                card.className = 'bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between';
                card.innerHTML = `
                    <div>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="text-xs font-bold px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-700">${t.star_case} ${idx + 1}</span>
                            <span class="text-xs font-semibold text-slate-500">${s.topic}</span>
                        </div>
                        <h4 class="text-sm font-bold text-slate-900 mb-4">"${s.question}"</h4>
                        
                        <div class="space-y-3 text-xs text-slate-600 mb-4">
                            <div><strong class="text-slate-800">${t.star_situation}</strong> ${s.situation}</div>
                            <div><strong class="text-slate-800">${t.star_task}</strong> ${s.task}</div>
                            <div><strong class="text-slate-800">${t.star_action}</strong> ${s.action}</div>
                        </div>
                    </div>
                    <div class="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 font-medium">
                        <strong>${t.star_result}</strong> ${s.result}
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function renderProfile() {
            if (!profileData) return;

            // Experience
            const expList = document.getElementById('cvExperienceList');
            expList.innerHTML = '';
            const experiences = profileData.experiencia_laboral || profileData.work_experience || [];
            experiences.forEach(exp => {
                const div = document.createElement('div');
                div.className = 'relative mb-6';
                div.innerHTML = `
                    <div class="absolute -left-[31px] top-1.5 w-3 h-3 bg-indigo-600 rounded-full border-2 border-white"></div>
                    <h4 class="text-sm font-bold text-slate-900">${exp.cargo || exp.role}</h4>
                    <div class="text-xs font-semibold text-indigo-600 mb-2">${exp.empresa || exp.company} &bull; <span class="text-slate-500 font-normal">${exp.periodo || exp.period}</span></div>
                    <ul class="list-disc list-inside space-y-1 text-xs text-slate-600">
                        ${(exp.logros || exp.achievements || []).map(l => `<li>${l}</li>`).join('')}
                    </ul>
                `;
                expList.appendChild(div);
            });

            // Skills
            const skillsDiv = document.getElementById('cvSkillsContainer');
            skillsDiv.innerHTML = '';
            const skills = profileData.habilidades_tecnicas || profileData.technical_skills || {};
            for (const [cat, list] of Object.entries(skills)) {
                const group = document.createElement('div');
                group.innerHTML = `
                    <div class="font-bold text-slate-800 mb-1.5 capitalize">${cat.replace(/_/g, ' ')}:</div>
                    <div class="flex flex-wrap gap-1.5">
                        ${list.map(s => `<span class="bg-slate-100 text-slate-700 px-2.5 py-0.5 rounded-md font-medium text-[11px]">${s}</span>`).join('')}
                    </div>
                `;
                skillsDiv.appendChild(group);
            }

            // Education
            const eduList = document.getElementById('cvEducationList');
            eduList.innerHTML = '';
            (profileData.educacion || profileData.education || []).forEach(edu => {
                const li = document.createElement('li');
                li.innerText = `• ${edu}`;
                eduList.appendChild(li);
            });

            // Languages
            const langList = document.getElementById('cvLangList');
            langList.innerHTML = '';
            const langs = profileData.idiomas || profileData.languages || {};
            for (const [k, v] of Object.entries(langs)) {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${k.toUpperCase()}:</strong> ${v}`;
                langList.appendChild(li);
            }
        }

        function copyToClipboard(elementId) {
            const textarea = document.getElementById(elementId);
            textarea.select();
            document.execCommand('copy');
            alert(I18N[currentLang].copied_alert);
        }

        window.onload = init;
    </script>
</body>
</html>
"""

class RousRequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif parsed.path == "/api/profile":
            params = parse_qs(parsed.query)
            lang = params.get("lang", ["es"])[0]
            profile = get_profile(lang)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(profile, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_body) if post_body else {}

            jd = data.get("jd", "")
            lang = data.get("lang", "es")
            profile = get_profile(lang)

            analysis = analyze_job_description(jd, profile, lang=lang)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(analysis, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Quiet standard logs
        pass

def run_server(port=8501):
    server_address = ('127.0.0.1', port)
    try:
        httpd = HTTPServer(server_address, RousRequestHandler)
    except OSError:
        # Fallback to port 8080 if 8501 is busy
        port = 8080
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, RousRequestHandler)

    url = f"http://127.0.0.1:{port}"
    print(f"\n=======================================================")
    print(f"  🤖 Rous AI Career Agent — Web Dashboard Activo")
    print(f"  Abre en tu navegador: {url}")
    print(f"  Presiona Ctrl + C en la terminal para detener el servidor")
    print(f"=======================================================\n")
    
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        httpd.server_close()

if __name__ == "__main__":
    port = 8501
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
