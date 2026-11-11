from django.db.models import Count, F, Q, Sum
from django.shortcuts import render
from django.views.generic import ListView

from .models import Producto


def home(request):
    resumen = Producto.objects.aggregate(
        total=Count('id'),
        disponibles=Count('id', filter=Q(disponible=True, stock__gt=0)),
        valor=Sum(F('precio') * F('stock')),
    )
    contexto = {
        'productos_recientes': Producto.objects.order_by('-fecha_creacion')[:5],
        'productos_alerta': Producto.objects.filter(
            Q(stock__lte=5) | Q(disponible=False)
        ).order_by('stock', 'nombre')[:5],
        'total_productos': resumen['total'],
        'productos_disponibles': resumen['disponibles'],
        'productos_bajo_stock': Producto.objects.filter(stock__lte=5).count(),
        'valor_inventario': resumen['valor'] or 0,
    }
    return render(request, 'catalogo/home.html', contexto)


class ProductoListView(ListView):
    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().annotate(valor_stock=F('precio') * F('stock'))
        busqueda = self.request.GET.get('q', '').strip()
        estado = self.request.GET.get('estado', '')
        orden = self.request.GET.get('orden', 'nombre')

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)
            )
        if estado == 'disponibles':
            queryset = queryset.filter(disponible=True, stock__gt=0)
        elif estado == 'agotados':
            queryset = queryset.filter(Q(disponible=False) | Q(stock=0))

        ordenes_permitidos = {
            'nombre', '-nombre', 'precio', '-precio', 'stock', '-stock',
        }
        if orden in ordenes_permitidos:
            return queryset.order_by(orden)
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['total_resultados'] = self.object_list.count()
        contexto['busqueda'] = self.request.GET.get('q', '').strip()
        contexto['estado_seleccionado'] = self.request.GET.get('estado', '')
        orden = self.request.GET.get('orden', 'nombre')
        contexto['orden_seleccionado'] = orden if orden in {
            'nombre', '-nombre', 'precio', '-precio', 'stock', '-stock',
        } else 'nombre'
        return contexto
