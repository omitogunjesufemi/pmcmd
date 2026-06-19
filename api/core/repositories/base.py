from django.db.models import Model
from typing import Type

class BaseRepository:
    model : Type[Model] = None

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, id):
        return self.model.objects.filter(id=id).first()