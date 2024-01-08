import random
import math

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
    monthly_payment_rounded = round(monthly_payment, 2)
    print("\nYour monthly payment will be: $" + str(monthly_payment_rounded))
    print("\n**Please be advised that this is only principal and interest payment (not including property tax or insurance)**\n\n")

    
def mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term, fico, state):
    interest_rate_month = interest_rate/100/12
    loan_amount = round(house_price * (1-(down_payment_percentage/100)),0)

    # need to group the FICO score into a group as the mortgage insurance premium is determined by range of FICO
    def round_down_to_nearest(num):
        num_in_units = num / 20
        unit_num = math.floor(num_in_units)
        return unit_num * 20
    
    if fico >= 780:
        fico = 760
    elif fico < 780:
        fico = int(round_down_to_nearest(fico))
    
    # down payment percentage is also being categorized into group for determining mortgage insurance premium
    down_payment_percentage = float(down_payment_percentage)
    LTV = 100 - down_payment_percentage
    if   85 >= LTV > 80:
        LTV = 85
    elif 90 >= LTV > 85:
        LTV = 90
    elif 95 >= LTV > 90:
        LTV = 95
    elif 97 >= LTV > 95:
        LTV = 97
    else:
        print("Ineligible down payment percentage for conventional program. Please at least 3\% \or greater for down payment %.")
    
    ##LTV_range dictionary is for finding insurance premium based on down payment percentage and FICO of the user input.
    LTV_range = {85:{760:0.0019, 740:0.0020, 720: 0.0023, 700:0.0025, 680:0.0028, 660:0.0038, 640:0.0040, 620:0.0044},
                 90:{760:0.0028, 740:0.0038, 720: 0.0046, 700:0.0055, 680:0.0065, 660:0.0090, 640:0.0091, 620:0.0094},
                 95:{760:0.0038, 740:0.0053, 720: 0.0066, 700:0.0078, 680:0.0096, 660:0.0128, 640:0.0133, 620:0.0142},
                 97:{760:0.0058, 740:0.0070, 720: 0.0087, 700:0.0099, 680:0.0121, 660:0.0154, 640:0.0165, 620:0.0186}}
    mortgage_insurance_premium = LTV_range[LTV][fico]

    if down_payment_percentage >= 20:
        monthly_payment = (loan_amount * interest_rate_month)/(1-(1+interest_rate_month)**(-1 * amortization_term))
    elif down_payment_percentage < 20:
        monthly_payment = (loan_amount * interest_rate_month)/(1-(1+interest_rate_month)**(-1 * amortization_term)) + (loan_amount * (mortgage_insurance_premium/12))
    else:
        print("Invalid down payment percentage for conventional program. Please at least 3\% \or greater for down payment %.")

    house_insurance_premium = {'AL':0.006524, 'AK':0.004224, 'AZ':0.005072, 'AR':0.008492, 'CA':0.0049,   'CO':0.008608, 'CT':0.004976, 
                               'DE':0.002716, 'FL':0.007924, 'GA':0.005576, 'HI':0.001528, 'ID':0.00362,  'IL':0.00564,  'ID':0.0049, 
                               'IA':0.005272, 'KS':0.012332, 'KY':0.008036, 'LA':0.007968, 'ME':0.003788, 'MD':0.004656, 'MS':0.004796, 
                               'MI':0.006108, 'MN':0.00772,  'MS':0.0076,   'MO':0.007076, 'MT':0.006944, 'NE':0.011804, 'NV':0.003556, 
                               'NH':0.002944, 'NJ':0.0031,   'NM':0.007156, 'NY':0.006024, 'NC':0.005176, 'ND':0.0076,   'OH':0.00456, 
                               'OK':0.014636, 'OR':0.002892, 'PA':0.00304,  'RI':0.004932, 'SC':0.004688, 'SD':0.00842,  'TN':0.00702, 
                               'TX':0.007868, 'UT':0.002784, 'VT':0.002632, 'VA':0.003548, 'WA':0.003792, 'WV':0.0045,   'WI':0.00356, 
                               'WY':0.003816, 'DC':0.003572}
    
    state = str(state.upper())
    if state == 'CA':
        monthly_MIP = round(loan_amount * (mortgage_insurance_premium/12), 2)
        monthly_tax = round((house_price * 0.0125 / 12),2)
        monthly_ins = round((house_price * house_insurance_premium[state])/12, 2)
        monthly_payment += monthly_tax + monthly_ins
        monthly_payment_PI = round(monthly_payment - monthly_tax - monthly_ins - monthly_MIP , 2)
    else:
        monthly_MIP = round(loan_amount * (mortgage_insurance_premium/12),2)
        monthly_tax = round((house_price * 0.015 / 12),2)
        monthly_ins = round((house_price * house_insurance_premium[state])/12,2)
        monthly_payment += monthly_tax + monthly_ins
        monthly_payment_PI = round(monthly_payment - monthly_tax - monthly_ins - monthly_MIP , 2)
            
    monthly_payment_rounded = round(monthly_payment, 2)
    print("\n Your loan amount is $" + str(loan_amount))
    print("\nYour total monthly payment will be: $" + str(monthly_payment_rounded) + 
          "\n**This consists of principal and interest payment of $" + str(monthly_payment_PI) + 
          "\n**Est. Property tax per month: $" + str(monthly_tax) +
          "\n**Est. Home insurance per month: $" + str(monthly_ins) +
          "\n**Mortgage insurance premium: $" + str(monthly_MIP))
    print("\n**Monthly payment total includes mortgage insurance premium, estimated property taxes, and hazard insurance premium relative to the house price**\n")

