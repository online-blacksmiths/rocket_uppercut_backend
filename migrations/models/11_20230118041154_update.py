from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `companies` MODIFY COLUMN `code` VARCHAR(100) NOT NULL;
        ALTER TABLE `positions` MODIFY COLUMN `code` VARCHAR(100) NOT NULL;
        ALTER TABLE `skills` MODIFY COLUMN `code` VARCHAR(100) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `skills` MODIFY COLUMN `code` VARCHAR(30) NOT NULL;
        ALTER TABLE `companies` MODIFY COLUMN `code` VARCHAR(30) NOT NULL;
        ALTER TABLE `positions` MODIFY COLUMN `code` VARCHAR(30) NOT NULL;"""
