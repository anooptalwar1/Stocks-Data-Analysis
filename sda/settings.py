import environ
from corsheaders.defaults import default_headers

root = environ.Path(__file__) - 2  # get root of the project
env = environ.Env()
# reading .env file
environ.Env.read_env()

BASE_DIR = root()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")
REFRESH_TOKEN_SECRET= SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "psqlextra",
    "sda",
    "reporting",
    "rest_framework",
    "corsheaders",
    "django_filters",
    # "drf_spectacular",
]

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%s000",
    "DATE_FORMAT": "%s000",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "reporting.middleware.auth_middleware.AuthMiddleware",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "ORDERING_PARAM": "order",
}

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "sda.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sda.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env.str("DATABASE_NAME", "postgres"),
        "USER": env.str("DATABASE_USER", "postgres"),
        "PASSWORD": env.str("DATABASE_PASSWORD"),
        "HOST": env.str("DATABASE_HOST", "localhost"),
        "PORT": env.int("DATABASE_PORT", 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

# CORS
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=False)
CORS_ORIGIN_WHITELIST = env.tuple("CORS_ORIGIN_WHITELIST")
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS", default=True)
CORS_ALLOW_HEADERS = list(default_headers) + env.list("CORS_ALLOW_HEADERS", default=[])

SPECTACULAR_SETTINGS = {
    "TITLE": "Stocks Data Analysis",
    "DESCRIPTION": "API for SDA",
    "VERSION": "1.0.0",
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "reporting.open_api.hooks.overview.populate",
        "reporting.open_api.hooks.drop_docs.drop",
        "reporting.open_api.hooks.securitySchemes.populate",
        "reporting.open_api.hooks.authorization.populate",
        "reporting.open_api.hooks.authorization_matrix.populate",
    ],
}
