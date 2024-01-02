import random

print("""

888b     d888                  888                                              888888b.                 888      888          
8888b   d8888                  888                                              888  "88b                888      888          
88888b.d88888                  888                                              888  .88P                888      888          
888Y88888P888  .d88b.  888d888 888888  .d88b.   8888b.   .d88b.   .d88b.        8888888K.  888  888  .d88888  .d88888 888  888 
888 Y888P 888 d88""88b 888P"   888    d88P"88b     "88b d88P"88b d8P  Y8b       888  "Y88b 888  888 d88" 888 d88" 888 888  888 
888  Y8P  888 888  888 888     888    888  888 .d888888 888  888 88888888       888    888 888  888 888  888 888  888 888  888 
888   "   888 Y88..88P 888     Y88b.  Y88b 888 888  888 Y88b 888 Y8b.           888   d88P Y88b 888 Y88b 888 Y88b 888 Y88b 888 
888       888  "Y88P"  888      "Y888  "Y88888 "Y888888  "Y88888  "Y8888        8888888P"   "Y88888  "Y88888  "Y88888  "Y88888 
                                           888               888                                                           888 
                                      Y8b d88P          Y8b d88P                                                      Y8b d88P 
                                       "Y88P"            "Y88P"                                                        "Y88P"  

""")

def mortgage_calculator(loan_amount, interest_rate, amortization_term):
    interest_rate_month = interest_rate/100/12
    monthly_payment = (loan_amount * interest_rate_month)/(1-(1+interest_rate_month)**(-1 * amortization_term))
    print("Your monthly payment will be: " + str(monthly_payment))
    print("**Please be advised that this is only principal and interest payment (not including property tax or insurance)**")

    
def mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term):
    print("not configured yet")


    
# def loan_qualification(income, liabilities)
    

while True:

    print("""Main menu:
      
      1. Calculate mortgage payment

      2. See if you qualify for a mortgage

      3. Current average interest rate

      4. Helpful tips about mortgage

      5. Exit

      """)

    choice = input('Enter your choice: ')
    choice = choice.strip()

    if choice == '1':
        calculation_method = input("Do you wish to calculate payment with house in mind or just simple payment calculator? (Y/N)")
        if calculation_method == 'Y':
            house_price = int(input("Enter the price of the house that you wish to buy: "))
            down_payment_percentage = float(input("How much do you want to put down in percentage?: "))
            interest_rate = input("Enter the interest rate: ")
            amortization_term = input("How many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
            payment = mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term)
            print(payment)
        elif calculation_method == 'N':
            loan_amount = float(input("Enter your loan amount: "))
            interest_rate = float(input("Enter the interest rate: "))
            amortization_term = float(input("How many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): "))
            payment = mortgage_calculator(loan_amount, interest_rate, amortization_term)
            print(payment)
    elif choice == '5':
        break
