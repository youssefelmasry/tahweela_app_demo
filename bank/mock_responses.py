from rest_framework.response import Response
from rest_framework import status
from tahweela_app.utils import update_users_balance

# A list of mocking responses from bank connection
connection_responses = {"success":Response({"success":True, "status":"Successful", "valid_token":"valid_token"}),
            "not_exist":Response({"success":False, "status":"Account name not exist", "valid_token":""}),
            "invalid":Response({"success":False, "status":"Invalid Account Number", "valid_token":""}, status=status.HTTP_400_BAD_REQUEST),
            "server_error":Response(None, status=status.HTTP_502_BAD_GATEWAY)
            }

# A list of mocking responses from uploading money from bank
money_responses = {"success":Response({"success":True, "status":"Successful", "transaction_reference_number":"9020110506321"}),
                    "not_enough":Response({"success":False, "status":"No enough balance in your account", "transaction_reference_number":"3215110506321"}),
                    "invalid":Response({"success":False, "status":"Invalid or expired token", "transaction_reference_number":""}, status=status.HTTP_401_UNAUTHORIZED),
                    "server_error":Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                }

def request_bank_connection(connection_instance, response_type):
    '''A mocking function that Assuming we sent a request to the bank to connect with it 
        and will return a response we decided just for mocking.
        In actual scenario will return the response from bank's API '''

    bank_api = connection_instance.bank_branch.bank.bank_api+"/connect"
    data = {
        "AccountNumber":connection_instance.account_number,
        "AccountName":connection_instance.account_name,
        "BranchNumber":connection_instance.bank_branch.branch_number
    }

    return connection_responses[response_type]

def connect_to_bank(connection_instance, response_type="success"):
    bank_response = request_bank_connection(connection_instance, response_type)

    if bank_response.status_code < 500:
        connection_instance.connected = bank_response.data['success']
        connection_instance.valid_token = bank_response.data['valid_token']
        connection_instance.save()
        return {"connected":bank_response.data['success'], 
                "bank_id":connection_instance.bank_branch.bank.id,
                "bank_name":connection_instance.bank_branch.bank.bank_name, 
                "status":bank_response.data['status']}

    return {"connected":False, "bank":connection_instance.bank_branch.bank.id, 
            "bank_name":connection_instance.bank_branch.bank.bank_name, "status":"Connection to Bank Failed"}

def request_upload_money(transaction_instance, response_type):
    # Assuming we make a request to bank to upload money from bank account to tahweela account. Same as request_bank_connection function
    return money_responses[response_type]

def upload_money(transaction_instance, response_type='success'):
    bank_response = request_upload_money(transaction_instance, response_type)

    if bank_response.status_code < 500:
        transaction_instance.status = bank_response.data["status"]
        transaction_instance.transaction_reference_number = bank_response.data["transaction_reference_number"]
        transaction_instance.save()

        if bank_response.data['success']:
            update_users_balance(transaction_instance.user, transaction_instance.amount)
        
        return {"money_uploaded":bank_response.data['success'],
                "status":bank_response.data['status'],
                "bank_id":transaction_instance.bank.id,
                "bank_name":transaction_instance.bank.bank_name,
                "amount":transaction_instance.amount,
                "current_tahweela_balance":transaction_instance.user.tahweela_account.tahweela_balance
        }
    return {"money_uploaded":False, "bank_id":transaction_instance.bank.id, 
            "bank_name":transaction_instance.bank.bank_name, "status":"Connection to Bank Failed"}

