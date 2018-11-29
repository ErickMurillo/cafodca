from notas.models import Notas

def global_notas(request):
    footer_notas = Notas.objects.order_by('-fecha', '-id')[:2]
    return {'footer_notas':footer_notas}
