from abc import ABC
from abc import abstractclassmethod
from abc import abstractproperty
import random
import re
import datetime

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = list()

    def make_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)
    
class Individual(Client):
    def __init__(self, name, date_of_birth, identification, email, phone, address):
        super().__init__(address)
        self.name = name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone = phone
        self.identification = identification

class Account:
    def __init__(self, number_account, client):
        self._balance = 0
        self._number_account = number_account
        self._agency = "0001"
        self._client = client
        self._historic = Historic()

    @classmethod
    def new_account(cls, client, number_account):
        return cls(number_account, client)
        
    @property
    def balance(self):
        return self._balance
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def client(self):
        return self._client
    
    @property
    def number_account(self):
        return self._number_account
    
    @property
    def historic(self):
        return self._historic
    
    def withdraw(self, amount):
        balance = self.balance
        
        balance_exceeded = amount > balance

        if balance_exceeded:
            print("\n\tTransaction invalid ! Insufficient balance ")

        elif amount > 0:
            self._balance -= amount
            print("\n\tSuccessful withdrawal !")
            return True
        
        else:
            print("\n\tInvalid operation ! Invalid amount ")

        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n\tSucessful deposit !")

        else:
            print("\n\tInvalid operation ! Negative amount ")
            return False
        
        return True
  
class CurrentAccount(Account):
    def __init__(self, number_account, client, limit = 500, limit_draw = 3):
        super().__init__(number_account, client)
        self._limit = limit
        self._limit_draw = limit_draw    
    
    def withdraw(self, amount):
        number_of_draws = len([transaction for transaction in self.historic.transactions if transaction["type"] == Withdraw.__name__])
        
        exceeded_limit =  amount > self.limit
        exceeded_draws = number_of_draws >= self._limit_draw

        if exceeded_limit:
            print("\n\tInvalid operation, withdrawal amount exceeds limit !")

        elif exceeded_draws:
            print("\n\tInvalid operation, withdrawal limits exceeded !")

        else:
            return super().withdraw(amount)
        
        return False
    
    def __str__(self) -> str:
        return f"""
        Client: {self.client.name}
        Agency: {self.agency}
        C\C: {self.number_account}
        Balance: {self.balance}
        """

class Historic:
    def __init__(self):
        self._transactions = list()

    @property
    def transactions(self):
        return self._transactions
    

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class.__.__name__,
                "value": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

class Transaction(ABC):
    @property
    @abstractproperty
    def amount(self):
        pass
    @abstractclassmethod
    def register(self,account):
        pass

