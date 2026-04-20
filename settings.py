"""
settings.py — oTree 5 configuration for the SHB Experiment
"""

from os import environ

SESSION_CONFIGS = [
    # ── Full experiment (production / Prolific) ───────────────
    {
        'name': 'shb_experiment_full',
        'display_name': "SHB Experiment — Full (3 rounds, real payment)",
        'app_sequence': ['shb_experiment'],
        'num_demo_participants': 4,
        'use_browser_bots': False,
        # Custom session-level configs (accessible via session.config[...])
        'real_world_currency_per_point': 0.10,  # $0.10 per ECU
        'participation_fee': 3.00,              # $3.00 base pay (handled in app)
        'prolific_completion_url': '',           # Set to your Prolific completion URL
    },
    # ── Short demo / pilot (1 round, no real payment) ─────────
    {
        'name': 'shb_experiment_demo',
        'display_name': "SHB Experiment — Demo (1 round, for piloting)",
        'app_sequence': ['shb_experiment'],
        'num_demo_participants': 4,
        'use_browser_bots': False,
        'real_world_currency_per_point': 0.0,
        'participation_fee': 0.0,
    },
]

# ── oTree configuration ────────────────────────────────────────
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10,
    participation_fee=3.00,
    doc="",
)

PARTICIPANT_FIELDS = [
    'condition',         # 'shb' or 'no_shb' — assigned once in round 1
    'prolific_id',       # captured via URL parameter from Prolific
]

SESSION_FIELDS = []

# ── Internationalisation ───────────────────────────────────────
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False        # We use ECU (stored as floats); convert to USD in app

# ── Admin ──────────────────────────────────────────────────────
ADMIN_USERNAME = 'admin'
# Use environment variable for password in production
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'change_me_in_production')

DEMO_PAGE_INTRO_HTML = """
<p>This is a demo of the <strong>Salary History Ban Experiment</strong>.</p>
<p>Participants are randomly assigned to either the <em>SHB condition</em>
(employer cannot see salary history) or the <em>No-SHB condition</em>
(employer can see full salary history).</p>
<p>The experiment tests whether salary history availability affects
human capital investment incentives.</p>
"""

SECRET_KEY = environ.get('OTREE_SECRET_KEY', '{{ secret_key }}')

# ── Debug mode ─────────────────────────────────────────────────
# Set OTREE_PRODUCTION=1 in environment to disable debug mode in production
DEBUG = not environ.get('OTREE_PRODUCTION')

# ── Prolific URL parameter (capture participant ID) ────────────
# In Prolific study settings, set completion URL redirect and pass
# the PROLIFIC_PID as a URL parameter:
#   https://your-server.com/InitializeParticipant?participant_label={{%PROLIFIC_PID%}}

# ── Room for Prolific (optional) ──────────────────────────────
ROOMS = [
    {
        'name': 'prolific_shb',
        'display_name': 'SHB Experiment (Prolific)',
        'participant_label_file': '_rooms/prolific_shb.txt',  # optional pre-generated labels
        'use_secure_urls': True,
    },
]

# ── Database configuration (Heroku PostgreSQL) ───────────────
try:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default='sqlite:///db.sqlite3')
    }
except ImportError:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# ── Static files (WhiteNoise for Heroku) ─────────────────────
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Allowed hosts (for Heroku deployment) ────────────────────
ALLOWED_HOSTS = ['*'] if DEBUG else [environ.get('HEROKU_APP_NAME', '') + '.herokuapp.com']
