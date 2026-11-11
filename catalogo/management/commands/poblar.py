from django.core.management.base import BaseCommand
from catalogo.models import Producto


class Command(BaseCommand):
    help = 'Puebla la base de datos con productos de ejemplo'

    def handle(self, *args, **options):
        datos = [
            ('laptop lenovo ideapad', 2499.90, 8, True),
            ('mouse inalambrico', 45.50, 30, True),
            ('teclado mecanico', 189.00, 12, True),
            ('monitor 24 pulgadas', 649.00, 0, True),
            ('audifonos bluetooth', 99.90, 20, False),
            ('webcam full hd', 129.90, 14, True),
            ('microfono usb condensador', 219.00, 7, True),
            ('parlante bluetooth portatil', 159.90, 18, True),
            ('disco duro externo 1 tb', 249.00, 11, True),
            ('unidad ssd 1 tb', 329.90, 9, True),
            ('memoria usb 64 gb', 29.90, 40, True),
            ('memoria ram ddr4 16 gb', 145.00, 6, True),
            ('router wifi doble banda', 179.90, 10, True),
            ('repetidor wifi', 89.00, 15, True),
            ('cable hdmi 2 metros', 25.90, 32, True),
            ('adaptador usb c multipuerto', 119.00, 8, True),
            ('hub usb 4 puertos', 49.90, 21, True),
            ('cargador usb c 65w', 99.00, 13, True),
            ('power bank 20000 mah', 139.90, 16, True),
            ('soporte para laptop', 79.00, 17, True),
            ('base refrigerante para laptop', 89.90, 12, True),
            ('silla ergonomica de oficina', 799.00, 4, True),
            ('escritorio gamer', 599.90, 3, True),
            ('lampara led de escritorio', 69.00, 19, True),
            ('impresora multifuncional', 549.00, 5, True),
            ('cartucho de tinta negro', 59.90, 22, True),
            ('papel para impresora paquete', 24.00, 28, True),
            ('tablet 10 pulgadas', 899.00, 6, True),
            ('smartphone 128 gb', 1299.90, 7, True),
            ('reloj inteligente deportivo', 249.00, 10, True),
            ('audifonos con cancelacion de ruido', 349.90, 8, True),
            ('mouse gamer rgb', 119.00, 15, True),
            ('teclado inalambrico compacto', 99.90, 14, True),
            ('alfombrilla gamer xl', 39.00, 25, True),
            ('control para videojuegos', 229.00, 9, True),
            ('camara web con microfono', 189.90, 6, True),
            ('lector de tarjetas usb', 35.00, 20, True),
            ('adaptador bluetooth usb', 29.00, 18, True),
            ('cable de red ethernet 5 metros', 22.90, 27, True),
            ('switch de red 8 puertos', 119.00, 8, True),
            ('protector de voltaje', 79.90, 11, True),
            ('estabilizador de voltaje', 169.00, 5, True),
            ('ups 600 va', 289.90, 4, True),
            ('lector de libros electronicos', 499.00, 3, True),
            ('monitor 27 pulgadas', 999.00, 4, True),
            ('brazo ajustable para monitor', 159.00, 7, True),
            ('proyector portatil', 749.90, 2, True),
            ('parlantes estereo para pc', 89.00, 16, True),
            ('microfono para streaming', 279.00, 5, True),
            ('mochila para laptop', 119.90, 13, True),
            ('funda protectora para tablet', 49.00, 18, True),
            ('kit de limpieza para electronicos', 19.90, 24, True),
            ('lapiz digital para tablet', 89.90, 9, True),
            ('estacion de acoplamiento usb c', 229.00, 5, True),
            ('cable de carga usb c', 18.90, 30, True),
        ]
        creados = 0
        for nombre, precio, stock, disp in datos:
            _, creado = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'precio': precio,
                    'stock': stock,
                    'disponible': disp,
                    'descripcion': f'Producto de tecnología y accesorios: {nombre}.',
                },
            )
            creados += creado
        self.stdout.write(self.style.SUCCESS(
            f'Productos nuevos agregados: {creados}. Total en BD: {Producto.objects.count()}'
        ))
