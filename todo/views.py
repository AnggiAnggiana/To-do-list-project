from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
# from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

# Untuk download file pdf
# Install di command prompt: pip install reportlab django
import io
# from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


from .forms import Regular_todoForm
from .forms import Urgent_todoForm
from .forms import Completed_todoForm
from django.urls import reverse
from .models import Regular_todo_list, Urgent_todo_list, Completed_todo_list
from django.contrib import messages

from django.utils import timezone
import json

# import groupby
from itertools import groupby


def handler404(request, exception):
    return render(request, '404.html', status=404)


# Add todo_list
@login_required
def todo_list(request):
    submitted = False
    regular_form = Regular_todoForm()
    urgent_form = Urgent_todoForm()
    regular_move_to_completed_task = True
    important_move_to_completed_task = True
    
    if request.method == "POST":
        regular_form = Regular_todoForm(request.POST)
        urgent_form = Urgent_todoForm(request.POST)
        regular_move_to_completed_task = request.POST.get('regular_move_to_completed_task')     # "Done" button function (regular task)
        important_move_to_completed_task = request.POST.get('important_move_to_completed_task')     # "Done" button function (important task)
        
        if regular_form.is_valid():
            regular_instance = regular_form.save(commit=False)
            regular_instance.author = request.user
            regular_instance.save()
            messages.success(request, 'Regular task successfully added')
            submitted = True
        
        if urgent_form.is_valid():
            important_instance = urgent_form.save(commit=False)
            important_instance.author = request.user
            important_instance.save()
            messages.success(request, 'Important task successfully added')
            submitted = True
            
        if regular_move_to_completed_task:
            reg_task_to_move = Regular_todo_list.objects.get(task=regular_move_to_completed_task)
            Completed_todo_list.move_task(regular_todo=reg_task_to_move)
            reg_task_to_move.delete()
            messages.success(request, 'Congratulations, you successfully completed your regular task')
            return redirect('todo_list')
        
        if important_move_to_completed_task:
            imp_task_to_move = Urgent_todo_list.objects.get(task=important_move_to_completed_task)
            Completed_todo_list.move_task(urgent_todo=imp_task_to_move)
            imp_task_to_move.delete()
            messages.success(request, 'Congratulations, you successfully completed your important task')
            return redirect('todo_list')
        
    regular_task = Regular_todo_list.objects.filter(author=request.user)
    important_task = Urgent_todo_list.objects.filter(author=request.user).order_by('due_date')
    
    # Grouping element regular_form by frequncy (regular task)
    regular_task_group = {k: list(g) for k, g in groupby(sorted(regular_task, key=lambda x: x.frequency), key=lambda x: x.frequency)}
    # Grouping element in important task
    # important_task_group = {k: list(g) for k, g in groupby(sorted(important_task, key=lambda x: x.task), key=lambda x: x.task)}
    important_task_group = {k: sorted(list(g), key=lambda x: x.due_date) for k, g in groupby(important_task, key=lambda x: x.task)}
            
    # Get completed tasks of 'Regular' and 'Urgent' separately
    completed_regular_tasks = Completed_todo_list.objects.filter(task_types=Completed_todo_list.REGULAR, author=request.user)
    completed_important_tasks = Completed_todo_list.objects.filter(task_types=Completed_todo_list.URGENT, author=request.user)
    
    # For Calendar
    
    # selected_date = Regular_todo_list.objects.filter(author=request.user)
    # context = {
    #     "events": selected_date,
    # }
    
    return render(request, 'todo/myTodo.html', {
        'regular_form': regular_form,
        'urgent_form': urgent_form,
        'submitted': submitted,
        'regular_task': regular_task,
        'important_task': important_task,
        'regular_task_group': regular_task_group,
        'important_task_group': important_task_group,
        'regular_move_to_completed_task': regular_move_to_completed_task,
        'important_move_to_completed_task': important_move_to_completed_task,
        'completed_regular_tasks': completed_regular_tasks,
        'completed_important_tasks': completed_important_tasks,
        # 'selected_date': selected_date,
        # 'context': context,
    })
    
@login_required
def data_calendar(request):
    selected_date = Urgent_todo_list.objects.filter(author=request.user)
    events = [{'title': task.task, 'start': timezone.localtime(task.due_date).strftime('%Y-%m-%d %H:%M:%S'),} for task in selected_date]
    return JsonResponse(events, safe=False)
    
    
@login_required
def delete_todo(request, task_type, todo_id):
    if task_type == 'regular':
        todo_model = Regular_todo_list
    elif task_type == 'important':
        todo_model = Urgent_todo_list
    elif task_type == 'completed':
        todo_model = Completed_todo_list
    else:
        pass
    
    delete_task = get_object_or_404(todo_model, pk=todo_id)
    delete_task.delete()
    messages.success(request, 'Task successfully deleted')
    return redirect('todo_list')


        
