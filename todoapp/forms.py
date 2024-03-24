from django import forms
from .models import Comment
from .models import todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name', 'description']
        labels = {
            'todo_name': 'Título',
            'description' : 'Descripción',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['todo_name'].widget.attrs.update({"placeholder": "Agregue un Título"})
        self.fields['description'].widget.attrs.update({"placeholder": "Agregue una descripción",'style': 'height: 80px;'})

    def clean_todo_name(self):
        todo_name = self.cleaned_data.get('todo_name')
        if not todo_name:
            raise forms.ValidationError('Este campo es requerido')
        return todo_name
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(
        label="Correo",
        widget=forms.TextInput(attrs={
            "placeholder": "Correo electrónico del destinatario",
            "style": "width: 300px;"
        })
    )
    comment = forms.CharField(
        label="Comentario",
        widget=forms.Textarea(attrs={ "placeholder": "Agregue un comentario",
            'rows': 3, 'cols': 38}), 
        required=False)


    

