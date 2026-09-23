import json
import streamlit as st
from groq import Groq

from utils import call_ai, get_api_key, validate_inputs

MODEL = "llama-3.3-70b-versatile"


def planning_stage(client, context):
    system = """You are a study planner AI.
Create a practical personalized study plan.
Return ONLY valid JSON."""
    user = f"""
Student context:
{json.dumps(context, ensure_ascii=False, indent=2)}

Create a plan with:
- learning_objectives: list of 4-6 objectives
- study_schedule: list of steps with time allocation
- prerequisites: list
- key_concepts: list
- difficulty_notes: string
"""
    return call_ai(client, system, user, "Planning")


def content_stage(client, context, planning):
    system = """You are an educational content generator.
Generate clear, accurate, beginner-friendly study content.
Return ONLY valid JSON."""
    user = f"""
Context:
{json.dumps(context, ensure_ascii=False, indent=2)}

Plan:
{json.dumps(planning, ensure_ascii=False, indent=2)}

Create:
- summary: concise topic explanation
- concepts: list of important concepts with explanations
- examples: list of practical examples
- study_tips: list
- key_takeaways: list
"""
    return call_ai(client, system, user, "Content Generation")


def assessment_stage(client, context, planning, content):
    system = """You are an assessment designer.
Create questions that test understanding of the supplied study material.
Return ONLY valid JSON."""
    user = f"""
Context:
{json.dumps(context, ensure_ascii=False, indent=2)}

Plan:
{json.dumps(planning, ensure_ascii=False, indent=2)}

Content:
{json.dumps(content, ensure_ascii=False, indent=2)}

Create:
- mcqs: 5 objects with question, options, answer, explanation
- short_questions: 3 objects with question and answer
- challenge_question: object with question and answer
"""
    return call_ai(client, system, user, "Assessment")


def review_stage(client, context, planning, content, assessment):
    system = """You are a strict educational reviewer.
Check the study pack for correctness, completeness, clarity, duplication, and alignment with the student's goal.
Return ONLY valid JSON."""
    user = f"""
Context:
{json.dumps(context, ensure_ascii=False, indent=2)}

Planning:
{json.dumps(planning, ensure_ascii=False, indent=2)}

Content:
{json.dumps(content, ensure_ascii=False, indent=2)}

Assessment:
{json.dumps(assessment, ensure_ascii=False, indent=2)}

Return:
- quality_score: number from 1 to 10
- strengths: list
- issues: list
- corrections: list
- refinement_instructions: list
"""
    return call_ai(client, system, user, "Review")


def refinement_stage(client, context, planning, content, assessment, review):
    system = """You are a final educational editor.
Improve the study pack using the review feedback.
Return ONLY valid JSON."""
    user = f"""
Context:
{json.dumps(context, ensure_ascii=False, indent=2)}

Planning:
{json.dumps(planning, ensure_ascii=False, indent=2)}

Content:
{json.dumps(content, ensure_ascii=False, indent=2)}

Assessment:
{json.dumps(assessment, ensure_ascii=False, indent=2)}

Review:
{json.dumps(review, ensure_ascii=False, indent=2)}

Produce the final study pack with:
- title
- study_plan
- summary
- key_concepts
- examples
- study_tips
- mcqs
- short_questions
- challenge_question
- key_takeaways
"""
    return call_ai(client, system, user, "Refinement")


def run_study_workflow(subject, topic, level, study_time, language, goal):
    validate_inputs(subject, topic)

    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file locally "
            "or Streamlit Secrets when deploying."
        )

    client = Groq(api_key=api_key)

    context = {
        "subject": subject,
        "topic": topic,
        "level": level,
        "study_time": study_time,
        "language": language,
        "goal": goal or "Understand the topic and build practical knowledge.",
    }

    progress = st.progress(0, text="Starting workflow...")

    planning = planning_stage(client, context)
    progress.progress(20, text="Planning completed...")

    content = content_stage(client, context, planning)
    progress.progress(40, text="Content generation completed...")

    assessment = assessment_stage(client, context, planning, content)
    progress.progress(60, text="Assessment completed...")

    review = review_stage(client, context, planning, content, assessment)
    progress.progress(80, text="Review completed...")

    final = refinement_stage(
        client, context, planning, content, assessment, review
    )
    progress.progress(100, text="Final study pack ready!")

    return {
        "context": context,
        "planning": planning,
        "content": content,
        "assessment": assessment,
        "review": review,
        "final": final,
    }


def render_final_pack(final):
    def bullets(items):
        if not items:
            return "No items available."
        return "\n".join(f"- {item}" for item in items)

    md = f"# {final.get('title', 'AI Study Pack')}\n\n"

    md += "## 📅 Study Plan\n"
    plan = final.get("study_plan", [])
    if isinstance(plan, list):
        md += bullets(plan)
    else:
        md += str(plan)

    md += "\n\n## 📖 Summary\n"
    md += str(final.get("summary", ""))

    md += "\n\n## 🧠 Key Concepts\n"
    concepts = final.get("key_concepts", [])
    if isinstance(concepts, list):
        for item in concepts:
            if isinstance(item, dict):
                md += f"\n### {item.get('concept', 'Concept')}\n"
                md += f"{item.get('explanation', '')}\n"
            else:
                md += f"- {item}\n"
    else:
        md += str(concepts)

    md += "\n## 💡 Examples\n"
    examples = final.get("examples", [])
    md += bullets(examples) if isinstance(examples, list) else str(examples)

    md += "\n\n## 🎯 Study Tips\n"
    tips = final.get("study_tips", [])
    md += bullets(tips) if isinstance(tips, list) else str(tips)

    md += "\n\n## 📝 MCQs\n"
    for i, q in enumerate(final.get("mcqs", []), 1):
        md += f"\n### {i}. {q.get('question', '')}\n"
        for option in q.get("options", []):
            md += f"- {option}\n"
        md += f"**Answer:** {q.get('answer', '')}\n"
        md += f"**Explanation:** {q.get('explanation', '')}\n"

    md += "\n## ✍️ Short Questions\n"
    for i, q in enumerate(final.get("short_questions", []), 1):
        md += f"\n**{i}. {q.get('question', '')}**\n"
        md += f"Answer: {q.get('answer', '')}\n"

    challenge = final.get("challenge_question", {})
    md += "\n## 🚀 Challenge Question\n"
    md += f"**Question:** {challenge.get('question', '')}\n\n"
    md += f"**Answer:** {challenge.get('answer', '')}\n"

    md += "\n## ✅ Key Takeaways\n"
    takeaways = final.get("key_takeaways", [])
    md += bullets(takeaways) if isinstance(takeaways, list) else str(takeaways)

    return md
