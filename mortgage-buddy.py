from random import randint
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
    elif LTV > 97:
        print("Ineligible down payment percentage for conventional program. Please at least 3% or greater for down payment %.")
    elif LTV <= 80:
        LTV = 80
    
    ##LTV_range dictionary is for finding insurance premium based on down payment percentage and FICO of the user input.
    LTV_range = {85:{760:0.0019, 740:0.0020, 720: 0.0023, 700:0.0025, 680:0.0028, 660:0.0038, 640:0.0040, 620:0.0044},
                 90:{760:0.0028, 740:0.0038, 720: 0.0046, 700:0.0055, 680:0.0065, 660:0.0090, 640:0.0091, 620:0.0094},
                 95:{760:0.0038, 740:0.0053, 720: 0.0066, 700:0.0078, 680:0.0096, 660:0.0128, 640:0.0133, 620:0.0142},
                 97:{760:0.0058, 740:0.0070, 720: 0.0087, 700:0.0099, 680:0.0121, 660:0.0154, 640:0.0165, 620:0.0186},
                 80:{760:0.0000, 740:0.0000, 720: 0.0000, 700:0.0000, 680:0.0000, 660:0.0000, 640:0.0000, 620:0.0000}}
    mortgage_insurance_premium = LTV_range[LTV][fico]

    if down_payment_percentage >= 20:
        monthly_payment = (loan_amount * interest_rate_month)/(1-(1+interest_rate_month)**(-1 * amortization_term))
    elif down_payment_percentage < 20:
        monthly_payment = (loan_amount * interest_rate_month)/(1-(1+interest_rate_month)**(-1 * amortization_term)) + (loan_amount * (mortgage_insurance_premium/12))
    else:
        print("Invalid down payment percentage for conventional program. Please at least 3% or greater for down payment %.")

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
    return monthly_payment_rounded

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
            user_input = round(float(user_input),2)
            break
        except ValueError:
            print("No special characters. Please enter numerical value only. Integers and decimals are acceptable")
            print("Please try again.")
    return float(user_input)

def userInputTextValidation(question):
    while True:
        user_input = str(input(question)).strip().upper()
        try:
            if user_input == 'A' or user_input == 'B' or user_input == 'C' or user_input == 'Y' or user_input == 'N' or user_input == 'H' or user_input == 'S':
                break
        except TypeError:
            print("No special characters. Please enter one of the valid options only.")
            print("Please try again.")
    return user_input
    
