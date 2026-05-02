from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Sale, Transaction # Updated to include all models

# --- Challenge 01: Concurrency Handling (Atomic Checkout) ---

@csrf_exempt
@api_view(['POST'])
def checkout(request):
    """
    Processes the entire cart in a single atomic transaction.
    Ensures that if one item fails (e.g., out of stock), no changes are made to the database.
    """
    cart_items = request.data.get('items', [])
    
    if not cart_items:
        return Response({"error": "Your cart is empty."}, status=400)

    try:
        # Start a database transaction block
        with transaction.atomic():
            for item in cart_items:
                # Use select_for_update() to lock the product row to prevent race conditions.
                product = Product.objects.select_for_update().get(id=item['id'])
                
                # Check if there is enough stock available
                if product.stock < 1:
                    # Raising an error here will automatically trigger a database ROLLBACK
                    raise ValueError(f"Insufficient stock for {product.name}.")

                # Deduct 1 unit from stock and save the changes
                product.stock -= 1
                product.save()

                # Create a Sale record for inventory tracking
                Sale.objects.create(
                    product=product, 
                    quantity=1, 
                    total_price=product.price
                )
                
                # Also create a Transaction record for the revenue analytics
                Transaction.objects.create(
                    product=product,
                    amount=product.price
                )

        # Changes are COMMITTED only if the entire loop finishes without errors
        return Response({"message": "Order processed successfully!"}, status=200)

    except Product.DoesNotExist:
        return Response({"error": "One or more products were not found in the database."}, status=404)
    except ValueError as ve:
        return Response({"error": str(ve)}, status=400)
    except Exception as e:
        return Response({"error": "An internal error occurred. Transaction rolled back."}, status=500)


# --- Challenge 02: Optimized Analytics ---

@api_view(['GET'])
def get_analytics(request):
    """
    Provides optimized business intelligence using the indexed Transaction model.
    """
    # Define the timeframe (past 30 days)
    last_30_days = timezone.now() - timezone.timedelta(days=30)

    # 1. Daily Revenue Calculation
    # Uses the Transaction model which has a database index on 'created_at' for speed
    daily_revenue = Transaction.objects.filter(created_at__gte=last_30_days)\
        .extra(select={'day': "DATE(created_at)"})\
        .values('day')\
        .annotate(total_revenue=Sum('amount'))\
        .order_by('day')

    # 2. Top 5 Products by sales volume
    top_products = Transaction.objects.values('product__name')\
        .annotate(total_sales=Count('id'))\
        .order_by('-total_sales')[:5]

    return Response({
        "status": "success",
        "daily_revenue": daily_revenue,
        "top_products": top_products
    })

@api_view(['POST'])
def purchase_item(request):
    
    return Response({"message": "This endpoint is deprecated. Use checkout instead."}, status=200)