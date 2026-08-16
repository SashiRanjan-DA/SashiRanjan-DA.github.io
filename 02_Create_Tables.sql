-- ============================================================================
-- SQL Script 02: Create Tables & Referential Constraints
-- Target Database Engine: MySQL 8.0+
-- Database: digital_lending_db
-- ============================================================================

USE digital_lending_db;

-- ----------------------------------------------------------------------------
-- Table 1: customer
-- Master records of loan applicants and borrowers
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS repayment;
DROP TABLE IF EXISTS loan_application;
DROP TABLE IF EXISTS customer_bank_account;
DROP TABLE IF EXISTS lender;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
    customer_id VARCHAR(20) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(15) NOT NULL,
    date_of_birth DATE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    employment_type VARCHAR(50) NOT NULL,
    monthly_income DECIMAL(12,2) NOT NULL,
    credit_score INT NOT NULL,
    kyc_status VARCHAR(20) NOT NULL,
    PRIMARY KEY (customer_id),
    UNIQUE KEY uq_customer_phone (phone_number),
    UNIQUE KEY uq_customer_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table 2: lender
-- Master records of partner banks, NBFCs, and Fintech lenders
-- ----------------------------------------------------------------------------
CREATE TABLE lender (
    lender_id VARCHAR(20) NOT NULL,
    lender_name VARCHAR(100) NOT NULL,
    lender_type VARCHAR(50) NOT NULL,
    head_office_city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    processing_fee_percent DECIMAL(5,2) NOT NULL,
    minimum_credit_score INT NOT NULL,
    maximum_loan_amount DECIMAL(14,2) NOT NULL,
    PRIMARY KEY (lender_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table 3: customer_bank_account
-- Bank accounts linked 1-to-1 to customers
-- ----------------------------------------------------------------------------
CREATE TABLE customer_bank_account (
    account_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(30) NOT NULL,
    ifsc_code VARCHAR(15) NOT NULL,
    account_open_date DATE NOT NULL,
    account_status VARCHAR(20) NOT NULL,
    salary_account VARCHAR(10) NOT NULL,
    average_balance DECIMAL(14,2) NOT NULL,
    upi_linked VARCHAR(10) NOT NULL,
    PRIMARY KEY (account_id),
    CONSTRAINT fk_bank_account_customer FOREIGN KEY (customer_id) 
        REFERENCES customer(customer_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table 4: loan_application
-- Digital loan applications and funnel lifecycle records
-- ----------------------------------------------------------------------------
CREATE TABLE loan_application (
    application_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    lender_id VARCHAR(20) NOT NULL,
    loan_amount DECIMAL(14,2) NOT NULL,
    approved_amount DECIMAL(14,2) NULL,
    interest_rate DECIMAL(5,2) NULL,
    loan_tenure_months INT NOT NULL,
    loan_purpose VARCHAR(100) NOT NULL,
    application_date DATE NOT NULL,
    approval_date DATE NULL,
    loan_status VARCHAR(20) NOT NULL,
    rejection_reason VARCHAR(150) NULL,
    loan_channel VARCHAR(50) NOT NULL,
    processing_fee DECIMAL(12,2) NULL,
    emi_amount DECIMAL(12,2) NULL,
    disbursement_date DATE NULL,
    PRIMARY KEY (application_id),
    CONSTRAINT fk_loan_app_customer FOREIGN KEY (customer_id) 
        REFERENCES customer(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_loan_app_lender FOREIGN KEY (lender_id) 
        REFERENCES lender(lender_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table 5: repayment
-- Scheduled and historical EMI repayments for approved loans
-- ----------------------------------------------------------------------------
CREATE TABLE repayment (
    repayment_id VARCHAR(20) NOT NULL,
    application_id VARCHAR(20) NOT NULL,
    emi_number INT NOT NULL,
    due_date DATE NOT NULL,
    payment_date DATE NULL,
    amount_due DECIMAL(12,2) NOT NULL,
    amount_paid DECIMAL(12,2) NOT NULL,
    payment_status VARCHAR(30) NOT NULL,
    late_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    days_overdue INT NOT NULL DEFAULT 0,
    payment_mode VARCHAR(30) NULL,
    remarks VARCHAR(255) NULL,
    PRIMARY KEY (repayment_id),
    CONSTRAINT fk_repayment_loan_app FOREIGN KEY (application_id) 
        REFERENCES loan_application(application_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table 6: collection
-- Collection agent actions and recovery workflows for delinquent loans
-- ----------------------------------------------------------------------------
CREATE TABLE collection (
    collection_id VARCHAR(20) NOT NULL,
    application_id VARCHAR(20) NOT NULL,
    collection_agent VARCHAR(100) NOT NULL,
    collection_date DATE NOT NULL,
    outstanding_amount DECIMAL(14,2) NOT NULL,
    collection_status VARCHAR(50) NOT NULL,
    collection_mode VARCHAR(50) NOT NULL,
    promise_to_pay_date DATE NULL,
    settlement_amount DECIMAL(14,2) NULL,
    settlement_status VARCHAR(30) NOT NULL,
    follow_up_count INT NOT NULL DEFAULT 1,
    last_follow_up_date DATE NOT NULL,
    remarks VARCHAR(255) NULL,
    PRIMARY KEY (collection_id),
    CONSTRAINT fk_collection_loan_app FOREIGN KEY (application_id) 
        REFERENCES loan_application(application_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SELECT 'All 6 DDL tables created successfully with Foreign Keys.' AS Status;
