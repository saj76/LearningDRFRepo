import os

from django import forms
from django.conf import settings
# from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage
from faust.exceptions import ValidationError


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, *args, **kwargs):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def get_field_names(instance, filters=None, excludes=None) -> set:
    field_names = {f.name for f in instance.__class__._meta.get_fields()}
    if filters is not None:
        field_names &= set(filters)
    field_names -= set(excludes or [])
    return field_names


def model_as_dict(instance, ignored_fields=None):
    fields = get_field_names(instance)
    if not ignored_fields:
        ignored_fields = ['id']

    for i_field in ignored_fields:
        if i_field in fields:
            fields.remove(i_field)
    dic = dict()
    for f in fields:
        value = getattr(instance, f, None)
        try:
            value = getattr(value, 'as_dict')()
        except AttributeError:
            pass
        if value is not None:
            dic[f] = value

    return dic


def update_model_instance(instance, update_dict, key_types=None):
    for k, v in update_dict.items():
        if isinstance(v, dict):
            if getattr(instance, k, None):
                update_model_instance(getattr(instance, k), v)
            else:
                klass = key_types[k]
                attr = klass.objects.create(**v)
                setattr(instance, k, attr)
        else:
            setattr(instance, k, v)

    instance.save()

#
# class ChoiceArrayField(ArrayField):
#     """
#     A field that allows us to store an array of choices.
#     Uses Django's Postgres ArrayField
#     and a MultipleChoiceField for its formfield.
#     """
#
#     def formfield(self, **kwargs):
#         defaults = {
#             'form_class': forms.MultipleChoiceField,
#             'choices': self.base_field.choices,
#         }
#         defaults.update(kwargs)
#         return super(ArrayField, self).formfield(**defaults)


def validate_lower_case(value):
    if not value.islower():
        return ValidationError('Only lowercase values are allowed')
    return value
