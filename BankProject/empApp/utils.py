from django.db import IntegrityError, connection

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
        return e
    

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
        return e