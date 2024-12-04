# myapp/cron.py
from django_cron import CronJobBase, Schedule
from Research.models import CollectionItems
from Research.getProduct import getProductBySKU, PrepareProductAndCollectionData
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

class PriceChangeCheckCronJob(CronJobBase):
    # This defines how often the job will run (every day at 12 AM in this case)
    schedule = Schedule(run_every_mins=1440)  # 1440 minutes = 1 day
    code = 'Research.price_change_check_cron_job'  # Unique code for this cron job

    def do(self):
        collectionitems = CollectionItems.objects.all()
        SKUS = ','.join(i.SKU for i in collectionitems)
        products = getProductBySKU(SKUS)
        Collection_Data, Product_Data = PrepareProductAndCollectionData(collectionitems, products)
        df1 = pd.DataFrame(Collection_Data)
        df2 = pd.DataFrame(Product_Data)

        # Perform the join (merge) on the "SKU" column
        joined_df = pd.merge(df1, df2, left_on="SKU", right_on="sku", how="inner")

        # Iterate over the rows and check for price changes
        for prd in joined_df.to_dict(orient="records"):
            if prd['price_x'] != prd['price_y']:
                subject = 'Product Price has been Changed'
                message = f'The price of "{prd["product_name"]}" has changed from {prd["price_x"]} to {prd["price_y"]}. Link: {prd["product_url"]}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = ['your-email@example.com']

                send_mail(subject, message, from_email, recipient_list)
