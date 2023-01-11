from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `sns_types` MODIFY COLUMN `type` VARCHAR(30) NOT NULL  COMMENT 'PHONE: PHONE\nEMAIL: EMAIL';
        ALTER TABLE `sns_types` MODIFY COLUMN `type` VARCHAR(30) NOT NULL  COMMENT 'PHONE: PHONE\nEMAIL: EMAIL';
        CREATE TABLE IF NOT EXISTS `steps` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `type` VARCHAR(30) NOT NULL  COMMENT 'PHONE: PHONE\nEMAIL: EMAIL',
    `step_1` BOOL NOT NULL  DEFAULT 0,
    `step_2` BOOL NOT NULL  DEFAULT 0,
    `step_3` BOOL NOT NULL  DEFAULT 0,
    `user_id` BIGINT NOT NULL UNIQUE,
    CONSTRAINT `fk_steps_users_6937ba41` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='인증, 프로필, 연결하기 스텝';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `sns_types` MODIFY COLUMN `type` VARCHAR(30) NOT NULL;
        ALTER TABLE `sns_types` MODIFY COLUMN `type` VARCHAR(30) NOT NULL;
        DROP TABLE IF EXISTS `steps`;"""
