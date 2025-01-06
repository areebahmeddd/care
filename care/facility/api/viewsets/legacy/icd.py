from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class ICDViewSet(ViewSet):
    def serialize_data(self, objects: list):
        return [diagnosis.get_representation() for diagnosis in objects]

    def retrieve(self, request, pk):
        obj = None
        if not obj:
            raise Http404
        return Response(obj)

    def list(self, request):
        result = []
        return Response(self.serialize_data(result))