# DOWNLOAD FILE PDF
@login_required
def download_mylist_pdf(request):
    # Membuat Bytestream buffer
    buf = io.BytesIO()
    # doc = SimpleDocTemplate(buf, pagesize=letter)
    
    # Membuat canvas/blank page
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    # Membuat judul di pdf
    title_text = "Data Todo List Saya"
    c.setFont("Helvetica-Bold", 16)
    
    inch = 85
    
    title_x_position = letter[0] / 2
    title_y_position = letter[0] / 15 
    c.drawCentredString(title_x_position, title_y_position, title_text)
    
    # Membuat teks untuk object isi filenya
    textobject = c.beginText()
    textobject.setTextOrigin(inch, inch)
    textobject.setFont("Helvetica", 12)
    
    # Isi dari filenya
    regular_tasks = Regular_todo_list.objects.filter(author=request.user)
    important_tasks = Urgent_todo_list.objects.filter(author=request.user)
    completed_regular_tasks = Completed_todo_list.objects.filter(task_types=Completed_todo_list.REGULAR, author=request.user)
    completed_important_tasks = Completed_todo_list.objects.filter(task_types=Completed_todo_list.URGENT, author=request.user)
    
    # Membuat baris teks
    lines = []
    
    lines.append(["1. Regular Task:", ""])
    if regular_tasks:
        for i, regular_task in enumerate(regular_tasks):
            lines.append([f"      {chr(97 + i)}) ({regular_task.frequency}) {regular_task.task}"])
    else:
        lines.append(["      None"])
        
        
    lines.append(["2. Important Task:", ""])
    if important_tasks:
        for i, important_task in enumerate(important_tasks):
            formatted_due_date = important_task.due_date.strftime("%d %B %Y, %H:%M")
            lines.append([f"      {chr(97 + i)}) {important_task.task} | Deadline: {formatted_due_date}"])
    else:
        lines.append(["      None"])
        
    lines.append(["3. Completed Regular Task:", ""])
    if completed_regular_tasks:
        for i, completed_regular_task in enumerate(completed_regular_tasks):
            lines.append([f"      {chr(97 + i)}) ({completed_regular_task.frequency}) {completed_regular_task.task}"])
    else:
        lines.append(["      None"])
        
    lines.append(["4. Completed Important Task:", ""])
    if completed_important_tasks:
        for i, completed_important_task in enumerate(completed_important_tasks):
            formatted_completed_due_date = completed_important_task.due_date.strftime("%d %B %Y, %H:%M")
            lines.append([f"      {chr(97 + i)}) {completed_important_task.task} | Deadline: {formatted_completed_due_date}"])
    else:
        lines.append(["      None"])

        
    # Looping
    # for baris in lines:
    #     textobject.textLine(baris)
    
    for line_pair in lines:
        line_label = line_pair[0]
        line_content = line_pair[1] if len(line_pair) > 1 else ""
        
        textobject.textLine(f"{line_label} {line_content} ")

        
    # Mengeksekusi/generate menjadi file
    c.drawText(textobject)
    c.showPage()
    c.save()
    buf.seek(0)
    
    # return FileResponse(buf, as_attachment=True, filename='mylist.pdf')
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Todo-List.pdf'
    
    return response


# VERSI FILE PDF DENGAN TABEL
# @login_required
# def download_mylist_pdf(request):
#     # Membuat Bytestream buffer
#     buf = io.BytesIO()
    
#     # Membuat canvas/blank page
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
#     # Membuat judul di pdf
#     title_text = "Data Todo List Saya"
#     c.setFont("Helvetica-Bold", 16)
    
#     title_x_position = letter[0] / 2
#     title_y_position = letter[0] - 8 * inch
#     c.drawCentredString(title_x_position, title_y_position, title_text)
    
#     # Isi dari filenya
#     TodoItems = TodoItem.objects.all()
    
#     # Membuat data untuk tabel
#     data = [['Task']]
    
#     for mytodo in TodoItems:
#         data.append([mytodo.task])
        
#     # Membuat blank page
#     c = SimpleDocTemplate(buf, pagesize=letter)
    
#     # Membuat Tabel
#     table_style = [('GRID', (0, 0), (-1, -1), 1, colors.black)]
#     table = Table(data, style=table_style)
    
#     # Menambahkan tabel ke dokumen
#     elements = [table]
    
#     # Menambahkan tabel ke dokumen
#     c.build(elements)
    
#     buf.seek(0)
    
#     # return FileResponse(buf, as_attachment=True, filename='mylist.pdf')
#     response = HttpResponse(buf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=mylist.pdf'
    
#     return response
