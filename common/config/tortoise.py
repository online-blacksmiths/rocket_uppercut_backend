from common.config.settings import conf

TORTOISE_ORM = {
    'connections': {
        'master': conf().DB_URL
    },
    'apps': {
        'models': {
            'models': [],
            'default_connection': 'master'
        }
    }
}
