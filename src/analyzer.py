"""
Core Analysis Engine for Rous - AI Career Agent for Rosmar Mendoza
Evaluates Job Descriptions, computes compatibility, identifies gaps,
and synthesizes tailored application materials & STAR interview responses.
"""

import re
from typing import Dict, List, Any

# Knowledge Base: Rosmar's Skills and Synonyms/Aliases
SKILL_TAXONOMY = {
    "Backend & Languages": {
        "Golang": ["golang", "go ", "go/", "go,", "go microservices"],
        "Python": ["python", "python3", "fastapi", "django"],
        "Java": ["java ", "java8", "java11", "java17", "jvm"],
        "SQL": ["sql", "postgresql", "postgres", "mysql", "relational database", "rdbms"],
        ".NET": [".net", "c#", "dotnet"]
    },
    "Architecture & APIs": {
        "Microservicios": ["microservice", "microservicios", "micro-service", "distributed systems", "sistemas distribuidos"],
        "REST APIs": ["rest", "restful", "api", "apis", "endpoints", "json", "http"],
        "Concurrencia / Alta Concurrencia": ["concurrency", "concurrencia", "goroutines", "goroutine", "channels", "high throughput", "alto tráfico", "low latency", "baja latencia"],
        "Clean Architecture / Patrones": ["clean architecture", "hexagonal", "solid", "design patterns", "patrones de diseño", "dry"]
    },
    "Bases de Datos & Cloud": {
        "PostgreSQL": ["postgresql", "postgres", "psql"],
        "MySQL": ["mysql"],
        "AWS": ["aws", "amazon web services", "s3", "ec2", "lambda", "rds", "cloud"],
        "Docker": ["docker", "container", "containers", "contenedores"],
        "Git": ["git", "github", "gitlab", "version control"]
    },
    "IA & Productividad": {
        "AI-Assisted Development": ["cursor", "claude", "copilot", "chatgpt", "generative ai", "ia generativa", "llm", "ai tools"],
        "Jira / Gestión": ["jira", "confluence", "scrum", "agile", "kanban", "sprints"]
    },
    "Operaciones & Metodologías": {
        "On-Call & Soporte SLA": ["on-call", "on call", "guardias", "sla", "incident management", "soporte l2", "troubleshooting", "producción"],
        "CI/CD": ["ci/cd", "ci / cd", "pipeline", "continuous integration", "despliegues", "deployments"],
        "Unit Testing": ["testing", "unit test", "pruebas unitarias", "test-driven", "tdd", "go test", "pytest"]
    }
}

# Known Adjacent Skills that Rosmar can easily adopt / mitigate
MITIGATION_STRATEGIES = {
    "kubernetes": "Aunque la vacante menciona Kubernetes/K8s, Rosmar cuenta con sólida base en contenedores Docker y microservicios en producción en MercadoLibre bajo arquitecturas cloud orquestadas.",
    "k8s": "Familiaridad con Docker y despliegues de microservicios distribuidos en alta escala, con rápida curva de adaptación a clusters de Kubernetes.",
    "kafka": "Experiencia con arquitectura de microservicios y procesamiento asíncrono/APIs de alto tráfico en MercadoLibre, lo que facilita el trabajo con event-driven streaming en Kafka o RabbitMQ.",
    "redis": "Amplio dominio de optimización de APIs y bases de datos relacionales (PostgreSQL/MySQL), con comprensión directa de estrategias de caching en memoria.",
    "nosql": "Sólida experiencia en modelado y rendimiento de datos SQL en Mo Technologies y MercadoLibre, extrapolable a almacenes NoSQL (DynamoDB, MongoDB).",
    "graphql": "Profundo dominio de diseño de APIs RESTful y contratos de datos, permitiendo una transición natural a schemas de GraphQL.",
    "terraform": "Experiencia con servicios cloud de AWS y despliegues de infraestructura moderna."
}

