import math

from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from traits.models import Trait
from traits.serializers import TraitSerializer

from .models import Animal, Genders


class AnimalDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Genders.choices, default=Genders.NÃO_INFORMADO
    )

    age_in_human_years = serializers.SerializerMethodField()

    def get_age_in_human_years(self, obj: Animal):
        human_age = 16 * math.log(obj.age) + 31
        round_age = math.ceil(human_age)
        return round_age

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def create(self, validated_data: dict) -> Animal:
        traits_list = validated_data.pop("traits")
        group_data = validated_data.pop("group")
        group_obj, _ = Group.objects.get_or_create(**group_data)

        animal_obj = Animal.objects.create(**validated_data, group=group_obj)

        for traits_dict in traits_list:
            trait_obj, _ = Trait.objects.get_or_create(**traits_dict)
            animal_obj.traits.add(trait_obj)

        return animal_obj

    def update(self, instance: Animal, validated_data: dict):
        coupled_keys = ("group", "traits", "sex")
        errors = {}

        for key, value in validated_data.items():
            if key in coupled_keys:
                errors.update({key: f"{key} property cannot be updated"})
                continue
            setattr(instance, key, value)
        if errors:
            raise ValidationError(errors)
        instance.save()

        return instance
