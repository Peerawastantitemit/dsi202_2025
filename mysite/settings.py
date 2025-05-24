import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f(0#gricomt=m=#b(ins_k$$z+c)$hpvw=e=zxnc30ma3+mtj^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'treevaq_app',

    # Allauth apps
    'allauth', # <--- เพิ่มบรรทัดนี้
    'allauth.account', # <--- เพิ่มบรรทัดนี้
    'allauth.socialaccount', # <--- เพิ่มบรรทัดนี้
    'allauth.socialaccount.providers.google', # <--- เพิ่มบรรทัดนี้สำหรับ Google
    # ถ้าอยากได้ provider อื่นๆ เช่น 'allauth.socialaccount.providers.facebook',
    'crispy_forms', # <--- เพิ่มบรรทัดนี้
    'crispy_bootstrap5', # <--- เพิ่มบรรทัดนี้ (เราจะใช้ Bootstrap 5 เป็นตัวอย่าง)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # อาจจะมี 'templates' ใน root project
        'APP_DIRS': True, # ให้ Django ค้นหา templates ในโฟลเดอร์ 'templates' ของแต่ละ app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', 
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # หรือชื่ออื่นที่ต้องการ
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'treevaq_app/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/' # เมื่อ Login สำเร็จจะเปลี่ยนเส้นทางไปหน้าแรก
LOGOUT_REDIRECT_URL = '/' # เมื่อ Logout สำเร็จจะเปลี่ยนเส้นทางไปหน้าแรก

# Allauth specific settings
SITE_ID = 1 # <--- สำคัญสำหรับ allauth (ต้องมี)

ACCOUNT_LOGIN_METHODS = {'email', 'username'}  # ใช้ได้หลายวิธี
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # * คือบังคับกรอก
ACCOUNT_SIGNUP_EMAIL_ENTER_UNIQUE = True # อีเมลต้องไม่ซ้ำกัน
ACCOUNT_LOGOUT_ON_GET = True # ทำให้ Logout ง่ายขึ้น (คลิกแล้วออกเลย)
ACCOUNT_EMAIL_VERIFICATION = 'none' # หรือ 'mandatory' ถ้าต้องการยืนยันอีเมล

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Crispy Forms setting
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'), # <--- อ่านจาก Environment Variable
            'secret': os.environ.get('GOOGLE_SECRET'), # <--- อ่านจาก Environment Variable
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}