MITIGATION_STRATEGIES_EN = {
    "kubernetes": "While the posting mentions Kubernetes/K8s, Rosmar brings extensive hands-on experience with Docker containerization and production microservices at MercadoLibre, ensuring an immediate transition to K8s orchestration.",
    "k8s": "Hands-on experience with Docker containers and distributed microservices at MercadoLibre scale allows for a frictionless ramp-up with Kubernetes clusters.",
    "kafka": "Proven background architecting microservices and high-throughput, low-latency APIs at MercadoLibre, making message-driven architecture in Kafka or RabbitMQ a natural extension.",
    "redis": "Deep experience optimizing backend APIs and relational databases (PostgreSQL/MySQL), with direct command of in-memory caching strategies and latency reduction.",
    "nosql": "Extensive track record in relational schema design and query tuning in PostgreSQL, smoothly adaptable to document/NoSQL stores like DynamoDB or MongoDB.",
    "graphql": "Strong expertise in RESTful API contract modeling, making GraphQL schema design, resolvers, and query optimization effortless to adopt.",
    "terraform": "Hands-on background with AWS cloud infrastructure integrations and automated CI/CD deployment pipelines."
}

SKILL_NAMES_EN = {
    "Microservicios": "Microservices",
    "Concurrencia / Alta Concurrencia": "High Concurrency & Throughput",
    "Clean Architecture / Patrones": "Clean Architecture & Design Patterns",
    "On-Call & Soporte SLA": "On-Call & SLA Operations",
    "Jira / Gestión": "Jira & Agile Management",
    "Unit Testing": "Unit Testing & QA"
}

def analyze_job_description(jd_text: str, profile: dict, lang: str = "es") -> Dict[str, Any]:
    """
    Evaluates a Job Description against Rosmar's profile.
    Returns matched skills, missing skills, match score, strategic advice,
    and auto-generated outreach templates.
    """
    if not jd_text or len(jd_text.strip()) < 20:
        return {
            "error": "El texto de la vacante es muy corto o está vacío." if lang == "es" else "Job description is too short."
        }

    jd_clean = " " + re.sub(r'[^\w\s\-\+\#\.\/]', ' ', jd_text.lower()) + " "

    matched_by_cat = {}
    all_matched = []
    
    # Check for skills in taxonomy
    for cat_name, skills in SKILL_TAXONOMY.items():
        matched_in_cat = []
        for skill_name, aliases in skills.items():
            for alias in aliases:
                # search with word boundaries or space padding
                pattern = r'(?:\b|\s)' + re.escape(alias) + r'(?:\b|\s)'
                if re.search(pattern, jd_clean):
                    matched_in_cat.append(skill_name)
                    all_matched.append(skill_name)
                    break
        if matched_in_cat:
            matched_by_cat[cat_name] = matched_in_cat

    # Identify potential gaps / external technologies in JD
    detected_gaps = []
    for tech, mit_text in MITIGATION_STRATEGIES.items():
        pattern = r'(?:\b|\s)' + re.escape(tech) + r'(?:\b|\s)'
        if re.search(pattern, jd_clean) and tech not in [s.lower() for s in all_matched]:
            mit_str = mit_text if lang == "es" else MITIGATION_STRATEGIES_EN.get(tech, f"Strong foundation in Docker & microservices at MercadoLibre enables rapid adoption of {tech.upper()}.")
            detected_gaps.append({
                "technology": tech.upper(),
                "mitigation": mit_str
            })

    # Scoring algorithm
    # Base score depends on core matches: Golang, Python, Microservices, APIs, AWS, SQL
    core_skills = ["Golang", "Python", "Microservicios", "REST APIs", "SQL", "AWS", "Docker"]
    core_matches = [s for s in core_skills if s in all_matched]
    
    # Calculate score
    if "Golang" in all_matched or "Python" in all_matched:
        base_score = 65
    elif any(s in all_matched for s in ["Backend & Languages", "Microservicios", "REST APIs"]):
        base_score = 50
    else:
        base_score = 35

    bonus = min(35, len(all_matched) * 5)
    penalty = min(20, len(detected_gaps) * 4)
    final_score = max(20, min(98, base_score + bonus - penalty))

    # Match Level Tag
    if final_score >= 85:
        match_tier = "🔥 Compatibilidad Alta (Strong Match)" if lang == "es" else "🔥 Strong Match"
        color = "green"
    elif final_score >= 70:
        match_tier = "✅ Compatibilidad Media-Alta (Solid Match)" if lang == "es" else "✅ Solid Match"
        color = "blue"
    else:
        match_tier = "⚠️ Compatibilidad Parcial (Moderate / Stretch)" if lang == "es" else "⚠️ Moderate Match"
        color = "orange"

    # Key highlights to promote
    highlights = generate_tailored_highlights(all_matched, lang)
    
    # Generated Outreach Materials
    cover_letter = generate_cover_letter(all_matched, detected_gaps, final_score, lang)
    linkedin_pitch = generate_linkedin_message(all_matched, lang)
    display_matched = [SKILL_NAMES_EN.get(s, s) for s in list(set(all_matched))] if lang == "en" else list(set(all_matched))

    return {
        "score": final_score,
        "match_tier": match_tier,
        "color": color,
        "matched_skills": display_matched,
        "matched_by_category": matched_by_cat,
        "gaps_with_mitigation": detected_gaps,
        "key_highlights": highlights,
        "generated_materials": {
            "cover_letter": cover_letter,
            "linkedin_pitch": linkedin_pitch,
            "star_prep": star_prep
        }
    }

