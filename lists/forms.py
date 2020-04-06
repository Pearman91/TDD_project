from django import forms

from lists.models import Item


EMPTY_ITEM_ERROR = "Nana, we won't let you put in empty items."


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Just write down sth.'})}
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}}
