from django.shortcuts import render
from django.db.models import Value, F, Func
from django.http import HttpResponse
from django.db.models.aggregates import Count, Max, Min, Aggregate
from  store.models import Product, Order, Customer, Collection, OrderItem
from tags.models import TaggedItem


def say_hello(request):
    try:
        # Assuming a Product with pk=1 exists in your database
        product_instance = Product.objects.get(pk=1)

        # Creating a Collection instance with the correct reference to the Product
        collection = Collection()
        collection.title = 'New Video Game'
        collection.featured_product = product_instance
        collection.save()

        result = f"Collection created with featured product: {product_instance.name}"
    except Product.DoesNotExist:
        result = "Product with pk=1 does not exist."

    return render(request, 'hello.html', {'name': 'Mosh', 'result': result})
 
