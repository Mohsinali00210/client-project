import pandas as pd
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from api.models import CollectionItems
from Research.getProduct import getProductBySKU, PrepareProductAndCollectionData  # Import your utility functions

class Command(BaseCommand):
    help = 'Check for price changes in products and send emails if prices have changed.'

    def handle(self, *args, **kwargs):
        # Fetch all collection items
        collectionitems = CollectionItems.objects.all()
        
        # Collect SKUs as a comma-separated string
        SKUS = ','.join([str(i.SKU) for i in collectionitems])
        
        # Fetch product details by SKUs
        products = getProductBySKU(SKUS)
        
        # Prepare the data
        Collection_Data, Product_Data = PrepareProductAndCollectionData(collectionitems, products)
        
        # Create DataFrames
        df1 = pd.DataFrame(Collection_Data)
        df2 = pd.DataFrame(Product_Data)

        # Perform the merge (join) on the SKU column
        joined_df = pd.merge(df1, df2, left_on="SKU", right_on="sku", how="inner")

        # Rename columns for clarity
        joined_df.rename(columns={"price_x": "OldPrice", "price_y": "NewPrice"}, inplace=True)

        # Convert the merged result to a list of dictionaries
        joined_list = joined_df.to_dict(orient="records")

        # Iterate through the list and check for price changes
        for prd in joined_list:
            # If there is a price change
            if prd['OldPrice'] != prd['NewPrice']:
                subject = 'Product Price has been Changed'
                message = (
                    f"The price of \"{prd['product_name']}\" has been changed "
                    f"from {prd['OldPrice']} to {prd['NewPrice']}. Link: {prd['product_url']}"
                )
                from_email = settings.EMAIL_HOST_USER
                recipient_list = ['mohsinali00210@gmail.com']  # List of recipients

                # Send email
                send_mail(subject, message, from_email, recipient_list)

        self.stdout.write(self.style.SUCCESS('Successfully checked price changes and sent emails if needed.'))
