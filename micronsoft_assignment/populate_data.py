import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Product, Transaction

def populate_data():
    print("⏳ Populating 100,000 records... This may take a moment.")
    
    # Get an existing product or create one if none exists
    product, created = Product.objects.get_or_create(
        id=1, 
        defaults={'name': 'Smart Watch Series 7', 'price': 12000, 'stock': 1000}
    )

    transactions = []
    start_date = datetime.now() - timedelta(days=180) # Last 6 months

    for i in range(100000):
        # Generate a random date within the last 6 months
        random_days = random.randint(0, 180)
        created_at = start_date + timedelta(days=random_days)
        
        # Create a Transaction object in memory
        transactions.append(Transaction(
            product=product,
            amount=product.price,
            created_at=created_at
        ))

        # Bulk insert every 5000 records to save memory and time
        if len(transactions) >= 5000:
            Transaction.objects.bulk_create(transactions)
            transactions = []
            print(f"✅ Inserted {i+1} records...")

    # Final bulk insert for remaining records
    if transactions:
        Transaction.objects.bulk_create(transactions)

    print("\n🚀 Successfully populated 100,000 transaction records!")

if __name__ == "__main__":
    populate_data()