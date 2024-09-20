from django.forms import IntegerField
from django.forms.widgets import Input
from django.forms.util import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class PercentInput(Input):
    """ A simple form input for a percentage """

    input_type = "text"

    def _format_value(self, value):
        if value is None:
            return ""
        return str(int(value * 100))

    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        return super(PercentInput, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        return super(PercentInput, self)._has_changed(self._format_value(initial), data)


class PercentField(IntegerField):
    """ A field that gets a value between 0 and 1 and displays as a value between 0 and 100"""

    widget = PercentInput(attrs={"class": "percentInput", "size": 4})

    default_error_messages = {
        "positive": _(u"Must be a positive number."),
    }

    def clean(self, value):
        """
        Validates that the input can be converted to a value between 0 and 1.
        Returns a Decimal
        """
        value = super(PercentField, self).clean(value)
        if value is None:
            return None
        if value < 0:
            raise ValidationError(self.error_messages["positive"])
        return Decimal("%.2f" % (value / 100.0))