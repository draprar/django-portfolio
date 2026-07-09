from django.conf import settings
from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage


class SupabasePublicStorage(S3Boto3Storage):
    """
    Storage domyślny dla CAŁEGO projektu (STORAGES["default"] w settings.py).
    Nietknięty — wszystkie appki poza 'bies' dalej jadą na Supabase.
    """
    default_acl = "public-read"
    file_overwrite = False

    def url(self, name, parameters=None, expire=None, http_method=None):
        return f"{settings.MEDIA_URL}{name}"


class R2MediaStorage(S3Boto3Storage):
    """
    Storage używany WYŁĄCZNIE przez appkę 'bies' (pola obraz/wideo modelu Swieto).
    Cloudflare R2 — S3-compatible, zero opłat za egress.
    Podpinany bezpośrednio w polach modelu (storage=get_bies_storage),
    więc nie dotyka globalnego STORAGES["default"] ani innych appek.
    """
    bucket_name = settings.R2_BUCKET_NAME
    endpoint_url = settings.R2_ENDPOINT_URL
    access_key = settings.R2_ACCESS_KEY_ID
    secret_key = settings.R2_SECRET_ACCESS_KEY
    region_name = "auto"
    default_acl = None          # R2 nie używa ACL — dostęp kontrolowany na poziomie bucketa
    file_overwrite = False
    querystring_auth = False    # bucket publiczny, bez podpisanych/wygasających URL-i
    custom_domain = settings.R2_PUBLIC_DOMAIN  # np. pub-xxxxxxxx.r2.dev


def get_bies_storage():
    """
    Callable przekazywany do storage= w polach ImageField/FileField appki 'bies'.
    Django rozwiązuje go leniwie przy każdym użyciu, więc:
      - w produkcji (USE_S3=True) zwraca R2MediaStorage(),
      - lokalnie/w dev (USE_S3=False) zwraca None -> Django użyje
        domyślnego FileSystemStorage, więc nic nie wymaga kluczy R2 do pracy lokalnej.
    """
    if settings.USE_S3:
        return R2MediaStorage()
    return default_storage
