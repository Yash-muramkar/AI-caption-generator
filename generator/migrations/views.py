from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .ai_utils import generate_caption

def upload_view(request):
    caption = hashtags = None

    if request.method == "POST":
        file = request.FILES['media']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        caption, hashtags, keywords = generate_caption(file_path)

    return render(request, 'upload.html', {
        'caption': caption,
        'hashtags': hashtags
    })
