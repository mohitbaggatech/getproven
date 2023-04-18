from django.forms import ModelForm, ChoiceField
from weather.models import Location, DETAILING_TYPES


class LocationForm(ModelForm):
    detailing = ChoiceField(choices=DETAILING_TYPES)

    class Meta:
        model = Location
        fields = ["lat", "long"]

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields["lat"].widget.attrs["class"] = "input input-md mr-5"
        self.fields["long"].widget.attrs["class"] = "input input-md mb-10"
