
DROP DATABASE bank_phase1;

Drop table customer;
drop table acc_owner;
drop table transaction;
drop table personal_banker;
drop table loans;
drop table employee;

-- DROP DATABASE Bank_demo;
CREATE DATABASE bank_phase1;

USE bank_phase1;
SHOW TABLES;

CREATE TABLE BRANCH (
    BID INT PRIMARY KEY,
    Name VARCHAR(100),
    Assets DECIMAL(15, 2),
    City VARCHAR(100),
    Address VARCHAR(255)
);

CREATE TABLE MANAGER (
	BID INT PRIMARY KEY,
    MANAGER INT
);

CREATE TABLE ASSISTANT_MGR(
	BID INT PRIMARY KEY,
    ASSISTANTMANAGER INT
);


CREATE TABLE EMPLOYEE (
	EmpID INT AUTO_INCREMENT PRIMARY KEY,
    SSN INT UNIQUE,
    Name VARCHAR(100),
    StartDate DATE,
    TeleNo VARCHAR(15),
    DependentName VARCHAR(100),
    BID INT
);
ALTER TABLE EMPLOYEE AUTO_INCREMENT = 1201;

/*
CREATE TABLE CUSTOMER (
    CSSN INT PRIMARY KEY,
    Name VARCHAR(100),
    City VARCHAR(100),
    State VARCHAR(100),
    Zipcode VARCHAR(10),
    StreetNo VARCHAR(10),
    AptNo VARCHAR(10)
);
*/


CREATE TABLE CUSTOMER (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CSSN INT UNIQUE,
    Name VARCHAR(100),
    City VARCHAR(100),
    State VARCHAR(100),
    Zipcode VARCHAR(10),
    StreetNo VARCHAR(10),
    AptNo VARCHAR(10)
);

-- Set the starting value for CustomerID to 1000
ALTER TABLE CUSTOMER AUTO_INCREMENT = 100000;


/*
CREATE TABLE ACCOUNT (
    AccNo INT PRIMARY KEY,
    Balance DECIMAL(15, 2),
    Type VARCHAR(50),
    RecentAccess DATE,
    InterestsRate DECIMAL(5, 2),
    OverDraft DECIMAL(15, 2)
);
*/

CREATE TABLE ACCOUNT (
    AccNo INT AUTO_INCREMENT PRIMARY KEY,
    Balance DECIMAL(15, 2),
    Type ENUM('Savings', 'Checking', 'Money Market', 'Loan'),
    RecentAccess DATETIME,
    InterestsRate DECIMAL(5, 2),
    OverDraft DECIMAL(15, 2)
);
ALTER TABLE ACCOUNT AUTO_INCREMENT = 3400001;

CREATE TABLE ACC_OWNER (
    CustomerID INT,
    AccNo INT,
    PRIMARY KEY (CustomerID, AccNo)
);


CREATE TABLE TRANSACTION (
    TID INT AUTO_INCREMENT,
    CSSN INT,
    AccNo INT,
    Code ENUM('WD', 'CD'),
    Date DATE,
    Time Time,
    Amount DECIMAL(15, 2),
    Charge DECIMAL(15, 2),
    PRIMARY KEY (TID, CSSN, AccNo)
);



CREATE TABLE PERSONAL_BANKER (
    CustomerID INT,
    BID INT,
    ESSN INT,
    PRIMARY KEY (CustomerID)
);



CREATE TABLE LOANS (
    CustomerID INT,
    AccNo INT,
    BID INT,
    Amount DECIMAL(15, 2),
    LoanNo INT PRIMARY KEY,
    MonthlyRepayment DECIMAL(15, 2)
);





ALTER TABLE EMPLOYEE
ADD FOREIGN KEY (BID) REFERENCES BRANCH(BID) ON DELETE CASCADE;

ALTER TABLE MANAGER
ADD FOREIGN KEY (Manager) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,
ADD foreign key (BID) references branch(BID) ON DELETE CASCADE;

ALTER TABLE ASSISTANT_MGR
ADD FOREIGN KEY (AssistantManager) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL,
ADD foreign key (BID) references branch(BID) ON DELETE CASCADE;

ALTER TABLE ACC_OWNER
ADD FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID) ON DELETE CASCADE,
ADD FOREIGN KEY (AccNo) REFERENCES ACCOUNT(AccNo) ON DELETE CASCADE;

/*
ALTER TABLE TRANSACTION
ADD FOREIGN KEY (CSSN) REFERENCES CUSTOMER(CSSN),
ADD FOREIGN KEY (AccNo) REFERENCES ACCOUNT(AccNo);
*/

ALTER TABLE PERSONAL_BANKER
ADD FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID) ON DELETE CASCADE,
ADD FOREIGN KEY (BID) REFERENCES BRANCH(BID) ON DELETE SET NULL,
ADD FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) ON DELETE SET NULL;

ALTER TABLE LOANS
ADD FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID) ON DELETE CASCADE,
ADD FOREIGN KEY (AccNo) REFERENCES ACCOUNT(AccNo) ON DELETE CASCADE,
ADD FOREIGN KEY (BID) REFERENCES BRANCH(BID) ON DELETE SET NULL;

select * from branch;
select * from employee;

select * from customer;
select * from personal_banker;

DELETE FROM customer where customerid=1015;

select * from acc_owner;
select * from account;
delete from account where accno=3400003;
select * from empapp_customuser;

delete from empapp_customuser where id =11;

select last_login from empapp_customuser where username='100015';
select recentaccess from account join acc_owner on account.accno = acc_owner.accno where acc_owner.customerid='100015';

alter table account modify column recentaccess datetime;
DESCRIBE account;


select *
from customer as c
join acc_owner as a on c.customerid=a.customerid
join account as p on p.accno=a.accno;

SELECT *
FROM customer AS c
LEFT JOIN acc_owner AS a ON c.customerid = a.customerid
LEFT JOIN account AS p ON p.accno = a.accno;

SELECT *
FROM customer AS c
LEFT JOIN acc_owner AS a ON c.customerid = a.customerid
LEFT JOIN account AS p ON p.accno = a.accno
WHERE c.customerid = '100012';


SELECT *
FROM account AS a
LEFT JOIN acc_owner p ON p.accno = a.accno
LEFT JOIN customer c ON c.customerid = p.customerid
;

select * from transaction;