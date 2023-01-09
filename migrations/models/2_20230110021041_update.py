from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` ADD `is_verified_email` BOOL NOT NULL  DEFAULT 0;
        ALTER TABLE `users` ADD `is_verified_phone` BOOL NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` DROP COLUMN `is_verified_email`;
        ALTER TABLE `users` DROP COLUMN `is_verified_phone`;"""
