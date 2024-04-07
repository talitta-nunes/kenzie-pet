from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView, Request, Response, status

from .models import Animal
from .serializers import AnimalDetailSerializer


class AnimalView(APIView):
    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalDetailSerializer(animals, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = AnimalDetailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class AnimalDetailView(APIView):
    def get(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalDetailSerializer(animal)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalDetailSerializer(
            animal, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValidationError as err:
            return Response(
                err.args,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
