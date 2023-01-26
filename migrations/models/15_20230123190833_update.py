from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `skills` ADD `is_initial` BOOL NOT NULL  DEFAULT 0;
        ALTER TABLE `skills` ADD INDEX `idx_skills_is_init_cb8423` (`is_initial`);
        ALTER TABLE `skills` ADD INDEX `idx_skills_sub_tit_4ab887` (`sub_title`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `skills` DROP INDEX `idx_skills_sub_tit_4ab887`;
        ALTER TABLE `skills` DROP INDEX `idx_skills_is_init_cb8423`;
        ALTER TABLE `skills` DROP COLUMN `is_initial`;"""