def userInputIntegerNumberValidation(question):
    while True:
        user_input = input(question)
        try:
            user_input = int(user_input)
            break
        except ValueError:
            print("No special characters. Please enter numerical value only. Integers and decimals are acceptable")
            print("Please try again.")
    return int(user_input)

def userInputFloatNumberValidation(question):
    while True:
        user_input = input(question)
        try:
            user_input = float(user_input)
            break
        except ValueError:
            print("No special characters. Please enter numerical value only. Integers and decimals are acceptable")
            print("Please try again.")
    return float(user_input)
    
def loan_qualification(income, liabilities):
    

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
        calculation_method = input("\nDo you wish to calculate payment with house in mind (Y) or just simple payment calculator (N)? (Y/N)")
        calculation_method = calculation_method.upper().strip()
        if calculation_method == 'Y':
            house_price = userInputIntegerNumberValidation("\nEnter the price of the house that you wish to buy: ")      
            down_payment_percentage = userInputFloatNumberValidation("\nHow much do you want to put down in percentage? (ex: 20%, or 15%, etc): ")
            interest_rate = userInputFloatNumberValidation("\nEnter the interest rate (refer to bankrate.com/mortgages/mortgage_rates/ if you don't know what interest rate to use): ")
            amortization_term = userInputIntegerNumberValidation("\nHow many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
            fico = userInputIntegerNumberValidation("\nWhat is your estimated FICO (credit) score (three digits ranging from 500-800+)?: ")
            state = input("\nWhich state is the house you're trying to buy located in? (please enter only two letter abbreviated version): ")
            state = state.strip().upper()
            mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term, fico, state)
        elif calculation_method == 'N':
            loan_amount = userInputIntegerNumberValidation("\nEnter your loan amount: ")
            interest_rate = userInputFloatNumberValidation("\nEnter the interest rate: ")
            amortization_term = userInputFloatNumberValidation("\nHow many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
            mortgage_calculator(loan_amount, interest_rate, amortization_term)
    elif choice == '5':
        break
    elif choice != '1' or '2' or '3' or '4' or '5':
        print("\nInput invalid. Please enter a number from 1-5.\n")
            
