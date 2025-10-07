from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import re
from .models import Recipe
from .serializers import RecipeSerializer


class RecipePagination(PageNumberPagination):
    """
    Custom pagination class for recipes.
    """
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100


class RecipeListView(generics.ListAPIView):
    """
    GET /api/recipes
    Returns paginated list of recipes sorted by rating (descending).
    Query params: page, limit
    """
    queryset = Recipe.objects.all().order_by('-rating', 'title')
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            # Custom response format
            return Response({
                'page': int(request.GET.get('page', 1)),
                'limit': int(request.GET.get('limit', 10)),
                'total': paginated_response.data['count'],
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecipeSearchView(generics.ListAPIView):
    """
    GET /api/recipes/search
    Search recipes with filters:
    - calories: supports operators (e.g., <=400, >=200, =300)
    - title: partial match (case-insensitive)
    - cuisine: partial match (case-insensitive)
    - total_time: supports operators (e.g., <=60, >=30)
    - rating: supports operators (e.g., >=4.5, <=5.0)
    """
    serializer_class = RecipeSerializer

    def parse_operator_value(self, param_value):
        """
        Parse parameter value with operator.
        Returns (operator, value) tuple.
        Supported operators: <=, >=, <, >, =
        """
        match = re.match(r'^(<=|>=|<|>|=)?(.+)$', str(param_value).strip())
        if match:
            operator = match.group(1) or '='
            value = match.group(2).strip()
            return operator, value
        return '=', param_value

    def get_queryset(self):
        queryset = Recipe.objects.all()

        # Filter by calories (from nutrients JSONB field)
        calories_param = self.request.query_params.get('calories', None)
        if calories_param:
            operator, value = self.parse_operator_value(calories_param)
            try:
                calories_value = float(value.replace('kcal', '').strip())

                # Query JSONB field for calories
                # Strip " kcal" from the value before casting
                if operator == '<=':
                    queryset = queryset.extra(
                        where=["CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) <= %s"],
                        params=[calories_value]
                    )
                elif operator == '>=':
                    queryset = queryset.extra(
                        where=["CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) >= %s"],
                        params=[calories_value]
                    )
                elif operator == '<':
                    queryset = queryset.extra(
                        where=["CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) < %s"],
                        params=[calories_value]
                    )
                elif operator == '>':
                    queryset = queryset.extra(
                        where=["CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) > %s"],
                        params=[calories_value]
                    )
                elif operator == '=':
                    queryset = queryset.extra(
                        where=["CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) = %s"],
                        params=[calories_value]
                    )
            except (ValueError, TypeError):
                pass

        # Filter by title (partial match)
        title_param = self.request.query_params.get('title', None)
        if title_param:
            queryset = queryset.filter(title__icontains=title_param)

        # Filter by cuisine (partial match)
        cuisine_param = self.request.query_params.get('cuisine', None)
        if cuisine_param:
            queryset = queryset.filter(cuisine__icontains=cuisine_param)

        # Filter by total_time
        total_time_param = self.request.query_params.get('total_time', None)
        if total_time_param:
            operator, value = self.parse_operator_value(total_time_param)
            try:
                time_value = int(value)
                if operator == '<=':
                    queryset = queryset.filter(total_time__lte=time_value)
                elif operator == '>=':
                    queryset = queryset.filter(total_time__gte=time_value)
                elif operator == '<':
                    queryset = queryset.filter(total_time__lt=time_value)
                elif operator == '>':
                    queryset = queryset.filter(total_time__gt=time_value)
                elif operator == '=':
                    queryset = queryset.filter(total_time=time_value)
            except (ValueError, TypeError):
                pass

        # Filter by rating
        rating_param = self.request.query_params.get('rating', None)
        if rating_param:
            operator, value = self.parse_operator_value(rating_param)
            try:
                rating_value = float(value)
                if operator == '<=':
                    queryset = queryset.filter(rating__lte=rating_value)
                elif operator == '>=':
                    queryset = queryset.filter(rating__gte=rating_value)
                elif operator == '<':
                    queryset = queryset.filter(rating__lt=rating_value)
                elif operator == '>':
                    queryset = queryset.filter(rating__gt=rating_value)
                elif operator == '=':
                    queryset = queryset.filter(rating=rating_value)
            except (ValueError, TypeError):
                pass

        return queryset.order_by('-rating', 'title')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'data': serializer.data
        })
