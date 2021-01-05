# -*- coding: utf-8 -*-
"""
CREATED BY : ASHI SAHU
LANGUAGE USED : PYTHON 3
DATABASE USED : SQLITE3
DATABASE FILE NAME : Railway.db
"""

import sqlite3
from prettytable import PrettyTable 
import pandas as pd
import datetime
import random
import string


from datetime import date


class User:
    
    def register(self,u,p):
    
        #conn = sqlite3.connect('D:\Internshala\SQLiteStudio\Railway.db')
        #print("Opened database successfully")
        user = (u,p)
        sql = "INSERT INTO USERS (USERNAME,PASSWORD) VALUES (?,?)"
        cur = conn.cursor()
        cur.execute(sql,user)
        conn.commit()
        print("Registration Done ... Sucessfully.... ")
        
        
    def login(self,u,p):
        user = (u,p)
        sql = "SELECT * FROM users WHERE USERNAME = ? AND PASSWORD = ?"
        cur = conn.cursor()
        cur.execute(sql,user)
        data=cur.fetchall()
        #print(data)
        self.login_flag=0
        if (len(data) == 0):
            print("Sorry ...No such user exists ...")
            print(".....OR.....")
            print("Either username or password is incorrect......")
            
            
        elif (len(data) == 1):
            print(".....................................")
            print("Hello ",u)
            self.login_flag=1
            
        return self.login_flag
            
                
                    
                  
                    

            
class Train:
    
    def __init__(self, source , dest,date):
        self.source = source
        self.dest = dest
        self.date=date
    
    def availability(self):
        t = (self.source,self.dest)
        sql="SELECT TRAIN_ID FROM TRAIN WHERE SOURCE = ? AND DESTINATION = ?"
        cur = conn.cursor()
        cur.execute(sql,t)
        data = cur.fetchall()
        train_ids=[]
        train_names=[]
        #print(len(data))
        if (len(data)>0):
            #print(len(data))
            for row in data:
                train_ids.append(row[0])    
            sql1 = "SELECT * FROM SEAT WHERE TRAIN_ID IN (SELECT TRAIN_ID FROM TRAIN WHERE SOURCE = ? AND DESTINATION = ?) and travel_date=?"
            y=(self.source,self.dest,self.date)
            cur.execute(sql1,y)
            data2 = cur.fetchall()
            #print(data2)
            #print(train_ids)
            if (len(data2)==0):
                sql2 = "INSERT INTO seat (train_id,seat_type,amount,count,travel_date) VALUES (?,?,?,?,?)"
                for i in train_ids:  
                    val = (i, 'AC1' ,3000, 20, self.date )
                    cur.execute(sql2, val)
                    val = (i, 'AC2' ,2000, 20, self.date )
                    cur.execute(sql2, val)
                    val= (i, 'AC3' ,1000, 20, self.date)
                    cur.execute(sql2, val)
                    conn.commit()    
                  
    
            S = PrettyTable(["Train_name","Dep","Dep_time", "Arrival","Arrival_time", "AC1","AC2","AC3"])
            for i in train_ids:
                    sql3 = "SELECT * FROM Train WHERE TRAIN_ID =?"
                    cur = conn.cursor()
                    cur.execute(sql3,[i])
                    data3 = cur.fetchall()
                    for row in data3:
                        s=row[1]
                        d=row[2]
                        n=row[3]
                        d_t=row[4]
                        a_t=row[5]
                        train_names.append(n)
                    
                    sql4 = "SELECT * FROM seat WHERE TRAIN_ID =? and travel_date=?"
                    v=(i,self.date)
                    cur = conn.cursor()
                    cur.execute(sql4,v)
                    data4 = cur.fetchall()
                    AC1=data4[0][3]
                    AC2=data4[1][3]
                    AC3=data4[2][3]
                    S.add_row([n,s,d_t,d,a_t,AC1,AC2,AC3])
                    
            print(S)  
            x = PrettyTable(["seat_type","Amount"])
            x.add_row(['AC1',3000])
            x.add_row(['AC2',2000])
            x.add_row(['AC3',1000])
            print(x)    
        return train_names  
        
