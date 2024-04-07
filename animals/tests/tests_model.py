from animals.models import Animal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from groups.models import Group
from traits.models import Trait


class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_1_data = {
            "name": "SunnyLee",
            "age": 5,
            "weight": 7,
            "sex": "Femea",
            "group": {"name": "gato", "scientific_name": "felinossauro"},
            "traits": [
                {"name": "gordinha"},
                {
                    "name": "peluda",
                },
            ],
        }
        cls.group_1_data = cls.animal_1_data.pop("group")
        cls.group_1 = Group.objects.create(**cls.group_1_data)
        cls.group_2_data = {
            "name": "peixe",
            "scientific_name": "conodonte",
        }
        cls.group_2 = Group.objects.create(**cls.group_2_data)
        cls.traits_1_data = cls.animal_1_data.pop("traits")
        cls.trait_1 = Trait.objects.create(**cls.traits_1_data[0])
        cls.trait_2 = Trait.objects.create(**cls.traits_1_data[1])
        cls.animal_1 = Animal.objects.create(
            **cls.animal_1_data, group=cls.group_1
        )

        cls.animal_1.traits.add(cls.trait_1)
        cls.animal_1.traits.add(cls.trait_2)

    def test_name_max_length(self):
        animal = Animal.objects.get(id=1)
        max_length = animal._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)

    def test_sex_max_length(self):
        animal = Animal.objects.get(id=1)
        max_length = animal._meta.get_field("sex").max_length
        self.assertEquals(max_length, 15)

    def test_group_name_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field("name").max_length
        self.assertEquals(max_length, 20)

    def test_group_scientific_name_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field("scientific_name").max_length
        self.assertEquals(max_length, 50)

    def test_traits_name_max_length(self):
        trait = Trait.objects.get(id=1)
        max_length = trait._meta.get_field("name").max_length
        self.assertEquals(max_length, 20)

    def test_animal_has_information_fields(self):
        self.assertEqual(self.animal_1.name, self.animal_1_data["name"])
        self.assertEqual(self.animal_1.age, self.animal_1_data["age"])
        self.assertEqual(self.animal_1.weight, self.animal_1_data["weight"])
        self.assertEqual(self.animal_1.sex, self.animal_1_data["sex"])

    def test_group_has_information_fields(self):
        self.assertEqual(self.group_1.name, self.group_1_data["name"])
        self.assertEqual(
            self.group_1.scientific_name, self.group_1_data["scientific_name"]
        )

    def test_traits_has_information_fields(self):
        self.assertEqual(
            self.trait_1.name, self.traits_1_data[0]["name"]
        )  # trait 1
        self.assertEqual(
            self.trait_2.name, self.traits_1_data[1]["name"]
        )  # trait 2

    # Teste de Relacionamento

    def test_animal_cannot_belong_to_more_than_one_group(self):
        self.animal_1.group = self.group_2
        self.assertNotEqual(self.animal_1.group, self.group_1)
        self.assertEqual(self.animal_1.group, self.group_2)

    def test_animal_can_be_attached_to_multiple_traits(self):
        self.assertEqual(len(self.traits_1_data), self.animal_1.traits.count())