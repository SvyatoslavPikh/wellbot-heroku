from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import datetime
import random

from .models import UserTakings, CorezoidState, CorezoidStateHistory
from wellbot.settings import DATETIME_FORMAT


def index(request):
    return HttpResponse("It`s working.")


def get_takings(request, user_id):
    takings = UserTakings.objects.all().filter(
        Q(user_id=user_id)
    ).distinct()

    start_date_text = request.GET.get("start_date")
    if start_date_text:
        start_date = datetime.datetime.strptime(start_date_text, DATETIME_FORMAT)
        takings = takings.filter(
            Q(date__gte=start_date)
        ).distinct()

    end_date_text = request.GET.get("end_date")
    if end_date_text:
        end_date = datetime.datetime.strptime(end_date_text, DATETIME_FORMAT)
        takings = takings.filter(
            Q(date__lte=end_date)
        ).distinct()

    results = {
        'takings': []
    }
    for taking in takings:
        results['takings'].append({
            'id': taking.id,
            'user_id': taking.user_id,
            'description': taking.description,
            'date': taking.date.strftime(DATETIME_FORMAT)
        })
    return JsonResponse(results)


def create_test_takings(request, user_id):
    now = datetime.datetime.now()
    now_add_1 = datetime.datetime.now() + datetime.timedelta(minutes=1)
    now_add_5 = datetime.datetime.now() + datetime.timedelta(minutes=5)
    now_add_10 = datetime.datetime.now() + datetime.timedelta(minutes=10)
    now_add_30 = datetime.datetime.now() + datetime.timedelta(minutes=30)
    now_add_60 = datetime.datetime.now() + datetime.timedelta(minutes=60)

    dates = [now, now_add_1, now_add_5, now_add_10, now_add_30, now_add_60]
    variants = ['meat', 'fish', 'potato', 'rice', 'vegetables']
    for date in dates:
        taking = UserTakings(user_id=user_id, date=date, description='Eat %s at %s' % (random.choice(variants), date.strftime(DATETIME_FORMAT)))
        taking.save()

    return JsonResponse({
        'message': 'OK',
        'success': True
    })


def create_taking(request):
    datetime_format = '%H:%M:%S %d.%m.%Y'

    user_id = request.GET.get("start_date")
    date_text = request.GET.get("date")
    description = request.GET.get("description")
    if not user_id or not date_text or not description:
        raise ValueError('No user_id, no date or no description provided.')

    date = datetime.datetime.strptime(date_text, datetime_format)
    taking = UserTakings(user_id=user_id, date=date,
                         description=description)
    taking.save()

    return JsonResponse({
        'message': 'OK',
        'success': True,
        'taking': {
            'id': taking.id,
            'user_id': taking.user_id,
            'description': taking.description,
            'date': taking.date.strftime(datetime_format)
        }
    })

def delete_taking(request, taking_id):
    taking = UserTakings.objects.all().filter(
        Q(id=taking_id)
    ).first()
    if taking:
        taking.delete()

    return JsonResponse({
        'message': 'OK',
        'success': True
    })

def get_taking(request, id):
    taking = UserTakings.objects.all().filter(
        Q(id=id)
    ).first()

    return JsonResponse({
        'message': 'OK',
        'success': True,
        'taking': {
            'id': taking.id,
            'user_id': taking.user_id,
            'description': taking.description,
            'date': taking.date.strftime(DATETIME_FORMAT)
        }
    })


@csrf_exempt
def set_corezoid_user_state(request):
    if request.method != 'POST':
        return HttpResponseNotFound('Only POST method supported.')

    chat_id = request.POST.get("chat_id")
    task_id = request.POST.get("task_id")
    timeout = request.POST.get("timeout") or 86400
    context = request.POST.get("context")

    if not chat_id or not task_id or not context:
        raise ValueError('No chat_id, no task_id or no context provided.')

    state = CorezoidState.objects.all().filter(chat_id=chat_id).first()
    if not state:
        state = CorezoidState(date=now())
    state.chat_id = chat_id
    state.task_id = task_id
    state.timeout = timeout
    state.context = context
    state.save()

    history = CorezoidStateHistory(chat_id=chat_id, task_id=task_id, date=now(), timeout=timeout, context=context)
    history.save()

    return JsonResponse({
        'message': 'OK',
        'success': True,
        'callback': {
            'id': state.id,
            'chat_id': state.chat_id,
            'task_id': state.task_id,
            'date': state.date.strftime(DATETIME_FORMAT),
            'timeout': state.timeout,
            'context': state.context
        }
    })


def get_corezoid_user_state(request, chat_id):
    state = CorezoidState.objects.all().filter(chat_id=chat_id).first()
    if not state:
        return JsonResponse({
            'message': 'OK',
            'success': True,
            'state': {
                'id': '',
                'chat_id': chat_id,
                'task_id': '',
                'date': '',
                'timeout': 0,
                'context': '{}'
            }
        })

    timeout_date = state.date + datetime.timedelta(seconds=state.timeout)
    if timeout_date < now():
        return JsonResponse({
            'message': 'OK',
            'success': True,
            'state': {
                'id': state.id,
                'chat_id': state.chat_id,
                'task_id': '',
                'date': state.date.strftime(DATETIME_FORMAT),
                'timeout': state.timeout,
                'context': '{}'
            }
        })

    return JsonResponse({
        'message': 'OK',
        'success': True,
        'state': {
            'id': state.id,
            'chat_id': state.chat_id,
            'task_id': state.task_id,
            'date': state.date.strftime(DATETIME_FORMAT),
            'timeout': state.timeout,
            'context': state.context
        }
    })
