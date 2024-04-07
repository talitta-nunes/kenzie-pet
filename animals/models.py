from django.db import models


class Genders(models.TextChoices):
    MACHO = "Macho"
    FEMEA = "Femea"
    NÃO_INFORMADO = "Não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=Genders.choices, default=Genders.NÃO_INFORMADO
    )

    # FK 1:N

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE
    )

    # FK N:N

    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    def __repr__(self) -> str:
        return f"<Animal[{self.id}] {self.name} - {self.age}>"
