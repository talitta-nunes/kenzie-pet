from animals.models import Animal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from groups.models import Group
from traits.models import Trait


class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_list_data = [
            {
                "name": "Sunny",
                "age": 5,
                "weight": 7,
                "sex": "Femea",
                "group": {
                    "name": "gato",
                    "scientific_name": "felinossauro",
                },
                "traits": [
                    {"name": "gordinha"},
                    {
                        "name": "peluda",
                    },
                ],
            },
            {
                "name": "Morena",
                "age": 4,
                "weight": 8,
                "sex": "Femea",
                "group": {
                    "name": "gato",
                    "scientific_name": "felinossauro",
                },
                "traits": [
                    {"name": "marrom"},
                    {
                        "name": "fofinha",
                    },
                ],
            },
        ]

        cls.group_1_data = cls.animal_list_data.pop("group")
        cls.group_1 = Group.objects.create(**cls.group_1_data)
        cls.group_2_data = {
            "name": "peixe",
            "scientific_name": "conodonte",
        }
        cls.group_2 = Group.objects.create(**cls.group_2_data)
        cls.traits_1_data = cls.animal_1_data.pop("traits")
        cls.trait_1 = Trait.objects.create(**cls.traits_1_data[0])
        cls.trait_2 = Trait.objects.create(**cls.traits_1_data[1])
        cls.animal_1_list = Animal.objects.create(
            **cls.animal_list_data, group=cls.group_1
        )

        cls.animal_1.traits.add(cls.trait_1)
        cls.animal_1.traits.add(cls.trait_2)

    def test_group_can_have_multiple_animals(self):

        for animal in self.animal_1_list:
            animal.group = self.group_1
            animal.save()

        self.assertEquals(
            len(self.animal_1_list), self.group_1.animal_1_list.count()
        )

        for animal in self.animal_1_list:
            self.assertIs(animal.group, self.group_1)
