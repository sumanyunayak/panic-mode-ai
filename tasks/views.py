from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import PanicSession, Task
from .gemini_service import (
    triage_situation,
    replan_after_checkin,
    explode_task,
    generate_recovery_plan
)
import json

@api_view(['POST'])
def triage(request):
    try:
        if isinstance(request.data, str):
            body = json.loads(request.data)
        else:
            body = request.data
            
        situation = body.get('situation')
        mood = body.get('mood')
        
        raw = triage_situation(situation, mood)
        clean = raw.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean)
        
        # Save session
        session = PanicSession.objects.create(
            situation=situation,
            mood=mood,
            diagnosis=data['diagnosis'],
            severity=data['severity'],
            success_probability=data['success_probability'],
            conversation_history=[{
                "role": "user",
                "parts": [{"text": situation}]
            }]
        )
        
        # Save tasks
        for t in data['tasks']:
            Task.objects.create(
                session=session,
                title=t['title'],
                duration_minutes=t['duration_minutes'],
                start_time=t['start_time'],
                order=t['order']
            )
        
        return Response({
            'session_id': session.id,
            'diagnosis': data['diagnosis'],
            'crisis_type': data.get('crisis_type', 'General Emergency'),
            'severity': data['severity'],
            'success_probability': data['success_probability'],
            'probability_reason': data.get('probability_reason', []),
            'critical_threat': data['critical_threat'],
            'do_not_list': data['do_not_list'],
            'tasks': data['tasks'],
            'recovery_tip': data['recovery_tip']
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def checkin(request):
    try:
        session_id = request.data.get('session_id')
        task_title = request.data.get('task_title')
        completed = request.data.get('completed')
        focus_rating = request.data.get('focus_rating', 3)
        
        session = PanicSession.objects.get(id=session_id)
        
        raw, updated_history = replan_after_checkin(
            session.conversation_history,
            completed,
            task_title,
            focus_rating
        )
        
        clean = raw.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean)
        
        session.conversation_history = updated_history
        session.success_probability = data['updated_success_probability']
        session.save()
        
        return Response(data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def explode(request):
    try:
        task_title = request.data.get('task_title')
        minutes = request.data.get('minutes_available', 30)
        focus_rating = request.data.get('focus_rating',3)
        
        raw = explode_task(
            task_title,
            minutes,
            focus_rating
        )
        clean = raw.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean)
        
        return Response(data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def recovery(request):
    try:
        session_id = request.data.get('session_id')
        missed_deadline = request.data.get('missed_deadline')
        
        session = PanicSession.objects.get(id=session_id)
        
        raw = generate_recovery_plan(session.situation, missed_deadline)
        clean = raw.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean)
        
        return Response(data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def home(request):
    return render(request, "index.html")