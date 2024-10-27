from django import forms
from content.models import SeekingAd

class CommentForm(forms.Form):
    name = forms.CharField()
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": "6", "cols": "50"}
        )
    )


class SeekingAdForm(forms.ModelForm):
    class Meta:
        model = SeekingAd
        fields = ["seeking", "member", "club",
                  "content"]
        labels = {'seeking': "I am seeking a"}
        help_texts = {"member": "Fill in if you are member seeking a club",
                      "club": "Fill in if you are club seeking a member"}
    # Alternitae way to populate labels, widgets and help texts
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["seeking"].label = "I am seeking a"
    #     self.fields["member"].help_text = \
    #         "Fill in if you are member seeking a club"
    #     self.fields["club"].help_text = \
    #         "Fill in if you are club seeking a member"
