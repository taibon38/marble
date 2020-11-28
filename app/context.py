from .models import MovieCharacter


def related(request):
    context = {
        'movie_character': MovieCharacter.objects.all(),
    }
    return context