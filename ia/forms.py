from django import forms
from .models import ConfiguracaoIA, CotaMensalIA


class ConfiguracaoIAForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoIA
        fields = [
            'nome',
            'provedor',
            'modelo',
            'api_key',
            'temperatura',
            'max_tokens_resposta',
            'cota_mensal_padrao',
            'ativo',
        ]
        widgets = {
            'api_key': forms.PasswordInput(render_value=True, attrs={'placeholder': 'AIzaSy...'}),
        }


class CotaUsuarioForm(forms.ModelForm):
    class Meta:
        model = CotaMensalIA
        fields = ['limite_tokens']