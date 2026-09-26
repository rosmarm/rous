#!/usr/bin/env python3
"""
Rous - AI Career Agent for Rosmar Mendoza
CLI tool to query CV data, evaluate job descriptions, and prepare interview answers.
"""

import os
import sys
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"

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

def quick_evaluate_job(jd_text: str, profile: dict) -> dict:
    """
    Offline heuristic analyzer for quick evaluation without requiring an API key.
    """
    skills = profile.get("habilidades_tecnicas", {})
    all_skills = []
    for cat in skills.values():
        if isinstance(cat, list):
            all_skills.extend(cat)

    jd_lower = jd_text.lower()
    matched = [s for s in all_skills if s.lower() in jd_lower]
    
    score = min(100, int((len(matched) / max(1, len(all_skills[:10]))) * 85) + 15) if matched else 30
    
    return {
        "estimated_match_score": f"{score}%",
        "matched_skills": matched,
        "recommended_focus": "Golang / Microservices / AWS" if "golang" in jd_lower or "microservice" in jd_lower else "Python / APIs / Cloud"
    }

def print_profile_summary(profile: dict):
    print("=" * 60)
    print(f"  ROUS - Career Agent for {profile.get('nombre', profile.get('name'))}")
    print(f"  Title: {profile.get('titulo', profile.get('title'))}")
    print(f"  Email: {profile.get('informacion_contacto', {}).get('correo_electronico', profile.get('contact_information', {}).get('email'))}")
    print("=" * 60)
    print("\n[Work Experience]")
    for exp in profile.get("experiencia_laboral", profile.get("work_experience", [])):
        company = exp.get("empresa", exp.get("company"))
        role = exp.get("cargo", exp.get("role"))
        period = exp.get("periodo", exp.get("period"))
        print(f" • {role} @ {company} ({period})")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Rous - AI Career Agent for Rosmar Mendoza")
    parser.add_argument("--lang", choices=["es", "en"], default="es", help="Preferred language (es/en)")
    parser.add_argument("--info", action="store_true", help="Display Rosmar's profile summary")
    parser.add_argument("--evaluate", type=str, help="Path to text file containing a Job Description to evaluate")
    parser.add_argument("--prompt", action="store_true", help="Print the full System Prompt for Rous")

    args = parser.parse_args()

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
        res = quick_evaluate_job(jd_text, profile)
        print("\n--- Heuristic Job Matching Result ---")
        print(f"Estimated Match Score: {res['estimated_match_score']}")
        print(f"Matched Skills: {', '.join(res['matched_skills']) if res['matched_skills'] else 'None directly identified'}")
        print(f"Strategic Focus: {res['recommended_focus']}")
        print("\nTip: Pass this Job Description along with prompts/job_match_prompt.md to ChatGPT or Claude for full LLM analysis.")
        return

    # Default action
    print_profile_summary(profile)
    print("\nUsage:")
    print("  python3 src/agent.py --info")
    print("  python3 src/agent.py --prompt")
    print("  python3 src/agent.py --evaluate path/to/job_description.txt")

if __name__ == "__main__":
    main()
