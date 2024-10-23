# from django import forms
# from .models import Collection

# class AddToWishlistForm(forms.Form):
#     collection = forms.ModelChoiceField(
#         queryset=Collection.objects.none(),
#         required=False,
#         empty_label="Default Wishlist"
#     )

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
#         self.fields['collection'].queryset = Collection.objects.filter(user=user)
