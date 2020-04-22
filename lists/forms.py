from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List

EMPTY_ITEM_ERROR = "Nana, we won't let you put in empty items."
DUPLICATE_ITEM_ERROR = "You aready have this on your list."


class ItemForm(forms.models.ModelForm):

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Just write down sth.'})}
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}}


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def save(self):
        return forms.models.ModelForm.save(self)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'],
                owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])
