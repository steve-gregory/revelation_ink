from django.contrib import admin

from website.models import AboutPagePhoto, FrontPagePhoto

class AboutPagePhotoAdmin(admin.ModelAdmin):
	pass


class FrontPagePhotoAdmin(admin.ModelAdmin):
	pass

admin.site.register(AboutPagePhoto, AboutPagePhotoAdmin)
admin.site.register(FrontPagePhoto, FrontPagePhotoAdmin)
