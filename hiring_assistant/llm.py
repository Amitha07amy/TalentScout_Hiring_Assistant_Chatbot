from __future__ import annotations

import json
import os
import random
from typing import Dict, List

from hiring_assistant.models import CandidateProfile
from hiring_assistant.prompts import QUESTION_GEN_PROMPT_TEMPLATE, SYSTEM_PROMPT
from hiring_assistant.question_bank import questions_for_tech

MAX_TECH_FOR_SCREEN = 5
QUESTIONS_PER_TECH = 3


def _bucket_for_tech(tech: str) -> str:
    t = tech.strip().lower()
    if t in {"python", "java", "javascript", "c++", "go", "c#", "r programming", "r"}:
        return "language"
    if t in {"tensorflow", "pytorch", "transformers", "nlp", "rag", "langchain", "llama", "openai api"}:
        return "ml_llm"
    if t in {"pandas", "numpy", "seaborn", "tableau", "powerbi", "eda/etl", "model evaluation"}:
        return "data_analytics"
    if t in {"fastapi", "rest apis", "docker", "linux", "git/github", "container deployment"}:
        return "backend_deploy"
    if t in {"mysql", "postgresql", "nosql", "sql", "mongodb"}:
        return "database"
    if t in {"aws", "azure", "gcp"}:
        return "cloud"
    return "other"


def _select_relevant_tech_stack(candidate: CandidateProfile) -> List[str]:
    tech_stack = candidate.tech_stack
    if len(tech_stack) <= MAX_TECH_FOR_SCREEN:
        return tech_stack

    bucketed: dict[str, List[str]] = {}
    for tech in tech_stack:
        bucket = _bucket_for_tech(tech)
        bucketed.setdefault(bucket, []).append(tech)

    for bucket_techs in bucketed.values():
        random.shuffle(bucket_techs)

    bucket_order = list(bucketed.keys())
    random.shuffle(bucket_order)

    selected: List[str] = []
    # First pass: encourage coverage across different tech areas.
    for bucket in bucket_order:
        if len(selected) >= MAX_TECH_FOR_SCREEN:
            break
        selected.append(bucketed[bucket].pop())

    # Second pass: fill remaining slots randomly from leftovers.
    leftovers: List[str] = []
    for bucket in bucket_order:
        leftovers.extend(bucketed[bucket])
    random.shuffle(leftovers)

    for tech in leftovers:
        if len(selected) >= MAX_TECH_FOR_SCREEN:
            break
        selected.append(tech)

    return selected


def _fallback_questions(tech_stack: List[str]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for tech in tech_stack:
        result[tech] = questions_for_tech(tech)[:QUESTIONS_PER_TECH]
    return result


def _extract_json_object(text: str) -> dict:
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model response")
    return json.loads(text[start : end + 1])


def generate_questions(candidate: CandidateProfile) -> Dict[str, List[str]]:
    tech_stack = _select_relevant_tech_stack(candidate)
    if not tech_stack:
        return {}

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    if not api_key:
        return _fallback_questions(tech_stack)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        user_prompt = QUESTION_GEN_PROMPT_TEMPLATE.format(
            full_name=candidate.full_name,
            years_experience=candidate.years_experience,
            desired_positions=candidate.desired_positions,
            location=candidate.location,
            tech_stack=", ".join(tech_stack),
            questions_per_tech=QUESTIONS_PER_TECH,
        )
        response = client.chat.completions.create(
            model=model_name,
            temperature=0.4,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content or ""
        payload = _extract_json_object(content)
        questions_by_tech = payload.get("questions_by_tech", {})

        normalized: Dict[str, List[str]] = {}
        for tech in tech_stack:
            generated = questions_by_tech.get(tech) or questions_by_tech.get(tech.lower())
            if not isinstance(generated, list) or not generated:
                normalized[tech] = questions_for_tech(tech)[:QUESTIONS_PER_TECH]
                continue

            filtered = [str(q).strip() for q in generated if str(q).strip()]
            normalized[tech] = (
                filtered[:QUESTIONS_PER_TECH] if filtered else questions_for_tech(tech)[:QUESTIONS_PER_TECH]
            )
        return normalized
    except Exception:
        return _fallback_questions(tech_stack)
