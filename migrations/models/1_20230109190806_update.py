from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_key` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(255) NOT NULL,
    `phone` VARCHAR(50) NOT NULL,
    `password` LONGTEXT NOT NULL,
    `refresh_token` LONGTEXT NOT NULL,
    `first_name` VARCHAR(30) NOT NULL,
    `last_name` VARCHAR(30) NOT NULL,
    `last_visit` DATETIME(6),
    `is_delete` BOOL NOT NULL  DEFAULT 0,
    KEY `idx_users_is_dele_18b3b3` (`is_delete`)
) CHARACTER SET utf8mb4 COMMENT='회원 테이블';
        CREATE TABLE IF NOT EXISTS `agrees` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_terms_of_service` BOOL NOT NULL  DEFAULT 0,
    `is_privacy_statement` BOOL NOT NULL  DEFAULT 0,
    `user_id` BIGINT NOT NULL,
    CONSTRAINT `fk_agrees_users_e9116128` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='유저 동의 항목';
        CREATE TABLE IF NOT EXISTS `sns_types` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `type` VARCHAR(30) NOT NULL,
    `user_id` BIGINT NOT NULL,
    UNIQUE KEY `uid_sns_types_user_id_479b3e` (`user_id`, `type`),
    CONSTRAINT `fk_sns_type_users_05440d8a` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='소셜 로그인 타입';
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `agrees`;
        DROP TABLE IF EXISTS `sns_types`;
        DROP TABLE IF EXISTS `users`;"""
