from django.contrib import admin

from .models import Articulator, Exercise, Funfact, OldPolish, Trivia, Twister

admin.site.register(Twister)
admin.site.register(Articulator)
admin.site.register(Exercise)
admin.site.register(Trivia)
admin.site.register(Funfact)
admin.site.register(OldPolish)
