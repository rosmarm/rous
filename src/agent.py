#!/usr/bin/env python3
"""
Rous - AI Career Agent for Rosmar Mendoza
CLI tool & launcher to query CV data, evaluate job descriptions, and launch web dashboard.
"""

import os
import sys
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))
from analyzer import analyze_job_description

def load_profile(lang="es"):
    filename = "cv_rosmar_es.json" if lang == "es" else "cv_rosmar_en.json"
    file_path = DATA_DIR / filename
    if not file_path.exists():
        file_path = DATA_DIR / "cv_rosmar_es.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_system_prompt():
    prompt_path = PROMPTS_DIR / "system_prompt.md"
    if prompt_path.exists():
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def print_profile_summary(profile: dict):
    print("=" * 65)
    print(f"  🤖 ROUS - Career Agent for {profile.get('nombre', profile.get('name'))}")
    print(f"  Title: {profile.get('titulo', profile.get('title'))}")
    print(f"  Email: {profile.get('informacion_contacto', {}).get('correo_electronico', profile.get('contact_information', {}).get('email'))}")
    print("=" * 65)
    print("\n[Work Experience]")
    for exp in profile.get("experiencia_laboral", profile.get("work_experience", [])):
        company = exp.get("empresa", exp.get("company"))
        role = exp.get("cargo", exp.get("role"))
        period = exp.get("periodo", exp.get("period"))
        print(f" • {role} @ {company} ({period})")
    
    print("\n[Technical Skills]")
    skills = profile.get("habilidades_tecnicas", profile.get("technical_skills", {}))
    for cat, items in skills.items():
        if isinstance(items, list):
            print(f" • {cat.replace('_', ' ').title()}: {', '.join(items)}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Rous - AI Career Agent for Rosmar Mendoza")
    parser.add_argument("--web", action="store_true", help="Launch the local Web Dashboard in your browser")
    parser.add_argument("--lang", choices=["es", "en"], default="es", help="Preferred language (es/en)")
    parser.add_argument("--info", action="store_true", help="Display Rosmar's profile summary")
    parser.add_argument("--evaluate", type=str, help="Path to text file containing a Job Description to evaluate")
    parser.add_argument("--prompt", action="store_true", help="Print the full System Prompt for Rous")

    args = parser.parse_args()

    if args.web:
        from web_ui import run_server
        run_server(8501)
        return

    if args.prompt:
        print(load_system_prompt())
        return

    profile = load_profile(args.lang)

    if args.evaluate:
        jd_path = Path(args.evaluate)
        if not jd_path.exists():
            print(f"Error: File not found {args.evaluate}")
            sys.exit(1)
        with open(jd_path, "r", encoding="utf-8") as f:
            jd_text = f.read()
        res = analyze_job_description(jd_text, profile, lang=args.lang)
        
        print("\n" + "=" * 65)
        print(f"  🎯 ROUS JOB MATCH ANALYSIS: {res['score']}% ({res['match_tier']})")
        print("=" * 65)
        print(f"\n[Matched Skills]:\n • {', '.join(res['matched_skills']) if res['matched_skills'] else 'None'}")
        
        if res.get("gaps_with_mitigation"):
            print("\n[Mitigation Strategies for Gaps]:")
            for gap in res["gaps_with_mitigation"]:
                print(f" • {gap['technology']}: {gap['mitigation']}")

        print("\n[Key Strategic Highlights]:")
        for h in res["key_highlights"]:
            print(f" • {h}")

        print("\n[Generated LinkedIn Message]:")
        print("-" * 50)
        print(res["generated_materials"]["linkedin_pitch"])
        print("-" * 50)
        return

    # Default action
    print_profile_summary(profile)
    print("\nComandos útiles:")
    print("  python3 src/agent.py --web          # 🌐 Abre la interfaz Web visual en tu navegador")
    print("  python3 src/agent.py --info         # 👤 Muestra el resumen del perfil")
    print("  python3 src/agent.py --evaluate jd.txt # 🎯 Evalúa una vacante desde la terminal")
    print("  python3 src/agent.py --prompt       # 📋 Imprime el System Prompt maestro")

if __name__ == "__main__":
    main()
