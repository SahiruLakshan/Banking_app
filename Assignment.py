import os
import time
import mysql.connector
from datetime import datetime
import re


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS bank_app")
mycursor.execute('use bank_app')

mycursor.execute("CREATE TABLE IF NOT EXISTS customer_details (customer_name VARCHAR(255), account_number VARCHAR(255),dw_update DOUBLE DEFAULT 0,interest FLOAT DEFAULT 0, total DOUBLE DEFAULT 0)")

file = open('transaction.txt', 'a')



def deposit():                  #Deposit Cash Section
   ac = "SELECT account_number FROM customer_details"
   mycursor.execute(ac)
   account_number = mycursor.fetchall()

   if account_number != []:
      os.system('cls')
      customer = "SELECT * FROM customer_details"
      mycursor.execute(customer)
      result2 = mycursor.fetchall()
      print("\t\t\tDeposit Cash Section\n\n")
      try:
        deposit_cash = float(input("Enter Deposit Cash:"))
        if deposit_cash < 0:
           print("")
           return "Minus Numbers are not valid"
      except:
        print("")
        return "Invalid Input"

      for row2 in result2:
            
            tot = float(row2[4])+deposit_cash
            query = """UPDATE customer_details SET dw_update=%s,total=%s WHERE customer_name=%s"""
            tuple1 = (deposit_cash,float(tot),row2[0])
            mycursor.execute(query,tuple1)
           
      file.write("Rs.{0:.2f}" .format(deposit_cash)+" Deposit Cash - Date and Time-"+str(datetime.today()))
      file.write("\n")
      print("")
      return "Cash Deposit Success.Your Current Account Balance is Rs:{0:.2f}".format(tot)

   else:
      print("")
      return "You didn't Register this app.Please Register First.."
      

def deposit_interest():
   if datetime.today().day == 30 or datetime.today().strftime("%m/%d") == '02/28':      #Calculate interest of deposits at end of month
          customers = "SELECT * FROM customer_details"
          mycursor.execute(customers)
          result2 = mycursor.fetchall()
          for x in result2:
             interest = x[4]*2/100
             total = interest + x[4]
             update = """UPDATE customer_details SET interest=%s,total=%s WHERE customer_name=%s"""
             tuple = (interest,total,x[0])
             mycursor.execute(update,tuple)


def withdraw():                                             #Withdraw Section
   ac = "SELECT account_number FROM customer_details"
   mycursor.execute(ac)
   account_number = mycursor.fetchall()
   if account_number != []:
      customer = "SELECT * FROM customer_details"
      mycursor.execute(customer)
      result2 = mycursor.fetchall()
      os.system('cls')
      print("\t\t\tWithdraw Cash Section\n\n")
      try:
         withdraw_cash =float(input("Enter Withdraw Cash:"))
         if withdraw_cash < 0:
            print("")
            return "Minus Numbers are not valid"
      except:
         print("")
         return "Invalid Input"
      dbtotal = "SELECT total FROM customer_details"
      mycursor.execute(dbtotal)
      i = mycursor.fetchall()
      x = i[0]
      total = float('.'.join(str(elem) for elem in x))
      if withdraw_cash < total:
            if total > 1000 and total - withdraw_cash>=1000:
               for row2 in result2:
                  total = row2[4]
                  tot = float(row2[4])-withdraw_cash
                  query = """UPDATE customer_details SET dw_update=%s,total=%s WHERE customer_name=%s"""
                  tuple1 = (withdraw_cash,tot,row2[0])
                  mycursor.execute(query,tuple1)
                 
               file.write("Rs.{0:.2f}" .format(withdraw_cash)+" Withdraw Cash - Date and Time-"+str(datetime.today()))
               file.write("\n")
               file.close()
               new_tot = "SELECT total FROM customer_details"
               mycursor.execute(new_tot)
               i = mycursor.fetchall()
               x = i[0]
               new_total = float('.'.join(str(elem) for elem in x))
               print("")
               return "Cash Withdraw Success.Your Current Account Balance is Rs:{0:.2f}".format(new_total)
            else:
               os.system('cls')
               return "Sorry!You can't withdraw cash from your account now.Because Rs. 1000.00 should be left in your account."     
      else:
            os.system('cls')
            return "Sorry!You You don't have enough money to withdraw."
   else:
      print("")
      return "You didn't Register this app.Please Register First.."
      
      
     

