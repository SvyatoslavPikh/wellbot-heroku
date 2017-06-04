from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import datetime
import random

from .models import UserTakings



def index(request):
    return HttpResponse("It`s working.")


def get_takings(request, user_id):
    datetime_format = '%H:%M:%S %d.%m.%Y'
    takings = UserTakings.objects.all().filter(
        Q(user_id=user_id)
    ).distinct()

    start_date_text = request.GET.get("start_date")
    if start_date_text:
        start_date = datetime.datetime.strptime(start_date_text, datetime_format)
        takings = takings.filter(
            Q(date__gte=start_date)
        ).distinct()

    end_date_text = request.GET.get("end_date")
    if end_date_text:
        end_date = datetime.datetime.strptime(end_date_text, datetime_format)
        takings = takings.filter(
            Q(date__lte=end_date)
        ).distinct()

    results = {
        'takings': []
    }
    for taking in takings:
        results['takings'].append({
            'user_id': taking.user_id,
            'description': taking.description,
            'date': taking.date.strftime(datetime_format)
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
        taking = UserTakings(user_id=user_id, date=date, description='Eat %s at %s' % (random.choice(variants), date.strftime('%H:%M:%S %d.%m.%Y')))
        taking.save()

    return JsonResponse({
        'message': 'OK',
        'success': True
    })
