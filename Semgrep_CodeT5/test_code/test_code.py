class AccountManager:
    def __init__(self, account_name, balance=0):
        self.account_name = account_name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than zero.")
        else:
            self.balance += amount
            print(f"Successfully deposited ${amount}. New balance: ${self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        elif amount > self.balance:
            print(f"Insufficient funds! Available balance: ${self.balance}")
        else:
            self.balance -= amount
            print(f"Successfully withdrew ${amount}. New balance: ${self.balance}")

    def transfer(self, target_account, amount):
        if not isinstance(target_account, AccountManager):
            print("Invalid account for transfer.")
            return
        if amount <= 0:
            print("Transfer amount must be greater than zero.")
        elif amount > self.balance:
            print(f"Insufficient funds for transfer! Available balance: ${self.balance}")
        else:
            self.withdraw(amount)
            target_account.deposit(amount)
            print(f"Transferred ${amount} to {target_account.account_name}.")

    def check_balance(self):
        if self.balance < 0:
            print(f"Warning! Your account is overdrawn: ${self.balance}")
        elif self.balance == 0:
            print(f"Your account balance is zero. Consider making a deposit.")
        else:
            print(f"Your current balance is: ${self.balance}")

    def apply_overdraft_fee(self):
        print(f"TRACE: Entering apply_overdraft_fee with parameters: self")
        if self.balance < 0:
            self.balance -= 35
            print(f"Overdraft fee applied! New balance: ${self.balance}")


    def auto_deposit(self, amount, months):
        if amount <= 0 or months <= 0:
            print("Deposit amount and months must be positive numbers.")
            return

        print(f"Starting automated deposit of ${amount} for {months} months.")
        for i in range(1, months + 1):
            self.deposit(amount)
            print(f"Month {i}: Balance updated.")

if __name__ == "__main__":
    account1 = AccountManager("Alice", 500)
    account2 = AccountManager("Bob", 300)

    account1.deposit(200)
    account1.withdraw(1000)
    account1.withdraw(150)
    account1.transfer(account2, 100)
    account1.apply_overdraft_fee()
    account1.auto_deposit(50, 3)
    account1.check_balance()
