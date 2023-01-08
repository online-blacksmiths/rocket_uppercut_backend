from common.config.settings import conf

TORTOISE_ORM = {
    'connections': {
        'master': conf().DB_URL if conf().API_ENV != 'test' else conf().TEST_DB_URL
    },
    'apps': {
        'models': {
            'models': [
                'aerich.models',
                'common.db.rdb.schema'
            ],
            'default_connection': 'master'
        }
    }
}