class Seat_selection():
    
    def __init__(self,ns,train_id,travel_date):
        self.ns = ns
        self.train_id = train_id
        self.travel_date=travel_date
        
        
    def same_seats(self):
        
        st = input("Enter Seat Type (AC1 / AC2 / AC3)")
        cur = conn.cursor()
        cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ? and travel_date=? and train_id=?",('AC1',self.travel_date,self.train_id))
        d1 = cur.fetchall()
        c1 = d1[0][0]
        cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ? and travel_date=? and train_id=?",('AC2',self.travel_date,self.train_id))
        d2 = cur.fetchall()
        c2 = d2[0][0]
        cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ? and travel_date=? and train_id=?",("AC3",self.travel_date,self.train_id))
        d3 = cur.fetchall()
        c3 = d3[0][0]
        
        #print(c1,c2,c3)
        #print(ns)
        
        
        for n in range(0,self.ns):
            
            #print(n)
            cur = conn.cursor()
            
            #print(st)
            #print(type(st))
            #print(st in 'AC1')
            
            if st in 'AC1':
                u = ('AC1',self.train_id,self.travel_date)
                
                cur = conn.cursor()
                cur.execute("UPDATE SEAT SET COUNT = COUNT-1 WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",u)
                #cur.execute("SELECT AMOUNT FROM SEAT WHERE SEAT_TYPE = ? AND TRAIN_ID = ?",(st,self.train_id))
                #data = cur.fetchall()
                #amt = data[0][0]
                cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",(st,self.train_id,self.travel_date))
                data = cur.fetchall()
                print(data[0][0])
                conn.commit()
                
                
            if st == "AC2":
                u = ('AC2',self.train_id,self.travel_date)
                cur.execute("UPDATE SEAT SET COUNT = COUNT-1 WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",u)
                conn.commit()
                
                
            if st == "AC3":
                cur.execute("UPDATE SEAT SET COUNT = COUNT-1 WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",('AC3',self.train_id,self.travel_date))
                conn.commit()
                
        return st
        
        
    def diff_seats(self):
        
        stt = []
        
        for n in range(self.ns):
            st = input("Enter "+str(n+1)+" Seat Type (AC1 / AC2 / AC3) :")
            cur = conn.cursor()
            cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ?and TRAIN_ID = ? and travel_date=? ",('AC1',self.train_id,self.travel_date))
            d1 = cur.fetchall()
            c1 = d1[0][0]
            cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ? and TRAIN_ID = ? and travel_date=?",('AC2',self.train_id,self.travel_date))
            d2 = cur.fetchall()
            c2 = d2[0][0]
            cur.execute("SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ?and TRAIN_ID = ? and travel_date=?",('AC3',self.train_id,self.travel_date))
            d3 = cur.fetchall()
            c3 = d3[0][0]
            
            cur = conn.cursor()
            if st in 'AC1':
                u = (c1-1,'AC1',self.train_id,self.travel_date)
                            
                cur = conn.cursor()
                cur.execute("UPDATE SEAT SET COUNT = ? WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",u)
                conn.commit()
                stt.append(st)
                #print("Done")
                
            if st == "AC2":
                u = (c2-1,'AC2',self.train_id,self.travel_date)
                cur.execute("UPDATE SEAT SET COUNT = ? WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",u)
                conn.commit()
                stt.append(st)
                
            if st == "AC3":
                cur.execute("UPDATE SEAT SET COUNT = ? WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=? ",(c3-1,'AC3',self.train_id,self.travel_date))
                conn.commit()
                stt.append(st)
                
        return stt
                 
            
class Payment():
    
    def __init__(self,amt = 0):
        
        self.amt = amt
    
    def  Amount(self,st,train_id):
        
        sql = "SELECT AMOUNT FROM SEAT WHERE SEAT_TYPE = ? AND TRAIN_ID = ?"
        cur = conn.cursor()
        cur.execute(sql,(st,train_id))
        
        data = cur.fetchall()
        
        self.amt = data[0][0]
        
        return self.amt
    
        
    
