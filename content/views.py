from rest_framework.views import APIView, Response, Request, status
from .models import Content
from django.forms.models import model_to_dict
from .serializers import ContentSerializer


class ContentView(APIView):
    def get(self, request: Request):
        content = Content.objects.all()

        content_dict = [model_to_dict(content) for content in content]

        return Response(content_dict, status.HTTP_200_OK)

    def post(self, request: Request):
        check_key = ContentSerializer(**request.data)
        if check_key.is_valid():
            content = Content.objects.create(**check_key.data)
            content.save()
            content_dict = model_to_dict(content)
            return Response(content_dict, status.HTTP_201_CREATED)
        else:
            return Response(check_key.errors, status.HTTP_400_BAD_REQUEST)


class ContentDetailView(APIView):
    def get(self, request: Request, content_id: int):
        try:
            content = Content.objects.get(pk=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status.HTTP_404_NOT_FOUND)

        return Response(model_to_dict(content), status.HTTP_200_OK)

    def patch(self, request: Request, content_id: int):
        try:
            content = Content.objects.get(pk=content_id)
            for content_key, content_value in request.data.items():
                setattr(content, content_key, content_value)
            Content.save(content)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status.HTTP_404_NOT_FOUND)

        return Response(model_to_dict(content), status.HTTP_200_OK)

    def delete(self, request: Request, content_id: int):
        try:
            content = Content.objects.get(pk=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status.HTTP_404_NOT_FOUND)

        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentFindView(APIView):
    def get(self, request: Request):
        title = request.query_params.get("title", None)

        content = Content.objects.filter(title__icontains=title)
        content_dict = [model_to_dict(content) for content in content]

        if len(content_dict) == 0:
            return Response({"message": "Content not found"}, status.HTTP_404_NOT_FOUND)

        return Response(content_dict, status=status.HTTP_200_OK)
