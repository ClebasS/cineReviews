from django import forms

from filmes.models import Comentario


class FilmeForm(forms.Form):
    choices = [('Ação', 'Ação'), ('Aventura', 'Aventura'), ('Animação', 'Animação'), ('Biografia', 'Biografia'), ('Comédia', 'Comédia'), ('Crime', 'Crime'), ('Documentário', 'Documentário'), ('Drama', 'Drama'),
               ('Desporto', 'Desporto'), ('Família', 'Família'), ('Fantasia', 'Fantasia'), ('Ficção Científica', 'Ficção Científica'), ('Faroeste', 'Faroeste'), ('Guerra', 'Guerra'), ('História', 'História'),
               ('Mistério', 'Mistério'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), ('Terror', 'Terror')]
    generos = forms.MultipleChoiceField(choices=choices,
                                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-column'}))
