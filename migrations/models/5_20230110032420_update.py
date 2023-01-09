from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `agrees` DROP FOREIGN KEY `fk_agrees_users_e9116128`;
        ALTER TABLE `agrees` ADD UNIQUE INDEX `uid_agrees_user_id_7913dc` (`user_id`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `agrees` DROP INDEX `idx_agrees_user_id_7913dc`;
        ALTER TABLE `agrees` ADD CONSTRAINT `fk_agrees_users_e9116128` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;"""
