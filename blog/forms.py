from django import forms
from .models import AIPrompt


class AIPromptForm(forms.ModelForm):
    """Form for creating AI-generated blog posts"""

    class Meta:
        model = AIPrompt
        fields = ['model_name', 'prompt_text']
        widgets = {
            'model_name': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'id': 'id_model_name'
            }),
            'prompt_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'id': 'id_prompt_text',
                'placeholder': 'Wprowadź szczegółowy prompt, np.: "Napisz post o pięknych plażach Bali, Indonezja. Współrzędne: -8.4095, 115.1889. Opisz najlepsze plaże, atrakcje turystyczne i porady dla podróżnych."'
            })
        }
        labels = {
            'model_name': 'Model AI',
            'prompt_text': 'Treść Promptu'
        }
        help_texts = {
            'prompt_text': 'Podaj szczegółowy prompt zawierający: nazwę miejsca, współrzędne geograficzne (szerokość, długość), oraz co AI powinno opisać.'
        }

