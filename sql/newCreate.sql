DROP DATABASE bank_phase1;

-- DROP DATABASE Bank_demo;
CREATE DATABASE bank_phase1;

USE bank_phase1;
SHOW TABLES;


-- Create AccOwner table
CREATE TABLE acc_owner (
    cssn INT NOT NULL,
    accno INT NOT NULL,
    PRIMARY KEY (cssn, accno),
    FOREIGN KEY (cssn) REFERENCES customer(CSSN),
    FOREIGN KEY (accno) REFERENCES account(AccNo)
);

-- Create Account table
CREATE TABLE account (
    AccNo INT AUTO_INCREMENT PRIMARY KEY,
    Balance DECIMAL(15, 2),
    Type VARCHAR(12),
    RecentAccess DATE,
    InterestsRate DECIMAL(5, 2),
    OverDraft DECIMAL(15, 2)
);

-- Create AssistantMgr table
CREATE TABLE assistant_mgr (
    BID INT NOT NULL,
    ASSISTANTMANAGER INT,
    PRIMARY KEY (BID),
    FOREIGN KEY (BID) REFERENCES branch(BID),
    FOREIGN KEY (ASSISTANTMANAGER) REFERENCES employee(EmpID)
);

-- Create Branch table
CREATE TABLE branch (
    BID INT PRIMARY KEY,
    Name VARCHAR(100),
    Assets DECIMAL(15, 2),
    City VARCHAR(100),
    Address VARCHAR(255)
);

-- Create Customer table
CREATE TABLE customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CSSN INT UNIQUE,
    Name VARCHAR(100),
    City VARCHAR(100),
    State VARCHAR(100),
    Zipcode VARCHAR(10),
    StreetNo VARCHAR(10),
    AptNo VARCHAR(10)
);

-- Create Employee table
CREATE TABLE employee (
    EmpID INT AUTO_INCREMENT PRIMARY KEY,
    SSN INT UNIQUE,
    Name VARCHAR(100),
    StartDate DATE,
    TeleNo VARCHAR(15),
    DependentName VARCHAR(100),
    BID INT,
    FOREIGN KEY (BID) REFERENCES branch(BID)
);

-- Create Loans table
CREATE TABLE loans (
    LoanNo INT PRIMARY KEY,
    CSSN INT,
    AccNo INT,
    BID INT,
    Amount DECIMAL(15, 2),
    MonthlyRepayment DECIMAL(15, 2),
    FOREIGN KEY (CSSN) REFERENCES customer(CSSN),
    FOREIGN KEY (AccNo) REFERENCES account(AccNo),
    FOREIGN KEY (BID) REFERENCES branch(BID)
);

-- Create Manager table
CREATE TABLE manager (
    BID INT PRIMARY KEY,
    MANAGER INT,
    FOREIGN KEY (BID) REFERENCES branch(BID),
    FOREIGN KEY (MANAGER) REFERENCES employee(EmpID)
);

-- Create PersonalBanker table
CREATE TABLE personal_banker (
    CSSN INT NOT NULL,
    BID INT,
    ESSN INT,
    PRIMARY KEY (CSSN, BID, ESSN),
    FOREIGN KEY (CSSN) REFERENCES customer(CSSN),
    FOREIGN KEY (BID) REFERENCES branch(BID),
    FOREIGN KEY (ESSN) REFERENCES employee(EmpID)
);

-- Create Transaction table
CREATE TABLE transaction (
    TID INT AUTO_INCREMENT PRIMARY KEY,
    CSSN INT,
    AccNo INT,
    Code VARCHAR(2),
    Date DATE,
    Time TIME,
    Amount DECIMAL(15, 2),
    Charge DECIMAL(15, 2),
    FOREIGN KEY (CSSN) REFERENCES customer(CSSN),
    FOREIGN KEY (AccNo) REFERENCES account(AccNo)
);