def generate_tailored_highlights(matched: List[str], lang: str) -> List[str]:
    """Generates 3-4 bullet points tailored for the CV header."""
    is_go = "Golang" in matched or "Concurrencia / Alta Concurrencia" in matched
    is_py = "Python" in matched
    
    if lang == "es":
        bullets = []
        if is_go:
            bullets.append("Desarrolladora Backend Semi-Senior especializada en Golang, diseño de microservicios y APIs RESTful de alto rendimiento en MercadoLibre.")
        elif is_py:
            bullets.append("Desarrolladora Backend Semi-Senior con experiencia sólida en Python (FastAPI, Django) y arquitecturas en la nube (AWS, PostgreSQL).")
        else:
            bullets.append("Desarrolladora Backend Semi-Senior con experiencia en sistemas distribuidos, microservicios y arquitecturas cloud de alto impacto.")

        bullets.append("Pionera en productividad asistida por IA (Cursor, Claude) para refactorización ágil, generación de pruebas y aceleración de entregas.")
        bullets.append("Experiencia operativa en producción: guardias On-Call bajo SLAs estrictos, diagnóstico de incidentes L2 y observabilidad.")
        return bullets
    else:
        bullets = []
        if is_go:
            bullets.append("Mid-Level Backend Developer specialized in Golang, microservices architecture, and high-throughput REST APIs at MercadoLibre.")
        elif is_py:
            bullets.append("Mid-Level Backend Developer experienced in Python (FastAPI, Django), PostgreSQL, and AWS cloud solutions.")
        else:
            bullets.append("Mid-Level Backend Software Developer experienced in distributed systems, microservices, and high-impact cloud architectures.")

        bullets.append("AI-augmented development champion (Cursor, Claude) for high-velocity refactoring, code quality, and fast time-to-market.")
        bullets.append("Proven production operations: On-Call SLA support, Level 2 incident troubleshooting, and distributed systems monitoring.")
        return bullets

