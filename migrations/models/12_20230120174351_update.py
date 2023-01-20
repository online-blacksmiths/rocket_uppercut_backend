from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `companies` RENAME COLUMN `name` TO `title`;
        ALTER TABLE `positions` RENAME COLUMN `name` TO `title`;
        ALTER TABLE `skills` RENAME COLUMN `name` TO `title`;
        CREATE TABLE IF NOT EXISTS `schools` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `title` VARCHAR(100) NOT NULL,
    `code` VARCHAR(100) NOT NULL UNIQUE,
    `category` VARCHAR(30) NOT NULL  COMMENT 'ELEMENTARY: 초등학교\nMIDDLE: 중학교\nHIGH: 고등학교\nCOLLEGE: 전문대학\nUNIVERSITY: 대학\nGRADUATE: 대학원'
) CHARACTER SET utf8mb4 COMMENT='학교 테이블';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `skills` RENAME COLUMN `title` TO `name`;
        ALTER TABLE `companies` RENAME COLUMN `title` TO `name`;
        ALTER TABLE `positions` RENAME COLUMN `title` TO `name`;
        DROP TABLE IF EXISTS `schools`;"""
