from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `skills` MODIFY COLUMN `name` VARCHAR(200) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `skills` MODIFY COLUMN `name` VARCHAR(100) NOT NULL;"""