def generate_linkedin_message(matched: List[str], lang: str) -> str:
    """Generates a concise, high-converting recruiter message for LinkedIn."""
    tech_str = "Golang y microservicios de alto tráfico" if "Golang" in matched else "Python (FastAPI/Django) y arquitecturas cloud"
    
    if lang == "es":
        return f"""Hola [Nombre del Reclutador], ¡un gusto saludarte!

Vi la oportunidad para el rol de Backend Developer y me llamó mucho la atención la propuesta del equipo. 

Como desarrolladora backend Semi-Senior, cuento con experiencia construyendo microservicios y APIs escalables en {tech_str}, respaldada por mi trayectoria en MercadoLibre y empresas fintech. Además, integro herramientas de IA (Cursor, Claude) en mi flujo diario para optimizar la velocidad y calidad de entrega, y tengo experiencia en guardias On-Call y resolución de incidencias en producción.

Me encantaría conocer más sobre los desafíos técnicos del equipo y compartir cómo puedo sumar valor. ¿Tendrías 10 minutos esta semana para una breve charla?

Saludos cordiales,
Rosmar Alejandra Mendoza
LinkedIn: linkedin.com/in/rosmar-mendoza | GitHub: github.com/rosmarm"""
    else:
        tech_str_en = "Golang and high-throughput microservices" if "Golang" in matched else "Python (FastAPI/Django) and cloud architectures"
        return f"""Hi [Recruiter Name], hope you're having a great week!

I came across the Backend Developer opening and was very impressed by the team's mission.

As a Mid-Level Backend Developer, I bring hands-on experience building scalable microservices and resilient APIs with {tech_str_en}, backed by my work at MercadoLibre and fintech environments. I also leverage AI-assisted development tools (Cursor, Claude) to drive delivery velocity and high code quality, along with production On-Call incident handling experience under strict SLAs.

I would love to learn more about the team's engineering goals and discuss how I can contribute. Would you be open to a quick 10-minute chat this week?

Best regards,
Rosmar Alejandra Mendoza
LinkedIn: linkedin.com/in/rosmar-mendoza | GitHub: github.com/rosmarm"""

def generate_cover_letter(matched: List[str], gaps: List[Dict], score: int, lang: str) -> str:
    """Generates an ATS-tailored cover letter."""
    if lang == "es":
        return f"""Estimado equipo de Selección / Líder de Ingeniería,

Les escribo con gran entusiasmo para presentar mi candidatura a la posición de Backend Developer. Mi trayectoria como Ingeniera en Informática y desarrolladora backend Semi-Senior en compañías de alto impacto como MercadoLibre y Mo Technologies me permite aportar soluciones escalables, código robusto y entrega continua desde el primer día.

Durante mi etapa en MercadoLibre, me especialicé en el desarrollo y mantenimiento de microservicios en Golang, operando APIs de alto tráfico bajo estrictos acuerdos de nivel de servicio (SLA) y participando activamente en rotaciones de soporte On-Call. Asimismo, mi experiencia previa en Mo Technologies me otorgó un profundo dominio en Python (FastAPI, Django), modelado relacional en PostgreSQL y despliegues en AWS.

Un factor diferencial de mi perfil es la adopción proactiva de Inteligencia Artificial (herramientas como Cursor y Claude) en mi ciclo de desarrollo, logrando refactorizaciones eficientes, mayor cobertura de pruebas y tiempos de ciclo reducidos sin comprometer la seguridad ni la mantenibilidad.

Estoy convencida de que mi combinación de rigor técnico, experiencia en sistemas distribuidos y mentalidad orientada a resultados será un activo de gran valor para su equipo. Agradezco de antemano su tiempo y consideración, y quedo a su total disposición para profundizar en una entrevista.

Atentamente,
Rosmar Alejandra Mendoza Canchica
mendozarosmar@gmail.com | +57 3173820550
LinkedIn: https://linkedin.com/in/rosmar-mendoza | GitHub: https://github.com/rosmarm"""
    else:
        return f"""Dear Hiring Team & Engineering Leadership,

I am writing to express my strong interest in the Backend Developer position. With a B.S. in Computer Engineering and a proven track record as a Mid-Level Backend Developer at high-scale tech organizations like MercadoLibre and fintech innovators like Mo Technologies, I am confident in my ability to build scalable backend architectures and deliver measurable engineering impact.

At MercadoLibre, I specialized in architecting and maintaining high-throughput microservices in Golang, supporting mission-critical APIs under strict SLAs, and executing On-Call production rotations. Previously at Mo Technologies, I engineered RESTful APIs with Python (FastAPI and Django), designed robust PostgreSQL data models, and deployed cloud integrations across AWS.

A key differentiator in my workflow is the strategic integration of AI-assisted engineering tools (Cursor, Claude), which accelerates feature delivery, streamlines refactoring, and elevates code testing standards while maintaining architectural discipline.

I look forward to discussing how my technical background in distributed systems, production resilience, and passion for engineering excellence align with your team's objectives. Thank you for your time and consideration.

Sincerely,
Rosmar Alejandra Mendoza Canchica
mendozarosmar@gmail.com | +57 3173820550
LinkedIn: https://linkedin.com/in/rosmar-mendoza | GitHub: https://github.com/rosmarm"""