def create():                      #Registration
   os.system('cls')
   print("\t\t\tRegistration Section\n\n")
   ac = "SELECT account_number FROM customer_details"
   mycursor.execute(ac)
   account_number = mycursor.fetchall()    

   if account_number==[]:        #Check availability of account
      
      
      name = input("Enter Name:")
      num = input("Enter your Account Number:")

      
      
      if(name!='' and num!=''):
         if re.search('[0-9]',name) or re.search('[a-zA-Z]', num):
           print("")
           return "Name or Account Number is Not Valid"
         else:
            mycursor.execute("INSERT INTO customer_details (customer_name, account_number,total) VALUES(%s, %s, %s)", (name,num,'1000'))
            print("")
            return "Account Create and Registration Success!"
      else:
            print("")
            return "Registartion is not Completed.Name or Account Number Missing!Check again."
   else:
      print("")
      return "You already have an account!"
    

def loan():                               #Loan Calculation
   os.system('cls')
   print("\t\t\tLoan Calculator")
   print("")
   print("Loan Schemes\n")
   print("3 (36 Months) Years Scheme - 10% Interest\n5 (60 Months) Years Scheme - 15% Interest\n7 (84 Months) Years Scheme - 20% Interest\nMore than 7 (More than 84 Months)Years Scheme - 25% Interest")
   print("")

   try:
      amount = float(input("Enter Capital Amount:"))
      if amount < 0:
         print("")
         return "Minus Numbers are not valid"
   except:
      print("")
      return "Invalid Input"
   
   try:
      months = int(input("Enter Number of Months:(36,60,84 etc.):"))
      if months < 0:
         print("")
         return "Minus Numbers are not valid"
      
   except:
      print("")
      return "Invalid Input"
   
   if months == 36:
      rate = (10/100)/12
    
   elif months == 60:
      rate = (15/100)/12
      
   elif months == 84:
      rate = (20/100)/12
   
   elif months>84:
      rate = (25/100)/12

   else:
      print("")
      return "Sorry!We don't have any loan scheme that you enterd."
      
   monthly_repay = (rate*amount*((1+rate)**months))/((1+rate)**months-1)
   print("")
   return "Monthly Repayment: Rs. {0:.2f}".format(monthly_repay)


def balance():                                           #Balance Check Section
   ac = "SELECT account_number FROM customer_details"
   mycursor.execute(ac)
   account_number = mycursor.fetchall()
   if account_number != []:
         customer = "SELECT * FROM customer_details"
         mycursor.execute(customer)
         result2 = mycursor.fetchall()
         os.system('cls')
         print("Your Account Balance-")
         print("=====================")
         for row in result2:
            print("Name: ", row[0])
            print("Account_Number: ", row[1])
            print("Interest: ", row[3])
            balance = row[4]
         return "Your Current Balance is Rs.{0:.2f}".format(balance)
   
   else:
      print("")
      return "You didn't Register this app.Please Register First.."
      
      


def option():          #Option Section
   os.system('cls')
   print("Choose one")
   print("1.Deposit Cash")
   print("2.Withdraw Cash")
   print("3.Check Account Balance")
   print("4.Register in App")
   print("5.Loan Calculate")
   print("6.Exit")
   
   x = int(input("Enter an option Number:"))

   if x==1:
      print("")
      output = deposit()
      print(output)
      time.sleep(2)

   elif x==2:
      print("")
      output = withdraw()
      print(output)
      time.sleep(2)
   
   elif x==3:
      print("")
      output = balance()
      print(output)
     
   elif x==4:
      output = create()
      print(output)
      time.sleep(2)

   elif x==5:
      output = loan()
      print(output)
      
   
   elif x==6:
      os.system('cls')
      print("\n\n\n\n\t\t\tYou are exit.Thank You!")
      time.sleep(2)
      exit()

   else:
      print("\n\n\n\n\t\t\tNot a Valid Option number!")
      time.sleep(2)
      option()
      
   deposit_interest()


if __name__ == "__main__":
    option()


mydb.commit()