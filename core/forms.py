from django import forms

from .models import CONTACT_MESSAGE_MAX_LENGTH, Contact


class ContactForm(forms.ModelForm):
    # honeypot
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "",
                "data-en": "Name",
                "data-pl": "Imię",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "",
                "data-en": "Email",
                "data-pl": "Email",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "maxlength": str(CONTACT_MESSAGE_MAX_LENGTH),
                "placeholder": "",
                "data-en": "Message",
                "data-pl": "Wiadomość",
            }),
        }

    def clean_website(self):
        data = self.cleaned_data.get("website")
        if data:
            raise forms.ValidationError("Bot detected.")
        return data


def portal_contact_form(*, bilingual: bool = True) -> ContactForm:
    """ContactForm styled for portal pages (kodzillin' / hub)."""
    form = ContactForm()
    extras = {
        "name": {"class": "portal-input", "autocomplete": "name"},
        "email": {"class": "portal-input", "autocomplete": "email"},
        "message": {"class": "portal-input", "rows": "4"},
    }
    for field, attrs in extras.items():
        form.fields[field].widget.attrs.update(attrs)
        if not bilingual:
            widget = form.fields[field].widget
            widget.attrs.pop("data-en", None)
            pl_label = widget.attrs.pop("data-pl", None)
            if pl_label:
                widget.attrs["placeholder"] = pl_label
    return form
