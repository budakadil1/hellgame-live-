from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Report
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from reports.forms import ReportForm
User = get_user_model()

# Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = ReportForm(data=request.POST, user_from=request.user.username)
            context = {'form' : form}
            return render(request, 'reports/report.html', context)
        if request.method == 'POST':
            form = ReportForm(data=request.POST, user_from = request.user.username)
            if form.is_valid():
                instance = form.save()
                report_reverse = instance.pk
                return redirect(reverse('reports:status', kwargs={'report_id':str(report_reverse)}))
    else:
        return redirect(reverse('user:login'))

# Create your views here.
def checkstatus(request, report_id):
    report_context = Report.objects.filter(report_id=report_id)
    context = {'report':report_context}
    return render(request, 'reports/checkstatus.html', context)
    