class Passenger():
    
    def __init__(self,count):
        self.count= count
        
    
    def set_passenger_details(self): 
        df_details=pd.DataFrame()
        p_name=[]
        p_age=[]
        p_gender=[]
        for i in range(0,self.count):
            n=input("name of the passenger: " )
            a=input("age of the passenger: ")
            f=0
            while(f==0):
                print("Select gender:")
                print("1. Male")
                print("2. Female")
                g=int(input("Select any one: "))
                if(g<0 or g>2):
                    print("choose either 1 or 2")
                else:
                    f=1
            p_name.append(n)
            p_age.append(a)
            
            if g == 1:
                p_gender.append("Male")
                
            else :
                p_gender.append("Female")
            
        df_details['name']=p_name
        df_details['age']=p_age
        df_details['gender']=p_gender    
        
        #print(df_details)
        sql = "INSERT INTO PASSENGER (USERNAME,NAME,AGE,GENDER,BOOKING_DATE) VALUES (?,?,?,?,?)"
        #--------------------------------------------------------------
        #print(df_details)
        try :
            for pde in df_details.values:
                cur = conn.cursor()
                #print(pde)
                #print(self.user,pde[0],pde[1],pde[2],self.booking_date)
                cur.execute(sql,(self.user,pde[0],pde[1],pde[2],self.booking_date))
                conn.commit()
                print("Passenger Details Added successfully .......")
                print()

        except :
            print("Invalid details ....")

    
        
                
        
