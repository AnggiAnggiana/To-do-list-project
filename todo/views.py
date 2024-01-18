# INI APLIKASINYA / SAMA DENGAN BLOGS
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


from .forms import Regular_todoForm
from .forms import Urgent_todoForm
from .forms import Completed_todoForm
from django.urls import reverse
from .models import Regular_todo_list, Urgent_todo_list
from django.contrib import messages

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
    
    if request.method == "POST":
        regular_form = Regular_todoForm(request.POST)
        urgent_form = Urgent_todoForm(request.POST)
        
        if regular_form.is_valid():
            regular_form.save()
            messages.success(request, 'Regular task successfully added')
            submitted = True
        
        if urgent_form.is_valid():
            urgent_form.save()
            messages.success(request, 'Important task successfully added')
            submitted = True
            
    regular_task = Regular_todo_list.objects.all()
    important_task = Urgent_todo_list.objects.all()
    
    # Grouping element regular_form by frequncy (regular task)
    regular_task_group = {k: list(g) for k, g in groupby(sorted(regular_task, key=lambda x: x.frequency), key=lambda x: x.frequency)}
    # Grouping element in important task
    important_task_group = {k: list(g) for k, g in groupby(sorted(important_task, key=lambda x: x.task), key=lambda x: x.task)}
            
    return render(request, 'todo/myTodo.html', {
        'regular_form': regular_form,
        'urgent_form': urgent_form,
        'submitted': submitted,
        'regular_task': regular_task,
        'important_task': important_task,
        'regular_task_group': regular_task_group,
        'important_task_group': important_task_group,
    })
    
        
# DOWNLOAD FILE PDF
@login_required
def download_mylist_pdf(request):
    # Membuat Bytestream buffer
    buf = io.BytesIO()
    
    # Membuat canvas/blank page
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    # Membuat judul di pdf
    title_text = "Data Todo List Saya"
    c.setFont("Helvetica-Bold", 16)
    
    title_x_position = letter[0] / 2
    title_y_position = letter[0] - 8 * inch
    c.drawCentredString(title_x_position, title_y_position, title_text)
    
    # Membuat teks untuk object isi filenya
    textobject = c.beginText()
    textobject.setTextOrigin(inch, inch)
    textobject.setFont("Helvetica", 12)
    
    # Isi dari filenya
    # TodoItems = TodoItem.objects.all()
    
    # Membuat baris teks
    lines = []
    
    # for mytodo in TodoItems:
    #     lines.append(mytodo.task)
        
    # Looping
    for baris in lines:
        textobject.textLine(baris)
        
    # Mengeksekusi/generate menjadi file
    c.drawText(textobject)
    c.showPage()
    c.save()
    buf.seek(0)
    
    # return FileResponse(buf, as_attachment=True, filename='mylist.pdf')
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=mylist.pdf'
    
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


# def delete_todo(request, todo_id):
#     task = TodoItem.objects.get(pk=todo_id)
#     task.delete()
#     return redirect('myList')
    

# def remove_todo(request, todo_id):
#     todo_item = get_object_or_404(TodoItem, pk=todo_id)
#     todo_item.delete()
#     return JsonResponse({'message': 'Task berhasil dihapus'})

