# views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import status
import re

from .models import Collection, CollectionItems
from .serializers import CategoryListSerializer,categoryFetchSerializer,CollectionItemsProductIdSerializer,CollectionSerializer, CollectionItemsSerializer
from .getComission import findCategoriesCommision
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class CollectionItemsViewSet(viewsets.ModelViewSet):
    queryset = CollectionItems.objects.all()
    serializer_class = CollectionItemsSerializer
# views.py

class CollectionCreateView(APIView):
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response":"collection saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionItemsCreateView(APIView):
    def post(self, request):
        serializer = CollectionItemsSerializer(data=request.data)
        collection_items = CollectionItems.objects.filter(
            user_id=request.data.get('user_id'), 
            product_id=request.data.get('product_id'),
            collection_id=request.data.get('collection_id')
        )
        
        # Check if any items exist
        if collection_items.exists():
            # Delete all matching items
            collection_items.delete()
            return Response({"response":"collection item deleted"}, status=status.HTTP_201_CREATED)


        if serializer.is_valid():
            serializer.save()
            return Response({"response":"collection item saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionItemsSearchView(generics.ListAPIView):
    serializer_class = CollectionItemsSerializer

    def get_queryset(self):
        queryset = CollectionItems.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        product_ids = self.request.query_params.getlist('product_ids', None)

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if product_ids:
            queryset = queryset.filter(product_id__in=product_ids)
        return queryset

class CollectionsSearchView(generics.ListAPIView):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        queryset = Collection.objects.all()
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

# class getCommision(generics.ListAPIView):
#     serializer_class = categoryFetchSerializer
#     def get_queryset(self):
#         # Retrieve the 'category_ids' from the POST data (JSON body)
#         category_ids = self.request.data.get('category_ids', None)
        
#         if category_ids:
#             category_data = 0
#             # category_data = findCategoriesCommision(category_ids)
            
#             # If commission data is found, return it in the response
#             if category_data:
#                 return JsonResponse({"category_data": category_data}, status=status.HTTP_200_OK)
#             else:
#                 # Return error message if no commission data is found
#                 return JsonResponse({"error": "No commission found for the given categories"}, status=status.HTTP_404_NOT_FOUND)
        
#         # If 'category_ids' is not provided in the request body
#         return JsonResponse({"error": "No category IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
    


class getCommision(APIView):
    def get(self, request):
        # Retrieve category_ids from query parameters
        category_ids = request.query_params.get('category_ids', None)
        title = request.query_params.get('title', None)

        if category_ids:
            # Ensure category_ids is a string (handle case where it might be bytes)
            if isinstance(category_ids, bytes):
                category_ids = category_ids.decode('utf-8')  # Decode bytes to string if needed
            category_ids = category_ids.replace(" ", "")  # Remove spaces

            # Split category_ids string into a list of strings
            category_ids_list = category_ids.split(',')
            category_ids_list = list(map(str, category_ids_list))  # Ensure they are strings

            # Wrap the list in a dictionary to match the serializer's expected input
            data = {'category_ids': category_ids_list}

            # Pass the data to the serializer
            serializer = categoryFetchSerializer(data=data)
            commisionsData=findCategoriesCommision(data['category_ids'])
            # Validate the serializer
            if serializer.is_valid():
                # Simulate commission data retrieval (replace with actual logic)
                commission_data = 0  
                index=0
                matched_commision=[]
                for commisionData in commisionsData:
                    print("category Id is ",category_ids_list[index])
                    if commisionData['category_id'] in category_ids_list:
                        print("category matched")
                        matched_commision.append(commisionData)
                    else:
                        keywords=commisionData['category_url']
                        keywords=keywords.split('-')
                        print(title)
                        print(keywords)
                        matched_keywords = [keyword for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', title, re.IGNORECASE)]
                        if matched_keywords:
                            matched_commision.append(commisionData)
                            print(matched_keywords)
                    index+=1
                if matched_commision:
                    print(matched_commision[-1])
                else:
                    if commisionsData:
                        matched_commision.append(commisionsData)
                if not matched_commision:
                    return Response({"success": True, "data":{"category_id":0, "category_url":"", "commission":15}}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": True, "data": matched_commision[-1]}, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Handle case where no category_ids are provided in the query parameters
        return Response({"error": "No category_ids provided in query parameters"}, status=status.HTTP_400_BAD_REQUEST)