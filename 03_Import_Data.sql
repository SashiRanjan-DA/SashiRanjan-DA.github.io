-- ============================================================================
-- SQL Script 03: Bulk Import CSV Datasets into MySQL
-- Target Database Engine: MySQL 8.0+
-- Database: digital_lending_db
-- ============================================================================
-- NOTE: Update file paths to match your absolute system directory.
-- Ensure local_infile option is enabled: SET GLOBAL local_infile = 1;
-- ============================================================================

USE digital_lending_db;

SET GLOBAL local_infile = 1;

-- ----------------------------------------------------------------------------
-- 1. Import Customers (1,500 rows)
-- ----------------------------------------------------------------------------
LOAD DATA INFILE 'C:/Users/ranja/Documents/FRONTEND/Digital_Lending_Data_Generator/data/customer.csv'
INTO TABLE customer
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(customer_id, first_name, last_name, gender, date_of_birth, phone_number, email, city, state, pincode, employment_type, monthly_income, credit_score, kyc_status);

-- ----------------------------------------------------------------------------
-- 2. Import Lenders (20 rows)
-- ----------------------------------------------------------------------------
LOAD DATA INFILE 'C:/Users/ranja/Documents/FRONTEND/Digital_Lending_Data_Generator/data/lender.csv'
INTO TABLE lender
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(lender_id, lender_name, lender_type, head_office_city, state, processing_fee_percent, minimum_credit_score, maximum_loan_amount);

-- ----------------------------------------------------------------------------
-- 3. Import Customer Bank Accounts (1,500 rows)
-- ----------------------------------------------------------------------------
LOAD DATA INFILE 'C:/Users/ranja/Documents/FRONTEND/Digital_Lending_Data_Generator/data/customer_bank_account.csv'
INTO TABLE customer_bank_account
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(account_id, customer_id, bank_name, account_type, ifsc_code, account_open_date, account_status, salary_account, average_balance, upi_linked);

-- ----------------------------------------------------------------------------
-- 4. Import Loan Applications (3,000 rows)
-- Handles NULLs for Rejected / Pending applications cleanly
-- ----------------------------------------------------------------------------
LOAD DATA INFILE 'C:/Users/ranja/Documents/FRONTEND/Digital_Lending_Data_Generator/data/loan_application.csv'
INTO TABLE loan_application
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(application_id, customer_id, lender_id, loan_amount, @v_approved_amount, @v_interest_rate, loan_tenure_months, loan_purpose, application_date, @v_approval_date, loan_status, @v_rejection_reason, loan_channel, @v_processing_fee, @v_emi_amount, @v_disbursement_date)
SET 
    approved_amount = NULLIF(@v_approved_amount, ''),
    interest_rate = NULLIF(@v_interest_rate, ''),
    approval_date = NULLIF(@v_approval_date, ''),
    rejection_reason = NULLIF(@v_rejection_reason, ''),
    processing_fee = NULLIF(@v_processing_fee, ''),
    emi_amount = NULLIF(@v_emi_amount, ''),
    disbursement_date = NULLIF(@v_disbursement_date, '');

-- ----------------------------------------------------------------------------
-- 5. Import Repayments (8,000 rows)
-- Handles NULL payment_date and payment_mode for missed EMIs
-- ----------------------------------------------------------------------------
LOAD DATA INFILE 'C:/Users/ranja/Documents/FRONTEND/Digital_Lending_Data_Generator/data/repayment.csv'
INTO TABLE repayment
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(repayment_id, application_id, emi_number, due_date, @v_payment_date, amount_due, amount_paid, payment_status, late_fee, days_overdue, @v_payment_mode, @v_remarks)
SET 
    payment_date = NULLIF(@v_payment_date, ''),
    payment_mode = NULLIF(@v_payment_mode, ''),
    remarks = NULLIF(@v_remarks, '');

-- ----------------------------------------------------------------------------
-- 6. Import Collections (2,000 rows)
-- Handles NULL promise_to_pay_date and settlement_amount
-- ----------------------------------------------------------------------------
LOAD DATA INFILE 'C:/Users/ranja/Documents/FRONTEND/Digital_Lending_Data_Generator/data/collection.csv'
INTO TABLE collection
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(collection_id, application_id, collection_agent, collection_date, outstanding_amount, collection_status, collection_mode, @v_promise_to_pay_date, @v_settlement_amount, settlement_status, follow_up_count, last_follow_up_date, @v_remarks)
SET 
    promise_to_pay_date = NULLIF(@v_promise_to_pay_date, ''),
    settlement_amount = NULLIF(@v_settlement_amount, ''),
    remarks = NULLIF(@v_remarks, '');

-- Row Verification Check
SELECT 'customer' AS Table_Name, COUNT(*) AS Total_Rows FROM customer
UNION ALL
SELECT 'lender', COUNT(*) FROM lender
UNION ALL
SELECT 'customer_bank_account', COUNT(*) FROM customer_bank_account
UNION ALL
SELECT 'loan_application', COUNT(*) FROM loan_application
UNION ALL
SELECT 'repayment', COUNT(*) FROM repayment
UNION ALL
SELECT 'collection', COUNT(*) FROM collection;
