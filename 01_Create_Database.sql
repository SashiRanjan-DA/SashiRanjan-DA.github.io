-- ============================================================================
-- SQL Script 01: Create Database for Digital Lending Funnel & Portfolio System
-- Target Database Engine: MySQL 8.0+
-- ============================================================================

DROP DATABASE IF EXISTS digital_lending_db;

CREATE DATABASE digital_lending_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE digital_lending_db;

SELECT 'Database digital_lending_db successfully created and selected.' AS Status;
