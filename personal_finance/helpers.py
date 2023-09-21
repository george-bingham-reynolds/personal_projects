import pandas as pd
import numpy as np

class taxed_account():
    def __init__(self, takehome, taxed, cap_gain):
        ''' A custom class meant for personal financial data storage. Takehome is how much a person keeps, cap_gain is how much money put in grew, and taxed is how much they pay in tax on this growth.'''

        self.takehome = takehome
        self.taxed = taxed
        self.cap_gain = cap_gain

class pre_tax():
    def investment_growth(self, principal, time, percent = 0.1015):
        '''A function designed to estimate how much money currently in the market can be expected to grow. Variables as follows:
        principal - the amount in the markets
        time - the amount of time it is allowed to grow
        percent - expected annual growth; by default this is set to the historical average return for the S&P 500 cited here: https://www.investopedia.com/ask/answers/042415/what-average-annual-return-sp-500.asp'''
        
        grows_to = principal * ((1 + percent) ** time) #SIMPLE COMPOUNDING GROWTH
        return round(grows_to, 2)
    
    def recurring_investment(self, amt, time, percent = 0.1015):
        '''The iterative ancestor of investment_growth().pre_tax - it sums a list of values defined by the pre_tax function with recurring investment amount as principal,
          one example for each year 0 to time input.'''
        
        every_val = []
        for i in range(time):

            #EACH YEAR SUBTRACT i TIME FOR YEARS OF REMAINING GROWTH, ADD COMPOUNDING FINAL VAL TO LIST
            every_val.append(pre_tax().investment_growth(amt, time - i, percent))
        total_amount = sum(every_val) #AND COMBINE ALL VALUES
        return round(total_amount, 2)
    
class post_tax():
    def investment_growth(self, principal, time, percent = 0.1015, bracket = 0.2):
        '''Similar to the pre_tax function, this finds the pre-tax total, defines cap gains as pre-tax growth total minus principal, taxed as tax rate * cap gain and takehome as pre-tax minus taxed. 
        Tax rate is define by bracket input, set by default to the maximum cited here: https://www.investopedia.com/terms/c/capital_gains_tax.asp'''

        grows_to = grows_to = principal * ((1 + percent) ** time) #SAME COMPOUNDING GROWTH
        cap_gain = grows_to - principal #HOW MUCH WAS INVESTMENT PROFIT?
        taxed = cap_gain * bracket #WHAT DO YOU PAY IN TAX?
        takehome = grows_to - taxed #LEAVING YOU WITH
        acct = taxed_account(takehome = round(takehome, 2), taxed = round(taxed, 2), cap_gain = round(cap_gain, 2)) #CONSOLIDATE TO CUSTOM CLASS
        return acct
    
    def recurring_investment(self, amt, time, percent = 0.1015, bracket = 0.2):
        '''The iterative ancestor of investment_growth().post_tax. See this function for explanation of equations and recurring_investment().pre_tax for iterative explanation.'''

        every_val = [] #EMPTY LIST FOR EACH YEAR
        for i in range(time):

            #EACH YEAR SUBTRACT i FROM TIME FOR NUMBER OF YEARS REMAINING FOR GROWTH, APPEND GROWTH OUTPUT
            every_val.append(pre_tax().investment_growth(amt, time - i, percent))
        total_amount = sum(every_val) 
        total_invested = amt * time #TOTAL PRINCIPAL
        cap_gain = total_amount - total_invested #HOW MUCH OF FINAL WAS GROWTH
        taxed = cap_gain * bracket #AMOUNT TAXED
        takehome = total_amount - taxed #LEAVING YOU WITH
        acct = taxed_account(takehome = round(takehome, 2), taxed = round(taxed, 2), cap_gain = round(cap_gain, 2)) #CONSOLIDATE
        return acct
    