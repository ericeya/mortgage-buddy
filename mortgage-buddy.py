import random
import math
from bs4 import BeautifulSoup
import requests

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
    
def income_calculation_w2():
    income_type_w2 = input("Are you paid by hourly rate (H) or salary rate(S)? Salary rate means your paystub shows flat salary rate per week or per month, etc. Enter either H or S: ").strip().upper()
    if income_type_w2 == 'H':
        print("""In order to calculate your qualifying income, we need to know if you work consistent or variable hours.
                By consistent, it means, if you work 40 hours per week (full-time job), then you always work 40 hours per week. Also,
                40 hours could be covered by any PTO, sick time, or any paid holidays that you make up for loss of hours worked
                to be paid 40 hours / week in total.

                Also, it could mean you work 30 hours/week consistently as if your hours are fixed at 30 hours/week and any time
                lost from not working is made up by PTO, sick time, paid holidays, or any other payment that makes up for it.
                
                By variable hours (considered part-time job), it means you work and get paid as much as you work. For example, 
                one week you work 30 hours, another week 36 hours, another week 29 hours, another week 39 hours, etc. 
                When you are paid variable hours your income will be averaged based on YTD and previous 2 years' earnings (base YTD only).
            
                If you work variable hours, try to guess how many hours you work on average per week. Please note that actual calculation
                of your income will be based on YTD average which will be calculated by the underwriter at a mortgage lending company.                    
                """)
        hours_worked = input("Please enter the number of hours worked as base regular pay per week: ")
        hourly_rate = input("Please enter your hourly rate: ")
        income = (hourly_rate * hours_worked * 52) / 12 
        return income
    if income_type_w2 == 'S':
        income = input("Enter your monthly salary: ")
        return income

