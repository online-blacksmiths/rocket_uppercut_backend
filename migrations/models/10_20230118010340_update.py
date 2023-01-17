from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `companies` RENAME COLUMN `latitude_y` TO `lng_y`;
        ALTER TABLE `companies` RENAME COLUMN `latitude_x` TO `lat_x`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `companies` RENAME COLUMN `lng_y` TO `latitude_y`;
        ALTER TABLE `companies` RENAME COLUMN `lat_x` TO `latitude_x`;"""
