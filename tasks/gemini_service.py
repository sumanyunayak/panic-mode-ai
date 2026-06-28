import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

def call_gemini(messages):
    prompt = messages[-1]["parts"][0]["text"]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if not response.text:
        raise Exception("No text returned from Vertex AI Gemini")

    return response.text

def triage_situation(situation, mood):
    prompt = f"""
You are an AI Emergency Room doctor for productivity crises. 
A user is in panic mode. Analyze their situation and respond ONLY in this exact JSON format:

{{
  "diagnosis": "One line crisis title (e.g. Presentation Crisis)",
  "crisis_type": "Academic Emergency / Work Emergency / Presentation Emergency / Client Emergency / General Emergency",
  "severity": "LOW or MEDIUM or HIGH or CRITICAL",
  "success_probability": <number 0-100>,
  "probability_reason": [
  "Reason 1",
  "Reason 2",
  "Reason 3"
],
  "critical_threat": "The single biggest risk right now",
  "do_not_list": [
    "Thing to avoid 1",
    "Thing to avoid 2",
    "Thing to avoid 3",
    "Thing to avoid 4"
  ],
  "tasks": [
    {{
      "title": "Task name",
      "duration_minutes": <number>,
      "start_time": "e.g. 2:00 PM",
      "order": 1
    }}
  ],
  "recovery_tip": "One powerful motivational line"
}}

User Mood: {mood}
User Situation: {situation}

Be realistic with success probability. Be brutally honest but supportive.
Return ONLY the JSON, no extra text.
"""
    messages = [{"role": "user", "parts": [{"text": prompt}]}]
    return call_gemini(messages)


def replan_after_checkin(conversation_history, completed, task_title, focus_rating):
    prompt = f"""
The user is in an active panic session.
Task: "{task_title}"
Completed: {"Yes" if completed else "No"}
Focus rating: {focus_rating}/5
Focus rating meaning:
1 = Easily distracted
2 = Struggling to concentrate
3 = Holding steady
4 = Focused
5 = Locked in

If focus rating is 1 or 2, reduce cognitive load, shorten future tasks if needed, and explain that in focus_feedback.
If focus rating is 3, keep the plan mostly stable.
If focus rating is 4 or 5, maintain momentum and avoid unnecessary replanning.

Interpret this as:

1 = Easily distracted
2 = Struggling to concentrate
3 = Holding steady
4 = Focused
5 = Locked in

The focus rating is extremely important.

If focus is 1 or 2:
- reduce cognitive load
- shorten future tasks
- encourage the user
- explain why the plan changed

If focus is 4 or 5:
- keep momentum
- avoid unnecessary simplification
- challenge the user only if realistic

{"Great progress! Adjust remaining timeline and keep momentum." if completed else "They didn't complete it. Replan the remaining tasks realistically. Be encouraging but honest."}

Respond ONLY in this JSON format:
{
  "message": "Your coach response here",
  "focus_feedback": "Explain how the user's focus level affected your decision. Example: Since your focus is low, I am reducing task size to help you regain momentum.",
  "replan_needed": true or false,
  "tasks": [
    {
      "title": "Task name",
      "duration_minutes": <number>,
      "start_time": "updated time",
      "order": <number>
    }
  ],
  "updated_success_probability": <number 0-100>
}

Return ONLY the JSON, no extra text.
"""
    conversation_history.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    return call_gemini(conversation_history), conversation_history


def explode_task(task_title, minutes_available,focus_rating):
    prompt = f"""
User is stuck on: "{task_title}"

Time available: {minutes_available} minutes

Current Focus Level: {focus_rating}/5

Focus meaning:

1 = Easily distracted
2 = Struggling to concentrate
3 = Holding steady
4 = Focused
5 = Locked in

Adjust your coaching style.

If focus is 1 or 2:
- Create smaller micro tasks
- Encourage the user
- Reduce mental load
- Keep each step simple

If focus is 3:
- Normal plan

If focus is 4 or 5:
- Keep momentum
- Give fewer but larger steps
- Challenge the user slightly

Respond ONLY in this JSON format...



Break this into micro-tasks of 5-10 minutes each.
Respond ONLY in this JSON format:
{{
  "micro_tasks": [
    {{
      "title": "Micro task name",
      "duration_minutes": <number>,
      "tip": "One quick tip"
    }}
  ]
}}

Return ONLY the JSON, no extra text.
"""
    messages = [{"role": "user", "parts": [{"text": prompt}]}]
    return call_gemini(messages)


def generate_recovery_plan(situation, missed_deadline):
    prompt = f"""
User missed a deadline. Help them recover professionally.
Original situation: {situation}
What they missed: {missed_deadline}

Respond ONLY in this JSON format:
{{
  "damage_control_steps": [
    {{
      "step": 1,
      "action": "What to do",
      "template": "Email/message template if needed"
    }}
  ],
  "reputation_recovery_percent": <number 0-100>,
  "harsh_truth": "One honest reality check",
  "silver_lining": "One genuine positive"
}}

Return ONLY the JSON, no extra text.
"""
    messages = [{"role": "user", "parts": [{"text": prompt}]}]
    return call_gemini(messages)