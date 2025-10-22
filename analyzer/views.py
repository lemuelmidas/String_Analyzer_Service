from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from urllib.parse import unquote
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from .utils import compute_properties, compute_sha256, parse_natural_language_query

class StringListCreateView(APIView):
    def get(self, request):
        qs = AnalyzedString.objects.all()
        qp = request.query_params

        try:
            if "is_palindrome" in qp:
                val = qp["is_palindrome"].lower() == "true"
                qs = [o for o in qs if o.properties["is_palindrome"] == val]
            if "min_length" in qp:
                qs = [o for o in qs if o.properties["length"] >= int(qp["min_length"])]
            if "max_length" in qp:
                qs = [o for o in qs if o.properties["length"] <= int(qp["max_length"])]
            if "word_count" in qp:
                qs = [o for o in qs if o.properties["word_count"] == int(qp["word_count"])]
            if "contains_character" in qp:
                c = qp["contains_character"]
                qs = [o for o in qs if c in o.value]
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

        ser = AnalyzedStringSerializer(qs, many=True)
        return Response({"data": ser.data, "count": len(ser.data)})

    def post(self, request):
        value = request.data.get("value")
        if not isinstance(value, str):
            return Response({"detail": "value must be a string"}, status=422)

        sha = compute_sha256(value)
        if AnalyzedString.objects.filter(sha256_hash=sha).exists():
            return Response({"detail": "String already exists"}, status=409)

        props = compute_properties(value)
        obj = AnalyzedString.objects.create(
            sha256_hash=sha,
            value=value,
            properties=props,
            created_at=timezone.now()
        )
        ser = AnalyzedStringSerializer(obj)
        return Response(ser.data, status=201)


class StringDetailView(APIView):
    def get(self, request, string_value):
        value = unquote(string_value)
        obj = AnalyzedString.objects.filter(value=value).first()
        if not obj:
            return Response({"detail": "Not found"}, status=404)
        return Response(AnalyzedStringSerializer(obj).data)

    def delete(self, request, string_value):
        value = unquote(string_value)
        obj = AnalyzedString.objects.filter(value=value).first()
        if not obj:
            return Response({"detail": "Not found"}, status=404)
        obj.delete()
        return Response(status=204)


class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"detail": "Missing query"}, status=400)

        try:
            filters = parse_natural_language_query(query)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        qs = AnalyzedString.objects.all()
        if filters.get("is_palindrome"):
            qs = [o for o in qs if o.properties["is_palindrome"]]
        if filters.get("word_count"):
            qs = [o for o in qs if o.properties["word_count"] == filters["word_count"]]
        if filters.get("min_length"):
            qs = [o for o in qs if o.properties["length"] >= filters["min_length"]]
        if filters.get("contains_character"):
            ch = filters["contains_character"]
            qs = [o for o in qs if ch in o.value]

        ser = AnalyzedStringSerializer(qs, many=True)
        return Response({
            "data": ser.data,
            "count": len(ser.data),
            "interpreted_query": {
                "original": query,
                "parsed_filters": filters
            }
        })
