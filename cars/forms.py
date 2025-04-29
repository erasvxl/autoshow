from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'engine_volume', 'fuel_type', 'mileage', 'price', 'condition', 'image']
class CarFilterForm(forms.Form):
    brand = forms.CharField(required=False, label="Марка")
    min_year = forms.IntegerField(required=False, label="От года")
    max_year = forms.IntegerField(required=False, label="До года")
    fuel_type = forms.ChoiceField(choices=[('', 'Любой')] + Car.FUEL_TYPES, required=False, label="Тип топлива")
    condition = forms.ChoiceField(choices=[('', 'Любое')] + Car.CONDITION_TYPES, required=False, label="Состояние")
from .models import SupplyOrder

class SupplyOrderForm(forms.ModelForm):
    class Meta:
        model = SupplyOrder
        fields = ['supplier', 'status']
class DiscountForm(forms.Form):
    discount_percentage = forms.IntegerField(min_value=1, max_value=100, label="Скидка %")
class VINCheckForm(forms.Form):
    vin = forms.CharField(max_length=17, label="Введите VIN-номер")
class CarBrandForm(forms.Form):
    brand = forms.CharField(max_length=100, label="Выберите марку")
from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


from django import forms
from .models import CarOrder

class CarOrderForm(forms.ModelForm):
    pickup_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = CarOrder
        fields = ['color', 'completion', 'payment_method', 'pickup_date']
