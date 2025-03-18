def deposit(self, amount):
    if amount <= 0:
        print("Deposit amount must be greater than zero.")
    else:
        self.balance += amount
        print(f"Successfully deposited ${amount}. New balance: ${self.balance}")