def income_calculation_self_employment():
    total_self_employment_income = 0
    while True:
        self_employment_type = input("""Please enter all businesses' income. Choose one of the options to enter each business entity's income.
Otherwise, if you're done, please enter 0.
    Options:
    1. C (for schedule C)
    2. 1065
    3. 1120S
    4. 1120
    5. 0
    : """).upper()
        if self_employment_type == 'C':
            calculation_method = input("Do you want to enter the total income estimate yourself (1) or use our calculator for exact details? (2) - Enter 1 or 2: ")
            if calculation_method == '1':
                income = input("Enter your total income per month: ")
                total_self_employment_income += income
            elif calculation_method == '2':
                print("You'll need most recent two years tax return. Let's start with the most recent year's earnings. Please flip to your schedule C pages in your tax return.\n")
                total_income = {'recent_year_income': 0, 'previous_year_income': 0}
                for each_year in total_income: 
                    net_profit = input("Enter net profit (line 31) : ")
                    other_income_or_loss = input("Other income or other loss (line 6 - enter negative number if other INCOME, and positive if other LOSS): ")
                    depletion = input("Enter depletion (line 12): ")
                    depreciation = input("Enter depreciation (line 13): ")
                    deductible_meals = input("Enter deductible meals (line 24(b)): ")
                    amortization = input("Enter amortization (Part V other expenses): ")
                    business_use_of_home = input("Enter business use of home (line 30): ")
                    subtotal = net_profit + other_income_or_loss + depletion + depreciation - deductible_meals + amortization + business_use_of_home
                    total_income[each_year] = subtotal 
                    if total_income['recent_year_income'] is not 0 and total_income['previous_year_income'] is 0:
                        print("Now please enter figures from schedule C for your previous year (the year before the one you just entered). ")
                if total_income['previous_year_income'] > total_income['recent_year_income']:
                    income = round((total_income['recent_year_income'])/12,2)
                    total_self_employment_income += income
                    return income + print("Your monthly qualifying income from this schedule C business is $" + income + ".\n")
                elif total_income['recent_year_income'] >= total_income['previous_year_income']:
                    income = round((total_income['previous_year_income'] + total_income['recent_year_income'])/24, 2)
                    total_self_employment_income += income
                    return income + print("Your monthly qualifying income from this schedule C business is $" + income + ".\n")
        if self_employment_type == '1065' or '1120S':
            calculation_method = input("Do you want to enter the total income estimate yourself (1) or use our calculator for exact details? (2) - Enter 1 or 2: ")
            if calculation_method == '1':
                income == input("Enter your total income per month: ")
                total_self_employment_income += income
            elif calculation_method == '2':
                print("You'll need most recent two years business tax return. Let's start with the most recent year's earnings. Please flip to your business tax return (1065 or 1120S) to enter the following.\n")
                total_income = {'recent_year_income': 0, 'previous_year_income': 0}
                for each_year in total_income:
                    self_employment_ownership = input("Enter the amount of percentage of ownership you have in this business: ") 
                    if self_employment_ownership >= 25:
                        schedule_K1 = input("Enter K-1 box 1,2,3 total (enter negative number if the sum is negative): ")
                        liquidity_test = input("Does your schedule K-1 show distribution (box 19 for 1065, box 16 with code D for 1120S) that is equal to or higher than box 1 amount? (Y/N): ").upper()
                        if liquidity_test == "Y":
                            schedule_K1 = round(float(schedule_K1),2)
                        elif liquidity_test == "N":
                            schedule_K1 = round(float(input("Enter the distribution amount (box 19 for 1065, box 16 with code D for 1120S): ")),2)
                        other_income_or_loss = input("Other income or other loss (line 7 for 1065 / line 5 for 1120S - enter negative number if other INCOME, and positive if other LOSS): ")
                        depletion = input("Enter depletion (line 17 for 1065, line 15 for 1120S): ")
                        depreciation = input("Enter depreciation (line 16c for 1065, line 14 for 1120S): ")
                        deductible_meals = input("Enter deductible meals (line M-1 - 4(b) for 1065, line M-1 - 3(b) for 1120S): ")
                        mortgage_notes_bonds_payable_in_less_than_one_year = input("Enter mortgage, notes, bonds, payable in less than 1 year (schedule L, line 16 for 1065, line 17 for 1120S): ")
                        amortization = input("Enter amortization (line 21 for 1065, line 20 for 1120S) - PLEASE ENTER AMORTIZATION EXPENSE ONLY from other deductions which is itemized and attached as statement in the end: ")
                        w_2 = input("If you received W-2 income from this job, enter the total W-2 income (box 5) amount: ")
                        subtotal = schedule_K1 + other_income_or_loss + depletion + depreciation - deductible_meals + amortization + business_use_of_home + w_2 - mortgage_notes_bonds_payable_in_less_than_one_year
                        total_income[each_year] = subtotal 
                        if total_income['recent_year_income'] is not 0 and total_income['previous_year_income'] is 0:
                            print("Now please enter figures from schedule C for your previous year (the year before the one you just entered). ")
                    elif self_employment_ownership < 25:
                        print("If you own less than 25\% \of the business, then you're not considered self-employed. You may still use K-1 income that is distributed to you.")
                        k1_income = input("Enter lesser of the K-1 box 1 or box 19 for 1065 or box 16 with code D for 1120S: ")
                        w2_income = input("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = k1_income + w2_income
                        if total_income['recent_year_income'] is not 0 and total_income['previous_year_income'] is 0:
                            print("Do the same for previous year K-1.")
                if total_income['previous_year_income'] > total_income['recent_year_income']:
                    income = round((total_income['recent_year_income'])/12,2)
                    total_self_employment_income += income
                    return income + print("Your monthly qualifying income from this 1065 or 1120S business is $" + income + ".\n")
                elif total_income['recent_year_income'] >= total_income['previous_year_income']:
                    income = round((total_income['previous_year_income'] + total_income['recent_year_income'])/24, 2)
                    total_self_employment_income += income
                    return income + print("Your monthly qualifying income from this schedule C business is $" + income + ".\n")
        if self_employment_type == '1120':
            calculation_method = input("Do you want to enter the total income estimate yourself (1) or use our calculator for exact details? (2) - Enter 1 or 2: ")
            if calculation_method == '1':
                income == input("Enter your total income per month: ")
                total_self_employment_income += income
            elif calculation_method == '2':
                print("You'll need most recent two years business tax return. Let's start with the most recent year's earnings. Please flip to your business tax return (1120) to enter the following.\n")
                total_income = {'recent_year_income': 0, 'previous_year_income': 0}
                for each_year in total_income:
                    depreciation = input("Enter depreciation (line 20): ")
                    depletion = input("Enter depletion (line 21): ")
                    amortization = input("Enter amortization or casualty loss (line 26) - PLEASE ENTER AMORTIZATION EXPENSE ONLY from other deductions which is itemized and attached as statement in the end: ")
                    other_income_or_loss = input("Other income or other loss (line 10 - enter negative number if other INCOME, and positive if other LOSS): ")
                    net_operating_loss = input("Enter net operating loss (line 29(c)): ")
                    taxable_income_or_loss = input("Enter taxable income or loss (line 30): ")
                    total_tax = input("Enter total tax (line 31): ")
                    mortgage_notes_bonds_payable_in_less_than_one_year = input("Enter mortgage, notes, bonds, payable in less than 1 year (schedule L, line 17): ")
                    deductible_meals = input("Enter deductible meals (line M-1 - 3(b)): ")
                    subtotal = depreciation + depletion + amortization + net_operating_loss + taxable_income_or_loss - total_tax - mortgage_notes_bonds_payable_in_less_than_one_year + other_income_or_loss - deductible_meals
                    self_employment_ownership = input("Enter the amount of percentage of ownership you have in this business: ")
                    if self_employment_ownership == 100:
                        w2_income = input("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = subtotal + w2_income
                    elif self_employment_ownership <100 or subtotal < 0:
                        w2_income = input("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = subtotal + w2_income
                    elif self_employment_ownership <100 and subtotal > 0:
                        print("In order to qualify business income, you must be 100% 'owner' of the business. You may only qualify W-2 income received from this business.")
                        w2_income = input("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = w2_income
                    if total_income['recent_year_income'] is not 0 and total_income['previous_year_income'] is 0:
                        print("Now please enter figures from your previous year (the year before the one you just entered).")
                if total_income['previous_year_income'] > total_income['recent_year_income']:
                    income = round((total_income['recent_year_income'])/12,2)
                    total_self_employment_income += income
                    return income + print("Your monthly qualifying income from this 1120 business is $" + income + ".\n")
                elif total_income['recent_year_income'] >= total_income['previous_year_income']:
                    income = round((total_income['previous_year_income'] + total_income['recent_year_income'])/24, 2)
                    total_self_employment_income += income
                    return income + print("Your monthly qualifying income from this 1120 business is $" + income + ".\n")            
        if self_employment_type == '0':
            print("Your total self employment income from all business(es) is: " + str(total_self_employment_income))
            break
    return total_self_employment_income

def liabilities():
    print("under construction")

def loan_qualification(income, liabilities):
    income = 10    

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
    elif choice == '2':
        print("\nIn order to help us evaluate your qualification for a conventional mortgage loan program, we'll need to ask you some questions.")
        print("\nPlease answer the following questions: ")
        income_type = input("Please confirm if you're paid W-2 as a wage earner (A) or if you're self-employed (B), or both (C): ")
        income_type = income_type.strip().upper()
        if income_type == 'A':
            income_w2 = income_calculation_w2()
            debts = liabilities()
            loan_qual = loan_qualification(income_w2, debts)
        elif income_type == 'B':
            income_se = income_calculation_self_employment()
            debts = liabilities()
            loan_qual = loan_qualification(income_se, debts)
        elif income_type == 'C':
            all_income = income_calculation_w2() + income_calculation_self_employment()
            debts = liabilities()
            loan_qual = loan_qualification(all_income, debts)
    elif choice == '3':        
        print("...Under construction...")
                      
    elif choice == '5':
        break
    elif choice != '1' or '2' or '3' or '4' or '5':
        print("\nInput invalid. Please enter a number from 1-5.\n")
            
