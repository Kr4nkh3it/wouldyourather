from django.contrib import admin
from .models import Question,Choice

# Register your models here.
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question',{'fields':['question_text']}),
        ('Date',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question,QuestionAdmin)
