from django.contrib import admin

# Register your models here.
from cms.models import Subject, Chapter, Subtopic, SAQ, Numerical, Subsection, SubsectionImage

class ChapterModelAdmin(admin.ModelAdmin):
	list_display = ["chapter_serial", "chapter_name"]
	list_display_links = ["chapter_name"]
	list_filter = ["section"]
	search_fields = ["chapter_name", "section"]
	class Meta:
		model = Chapter

class SubtopicModelAdmin(admin.ModelAdmin):
	list_display = ["subtopic_serial", "title"]
	list_display_links = ["title"]
	list_filter = ["chapter"]
	search_fields = ["title"]
	class Meta:
		model = Subtopic

class SAQModelAdmin(admin.ModelAdmin):
	list_display = ["question_serial", "question"]
	list_display_links = ["question"]
	list_filter = ["chapter"]
	class Meta:
		model = SAQ

class NumericalModelAdmin(admin.ModelAdmin):
	list_display = ["numerical_serial", "question"]
	list_display_links = ["question"]
	list_filter = ["chapter"]
	class Meta:
		model = Numerical

admin.site.register(Subject)
admin.site.register(Chapter, ChapterModelAdmin)
admin.site.register(Subtopic, SubtopicModelAdmin)
admin.site.register(SAQ, SAQModelAdmin)
admin.site.register(Numerical, NumericalModelAdmin)
admin.site.register(Subsection)
admin.site.register(SubsectionImage)