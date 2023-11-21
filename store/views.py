from rest_framework import status
from .filters import ProductFilter
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, Collection, OrderItem, Review
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer


# PRODUCT [GET, POST] =======================>
# SINGLE PRODUCT [GET, PUT, DELETE] =======================>

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted. because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)      


# COLLECTION [GET, POST] =======================>
# SINGLE COLLECTION [GET, PUT, DELETE] =======================>

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted. because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# REVIEW [GET, POST] =======================>
# SINGLE REVIEW [GET, PUT, DELETE] =======================>

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'product_id': self.kwargs['product_pk']})
        return context




