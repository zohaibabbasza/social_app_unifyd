from django.contrib import admin
from albums.models import Album,AlbumMedia

admin.site.register(AlbumMedia)
admin.site.register(Album)