class Ticket(Train,Seat_selection,Passenger,Payment):
    
    def __init__(self,user):
        self.user=user
    
    def book_ticket(self):
        
        #print('enters')
        source = input("Enter Source : ")
        dest = input("Enter Destination : ")
        d_flag=1
        while(d_flag):
            date=input("Enter Date in DD/MM/YYYY: ")  
            f=0
            try:    
                d3=datetime.datetime.strptime(date,"%d/%m/%Y")
                f=1
            except:
                print("Incorrect data format") 
            if (f==1):
                present=datetime.datetime.today()
                today=present.strftime("%d/%m/%Y")
                self.booking_date=today
                d1=date.split('/')
                d2=today.split('/')
                validDate=1
                #checking the date is previous date or not.
                if(d1[2]<d2[2]): 
                    print("Date should not be previous date.")
                    validDate=0
                elif(d1[2] == d2[2]):    
                    if(d1[1]<d2[1]):
                        print("Date should not be previous date.")
                        validDate=0
                    else:
                        if(d1[1] == d2[1]):
                              if(d1[0]<d2[0]):
                                print("Date should not be previous date.")
                                validDate=0
                if(validDate==1):
                    date_t=0
                    if(d1[0]==d2[0]  and d1[1]==d2[1] and d1[2]==d2[2]):
                        date_t=1          
                    isValid=True 
                    d_flag=0
            
            # if the date format is correct and the date is not a previous date then display the trains
            # and available seats.        
        if(isValid==True and validDate == 1):
            self.travel_date=date
            Train.__init__(self,source,dest,self.travel_date)
            train_names=Train.availability(self)
            if (len(train_names)==0):
                print("Sorry!!!!!! No train available.")
            else:
                print("enter the train name you want to travel with:")
                for name in train_names:
                        print(name)
                train_name=input("input the train name:")
                cur = conn.cursor()
                cur.execute("SELECT train_id from train WHERE name=?",[train_name])
                trainData = cur.fetchall()
                self.train_id=trainData[0][0]
                flag=0
                while(flag==0):
                    #Number of seats to be booked
                    self.ns = int(input("Enter Number of seats to be booked between 1 to 5 : "))
                    if(self.ns<1 or self.ns>5):
                        print("Cannot take passenger count less than 1 or more than 5.")   
                    else:
                        flag=1

                #Seat_selection.__init__(self,ns,train_id)
                ss1 = Seat_selection(self.ns,self.train_id,self.travel_date)

                #Seat Selection for booking 
                if self.ns == 1:
                    self.info = 'S'

                else:
                    self.info = input("Type of Seats to be booked are Same or Different ? (S = Same / D = Different) ")

                if self.info in 'S':

                    #update number of seats in seat table
                    self.st = ss1.same_seats()
                    #Taking Passenger Details

                elif self.info in 'D':
                    self.stt = ss1.diff_seats()
                    #Taking Passenger details 
                    
                else:
                    print("Invalid Type ....")

                #--------------------------------------------------------------
                #Enter Passenger Details
                Passenger.__init__(self,self.ns)
                Passenger.set_passenger_details(self)
                
                #----------------------------------------------------
                #Payment
                self.total = 0
                print("..........................................................")
                if self.info in "S":
                    for n in range(self.ns):
                        self.total += Payment.Amount(self,self.st,self.train_id)

                else:
                    for st1 in self.stt:
                        self.total += Payment.Amount(self,st1, self.train_id)

                print("Total Amount to be paid : ",self.total)
                print(".............................................................") 
                
            
            #--------------------------------------------------------------
            #Confirmation done using confirm_ticket()
                
            self.confirm_ticket()

    def cancel_ticket(self,PNR,TID):
        
        #add the count to respective seat_type
        #takes PNR and TID as input  
        sql = "SELECT * FROM PAYMENT WHERE PNR = ? AND TID = ?"
        cur = conn.cursor()
        cur.execute(sql,(PNR,TID))
        
        data = cur.fetchall()
        #print(data)
        t_date = date.today()
        
        d1, m1, y1 = [int(x) for x in data[0][7].split('/')]
        
        travel_date = date(y1,m1,d1)
        

        if t_date < travel_date:
            
            sql2 = "SELECT AC1 FROM PNR_DETAILS WHERE PNR = ? AND TID = ?"
            cur.execute(sql2,(PNR,TID))
            data1 = cur.fetchall()
            ac1 = data1[0][0]
            
            sql3 = "SELECT AC2 FROM PNR_DETAILS WHERE PNR = ? AND TID = ?"
            cur.execute(sql3,(PNR,TID))
            data2 = cur.fetchall()
            ac2 = data2[0][0]
            
            sql4 = "SELECT AC3 FROM PNR_DETAILS WHERE PNR = ? AND TID = ?"
            cur.execute(sql4,(PNR,TID))
            data3 = cur.fetchall()
            ac3 = data3[0][0]
            
            #print(ac1,ac2,ac3) 
            
            sql5 = "SELECT TRAIN_ID FROM PNR_DETAILS WHERE PNR = ? AND TID = ?"
            cur.execute(sql5,(PNR,TID))
            data3 = cur.fetchall()
            self.train_id = data3[0][0]
            
            #print(data3)
            
            sql5 = "SELECT TRAVEL_DATE FROM PNR_DETAILS WHERE PNR = ? AND TID = ?"
            cur.execute(sql5,(PNR,TID))
            data3 = cur.fetchall()
            self.travel_date = data3[0][0]
            
            #print(data3)
            
        
            sql = "SELECT COUNT FROM SEAT WHERE SEAT_TYPE = ? AND TRAIN_ID = ? AND TRAVEL_DATE = ?"
            cur.execute(sql,('AC1',self.train_id,self.travel_date))
            data = cur.fetchall()
            #print(data)
            p_ac1 = data[0][0]
            
            cur.execute(sql,('AC2',self.train_id,self.travel_date))
            data = cur.fetchall()
            p_ac2 = data[0][0]
            
            cur.execute(sql,('AC3',self.train_id,self.travel_date))
            data = cur.fetchall()
            p_ac3 = data[0][0]
            
            sql = "UPDATE SEAT SET COUNT = ? WHERE SEAT_TYPE = ? AND TRAIN_ID = ? AND TRAVEL_DATE = ?"
            
            cur.execute(sql,(ac1+p_ac1,'AC1',self.train_id,self.travel_date))
            conn.commit()
            
            #sql = "UPDATE SEAT SET COUNT = ? WHERE SEAT_TYPE = ? AND TRAIN_ID = ? AND TRAVEL_DATE = ?"
            cur.execute(sql,(ac2+p_ac2,'AC2',self.train_id,self.travel_date))
            conn.commit()
            
            #sql = "UPDATE SEAT SET COUNT = ? WHERE SEAT_TYPE = ? AND TRAIN_ID = ? AND TRAVEL_DATE = ?"
            cur.execute(sql,(ac3+p_ac3,'AC3',self.train_id,self.travel_date))
            conn.commit()
            
            #-------------------------------------
            sql = "UPDATE PNR_DETAILS SET STATUS = 'CANCELLED' WHERE PNR = ? AND TID = ?"
            cur.execute(sql,(PNR,TID))
            conn.commit()
            
            sql = "UPDATE PAYMENT SET SERVICE_TYPE = 'cancel' WHERE TID =? AND PNR = ?"
            cur.execute(sql,(TID,PNR))
            conn.commit()
            
            print("Ticket Cancellation done Successfully ............")
            
        else:
            print("Can't cancel ... Ticket expires ....")
        
        
    def confirm_ticket(self):
        
        #returns the total amount using Payment class
        #--------------------------------------------------------------
        #Confirmation 
        c = input("Do you want to confirm Booking ? (Y/N) ")
        
        if c in "Y" and (self.info in "S" or self.info in "D"):
            #conn.commit()
            '''
            sql2 = "SELECT * FROM SEAT WHERE TRAIN_ID = ?"
            cur = conn.cursor()
            cur.execute(sql2,(self.train_id,))
            data = cur.fetchall()
            
            S = PrettyTable(["Seat_Type", "Amount", "Number of Seats Available"])
            
            for row in data:
                S.add_row([row[0],row[1],row[2]])
                
            print(S)
            
            '''
           
            #====================================================================
            #PNR GENERATION AND TRANSACTION ID GENERATION CODE .....
            
            pno=''.join(random.choices(string.digits, k=5))
            self.pnrNo="PNR"+pno
            
            tno=''.join(random.choices(string.digits, k=4))
            self.tid="T"+tno
            
            #==============================================================
            #UPDATE PAYMENT TABLE
            sql = "INSERT INTO PAYMENT (TID,USERNAME,TOTAL,SERVICE_TYPE,PNR,SERVICE_DATE,PCount,TRAVEL_DATE) VALUES (?,?,?,?,?,?,?,?)"
            cur=conn.cursor()
            cur.execute(sql,(self.tid,self.user,self.total,'book',self.pnrNo,self.booking_date,self.ns,self.travel_date))
            conn.commit()
            #============================================================
            #UPDATE PNR-DETAILS
            
            if self.info in "S":
                
                sql = "INSERT INTO PNR_DETAILS (PNR,TID,AC1,AC2,AC3,PCount,TRAVEL_DATE,BOOKING_DATE,STATUS,TRAIN_ID) VALUES (?,?,?,?,?,?,?,?,?,?)"
                if self.st in 'AC1':
                    cur.execute(sql,(self.pnrNo,self.tid,self.ns,0,0,self.ns,self.travel_date,self.booking_date,'CONFIRMED',self.train_id))
                    conn.commit()
                    
                if self.st in 'AC2':
                    cur.execute(sql,(self.pnrNo,self.tid,0,self.ns,0,self.ns,self.travel_date,self.booking_date,'CONFIRMED',self.train_id))
                    conn.commit()
                    
                if self.st in 'AC3':
                    cur.execute(sql,(self.pnrNo,self.tid,0,0,self.ns,self.ns,self.travel_date,self.booking_date,'CONFIRMED',self.train_id))
                    conn.commit()
            else :
                
                sql = "INSERT INTO PNR_DETAILS (PNR,TID,AC1,AC2,AC3,PCount,TRAVEL_DATE,BOOKING_DATE,STATUS,TRAIN_ID) VALUES (?,?,?,?,?,?,?,?,?,?)"
                freq = {'AC1':0,'AC2':0,'AC3':0}
                
                for st1 in self.stt:
                    if st1 not in freq:
                        freq[st1] = 1
                        
                    else:
                        freq[st1] += 1
                        
                cur.execute(sql,(self.pnrNo,self.tid,freq['AC1'],freq['AC2'],freq['AC3'],len(self.stt),self.travel_date,self.booking_date,'CONFIRMED',self.train_id))
                conn.commit()
                
            print('-------------------------------------')
            print("Your transaction ID is: ",self.tid)
            print('-------------------------------------')
            
            
            self.print_ticket()
            
            
            #PRINT TRANSACTION ID AND PNR NUMBER
        elif c in "N" and (self.info in "S"):
            for n in range(self.ns):
                #print(n)
                cur = conn.cursor()
                cur.execute("UPDATE SEAT SET COUNT = COUNT+1 WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",(self.st,self.train_id,self.travel_date))
                conn.commit()
                
            '''
            sql2 = "SELECT * FROM SEAT WHERE TRAIN_ID = ?"
            cur = conn.cursor()
            cur.execute(sql2,(self.train_id,))
            data = cur.fetchall()
            
            S = PrettyTable(["Seat_Type", "Amount", "Number of Seats Available"])
            
            for row in data:
                S.add_row([row[0],row[1],row[2]])
                
            print(S)
            '''
            
            print(".....Thank you....")
            
        elif c in "N" and (self.info in "D"):
            for st1 in self.stt:
                cur = conn.cursor()
                cur.execute("UPDATE SEAT SET COUNT = COUNT+1 WHERE SEAT_TYPE = ? AND TRAIN_ID = ? and travel_date=?",(st1,self.train_id,self.travel_date))
                conn.commit()
            '''
            sql2 = "SELECT * FROM SEAT WHERE TRAIN_ID = ?"
            cur = conn.cursor()
            cur.execute(sql2,(self.train_id,))
            data = cur.fetchall()
            
            S = PrettyTable(["Seat_Type", "Amount", "Number of Seats Available"])
            
            for row in data:
                S.add_row([row[0],row[1],row[2]])
                
            print(S)
            '''
            
            
        else:
            print("Invalid response .... TRY AGAIN BY LOGGING IN")
        
        
        
    
    def enquiry_ticket(self,PNR,TID):
        
        sql = "SELECT STATUS FROM PNR_DETAILS WHERE PNR = ? AND TID = ?"
        cur = conn.cursor()
        cur.execute(sql,(PNR,TID))
        
        data = cur.fetchall()
        
        P = PrettyTable(["PNR NUMBER","STATUS"])
        P.add_row([PNR,data[0][0]])
        print(P)
        
    def print_ticket(self):
        sql = "SELECT PCOUNT FROM PNR_DETAILS WHERE PNR = ?"
        cur = conn.cursor()
        cur.execute(sql,(self.pnrNo,))
        
        data = cur.fetchall()
        p_count = data[0][0] 
        print("--------------------------------------------------------------")
        print("PNR number: ",self.pnrNo,"           Booking date: ",self.booking_date)
        print("Date of travel: ",self.travel_date)
        print("Number of Passengers : ",p_count)
        print("                                           Status:","CONFIRMED")
        print("--------------------------------------------------------------")
        
        
