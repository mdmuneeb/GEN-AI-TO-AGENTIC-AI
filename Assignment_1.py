balance = 0

ask_user_to_add = int(input("How much money do you want to add ?"))
balance += ask_user_to_add

ask_user_how_much_spend_on_food = int(input("How much money did you spend on food ?"))
balance -= ask_user_how_much_spend_on_food

ask_user_how_much_spend_on_transport = int(input("How much money did you spend on transport ?"))
balance -= ask_user_how_much_spend_on_transport

ask_user_how_much_spend_on_shopping = int(input("How much money did you spend on shopping ?"))
balance -= ask_user_how_much_spend_on_shopping

final_balance = (balance > 500) & (balance < 5000)
print(f"Your final balance is in between 500 and 5000 : {final_balance}")