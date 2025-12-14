from django.contrib import admin

from . models import Election,Candidates,Position,Vote

# Register your models here.

@admin.register(Election)

class Electionadmin(admin.ModelAdmin):
    display=("name","start_date","end_date",)


@admin.register(Candidates)

class Candidatesadmin(admin.ModelAdmin):
    display=("user","position","manifesto")


@admin.register(Position)

class Positionadmin(admin.ModelAdmin):
    display=("name","election")


@admin.register(Vote)

class Voteadmin(admin.ModelAdmin):
    display=("voter","position","candiate")
