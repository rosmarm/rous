# 🤖 Rous — AI Career Agent for Rosmar Mendoza

> **Rous** is a bilingual AI Career Agent and Technical Advocate designed to consult, analyze, and strategically position the professional profile of **Rosmar Mendoza (Backend Software Developer)** for international and Latin American engineering roles.

[![GitHub](https://img.shields.io/badge/GitHub-rosmarmendoza-black?logo=github)](https://github.com/rosmarmendoza)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-rosmar--mendoza-blue?logo=linkedin)](https://linkedin.com/in/rosmar-mendoza)
[![Profile](https://img.shields.io/badge/Focus-Backend%20Engineer%20(Golang%20%2F%20Python)-brightgreen)](#)
[![Languages](https://img.shields.io/badge/Languages-Spanish%20%7C%20English-orange)](#)

---

## 🎯 Purpose

When applying for engineering opportunities, tailoring your profile, evaluating match against complex Job Descriptions (JDs), and crafting personalized pitches takes significant time. **Rous** acts as a 24/7 personal career agent that:

1. **Evaluates Job Fit**: Computes a compatibility match score (0–100%) against any Job Description.
2. **Bilingual Agility**: Automatically handles queries, pitches, and interviews in **Spanish** or **English**.
3. **Identifies Strengths & Gaps**: Accurately maps requirements to Rosmar's experience (MercadoLibre, Mo Technologies, etc.) and offers mitigation strategies for missing keywords.
4. **Generates Application Artifacts**: Writes high-conversion cover letters, LinkedIn recruiter outreach messages, and ATS-tailored CV summaries.
5. **Simulates Interviews**: Prepares STAR-format responses for behavioral rounds and deep-dive technical questions on Golang microservices, APIs, and cloud architecture.

---

## 📁 Repository Structure

```text
rous-agent/
├── README.md                     # Comprehensive project documentation
├── requirements.txt              # Optional dependencies for LLM integration
├── .env.example                  # Environment configuration template
├── .gitignore                    # Prevents leaking sensitive files or tokens
├── data/
│   ├── cv_rosmar_es.json         # Structured profile in Spanish
│   └── cv_rosmar_en.json         # Structured profile in English
├── prompts/
│   ├── system_prompt.md          # Master bilingual system prompt for LLMs
│   ├── job_match_prompt.md       # Template for analyzing Job Descriptions
│   └── interview_prep_prompt.md  # Template for STAR interview preparation
└── src/
    └── agent.py                  # Standalone CLI tool to query profile & run evaluations
```

---

## 🚀 Quick Start

### 1. Using Rous as a CLI Tool

Clone or navigate to the directory:
```bash
cd rous-agent
```

Check profile summary:
```bash
python3 src/agent.py --info
```

Check profile in English:
```bash
python3 src/agent.py --info --lang en
```

Evaluate a Job Description offline:
```bash
python3 src/agent.py --evaluate path/to/job_description.txt
```

Print the master System Prompt to copy into ChatGPT or Claude:
```bash
python3 src/agent.py --prompt
```

---

### 2. Using Rous with AI Platforms (ChatGPT, Claude, Cursor)

You can load the master prompt into your preferred AI tool:

1. Open [`prompts/system_prompt.md`](prompts/system_prompt.md).
2. Copy the content into:
   - **ChatGPT / Custom GPT**: Paste into the *Instructions* box.
   - **Claude Projects**: Add to *Project Knowledge* & *Custom Instructions*.
   - **Cursor / Copilot**: Add as an agent rule or context document.
3. Test with queries like:
   - *"Rous, evaluate this Senior Go Developer opportunity: [paste JD]"*
   - *"Rous, ayúdame a preparar una respuesta STAR para una pregunta sobre cómo manejo incidencias en producción basándome en MercadoLibre."*

---

## 🛠️ Ground Truth Profile Summary

- **Candidate**: Rosmar Alejandra Mendoza Canchica
- **Primary Roles**: Backend Software Developer | Golang & Python Engineer | Microservices Specialist
- **Core Companies**:
  - **MercadoLibre** (*Aug 2023 – Mar 2026*): Backend Developer (Golang microservices, high-traffic APIs, On-call SLA support, AI productivity).
  - **Mo Technologies** (*2022 – 2023*): Backend Intern & L2 Support (Python, FastAPI, Django, PostgreSQL, AWS).
- **Core Stack**: Golang, Python, Java, SQL, FastAPI, Django, PostgreSQL, MySQL, AWS, Docker, Git, Cursor, Claude.
- **Education**: B.S. in Computer Engineering (UNET) & Certified Tech Developer (Digital House).

---

## 🚢 Publishing to GitHub

To push this repository to your personal GitHub account ([github.com/rosmarmendoza](https://github.com/rosmarmendoza)):

1. Create a new empty repository on GitHub named `rous-agent` (or `rous-career-agent`).
2. Run the following commands:
```bash
cd rous-agent
git init
git add .
git commit -m "feat: initial commit for Rous AI Career Agent"
git branch -M main
git remote add origin https://github.com/rosmarmendoza/rous-agent.git
git push -u origin main
```

---

## 📄 License
MIT License. Created by [Rosmar Mendoza](https://github.com/rosmarmendoza).
