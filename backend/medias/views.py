import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from config import settings
from .models import Photo


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        # room = Room.objects.get(pk=photo.room)
        # experience = Experience.objects.get(pk=photo.experience)
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class GetUploadURL(APIView):
    def post(self, request):
        one_time_url = requests.post(
            url=f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload",
            headers={"Authorization": f"Bearer {settings.CF_TOKEN}"},
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        return Response({"id": result.get("id"), "uploadURL": result.get("uploadURL")})
