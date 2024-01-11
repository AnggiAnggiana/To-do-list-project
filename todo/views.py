# INI APLIKASINYA / SAMA DENGAN BLOGS
from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from django.http import JsonResponse
# from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
# Yg bawah dari tutorial ytube
# from django.views import View

# Untuk download file pdf
# Install di command prompt: pip install reportlab django
import io
# from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse


def handler404(request, exception):
    return render(request, '404.html', status=404)

# Untuk menambahkan list
@login_required
def todo_list(request):
    if request.method == 'POST':
        task = request.POST.getlist('task[]')
        for task in task:
            TodoItem.objects.create(task=task)
        return JsonResponse({'message': 'Task berhasil ditambahkan'})
    
    elif request.method == 'GET':
        task = TodoItem.objects.all().values('id', 'task', 'completed')
        return render(request, 'isi.html', {'task': task})

    todo_items = TodoItem.objects.all()
    return render(request, 'isi.html', {'todo_items': todo_items})


# Untuk menampilkan to-do list
@login_required
def myList(request):
    # Tampilan website, mengambil data dari database
    if request.method == 'GET':
        task = TodoItem.objects.all().values('id', 'task', 'completed')
        return render(request, 'myList.html', {'task': task})
    # Mendapatkan Id dari database untuk dihapus
    elif request.method == 'DELETE':
        todo_id = request.GET.get('todo_id')

        try:
            todo_to_delete = TodoItem.objects.get(id=todo_id)
            todo_to_delete.delete()
            return JsonResponse({"message": "Data berhasil dihapus"})
        except TodoItem.DoesNotExist:
            return JsonResponse({"message": "Data tidak ditemukan"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
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
    TodoItems = TodoItem.objects.all()
    
    # Membuat baris teks
    lines = []
    
    for mytodo in TodoItems:
        lines.append(mytodo.task)
        
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


def delete_todo(request, todo_id):
    task = TodoItem.objects.get(pk=todo_id)
    task.delete()
    return redirect('myList')
    

def remove_todo(request, todo_id):
    todo_item = get_object_or_404(TodoItem, pk=todo_id)
    todo_item.delete()
    return JsonResponse({'message': 'Task berhasil dihapus'})

