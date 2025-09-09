import datetime
import random
import os
import ast

class BankingSystem:
    def __init__(self, data_file="bank_data.txt"):
        self.data_file = data_file
        self.accounts = {}
        self.transactions = []
        self.logged_in_account = None
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        data = ast.literal_eval(content)
                        self.accounts = data.get('accounts', {})
                        self.transactions = data.get('transactions', [])
                        
                        for account in self.accounts.values():
                            if 'created_date' in account and isinstance(account['created_date'], str):
                                account['created_date'] = datetime.datetime.fromisoformat(account['created_date'])
                        
                        for transaction in self.transactions:
                            if 'timestamp' in transaction and isinstance(transaction['timestamp'], str):
                                transaction['timestamp'] = datetime.datetime.fromisoformat(transaction['timestamp'])
                
                print("Previous data loaded successfully!")
            else:
                print("No existing data found. Starting fresh.")
        except Exception as e:
            print(f"Error loading data: {e}")
            print("Starting with fresh data.")
            self.accounts = {}
            self.transactions = []
    
    def save_data(self):
        try:
            data_to_save = {
                'accounts': {},
                'transactions': []
            }
            
            for acc_num, account in self.accounts.items():
                data_to_save['accounts'][acc_num] = account.copy()
                if 'created_date' in data_to_save['accounts'][acc_num]:
                    data_to_save['accounts'][acc_num]['created_date'] = data_to_save['accounts'][acc_num]['created_date'].isoformat()
            
            for transaction in self.transactions:
                transaction_copy = transaction.copy()
                if 'timestamp' in transaction_copy:
                    transaction_copy['timestamp'] = transaction_copy['timestamp'].isoformat()
                data_to_save['transactions'].append(transaction_copy)
            
            with open(self.data_file, 'w') as f:
                f.write("{\n")
                f.write(f"  'accounts': {data_to_save['accounts']},\n")
                f.write(f"  'transactions': {data_to_save['transactions']}\n")
                f.write("}\n")
            
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def main_menu(self):
        try:
            while True:
                print("\n=== Welcome to Python Bank ===")
                print("1. Create New Account")
                print("2. Login to Existing Account")
                print("3. Exit")
                
                choice = input("Please select an option: ").strip()
                
                if choice.lower() == 'exit':
                    print("Thank you for banking with us. Goodbye!")
                    self.save_data()
                    break
                elif choice == '1':
                    self.create_account()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    print("Thank you for banking with us. Goodbye!")
                    self.save_data()
                    break
                else:
                    print("Sorry, that's not a valid option. Please try again.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Saving data before exit...")
            self.save_data()
            print("Goodbye!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Saving data before exit...")
            self.save_data()
            print("Goodbye!")
    
    def generate_account_number(self):
        while True:
            account_number = str(random.randint(100000, 999999))
            if account_number not in self.accounts:
                return account_number
    
    def create_account(self):
        try:
            print("\n=== Let's Create Your Account ===")
            print("Type 'exit' anytime to go back to main menu.")
            
            name = input("What's your full name? ").strip()
            if name.lower() == 'exit':
                return
            if not name:
                print("Name is required to create an account!")
                return
            
            account_number = self.generate_account_number()
            print(f"Your new account number is: {account_number}")
            
            while True:
                initial_deposit = input("How much would you like to deposit initially? $").strip()
                if initial_deposit.lower() == 'exit':
                    return
                try:
                    initial_deposit = float(initial_deposit)
                    if initial_deposit < 0:
                        print("Deposit amount cannot be negative!")
                        continue
                    elif initial_deposit < 500:
                        print("Minimum deposit should be $500!")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                except Exception as e:
                    print(f"Error processing deposit amount: {e}")
                    print("Please try again.")
            
            while True:
                account_type = input("What type of account? (savings/current): ").strip().lower()
                if account_type.lower() == 'exit':
                    return
                if account_type not in ['savings', 'current']:
                    print("Please choose either 'savings' or 'current'")
                    continue
                break
            
            while True:
                password = input("Create a secure password (minimum 6 characters): ").strip()
                if password.lower() == 'exit':
                    return
                if len(password) < 6:
                    print("Password must be at least 6 characters long!")
                    continue
                break
            
            self.accounts[account_number] = {
                'name': name,
                'balance': initial_deposit,
                'account_type': account_type,
                'password': password,
                'created_date': datetime.datetime.now()
            }
            
            self.transactions.append({
                'type': 'account_creation',
                'account_number': account_number,
                'amount': initial_deposit,
                'balance_after': initial_deposit,
                'timestamp': datetime.datetime.now(),
                'description': f'Account opened with initial deposit of ${initial_deposit:.2f}'
            })
            
            print(f"\n🎉 Congratulations {name}!")
            print(f"Your account has been created successfully!")
            print(f"Account Number: {account_number}")
            print(f"Current Balance: ${initial_deposit:.2f}")
            
        except KeyboardInterrupt:
            print("\nAccount creation cancelled.")
        except Exception as e:
            print(f"An error occurred while creating your account: {e}")
            print("Please try again.")
    
    def login(self):
        try:
            print("\n=== Account Login ===")
            print("Type 'exit' to go back to main menu.")
            
            account_number = input("Enter your account number: ").strip()
            if account_number.lower() == 'exit':
                return
            
            if account_number not in self.accounts:
                print("Account not found. Please check your account number.")
                return
            
            password = input("Enter your password: ").strip()
            if password.lower() == 'exit':
                return
            
            if self.accounts[account_number]['password'] != password:
                print("Incorrect password. Please try again.")
                return
            
            self.logged_in_account = account_number
            print(f"\nWelcome back, {self.accounts[account_number]['name']}!")
            self.account_menu()
            
        except KeyboardInterrupt:
            print("\nLogin cancelled.")
        except Exception as e:
            print(f"An error occurred during login: {e}")
            print("Please try again.")
    
    def account_menu(self):
        while True:
            try:
                account_data = self.accounts[self.logged_in_account]
                print(f"\n=== {account_data['name']}'s Account ===")
                print(f"Account #: {self.logged_in_account}")
                print(f"Account Type: {account_data['account_type'].title()}")
                print(f"Current Balance: ${account_data['balance']:.2f}")
                print("\nWhat would you like to do today?")
                print("1. Deposit Money")
                print("2. Withdraw Money")
                print("3. Transfer Money")
                print("4. View Transaction History")
                print("5. Calculate Interest")
                print("6. Update Account Information")
                print("7. Logout")
                
                choice = input("Please select an option: ").strip()
                
                if choice.lower() == 'exit' or choice == '7':
                    self.logged_in_account = None
                    print("You have been logged out. See you soon!")
                    break
                elif choice == '1':
                    self.deposit()
                elif choice == '2':
                    self.withdraw()
                elif choice == '3':
                    self.transfer()
                elif choice == '4':
                    self.view_transaction_history()
                elif choice == '5':
                    self.calculate_interest()
                elif choice == '6':
                    self.modify_account()
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nReturning to main menu...")
                self.logged_in_account = None
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")
    
    def deposit(self):
        try:
            print("\n=== Make a Deposit ===")
            print("Type 'exit' to go back to account menu.")
            
            while True:
                amount_str = input("How much would you like to deposit? $").strip()
                if amount_str.lower() == 'exit':
                    return
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("Please enter a positive amount!")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                except Exception as e:
                    print(f"Error processing deposit amount: {e}")
                    print("Please try again.")
            
            old_balance = self.accounts[self.logged_in_account]['balance']
            self.accounts[self.logged_in_account]['balance'] += amount
            
            self.transactions.append({
                'type': 'deposit',
                'account_number': self.logged_in_account,
                'amount': amount,
                'balance_after': self.accounts[self.logged_in_account]['balance'],
                'timestamp': datetime.datetime.now(),
                'description': f'Deposited ${amount:.2f}'
            })
            
            print(f"✅ Deposit successful!")
            print(f"Previous Balance: ${old_balance:.2f}")
            print(f"New Balance: ${self.accounts[self.logged_in_account]['balance']:.2f}")
            
        except KeyboardInterrupt:
            print("\nDeposit cancelled.")
        except Exception as e:
            print(f"An error occurred during deposit: {e}")
            print("Please try again.")
    
    def withdraw(self):
        try:
            print("\n=== Withdraw Money ===")
            print("Type 'exit' to go back to account menu.")
            
            while True:
                amount_str = input("How much would you like to withdraw? $").strip()
                if amount_str.lower() == 'exit':
                    return
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("Please enter a positive amount!")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                except Exception as e:
                    print(f"Error processing withdrawal amount: {e}")
                    print("Please try again.")
            
            account_data = self.accounts[self.logged_in_account]
            if account_data['balance'] < amount:
                print("❌ Sorry, you don't have enough funds for this transaction.")
                print(f"Your current balance is ${account_data['balance']:.2f}")
                return
            
            old_balance = account_data['balance']
            self.accounts[self.logged_in_account]['balance'] -= amount
            
            self.transactions.append({
                'type': 'withdrawal',
                'account_number': self.logged_in_account,
                'amount': amount,
                'balance_after': self.accounts[self.logged_in_account]['balance'],
                'timestamp': datetime.datetime.now(),
                'description': f'Withdrew ${amount:.2f}'
            })
            
            print(f"✅ Withdrawal successful!")
            print(f"Previous Balance: ${old_balance:.2f}")
            print(f"New Balance: ${self.accounts[self.logged_in_account]['balance']:.2f}")
            
        except KeyboardInterrupt:
            print("\nWithdrawal cancelled.")
        except Exception as e:
            print(f"An error occurred during withdrawal: {e}")
            print("Please try again.")
    
    def transfer(self):
        try:
            print("\n=== Transfer Money ===")
            print("Type 'exit' to go back to account menu.")
            
            target_account = input("Enter recipient's account number: ").strip()
            if target_account.lower() == 'exit':
                return
            
            if target_account not in self.accounts:
                print("Recipient account not found. Please check the account number.")
                return
            
            if target_account == self.logged_in_account:
                print("You cannot transfer money to your own account!")
                return
            
            while True:
                amount_str = input("How much would you like to transfer? $").strip()
                if amount_str.lower() == 'exit':
                    return
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("Please enter a positive amount!")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid amount!")
                except Exception as e:
                    print(f"Error processing transfer amount: {e}")
                    print("Please try again.")
            
            sender_data = self.accounts[self.logged_in_account]
            if sender_data['balance'] < amount:
                print("❌ Sorry, you don't have enough funds for this transfer.")
                print(f"Your current balance is ${sender_data['balance']:.2f}")
                return
            
            self.accounts[self.logged_in_account]['balance'] -= amount
            self.accounts[target_account]['balance'] += amount
            
            self.transactions.append({
                'type': 'transfer_out',
                'account_number': self.logged_in_account,
                'target_account': target_account,
                'amount': amount,
                'balance_after': self.accounts[self.logged_in_account]['balance'],
                'timestamp': datetime.datetime.now(),
                'description': f'Transferred ${amount:.2f} to account {target_account}'
            })
            
            self.transactions.append({
                'type': 'transfer_in',
                'account_number': target_account,
                'source_account': self.logged_in_account,
                'amount': amount,
                'balance_after': self.accounts[target_account]['balance'],
                'timestamp': datetime.datetime.now(),
                'description': f'Received ${amount:.2f} from account {self.logged_in_account}'
            })
            
            print(f"✅ Transfer successful!")
            print(f"Your new balance: ${self.accounts[self.logged_in_account]['balance']:.2f}")
            print(f"Recipient's new balance: ${self.accounts[target_account]['balance']:.2f}")
            
        except KeyboardInterrupt:
            print("\nTransfer cancelled.")
        except Exception as e:
            print(f"An error occurred during transfer: {e}")
            print("Please try again.")
    
    def view_transaction_history(self):
        try:
            print("\n=== Transaction History ===")
            account_transactions = [
                t for t in self.transactions 
                if t['account_number'] == self.logged_in_account
            ]
            
            if not account_transactions:
                print("No transactions found for your account.")
                return
            
            print(f"Showing {len(account_transactions)} transactions:")
            print("-" * 50)
            
            for transaction in reversed(account_transactions):
                try:
                    timestamp = transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    print(f"📅 {timestamp}")
                    print(f"   {transaction['description']}")
                    print(f"   Balance: ${transaction['balance_after']:.2f}")
                    if 'target_account' in transaction:
                        print(f"   To: {transaction['target_account']}")
                    if 'source_account' in transaction:
                        print(f"   From: {transaction['source_account']}")
                    print("-" * 30)
                except Exception as e:
                    print(f"Error displaying transaction: {e}")
                    continue
                    
        except KeyboardInterrupt:
            print("\nTransaction history view cancelled.")
        except Exception as e:
            print(f"An error occurred while viewing transaction history: {e}")
            print("Please try again.")
    
    def calculate_interest(self):
        try:
            print("\n=== Interest Calculator ===")
            account_data = self.accounts[self.logged_in_account]
            
            if account_data['account_type'] != 'savings':
                print("Interest calculation is only available for savings accounts.")
                print("Consider upgrading to a savings account for better benefits!")
                return
            
            annual_rate = 0.03
            monthly_rate = annual_rate / 12
            
            interest = account_data['balance'] * monthly_rate
            
            print(f"Account Type: {account_data['account_type'].title()}")
            print(f"Current Balance: ${account_data['balance']:.2f}")
            print(f"Monthly Interest Rate: {annual_rate*100/12:.2f}%")
            print(f"Estimated Monthly Interest: ${interest:.2f}")
            print(f"Balance after one month: ${account_data['balance'] + interest:.2f}")
            
        except KeyboardInterrupt:
            print("\nInterest calculation cancelled.")
        except Exception as e:
            print(f"An error occurred during interest calculation: {e}")
            print("Please try again.")
    
    def modify_account(self):
        try:
            print("\n=== Update Account Information ===")
            print("Type 'exit' to go back to account menu.")
            print("Note: Account number cannot be changed for security reasons.")
            
            account_data = self.accounts[self.logged_in_account]
            
            print(f"Current name: {account_data['name']}")
            new_name = input("Enter new name (press Enter to keep current): ").strip()
            if new_name.lower() == 'exit':
                return
            if new_name:
                account_data['name'] = new_name
                print("Name updated successfully!")
            
            print(f"Current account type: {account_data['account_type']}")
            while True:
                new_type = input("Enter new account type (savings/current) or Enter to keep current: ").strip().lower()
                if new_type.lower() == 'exit':
                    return
                if new_type and new_type not in ['savings', 'current']:
                    print("Please choose either 'savings' or 'current'")
                    continue
                if new_type:
                    account_data['account_type'] = new_type
                    print("Account type updated successfully!")
                break
            
            while True:
                new_password = input("Enter new password (minimum 6 characters, press Enter to keep current): ").strip()
                if new_password.lower() == 'exit':
                    return
                if new_password and len(new_password) < 6:
                    print("Password must be at least 6 characters long!")
                    continue
                if new_password:
                    account_data['password'] = new_password
                    print("Password updated successfully!")
                break
            
            if not new_name and not new_type and not new_password:
                print("No changes were made to your account.")
                
        except KeyboardInterrupt:
            print("\nAccount modification cancelled.")
        except Exception as e:
            print(f"An error occurred while updating account information: {e}")
            print("Please try again.")

if __name__ == "__main__":
    try:
        bank = BankingSystem()
        bank.main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Saving data before exit...")
        bank.save_data()
        print("Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Saving data before exit...")
        bank.save_data()
        print("The program will now exit.")