def income_calculation_w2():
    income_type_w2 = userInputTextValidation("Are you paid by hourly rate (H) or salary rate(S)? Salary rate means your paystub shows flat salary rate per week or per month, etc. Enter either H or S: ")
    if income_type_w2 == 'H':
        print("""\nIn order to calculate your qualifying income, we need to know if you work consistent or variable hours.
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
        hours_worked = userInputFloatNumberValidation("Please enter the number of hours worked as base regular pay per week: ")
        hourly_rate = userInputFloatNumberValidation("Please enter your hourly rate: ")
        income = (hourly_rate * hours_worked * 52) / 12 
        return income
    if income_type_w2 == 'S':
        income = userInputFloatNumberValidation("Enter your monthly salary: ")
        return income

def income_calculation_self_employment():
    total_self_employment_income = float(0)
    while True:
        self_employment_type = userInputIntegerNumberValidation("""\nPlease enter all businesses' income. Choose one of the options to enter each business entity's income.
Please select from 1-5.  choose 5.
  Options:
    1. C (for schedule C)
    2. 1065
    3. 1120S
    4. 1120
    5. Exit
    : """)
        if self_employment_type == 1:
            calculation_method = userInputIntegerNumberValidation("Do you want to enter the total income estimate yourself(1) or use our calculator for exact details(2)? - Enter 1 or 2: ")
            if calculation_method == 1:
                income = userInputFloatNumberValidation("Enter your total income per month: ")
                total_self_employment_income += income
            elif calculation_method == 2:
                print("\nYou'll need most recent two years tax return. Let's start with the most recent year's earnings. Please flip to your schedule C pages in your tax return.\n")
                total_income = {'recent_year_income': 0, 'previous_year_income': 0}
                for each_year in total_income: 
                    net_profit = userInputFloatNumberValidation("Enter net profit (line 31) : ")
                    other_income_or_loss = userInputFloatNumberValidation("Other income or other loss (line 6 - enter negative number if other INCOME, and positive if other LOSS): ")
                    depletion = userInputFloatNumberValidation("Enter depletion (line 12): ")
                    depreciation = userInputFloatNumberValidation("Enter depreciation (line 13): ")
                    deductible_meals = userInputFloatNumberValidation("Enter deductible meals (line 24(b)): ")
                    amortization = userInputFloatNumberValidation("Enter amortization (Part V other expenses): ")
                    business_use_of_home = userInputFloatNumberValidation("Enter business use of home (line 30): ")
                    subtotal = net_profit + other_income_or_loss + depletion + depreciation - deductible_meals + amortization + business_use_of_home
                    total_income[each_year] = subtotal 
                    if total_income['recent_year_income'] != 0 and total_income['previous_year_income'] == 0:
                        print("\nNow please enter figures from schedule C for your previous year (the year before the one you just entered).\n ")
                if total_income['previous_year_income'] > total_income['recent_year_income']:
                    income = round((total_income['recent_year_income'])/12,2)
                    total_self_employment_income += income
                    print("Your monthly qualifying income from this schedule C business is $" + income + ".\n")
                elif total_income['recent_year_income'] >= total_income['previous_year_income']:
                    income = round((total_income['previous_year_income'] + total_income['recent_year_income'])/24, 2)
                    total_self_employment_income += income
                    print("Your monthly qualifying income from this schedule C business is $" + str(income) + ".\n")
        elif self_employment_type == 2 or self_employment_type == 3:
            calculation_method = userInputIntegerNumberValidation("Do you want to enter the total income estimate yourself(1) or use our calculator for exact details(2)? - Enter 1 or 2: ")
            if calculation_method == 1:
                income = userInputFloatNumberValidation("Enter your total income per month: ")
                total_self_employment_income += income
            elif calculation_method == 2:
                print("You'll need most recent two years business tax return. Let's start with the most recent year's earnings. Please flip to your business tax return (1065 or 1120S) to enter the following.\n")
                total_income = {'recent_year_income': 0, 'previous_year_income': 0}
                for each_year in total_income:
                    self_employment_ownership = userInputFloatNumberValidation("Enter the amount of percentage of ownership you have in this business: ") 
                    if self_employment_ownership >= 25:
                        schedule_K1 = userInputFloatNumberValidation("Enter K-1 box 1,2,3 total (enter negative number if the sum is negative): ")
                        liquidity_test = userInputTextValidation("Does your schedule K-1 show distribution (box 19 for 1065, box 16 with code D for 1120S) that is equal to or higher than box 1 amount? (Y/N): ").upper()
                        if liquidity_test == "Y":
                            schedule_K1 = schedule_K1
                        elif liquidity_test == "N":
                            schedule_K1 = round(float(input("Enter the distribution amount (box 19 for 1065, box 16 with code D for 1120S): ")),2)
                        other_income_or_loss = userInputFloatNumberValidation("Other income or other loss (line 7 for 1065 / line 5 for 1120S - enter negative number if other INCOME, and positive if other LOSS): ")
                        depletion = userInputFloatNumberValidation("Enter depletion (line 17 for 1065, line 15 for 1120S): ")
                        depreciation = userInputFloatNumberValidation("Enter depreciation (line 16c for 1065, line 14 for 1120S): ")
                        deductible_meals = userInputFloatNumberValidation("Enter deductible meals (line M-1 - 4(b) for 1065, line M-1 - 3(b) for 1120S): ")
                        mortgage_notes_bonds_payable_in_less_than_one_year = userInputFloatNumberValidation("Enter mortgage, notes, bonds, payable in less than 1 year (schedule L, line 16 for 1065, line 17 for 1120S): ")
                        amortization = userInputFloatNumberValidation("Enter amortization (line 21 for 1065, line 20 for 1120S) - PLEASE ENTER AMORTIZATION EXPENSE ONLY from other deductions which is itemized and attached as statement in the end: ")
                        w_2 = userInputFloatNumberValidation("If you received W-2 income from this job, enter the total W-2 income (box 5) amount: ")
                        subtotal = schedule_K1 + other_income_or_loss + depletion + depreciation - deductible_meals + amortization + w_2 - mortgage_notes_bonds_payable_in_less_than_one_year
                        total_income[each_year] = subtotal 
                        if total_income['recent_year_income'] != 0 and total_income['previous_year_income'] == 0:
                            print("\nNow please enter figures from schedule C for your previous year (the year before the one you just entered).\n ")
                    elif self_employment_ownership < 25:
                        print("If you own less than 25% of the business, then you're not considered self-employed. You may still use K-1 income that is distributed to you.")
                        k1_income = userInputFloatNumberValidation("Enter lesser of the K-1 box 1 or box 19 for 1065 or box 16 with code D for 1120S: ")
                        w2_income = userInputFloatNumberValidation("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = k1_income + w2_income
                        if total_income['recent_year_income'] != 0 and total_income['previous_year_income'] == 0:
                            print("Do the same for previous year K-1.")
                if total_income['previous_year_income'] > total_income['recent_year_income']:
                    income = round((total_income['recent_year_income'])/12,2)
                    total_self_employment_income += income
                    print("Your monthly qualifying income from this 1065 or 1120S business is $" + str(income) + ".\n")
                elif total_income['recent_year_income'] >= total_income['previous_year_income']:
                    income = round((total_income['previous_year_income'] + total_income['recent_year_income'])/24, 2)
                    total_self_employment_income += income
                    print("Your monthly qualifying income from this schedule C business is $" + str(income) + ".\n")
        elif self_employment_type == 4:
            calculation_method = userInputIntegerNumberValidation("Do you want to enter the total income estimate yourself(1) or use our calculator for exact details(2)? - Enter 1 or 2: ")
            if calculation_method == 1:
                income == userInputFloatNumberValidation("Enter your total income per month: ")
                total_self_employment_income += income
            elif calculation_method == 2:
                print("You'll need most recent two years business tax return. Let's start with the most recent year's earnings. Please flip to your business tax return (1120) to enter the following.\n")
                total_income = {'recent_year_income': 0, 'previous_year_income': 0}
                for each_year in total_income:
                    depreciation = userInputFloatNumberValidation("Enter depreciation (line 20): ")
                    depletion = userInputFloatNumberValidation("Enter depletion (line 21): ")
                    amortization = userInputFloatNumberValidation("Enter amortization or casualty loss (line 26) - PLEASE ENTER AMORTIZATION EXPENSE ONLY from other deductions which is itemized and attached as statement in the end: ")
                    other_income_or_loss = userInputFloatNumberValidation("Other income or other loss (line 10 - enter negative number if other INCOME, and positive if other LOSS): ")
                    net_operating_loss = userInputFloatNumberValidation("Enter net operating loss (line 29(c)): ")
                    taxable_income_or_loss = userInputFloatNumberValidation("Enter taxable income or loss (line 30): ")
                    total_tax = userInputFloatNumberValidation("Enter total tax (line 31): ")
                    mortgage_notes_bonds_payable_in_less_than_one_year = userInputFloatNumberValidation("Enter mortgage, notes, bonds, payable in less than 1 year (schedule L, line 17): ")
                    deductible_meals = userInputFloatNumberValidation("Enter deductible meals (line M-1 - 3(b)): ")
                    subtotal = depreciation + depletion + amortization + net_operating_loss + taxable_income_or_loss - total_tax - mortgage_notes_bonds_payable_in_less_than_one_year + other_income_or_loss - deductible_meals
                    self_employment_ownership = userInputFloatNumberValidation("Enter the amount of percentage of ownership you have in this business: ")
                    if self_employment_ownership == 100.00:
                        w2_income = userInputFloatNumberValidation("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = subtotal + w2_income
                    elif self_employment_ownership <100.00 or subtotal < 0.00:
                        w2_income = userInputFloatNumberValidation("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = subtotal + w2_income
                    elif self_employment_ownership <100.00 and subtotal > 0.00:
                        print("In order to qualify business income, you must be 100% 'owner' of the business. You may only qualify W-2 income received from this business.")
                        w2_income = userInputFloatNumberValidation("If you received any W-2 income from this business, then enter the amount from box 5: ")
                        total_income[each_year] = w2_income
                    if total_income['recent_year_income'] != 0 and total_income['previous_year_income'] == 0:
                        print("Now please enter figures from your previous year (the year before the one you just entered).")
                if total_income['previous_year_income'] > total_income['recent_year_income']:
                    income = round((total_income['recent_year_income'])/12,2)
                    total_self_employment_income += income
                    print("Your monthly qualifying income from this 1120 business is $" + str(income) + ".\n")
                elif total_income['recent_year_income'] >= total_income['previous_year_income']:
                    income = round((total_income['previous_year_income'] + total_income['recent_year_income'])/24, 2)
                    total_self_employment_income += income
                    print("Your monthly qualifying income from this 1120 business is $" + str(income) + ".\n")            
        elif self_employment_type == 5:
            print(total_self_employment_income)
            print("Your total self employment income from all business(es) is: " + str(total_self_employment_income))
            break
    return total_self_employment_income

def calculate_liability():
    mortgages_owned = userInputIntegerNumberValidation("""\n   To confirm if you can qualify for a mortgage, we will need to know the house price and loan amount you'll be getting and how many mortgages you have. 
                            
If the house that you're trying to purchase is the only house, then enter 1.
                            
If you have multiple houses with or without mortgages, enter 2: """)
    if mortgages_owned == 1:
        house_price = userInputIntegerNumberValidation("\nEnter the price of the house that you wish to buy: ")      
        down_payment_percentage = userInputFloatNumberValidation("\nHow much do you want to put down in percentage? (ex: 20%, or 15%, etc): ")
        interest_rate = userInputFloatNumberValidation("\nPlease confirm if you want to use current national average rate (1) or if you want to enter your own rate (2):  ")
        if interest_rate == 1:
            mortgage_rate_scrape = requests.get("https://www.bankrate.com/mortgages/mortgage-rates/")
            soup = BeautifulSoup(mortgage_rate_scrape.text, "html.parser")
            national_interest_rate_average = soup.findAll("span", attrs={"class":"text-black font-bold","id":"brPreRateTrendsVisualV2-national-rate"})
            for rate in national_interest_rate_average:
                interest_rate = float(rate.text[1:5])
                print("Current national average rate: " + (rate.text[1:]))
        elif interest_rate == 2:
            interest_rate = userInputFloatNumberValidation("Please enter the interest rate: ")
        else:
            print("Please enter either 1 or 2.")
        amortization_term = userInputIntegerNumberValidation("\nHow many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
        fico = userInputIntegerNumberValidation("\nWhat is your estimated FICO (credit) score (three digits ranging from 500-800+)?: ")
        state = input("\nWhich state is the house you're trying to buy located in? (please enter only two letter abbreviated version): ")
        state = state.strip().upper()
        subject_mortgage = mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term, fico, state)
        installment_debts = userInputFloatNumberValidation("Enter total amount of monthly installment debts (auto loan, personal loan, time share, or any other loan): ")
        student_loans = userInputFloatNumberValidation("Enter the total amount of monthly student loan debts. If the payment is deferred, use 1% of the balance as monthly payment amount: ")
        credit_card_debts = userInputFloatNumberValidation("Enter the total amount of all of your credit cards' monthly required minimum payment: ")
        child_support_or_alimony = userInputFloatNumberValidation("Enter any monthly obligated child support or alimony being paid: ")
        subtotal_liab = subject_mortgage + installment_debts + student_loans + credit_card_debts + child_support_or_alimony
        subtotal_liab = float(subtotal_liab)
        print("Your total monthly debts is: $" + str(subtotal_liab))
        return subtotal_liab
    if mortgages_owned == 2:
        #this one looks same as above, but it has other_reo_pitia added to account for multiple mortgages and the subtotal_liab accounts for the difference.
        print("Let's start with subject property's house price / mortgage payments / etc.")
        house_price = userInputIntegerNumberValidation("\nEnter the price of the house that you wish to buy: ")      
        down_payment_percentage = userInputFloatNumberValidation("\nHow much do you want to put down in percentage? (ex: 20%, or 15%, etc): ")
        interest_rate = userInputFloatNumberValidation("\nPlease confirm if you want to use current national average rate (1) or if you want to enter your own rate (2):  ")
        if interest_rate == 1:
            mortgage_rate_scrape = requests.get("https://www.bankrate.com/mortgages/mortgage-rates/")
            soup = BeautifulSoup(mortgage_rate_scrape.text, "html.parser")
            national_interest_rate_average = soup.findAll("span", attrs={"class":"text-black font-bold","id":"brPreRateTrendsVisualV2-national-rate"})
            for rate in national_interest_rate_average:
                interest_rate = float(rate.text[1:5])
                print("Current national average rate: " + (rate.text[1:]))
        elif interest_rate == 2:
            interest_rate = userInputFloatNumberValidation("Please enter the interest rate: ")
        else:
            print("Please enter either 1 or 2.")
        amortization_term = userInputIntegerNumberValidation("\nHow many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
        fico = userInputIntegerNumberValidation("\nWhat is your estimated FICO (credit) score (three digits ranging from 500-800+)?: ")
        state = input("\nWhich state is the house you're trying to buy located in? (please enter only two letter abbreviated version): ")
        state = state.strip().upper()
        subject_mortgage = mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term, fico, state)
        other_reo_pitia = userInputFloatNumberValidation("Enter the monthly PITIA (principal / interest / property tax / insurance / HOA dues) of other real estates owned: ")
        installment_debts = userInputFloatNumberValidation("Enter total amount of monthly installment debts (auto loan, personal loan, time share, or any other loan): ")
        student_loans = userInputFloatNumberValidation("Enter the total amount of monthly student loan debts. If the payment is deferred, use 1% of the balance as monthly payment amount: ")
        credit_card_debts = userInputFloatNumberValidation("Enter the total amount of all of your credit cards' monthly required minimum payment: ")
        child_support_or_alimony = userInputFloatNumberValidation("Enter any monthly obligated child support or alimony being paid: ")
        subtotal_liab = subject_mortgage + installment_debts + student_loans + credit_card_debts + child_support_or_alimony + other_reo_pitia
        print("Your total monthly debts is: $" + str(subtotal_liab))
        subtotal_liab = float(subtotal_liab)
        return subtotal_liab

def liabilities():
    print("\n   In order to check for your loan qualification, we'll need to know your liabilities (debts) as well. Please answer the following questions.")
    liabilities_total = float(0)
    bankruptcy = userInputTextValidation("\nBefore we proceed into details, did you have any type of bankruptcy or short sale within the past 4 years? (Y/N): ").upper()
    if bankruptcy == 'Y':
        print("\nUnfortunately, if you had any bankruptcy or short sale within the last 4 years, you need to wait until 4 years has passed in order to get mortgage financing.")
        liabilities_total = 0
    elif bankruptcy == 'N':
        foreclosure = input("\nHave you had any foreclosure within the last 7 years? (Y/N): ").upper()
        if foreclosure == 'Y':
            foreclosure_and_bankruptcy = userInputTextValidation("\nWas the mortgage on that foreclosed property discharged through a bankruptcy and 4 years has passed since bankruptcy being discharged? (Y/N): ").upper()
            if foreclosure_and_bankruptcy == 'Y':
                subtotal_liab = calculate_liability()
                liabilities_total += subtotal_liab
            elif foreclosure_and_bankruptcy == 'N':
                print("\nUnfortunately, if you had a foreclosure within the last 7 years, you need to wait until 7 years has passed in order to get mortgage financing.")
        elif foreclosure == 'N': 
            subtotal_liab = calculate_liability()
            liabilities_total += subtotal_liab
    return liabilities_total
        

def loan_qualification(income, liabilities):
    if income == 0.00:
        print("\nSorry you have entered zero income. You are ineligible to proceed with this loan program.")
    else:
        dti = round(float(liabilities/income),2)
        print("\nYour DTI is: " + str(dti*100) + "%")
        if 0.45 <= dti < 0.5:        
            print("""\nCongratulations! Your debt to income (DTI) ratio meets general eligibility requirement for conventional program. 
However, DTI ratio that is greater than 45% may result in ineligible findings for final approval. You may be asked to provide additional assets 
as reserves or pay off additional debts to lower the DTI. """)    
            print("""\n***Disclaimer***
Please be advised that this is a general helpful tool for you to evaluate your financing situation and not an actual approval for loan. 
Mortgage lender may ask for additional requirements and this is different on case by case per inidividuals applying for the loan. """)
        elif 0 < dti < 0.45:
            print("\nCongratulations! Your debt to income (DTI) ratio meets general eligibility requirement for conventional program. You're most likely to get approved for financing! ")
            print("""\n***Disclaimer***\n
Please be advised that this is a general helpful tool for you to evaluate your financing situation and not an actual approval for loan. 
Mortgage lender may ask for additional requirements and this is different on case by case per inidividuals applying for the loan. """)
        elif dti == 0:
            print("\nUnfortunately, due to your significant derogatory credit event (bankruptcy / foreclosure), you're ineligible for financing at this time.")
        elif dti > 0.5:
            print("\nUnfortunately, your DTI is over 50% which is ineligible for financing for conventional mortgage program. Please consider adding a co-applicant or restructure to be within 50% DTI to be eligible.")

while True:

    print("""\n\nMain menu:
      
      1. Calculate mortgage payment

      2. See if you qualify for a mortgage

      3. Current average interest rate

      4. Helpful tips about mortgage

      5. Exit

      """)

    choice = input('Enter your choice: ')
    choice = choice.strip()

    if choice == '1':
        calculation_method = userInputIntegerNumberValidation("\nDo you wish to calculate payment with house in mind (1) or just simple payment calculator (2)?: ")
        calculation_method = str(calculation_method)
        if calculation_method == '1':
            house_price = userInputIntegerNumberValidation("\nEnter the price of the house that you wish to buy: ")      
            down_payment_percentage = userInputFloatNumberValidation("\nHow much do you want to put down in percentage? (ex: 20%, or 15%, etc): ")
            interest_rate = userInputFloatNumberValidation("\nPlease confirm if you want to use current national average rate (1) or if you want to enter your own rate (2):  ")
            if interest_rate == 1:
                mortgage_rate_scrape = requests.get("https://www.bankrate.com/mortgages/mortgage-rates/")
                soup = BeautifulSoup(mortgage_rate_scrape.text, "html.parser")
                national_interest_rate_average = soup.findAll("span", attrs={"class":"text-black font-bold","id":"brPreRateTrendsVisualV2-national-rate"})
                for rate in national_interest_rate_average:
                    interest_rate = float(rate.text[1:5])
                    print("Current national average rate: " + (rate.text[1:]))
            elif interest_rate == 2:
                interest_rate = userInputFloatNumberValidation("Please enter the interest rate: ")
            else:
                print("Please enter either 1 or 2.")
            amortization_term = userInputIntegerNumberValidation("\nHow many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
            fico = userInputIntegerNumberValidation("\nWhat is your estimated FICO (credit) score (three digits ranging from 500-800+)?: ")
            state = input("\nWhich state is the house you're trying to buy located in? (please enter only two letter abbreviated version): ")
            state = state.strip().upper()
            mortgage_calculator_with_house_price(house_price, down_payment_percentage, interest_rate, amortization_term, fico, state)
        elif calculation_method == '2':
            loan_amount = userInputIntegerNumberValidation("\nEnter your loan amount: ")
            interest_rate = userInputFloatNumberValidation("\nPlease confirm if you want to use current national average rate (1) or if you want to enter your own rate (2):  ")
            if interest_rate == 1:
                mortgage_rate_scrape = requests.get("https://www.bankrate.com/mortgages/mortgage-rates/")
                soup = BeautifulSoup(mortgage_rate_scrape.text, "html.parser")
                national_interest_rate_average = soup.findAll("span", attrs={"class":"text-black font-bold","id":"brPreRateTrendsVisualV2-national-rate"})
                for rate in national_interest_rate_average:
                    interest_rate = float(rate.text[1:5])
                    print("Current national average rate: " + (rate.text[1:]))
            elif interest_rate == 2:
                interest_rate = userInputFloatNumberValidation("Please enter the interest rate: ")
            else:
                print("Please enter either 1 or 2.")
            amortization_term = userInputFloatNumberValidation("\nHow many years for loan maturity calculated in months (30 years = 360 months, 15 years = 180 months, etc): ")
            mortgage_calculator(loan_amount, interest_rate, amortization_term)
    elif choice == '2':
        print("\nIn order to help us evaluate your qualification for a conventional mortgage loan program, we'll need to ask you some questions.")
        print("\nPlease answer the following questions: ")
        income_type = userInputTextValidation("\nPlease confirm if you're paid W-2 as a wage earner (A) or if you're self-employed (B), or both (C): ")
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
        mortgage_rate_scrape = requests.get("https://www.bankrate.com/mortgages/mortgage-rates/")
        soup = BeautifulSoup(mortgage_rate_scrape.text, "html.parser")
        national_interest_rate_average = soup.findAll("span", attrs={"class":"text-black font-bold","id":"brPreRateTrendsVisualV2-national-rate"})
        for rate in national_interest_rate_average:
            print("\nCurrent national average rate is: " + (rate.text[1:]))
    elif choice == '4':
        list_of_facts = {1: '\nWhen you are trying to buy a house, it is always helpful to use a mortgage broker to get your mortgage. \nMortgage brokers are most likely to be able to get you the lowest market rate possible. \nThis is possible due to the nature of the brokers are able to negotiate deals with the big lenders. \nGoing directly to your bank may not be the best choice. Think of it as retail vs wholesale.\n',
                         2: '\nTo qualify for a conventional mortgage, debt to income (DTI) ratio must be lower than 50% in order to qualify in general. \nEven if the DTI is lower than 50%, if DTI is over 40%, there are other discreet factors that plays into the approval \nas most lenders will rely on automated underwriting system (AUS) to see if you qualify.\n',
                         3: '\nIn order to lower debt to income (DTI) ratio, there are several ways. You can pay off the credit cards or auto loans. \nIf auto loans have less than 10 payments left, then it can be excluded from being calculated into DTI.\n',
                         4: '\nWhen your FICO is over 760, you are more likely to get better interest rate.\n',
                         5: '\nAuto loan can be excluded from debt to income (DTI) ratio, but lease cannot be excluded even if it has less than 10 payments left. \nThis is because lease is considered a renewing payment obligation. There is a way to exclude it but it requires a hassling documentation requirement. \nIf you want to get lease payment off your DTI, you may want to cancel the lease before applying for the \nloan or have the lease transferred to another family member.\n',
                         6: '\nWhen you have a mortgage or installment debt (auto loan, personal loan, etc), if you are only a co-signer, \nthen you can exclude the payment from your DTI if you can provide 12 months of bank statement \nfrom the primary obligor as well as the copy of the note to verify you are only a co-signor.\n',
                         7: '\nIf you have a history of bankruptcy, you need to wait 4 years before you can get mortgage financing. \nIf you have a history of foreclosure, then the waiting period is 7 years.\n',
                         8: '\nWhen you send bank statements to the lender, please be advised that the lender will be noticing any \nrecurring monthly payments and will confirm if this is a private obligation that is not disclosed. \nIf it is, then it may be counted against your DTI.\n',
                         9: '\nAny large cash deposits into your bank statement will be questioned. \nMost of the time, cash deposits cannot be qualified as an eligible asset and cannot be used towards your down payment. \nYou must ensure these cash deposits have been deposited long time \nbefore financing for it to be a seasoned eligible funds.\n',
                         10: '\nWhen you have large deposits into your bank statements, they will be questioned for documentation \nto verify the asset came from an eligible source. \nGeneral rule for defining large deposit is if the deposit is more than 50% of your gross income, it is considered large deposit.\n'}
        a = [1,2,3,4,5,6,7,8,9,10]
        for i in range(1,11):
            random_integer = randint(1,11)
            while random_integer not in a:
                random_integer = randint(1,11)
            if random_integer in a:          
                print(list_of_facts[random_integer])
                a.remove(random_integer)
            proceed = input("Press enter for next, or press 1 to exit: ")
            if proceed == '1':
                break
    elif choice == '5':
        break
    elif choice != '1' or '2' or '3' or '4' or '5':
        print("\nInput invalid. Please enter a number from 1-5.\n")
            
