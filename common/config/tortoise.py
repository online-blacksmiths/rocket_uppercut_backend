from common.config.settings import conf

TORTOISE_ORM = {
    'connections': {
        'master': conf().DB_URL if not conf().TEST_MODE else conf().TEST_DB_URL
    },
    'apps': {
        'models': {
            'models': [
                'aerich.models',
                'common.db.rdb.schema',
                'user.db.rdb.schema',
                'recruit.db.rdb.schema',
                'biography.db.rdb.schema',
            ],
            'default_connection': 'master'
        }
    }
}