class History:
    
    def __init__(self,user):
        
        self.user = user
        
    def transaction(self):
        
        sql = "SELECT * FROM PAYMENT WHERE USERNAME = ?"
        
        cur = conn.cursor()
        cur.execute(sql,(self.user,))
        
        data = cur.fetchall()
        #print(data)
        for row in data:
            
            print("TID :",row[0])
            print("Total : ",row[2])
            print("Service Type : ",row[3])
            print("PNR Number : ",row[4])
            print("Service Date : ",row[5])
            print("Passenger count : ",row[6])
            print("Travel Date : ",row[7])
            
            print("------------------------------------------")
        

        
if __name__ == "__main__":
    
    #in connect insert the path of your .db file
    conn = sqlite3.connect('D:\Internshala\SQLiteStudio\Railway.db')
    print("Opened database successfully")
    print("..................RAILWAY RESERVATION SYSTEM.......................")
    print("1. LOGIN")
    print("2. REGISTER")
    su = int(input("Select any one..... "))
    
    u1 = User()
    
    if (su == 1):
        u = input("Enter username : ")
        p = int(input("Enter password : "))
        flag=u1.login(u,p) 
        if (flag==1):
            print("......................................")
            print("..............SERVICES......................")
            print("1. BOOK")
            print("2. CANCEL")
            print("3. ENQUIRY")
            print("4. History")
            
            s = int(input("Select any one..... "))
            tkt = Ticket(u)
            if (s==1):
                print("...............BOOK...................")
                #print(u)
                tkt.book_ticket()
                #tkt.print_ticket()
            elif (s==2):
                print("...............CANCEL...................")
                PNR = input("Enter PNR Number of ticket : ")
                TID = input("Enter Transaction ID : ")
                tkt.cancel_ticket(PNR,TID) 
            elif(s==3):
                 print("...............ENQUIRY...................")
                 PNR = input("Enter PNR Number of ticket : ")
                 TID = input("Enter Transaction ID : ")
                 tkt.enquiry_ticket(PNR,TID)
                 
            elif (s==4) :
                print(".............HISTORY..................")
                h1 = History(u)
                h1.transaction()
            else:
                print("invalid choice!!!!")
        
    elif(su == 2):
        u = input("Enter username : ")
        p = int(input("Enter password : "))
        u1.register(u, p)

    else :
        print("Invalid Choice.....") 
        
    #closing the connection from sqlite3 database otherwise Database down error will appear 
    conn.close()


