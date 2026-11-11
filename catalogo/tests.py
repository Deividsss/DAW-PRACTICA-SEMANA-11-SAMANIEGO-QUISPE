from django.test import TestCase
from django.core.management import call_command

from django.urls import reverse

from .models import Producto


class CatalogoViewsTests(TestCase):
    def setUp(self):
        Producto.objects.create(
            nombre='Laptop de prueba',
            descripcion='Equipo portátil',
            precio='2500.00',
            stock=8,
            disponible=True,
        )
        Producto.objects.create(
            nombre='Mouse agotado',
            descripcion='Accesorio inalámbrico',
            precio='50.00',
            stock=0,
            disponible=True,
        )
        Producto.objects.create(
            nombre='Teclado no disponible',
            descripcion='Teclado mecánico',
            precio='180.00',
            stock=3,
            disponible=False,
        )

    def test_home_shows_inventory_metrics_and_products(self):
        response = self.client.get(reverse('catalogo:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Productos recientes')
        self.assertContains(response, 'Valor en inventario')
        self.assertEqual(response.context['total_productos'], 3)
        self.assertEqual(response.context['productos_disponibles'], 1)
        self.assertEqual(response.context['productos_bajo_stock'], 2)

    def test_catalog_search_matches_description(self):
        response = self.client.get(reverse('catalogo:catalogo'), {'q': 'inalámbrico'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['productos']), [Producto.objects.get(nombre='Mouse agotado')])

    def test_catalog_filters_out_of_stock_and_unavailable_products(self):
        response = self.client.get(reverse('catalogo:catalogo'), {'estado': 'agotados'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_resultados'], 2)

    def test_catalog_orders_by_price(self):
        response = self.client.get(reverse('catalogo:catalogo'), {'orden': '-precio'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [producto.nombre for producto in response.context['productos']],
            ['Laptop de prueba', 'Teclado no disponible', 'Mouse agotado'],
        )

    def test_catalog_paginates_products(self):
        for index in range(10):
            Producto.objects.create(
                nombre=f'Producto adicional {index}',
                precio='10.00',
                stock=1,
            )

        response = self.client.get(reverse('catalogo:catalogo'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['productos']), 10)
        self.assertTrue(response.context['is_paginated'])


class PoblarCommandTests(TestCase):
    def test_poblar_adds_50_products_once(self):
        call_command('poblar', stdout=None)

        self.assertEqual(Producto.objects.count(), 55)

        call_command('poblar', stdout=None)

        self.assertEqual(Producto.objects.count(), 55)
