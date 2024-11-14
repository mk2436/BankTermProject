from django.db import IntegrityError, connection


# Template for functions
'''
    try:
        with connection.cursor() as cursor:
            cursor.execute()
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        return
'''

def list_all_users():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM customer AS c
                LEFT JOIN acc_owner AS a ON c.customerid = a.customerid
                LEFT JOIN account AS p ON p.accno = a.accno;
                """
            )
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        return
    

def list_user(customerid):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM customer AS c
                LEFT JOIN acc_owner AS a ON c.customerid = a.customerid
                LEFT JOIN account AS p ON p.accno = a.accno
                WHERE c.customerid = {customerid} ;
                """
            )
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        return
    

def add_accowner(customerid,accno):
    try:
        with connection.cursor() as cursor:
            print(customerid)
            cursor.execute(
                f"""
                INSERT INTO ACC_OWNER (CustomerID, AccNo) VALUES
                ({customerid},{accno});
                """)
            return "Success"
    except Exception as e:
        print(e)
        return
    

def list_all_accounts():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM account AS a
                LEFT JOIN acc_owner p ON p.accno = a.accno
                LEFT JOIN customer c ON c.customerid = p.customerid
                ;
                """
            )
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        return
    

def list_account(accno):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM account AS a
                LEFT JOIN acc_owner p ON p.accno = a.accno
                LEFT JOIN customer c ON c.customerid = p.customerid
                WHERE a.accno={accno}
                ;
                """
            )
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        return
    
def add_loan(customerid,accno,bid,amount,monthlyrepayment,outstandingamount):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO LOANS (CustomerID, AccNo, BID, Amount, LoanNo, MonthlyRepayment) VALUES
                ({customerid},{accno},{bid},{amount},{monthlyrepayment},{outstandingamount});
                """
            )
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(e)
        return