def generate_star_scenarios(matched: List[str], lang: str) -> List[Dict[str, str]]:
    """Generates structured STAR interview answers relevant to the vacancy."""
    if lang == "es":
        return [
            {
                "topic": "Gestión de Incidencias en Producción & Guardias On-Call",
                "question": "¿Cómo manejas una caída crítica o latencia elevada en un microservicio en producción?",
                "situation": "En MercadoLibre, durante una guardia On-Call, uno de los microservicios core de alta concurrencia presentó un pico inusual de latencia que amenazaba los SLAs del servicio.",
                "task": "Identificar la causa raíz con rapidez, mitigar el impacto para los usuarios finales y restablecer el rendimiento normal sin provocar efectos colaterales.",
                "action": "Analicé las métricas y logs del servicio, identificando saturación en conexiones a la base de datos debido a un endpoint que no liberaba recursos eficientemente. Apliqué un fix temporal de throttling y escalado de pods mientras refactorizaba el pool de conexiones en Golang.",
                "result": "El servicio recuperó su latencia óptima en menos de 20 minutos, cumpliendo el SLA. Posteriormente documenté el post-mortem e implementé alertas preventivas en el pipeline."
            },
            {
                "topic": "Productividad con Inteligencia Artificial (Cursor / Claude)",
                "question": "¿Cómo integras herramientas de IA en tu desarrollo diario sin descuidar la calidad del código?",
                "situation": "En proyectos de backend con requerimientos complejos de refactorización y cobertura de pruebas unitarias bajo plazos ajustados.",
                "task": "Acelerar la entrega de features manteniendo estándares altos de Clean Code y cobertura de tests.",
                "action": "Utilizo Cursor y Claude como pair-programmers para generar boilerplate, explorar casos límite en tests unitarios y proponer alternativas de refactorización idiomática en Golang y Python, siempre validando y auditando cada línea manualmente.",
                "result": "Reducción estimada del 35% en tiempo de desarrollo de pruebas y tareas repetitivas, permitiéndome enfocar más tiempo en arquitectura y lógica de negocio crítica."
            }
        ]
    else:
        return [
            {
                "topic": "Production Incident Management & On-Call",
                "question": "Tell me about a time you handled a critical production incident under pressure.",
                "situation": "At MercadoLibre, during an On-Call rotation, a critical microservice experienced a sudden latency spike threatening service SLAs.",
                "task": "Quickly isolate the root cause, mitigate user impact, and restore normal performance within strict incident response limits.",
                "action": "Inspected real-time logs and telemetry, traced the bottleneck to connection pool starvation on a database dependency, and deployed mitigation throttling while refactoring the Golang connection pool handling.",
                "result": "Restored baseline response times within 20 minutes well within SLA limits, followed by a detailed post-mortem and automated monitoring alarms."
            },
            {
                "topic": "AI-Augmented Engineering (Cursor / Claude)",
                "question": "How do you leverage AI tools in your development workflow?",
                "situation": "Delivering high-velocity backend features and thorough test suites under tight sprint commitments.",
                "task": "Boost engineering throughput while safeguarding architectural rigor and code maintainability.",
                "action": "I use Cursor and Claude as interactive pair programmers to draft comprehensive test edge cases, refactor boilerplate, and benchmark Go routines, auditing every recommendation through peer reviews and CI checks.",
                "result": "Accelerated test suite delivery by ~35% and minimized regressions while maintaining full focus on core business logic and scalability."
            }
        ]