class Withdraw(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def value(self):
        return self._amount
    
    def register(self, account):
        sucess_transaction = account.withdraw(self.amount)
        if sucess_transaction:
            account.historic.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount
    
    def register(self, account):
        sucess_transaction = account.deposit(self.amount)
        if sucess_transaction:
            account.historic.add_transaction(self)

# Function to validate the date of birth format
def validate_date_of_birth(date):
    if re.match(r'^\d{4}/\d{2}/\d{2}$', date):
        return True
    else:
        return False

# Function to validate phone number format
def validate_phone_number(phone):
    if re.match(r'^\+\d{2}\d{2}\d{5}-\d{4}$', phone):
        return True
    else:
        return False

# Function to validate the customer ID format
def validate_identification(identification):
    if re.match(r'^[0-9]{9}-[0-9]{2}$', identification):
        return True
    else:
        return False

# Function to display the banking system options menu 
def menu():
    print(
        """
        \t ===================================
        \t =  Welcome to the banking system  =
        \t ===================================

        \t     ----------------------
        \t    | [1]  Withdraw        |
        \t    | [2]  Deposit         |
        \t    | [3]  Extract         |
        \t    | [4]  Create Client   |
        \t    | [5]  Create Account  |
        \t     ----------------------
        """
          )
    option = input("Choose which action to take ==> ")
    return option

def filter_clients(identification, clients):
    clients_filtered = [client for client in clients if client.identification == identification]
    return clients_filtered[0] if clients_filtered else None

def recovery_account(client):
    if not client.accounts:
        print("\nClient don't have account")
        return
    number = input("\nProvide your number account here ==> ")
    account = [account for account in client.accounts if account.number_account == number]
    return account[0] if account else None
    
    # FIXME: não permite cliente escolher a conta
    #return client.accounts[0]

# Function for making a deposit into a bank account
def deposit(clients):

    identification = input("\nEnter with your identification in the following format (XXXYYYWWW-AA) ==> ")
    client = filter_clients(identification,clients)
    if not client:
        print("\nClient not found ")

    amount = float(input("\nEnter the amount you want to deposit ==> "))
    transaction = Deposit(amount)

    account = recovery_account(client)
    if not account:
        print("\nAccount not found")
        return
    
    client.make_transaction(account, transaction)

# Function for making a withdrawal from a bank account
def withdraw(clients):

    identification = input("\nEnter with your identification in the following format (XXXYYYWWW-AA) ==> ")
    client = filter_clients(identification,clients)
    if not client:
        print("\nClient not found ")

    amount = float(input("\nEnter the amount you want to withdraw ==> "))
    transaction = Withdraw(amount)

    account = recovery_account(client)
    if not account:
        print("\nAccount not found")
        return
    
    client.make_transaction(account, transaction)

# Function to display a bank account statement
def extract(clients):
    identification = input("\nEnter with your identification in the following format (XXXYYYWWW-AA) ==> ")

    client = filter_clients(identification,clients)
    if not client:
        print("\nClient not found ")

    account = recovery_account(client)
    if not account:
        print("\nAccount not found")
        return
    
    print(f"""
        \t =============
        \t =  Extract  =
        \t =============
    """)
    transactions = account.historic.transactions
    extract = ""
    if not transactions:
        extract = "\nHas not made any moves yet"
    else:
        for transaction in transactions:
            extract += f"\n{transaction['tipo']}:\tR$ {transaction['valor']:.2f}"

    print(extract)
    print(f"Balance:\tR$ {account.balance:.2f}")

# Function for adding a new customer to the banking system
def create_user_client(clients):

    identification = input("\n Enter with your identification in the following format (XXXYYYWWW-AA) ==> ")
    while not validate_identification(identification):

        print("Invalid identification format! Please use XXXYYYWWW-AA format.")
        identification = input("\n Enter with your identification in the following format (XXXYYYWWW-AA) ==> ")

    client_exists = filter_clients(identification, clients)
    if client_exists:
        print(" Client already exists ")
        return
    
    name = input("\n Enter your name here ==> ")
    email = input("\n Enter your email here ==> ")

    date_of_birth = input("\n Enter your date of birth in the following format (YY/MM/DD) ==> ")
    while not validate_date_of_birth(date_of_birth):

        print("Invalid date of birth format! Please use YY/MM/DD format.")
        date_of_birth = input("\n Enter your date of birth in the following format (YY/MM/DD) ==> ")
    
    phone = input("\n Enter with your phone number in the following format (+55DDXXXX-YYYY) ==> ")
    while not validate_phone_number(phone):

        print("Invalid phone number format! Please use +55DDXXXX-YYYY format.")
        phone = input("\n Enter with your phone number in the following format (+55DDXXXX-YYYY) ==> ")
    
    address = input("\n  Enter your address in the following format (street - number - complement - city - state) ==> ")

    client =  Individual(name=name, date_of_birth=date_of_birth, identification=identification, email=email, phone=phone,  address=address) 
    clients.append(client)

    print("\nCongratulations! You are now part of the bank")

# Function to create a new current account for a customer
def create_current_account(clients,accounts):

    print("\nLet's create a current account for you now ")
    identification = input("\nEnter with your identification in the following format (XXXYYYWWW-AA) ==> ")
    client = filter_clients(identification, clients)
    if not client:
        print("\nClient not found")


    number_account = "".join([str(random.randint(0,9)) for _ in range(11)])
    print(number_account)
    account = CurrentAccount.new_account(client,number_account)
    accounts.append(account)
    client.accounts.append(account)
    print("\nAccount successfully created ")
        
# Main function that controls the flow of the banking system
def main():
    clients = list()
    accounts = list()
    while True:

        action = menu()
        
        match action:
            case "1":
                withdraw(clients)
            case "2":
                deposit(clients)
            case "3":
                extract(clients)
            case "4":
                create_user_client(clients)
            case "5":
                create_current_account(clients,accounts)

main()