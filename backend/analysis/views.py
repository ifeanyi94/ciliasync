from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AnalysisResult
from .serializers import AnalysisResultSerializer

# ViewSet for CRUD operations, including image upload
class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors if invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Optional simple endpoint (not required)
def results_view(request):
    return JsonResponse({'message': 'This is the Django /results/ endpoint'})

# New API view for filtered results
@api_view(['GET'])
def filtered_results(request):
    queryset = AnalysisResult.objects.all()

    # Optional filters (update field names accordingly if needed)
    tags = request.GET.get('tags')
    condition = request.GET.get('condition')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # You may want to add these fields to your model if filtering by them is needed
    if tags:
        queryset = queryset.filter(tags__icontains=tags)
    if condition:
        queryset = queryset.filter(condition__iexact=condition)
    if start_date and end_date:
        queryset = queryset.filter(uploaded_at__range=[start_date, end_date])

    serializer = AnalysisResultSerializer(queryset, many=True)
    return Response(serializer.data)
