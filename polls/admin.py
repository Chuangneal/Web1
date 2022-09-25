from django.contrib import admin

from .models import *


# TabularInline / StackedInline
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    # 1. Define the order simply
    fields = ['pub_date', 'question_text']

    # 2. Add subtitle
    # fieldsets = [
    #     (None, {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]

    inlines = [ChoiceInline]  # Add the operation of corresponding subclass

    list_display = ('question_text', 'pub_date', 'was_published_recently')  # Show more information (attribute)

    list_filter = ['pub_date']  # Add a filter

    search_fields = ['question_text']  # Search capacity


class PosterAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'programme', 'division')


admin.site.register(Question, QuestionAdmin)  # Register it to admin page

admin.site.register(Choice)

admin.site.register(Poster, PosterAdmin)

admin.site.register(Attendee)

admin.site.register(Conference)

admin.site.register(Staff)

admin.site.register(ProgrammeJudge)

admin.site.register(HeadJudge)

admin.site.register(Chairman)

admin.site.register(Coordinator)

admin.site.register(Admin)

admin.site.register(EmailHistory)

admin.site.register(UICInfo)
