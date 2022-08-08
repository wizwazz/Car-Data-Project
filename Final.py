#Program created by Wazir Hamed
#12/04/2020
import tkinter as tk
import sqlite3,os


#Setting up the database
#It will contain 4 tables
if not os.path.isfile("Garage.db"):
    db = sqlite3.connect("Garage.db")
    curs = db.cursor()
    #Creates a table for workers
    curs.execute('''CREATE TABLE Workers
    (WorkerID integer PRIMARY KEY,
    First_Name text,
    Last_Name text,
    Role text,
    Password text)
    ''')
    #Creates a table for vehicle's
    curs.execute('''CREATE TABLE Vehicles
    (Number_Plate text PRIMARY KEY,
    Year integer,
    Make text,
    Model text,
    Colour text)
    ''')
    #Creates a table for vehicle's faults
    curs.execute('''CREATE TABLE Faults
    (Number_Plate text,
    Fault text,
    Serious text,
    Location text,
    Fixed text,
    ID integer PRIMARY KEY)
    ''')
    #Creates a table for Bills
    curs.execute('''CREATE TABLE Bills
    (Invoice integer PRIMARY KEY,
    Number_Plate integer,
    Amount real,
    Amount_Paid real)
    ''')
    #Creates a table for Customers
    curs.execute('''CREATE TABLE Customer
    (CustomerID integer PRIMARY KEY,
    First_Name text,
    Last_Name text,
    Phone_Number integer)
    ''')
    #Creates a table for Customer and Bills
    curs.execute('''CREATE TABLE Customer_Bills
    (Invoice integer,
    CustomerID ineger)
    ''')
    db.commit()
    curs.execute('''INSERT INTO Workers(WorkerID,First_Name,Last_Name,Role,Password) VALUES("1000000","Admin","Admin","Manager","admin")''')
    db.commit()
    db.close()
    
#Setup
#Sets up all the pages
class setup(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        window = tk.Frame(self)
        self.frames = {}
        window.grid()
        #This gets every class and makes it a Frame with the window and puts the widgets inside it when called.
        for i in (Login,MenuW,MenuM,AddW,SearchW,FaultyAddW,MenuA,FaultySearchW,AddAccounts,SearchAccounts,UpdateAccounts,Register):#All the different pages
            frame = i(window,self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.resizable(width = False, height = False)
            self.geometry("500x300")
        #First Page the user will see
        self.show(Login)
    def show(self, controller): 
        frame = self.frames[controller]
        frame.tkraise()


#Login Page
class Login(tk.Frame):
    #Checks if the workerID and password match with any in the program
    def login_button(self,user,pasw,hidden,controller):
        hidden.config(text="\n")
        base = sqlite3.connect("Garage.db")
        c = base.cursor()
        c.execute('''SELECT WorkerID, Password FROM Workers WHERE WorkerID=? AND Password=?''',(user.get(),pasw.get(),))
        results = c.fetchone()
        if results:
            c.execute('''SELECT Role FROM Workers WHERE WorkerID=?''',(user.get(),))
            get = c.fetchone()
            role = get[0]
            if role == "Worker":
                controller.show(MenuW)
            elif role == "Manager":
                controller.show(MenuM)
            elif role == "Accountant":
                controller.show(MenuA)
        else:
            hidden.config(text="Username/Password \nInvalid")
        user.delete(first=0,last=22)
        pasw.delete(first=0,last=22)
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #All the widegets in the program
        title = tk.Label(self, text="Login")
        title.config(font=("Courier", 20))
        user = tk.Label(self, text="Username:")
        pasw = tk.Label(self, text="Password:")
        usertext = tk.Entry(self, width=15)
        paswtext = tk.Entry(self, show="*", width=15)
        Move = tk.Button(self, text = "Login", width=15,
                         command=lambda: self.login_button(usertext, paswtext,hidden,controller))
        hidden = tk.Label(self, text="\n")

        #Positioning all widgets
        title.grid(pady=10,padx=10)
        user.grid(column=0, row=1)
        pasw.grid(column=0, row=2)
        paswtext.grid(column=1, row=2)
        usertext.grid(column=1, row=1)
        hidden.grid(column=1, row=3)
        Move.grid(column=1, row=4)




#Worker View
#This is workers Menu And all that they can see       
class MenuW(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #All the widegets in the program
        title = tk.Label(self, text="Worker Menu")
        title.config(font=("Courier", 20))
        logout = tk.Button(self, text="Logout", width=15, command=lambda: controller.show(Login))
        Add = tk.Button(self, text="New Vehicle",
                           command=lambda: controller.show(AddW),width = 15)
        Search = tk.Button(self, text="Search Vehicle",
                           command=lambda: controller.show(SearchW),width = 15)
        Faultys = tk.Button(self, text="Faults Search",
                           command=lambda: controller.show(FaultySearchW),width = 15)
        Faultya = tk.Button(self, text="Faults Add",
                            command=lambda: controller.show(FaultyAddW),width = 15)

        #Positioning all widgets
        title.grid(pady=10,padx=108)
        logout.grid(row=0,column=1, sticky = "NE")
        Add.grid(row=1,pady=10,padx=10)
        Faultya.grid(row=2,pady=10,padx=10)
        Search.grid(row=3,pady=10,padx=10)
        Faultys.grid(row=4,pady=10,padx=10)

        
#AddWorker
class AddW(tk.Frame):
    def clearing(self,reg,year,make,model,colour,hidden,controller):
        #This removes any inputs on the screen
        reg.delete(first=0,last=22)
        year.delete(first=0,last=22)
        make.delete(first=0,last=22)
        model.delete(first=0,last=22)
        colour.delete(first=0,last=22)
        hidden.config(text = "\n")
        controller.show(MenuW)
    
    def adding(self,reg,year,make,model,colour,hidden):
        #checks if the car doesn't exists
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Number_Plate FROM Vehicles WHERE Number_Plate=?''',(reg,))
        result = curs.fetchone()
        if result:
            hidden.config(text="Vehicle Already \nExists")
            db.commit()
            db.close()
        else:
            if (year.isdigit()):
                print("woo")
            curs.execute('''INSERT INTO Vehicles VALUES(?,?,?,?,?)''',(reg,year,make,model,colour))
            hidden.config(text="Vehicle Added \nto Database")
            db.commit()
            db.close()

    def __init__(self, parent, controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Add Vehicle:")
        label.grid(pady=10,padx=10)
        label.config(font=("Courier", 20))
        
        regl = tk.Label(self, text="Number Plate:")
        reg = tk.Entry(self, width=15)
        regl.grid(row = 1)
        reg.grid(row = 1, column = 1)
        
        yearl = tk.Label(self, text="Year:")
        year = tk.Entry(self, width=15)
        yearl.grid(row = 2)
        year.grid(row = 2, column = 1)
    
        makel = tk.Label(self, text="Manufacturer:")
        make = tk.Entry(self, width=15)
        makel.grid(row = 3)
        make.grid(row = 3, column = 1)

        modell = tk.Label(self, text="Model:")
        model = tk.Entry(self, width=15)
        modell.grid(row = 4)
        model.grid(row = 4, column = 1)

        colourl = tk.Label(self, text="Colour:")
        colour = tk.Entry(self, width=15)
        colourl.grid(row = 5)
        colour.grid(row = 5, column = 1)
        #buttons to call different functions
        add = tk.Button(self, text="Add",
                        command=lambda: self.adding(reg.get(),year.get(),make.get(),model.get(),colour.get(),hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearing(reg,year,make,model,colour,hidden,controller), width=8)
        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 6, column = 1)
        menu.grid(row = 6)
        add.grid(row = 6, column = 2)
        

#SearchWorker
class SearchW(tk.Frame):
    def searching(self,regcheck,reg,year,make,model,colour,hidden):
        #checks if the car exists
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Number_Plate FROM Vehicles WHERE Number_Plate=?''',(regcheck,))
        result = curs.fetchone()
        if result:
            curs.execute('''SELECT * FROM Vehicles WHERE Number_Plate=?''',(regcheck,))
            #prints out everything saved about the car
            alone = curs.fetchone()
            reg.config(text = alone[0])
            year.config(text = alone[1])
            make.config(text = alone[2])
            model.config(text = alone[3])
            colour.config(text = alone[4])
            hidden.config(text="\n")
            db.commit()
            db.close()
        else:
            hidden.config(text="Doesn't Exist\n")
            db.commit()
            db.close()
            
    def clearing(self,reg,year,make,model,colour,enter):
        #This removes any inputs on the screen
        reg.config(text = "")
        year.config(text = "")
        make.config(text = "")
        model.config(text = "")
        colour.config(text = "")
        enter.delete(first=0,last=22)

    def clearmenu(self,reg,year,make,model,colour,enter,hidden,controller):
        #This removes any inputs on the screen and returns use to main screen
        reg.config(text = "")
        year.config(text = "")
        make.config(text = "")
        model.config(text = "")
        colour.config(text = "")
        enter.delete(first=0,last=22)
        hidden.config(text="\n")
        controller.show(MenuW)
    
    def __init__(self, parent, controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Search Vehicle:")
        label.grid(pady=10,padx=10)
        label.config(font=("Courier", 20))

        enterl = tk.Label(self, text="Enter Number Plate: ")
        enter = tk.Entry(self, width = 15)
        enterl.grid(row = 1)
        enter.grid(row = 1, column = 1)

        regl = tk.Label(self, text="Number Plate:")
        reg = tk.Label(self, text = "")
        regl.grid(row = 2)
        reg.grid(row = 2, column = 1)
        
        yearl = tk.Label(self, text="Year:")
        year = tk.Label(self, text = "")
        yearl.grid(row = 3)
        year.grid(row = 3, column = 1)
    
        makel = tk.Label(self, text="Manufacturer:")
        make = tk.Label(self, text = "")
        makel.grid(row = 4)
        make.grid(row = 4, column = 1)

        modell = tk.Label(self, text="Model:")
        model = tk.Label(self, text = "")
        modell.grid(row = 5)
        model.grid(row = 5, column = 1)

        colourl = tk.Label(self, text="Colour:")
        colour = tk.Label(self, text = "")
        colourl.grid(row = 6)
        colour.grid(row = 6, column = 1)

        #buttons that call different functions when clicked
        add = tk.Button(self, text="Search",
                        command=lambda: self.searching(enter.get(),reg,year,make,model,colour,hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearmenu(reg,year,make,model,colour,enter,hidden,controller), width=8)
        clear = tk.Button(self, text="clear",
                        command=lambda: self.clearing(reg,year,make,model,colour,enter), width=8)
        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 7, column = 1)
        menu.grid(row = 7)
        add.grid(row = 7, column = 2)
        clear.grid(row = 8, column = 0)

#FaultyAddWorker
class FaultyAddW(tk.Frame):
    def clear(self,reg,location,serious,problem):
        #This removes any inputs on the screen
        reg.delete(first=0,last=22)
        location.delete(first=0,last=22)
        serious.delete(first=0,last=22)
        problem.delete(first=0,last=22)
        
    def clearmenu(self,reg,location,serious,problem,controller,hidden):
        #This removes any inputs on the screen and returns use to main screen
        reg.delete(first=0,last=22)
        location.delete(first=0,last=22)
        serious.delete(first=0,last=22)
        problem.delete(first=0,last=22)
        hidden.config(text="\n")
        controller.show(MenuW)
        
    def adding(self,reg,location,serious,problem,hidden):
        #checks if the car exists
        fixed = "No"
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Number_Plate FROM Vehicles WHERE Number_Plate=?''',(reg.get(),))
        result = curs.fetchone()
        if result:
            #saves all inputs into faults
            curs.execute('''INSERT INTO Faults(Number_Plate,Fault,Location,Serious,Fixed) VALUES(?,?,?,?,?)''',(reg.get(),location.get(),serious.get(),problem.get(),fixed))
            hidden.config(text="Fault added")
            self.clear(reg,location,serious,problem)
            db.commit()
            db.close()
        else:
            hidden.config(text="Vehicle Doesn't \nExist")
            db.commit()
            db.close()
            
    def __init__(self,parent,controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Add Fault:")
        label.grid(pady=10,padx=10)
        label.config(font=("Courier", 20))
        
        regl = tk.Label(self, text="Number Plate:")
        reg = tk.Entry(self, width=15)
        regl.grid(row = 1)
        reg.grid(row = 1, column = 1)

        locationl = tk.Label(self, text="Location:")
        location = tk.Entry(self, width=15)
        locationl.grid(row = 2)
        location.grid(row = 2, column = 1)

        seriousl = tk.Label(self, text="Is it serious?")
        serious = tk.Entry(self, width=15)
        seriousl.grid(row = 3)
        serious.grid(row = 3, column = 1)

        probleml = tk.Label(self, text="Problem:")
        problem = tk.Entry(self, width=15)
        probleml.grid(row = 4)
        problem.grid(row = 4, column = 1)

        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 5, column = 1)

        #buttons thats call differnt functions
        add = tk.Button(self, text="Add",
                        command=lambda: self.adding(reg,location,serious,problem,hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearmenu(reg,location,serious,problem,controller,hidden), width=8)
        
        menu.grid(row = 7)
        add.grid(row = 7, column = 2)


#FaultySearchWorker
class FaultySearchW(tk.Frame):
    def fixing(self,reg,ID,location,serious,problem):
        #if button fixed is pressed the program updates the database with fixed
        fixed = "Yes"
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''UPDATE Faults SET Fixed=? WHERE Number_Plate=? AND ID=?''',(fixed,reg.get(),ID))
        db.commit()
        db.close()
        location.config(text="")
        serious.config(text="")
        problem.config(text="")
        
    def clearing(self,reg,location,serious,problem,hidden,controller):
        #clears all the inputs and returns to main menu
        location.config(text="")
        serious.config(text="")
        problem.config(text="")
        hidden.config(text="\n")
        reg.delete(first=0,last=22)
        controller.show(MenuW)
        
    def search(self,reg,location,serious,problem,hidden):
        #searchs the whole database and looks for cars that aren't fixed and displays them all
        fixed = "No"
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Number_Plate FROM Vehicles WHERE Number_Plate=?''',(reg.get(),))
        result = curs.fetchone()
        if result:
            hidden.config(text="\n")
            curs.execute('''SELECT * FROM Faults WHERE Number_Plate=? AND Fixed=?''',(reg.get(),fixed))
            hmm = curs.fetchone()
            if hmm:
                problem.config(text = hmm[1])
                serious.config(text = hmm[2])
                location.config(text = hmm[3])
                db.close()
                fix = tk.Button(self, text="Fixed", command=lambda:self.fixing(reg,hmm[5],location,serious,problem))
                fix.grid(row = 8)
            else:
                hidden.config(text="There are no\n faults")
                
                
        else:
            hidden.config(text="Vehicle Doesn't \n Exist")
        
    def __init__(self, parent, controller):
        #sets up all the frames widgets
        tk.Frame.__init__(self,parent)
        title = tk.Label(self, text="Search Fault:")
        title.config(font=("Courier", 20))
        title.grid(pady=10,padx=10)
        
        regl = tk.Label(self, text="Number Plate:")
        reg = tk.Entry(self, width=15)
        regl.grid(row = 1)
        reg.grid(row = 1, column = 1)

        locationl = tk.Label(self, text="Location:")
        location = tk.Label(self,text="", width=15)
        locationl.grid(row = 2)
        location.grid(row = 2, column = 1)

        seriousl = tk.Label(self, text="Is it serious?")
        serious = tk.Label(self,text="", width=15)
        seriousl.grid(row = 3)
        serious.grid(row = 3, column = 1)

        probleml = tk.Label(self, text="Problem:")
        problem = tk.Label(self,text="", width=15)
        probleml.grid(row = 4)
        problem.grid(row = 4, column = 1)

        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 5, column = 1)

        #buttons that call different functions when clicked
        searchi = tk.Button(self, text="Search",
                        command=lambda: self.search(reg,location,serious,problem,hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearing(reg,location,serious,problem,hidden,controller), width=8)
        
        menu.grid(row = 7)
        searchi.grid(row = 7, column = 2)





#Accountant View

class MenuA(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self, text="Accountant Menu")
        title.config(font=("Courier", 20))
        logout = tk.Button(self, text="Logout", width=15, command=lambda: controller.show(Login))
        Add = tk.Button(self, text="New Paymemt",
                           command=lambda: controller.show(AddAccounts),width = 15)
        Search = tk.Button(self, text="Search Payment",
                           command=lambda: controller.show(SearchAccounts),width = 15)
        Update = tk.Button(self, text="Update Payment",
                           command=lambda: controller.show(UpdateAccounts),width = 15)
        
        #Positioning all widgets
        title.grid(pady=10,padx=50)
        logout.grid(row=0,column=1, sticky = "NE")
        Add.grid(row=1,pady=10,padx=10)
        Search.grid(row=2,pady=10,padx=10)
        Update.grid(row=3,pady=10,padx=10)

class AddAccounts(tk.Frame):
    def clearing(self,first,last,repair,paid,phone,reg,hidden,controller):
        #This removes any inputs on the screen and returns to Main Menu 
        first.delete(first=0,last=22)
        last.delete(first=0,last=22)
        repair.delete(first=0,last=22)
        paid.delete(first=0,last=22)
        phone.delete(first=0,last=22)
        reg.delete(first=0,last=22)
        hidden.config(text = "\n")
        controller.show(MenuA)

    def checking(self,first,last,repaid,paid,phone,reg,hidden):
        if first.get() == "" or last.get() == "" or repaid.get() == "" or paid.get() == "" or len(phone.get()) != 11:
            hidden.config(text = "Missing Gaps \n OR\n Number too samll")
        else:
            self.adding(first,last,repaid,paid,phone,reg,hidden)
    
    def adding(self,first,last,repair,paid,phone,reg,hidden):
        #checks if the car exists
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Number_Plate FROM Vehicles WHERE Number_Plate=?''',(reg.get(),))
        result = curs.fetchone()
        if result:
            left = float(repair.get()) - float(paid.get())
            curs.execute('''INSERT INTO Customer(First_Name,Last_Name,Phone_Number) VALUES(?,?,?)''',(first.get(),last.get(),phone.get()))
            db.commit()
            k = str(curs.lastrowid)
            curs.execute('''INSERT INTO Bills(Number_Plate,Amount,Amount_Paid) VALUES(?,?,?)''',(reg.get(),repair.get(),paid.get()))
            db.commit()
            s = str(curs.lastrowid)
            print(k,s)
            curs.execute('''INSERT INTO Customer_Bills(Invoice,CustomerID) VALUES(?,?)''',(s,k))
            last = "Inovice Number: \n" + s + "\nAmount Left: \n" + str(left)
            db.commit()
            hidden.config(text=last)
            db.close()
        else:
            hidden.config(text="Not valid\ number plater")
            
    def __init__(self, parent, controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Add Payment:")
        label.grid(pady=10,padx=10)
        label.config(font=("Courier", 20))
        
        firstl = tk.Label(self, text="First Name:")
        first = tk.Entry(self, width=15)
        firstl.grid(row = 1)
        first.grid(row = 1, column = 1)
        
        lastl = tk.Label(self, text="Last Name:")
        last = tk.Entry(self, width=15)
        lastl.grid(row = 2)
        last.grid(row = 2, column = 1)
    
        repairl = tk.Label(self, text="Repair cost:")
        repair = tk.Entry(self, width=15)
        repairl.grid(row = 3)
        repair.grid(row = 3, column = 1)

        paidl = tk.Label(self, text="Amount paid:")
        paid = tk.Entry(self, width=15)
        paidl.grid(row = 4)
        paid.grid(row = 4, column = 1)

        phonel = tk.Label(self, text="Phone Number:")
        phone = tk.Entry(self, width=15)
        phonel.grid(row = 5)
        phone.grid(row = 5, column = 1)

        regl = tk.Label(self, text="Number Plate:")
        reg = tk.Entry(self, width=15)
        regl.grid(row = 6)
        reg.grid(row = 6, column = 1)

        #buttons that call different functions when clicked
        add = tk.Button(self, text="Add",
                        command=lambda:self.checking(first,last,repair,paid,phone,reg,hidden,),width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearing(first,last,repair,paid,phone,reg,hidden,controller), width=8)
        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 8, column = 1)
        menu.grid(row = 7)
        add.grid(row = 7, column = 2)

class SearchAccounts(tk.Frame):
    def searching(self,invoicecheck,first,last,repair,paid,left,phone,reg,hidden):
        #checks if the payments exists
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Invoice FROM Customer_Bills WHERE Invoice=?''',(invoicecheck,))
        result = curs.fetchone()
        if result:
            curs.execute('''SELECT * FROM Customer_Bills WHERE Invoice=?''',(invoicecheck,))
            k = curs.fetchone()
            db.commit()
            curs.execute('''SELECT * FROM Customer WHERE CustomerID=?''',(k[1],))
            b = curs.fetchone()
            db.commit()
            curs.execute('''SELECT * FROM Bills WHERE Invoice=?''',(k[0],))
            t = curs.fetchone()
            alone = curs.fetchone()
            remain = float(t[2]) - float(t[3])
            reg.config(text = t[1])
            first.config(text = b[1])
            last.config(text = b[2])
            repair.config(text = t[2])
            paid.config(text = t[3])
            left.config(text = str(remain))
            phone.config(text = b[3])
            hidden.config(text="\n")
            db.commit()
            db.close()
        else:
            hidden.config(text="Doesn't Exist\n")
            db.commit()
            db.close()
            
    def clearing(self,enter,first,last,repair,paid,left,phone,reg):
        #This removes any inputs on the screen
        first.config(text = "")
        last.config(text = "")
        repair.config(text = "")
        paid.config(text = "")
        left.config(text = "")
        phone.config(text = "")
        reg.config(text = "")
        enter.delete(first=0,last=22)

    def clearmenu(self,enter,first,last,repair,paid,left,phone,reg,hidden,controller):
        #This removes any inputs on the screen and returns use to main screen
        first.config(text = "")
        last.config(text = "")
        repair.config(text = "")
        paid.config(text = "")
        left.config(text = "")
        phone.config(text = "")
        reg.config(text = "")
        hidden.config(text="\n")
        enter.delete(first=0,last=22)
        controller.show(MenuA)
    
    def __init__(self, parent, controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Search Payment:")
        label.grid(pady=10,padx=10)
        label.config(font=("Courier", 20))

        enterl = tk.Label(self, text="Enter Inovice Number: ")
        enter = tk.Entry(self, width = 15)
        enterl.grid(row = 1)
        enter.grid(row = 1, column = 1)

        regl = tk.Label(self, text="Number Plate:")
        reg = tk.Label(self, text = "")
        regl.grid(row = 2)
        reg.grid(row = 2, column = 1)
        
        firstl = tk.Label(self, text="First Name:")
        first = tk.Label(self, width=15)
        firstl.grid(row = 3)
        first.grid(row = 3, column = 1)
        
        lastl = tk.Label(self, text="Last Name:")
        last = tk.Label(self, width=15)
        lastl.grid(row = 4)
        last.grid(row = 4, column = 1)
    
        repairl = tk.Label(self, text="Repair cost:")
        repair = tk.Label(self, width=15)
        repairl.grid(row = 5)
        repair.grid(row = 5, column = 1)

        paidl = tk.Label(self, text="Amount paid:")
        paid = tk.Label(self, width=15)
        paidl.grid(row = 6)
        paid.grid(row = 6, column = 1)

        leftl = tk.Label(self, text="Amount left:")
        left = tk.Label(self, width = 15)
        leftl.grid(row=7)
        left.grid(row=7,column=1)

        phonel = tk.Label(self, text="Phone Number:")
        phone = tk.Label(self, width=15)
        phonel.grid(row = 8)
        phone.grid(row = 8, column = 1)


        #buttons that call different functions when clicked
        search = tk.Button(self, text="Search",
                        command=lambda: self.searching(enter.get(),first,last,repair,paid,left,phone,reg,hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearmenu(enter,first,last,repair,paid,left,phone,reg,hidden,controller), width=8)
        clear = tk.Button(self, text="clear",
                        command=lambda: self.clearing(enter,first,last,repair,paid,left,phone,reg), width=8)
        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 9, column = 1)
        menu.grid(row = 9)
        search.grid(row = 9, column = 2)
        clear.grid(row = 10, column = 0)

class UpdateAccounts(tk.Frame):
    def clearing(self,enter,npaid,left,paid,hidden):
        #This removes any inputs on the screen
        hidden.config(text = "\n")
        left.config(text = "")
        paid.config(text = "")
        enter.delete(first=0,last=22)
        npaid.delete(first=0,last=22)

    def clearmenu(self,enter,npaid,left,paid,hidden,controller):
        #This removes any inputs on the screen and returns use to main screen
        left.config(text = "")
        paid.config(text = "")
        enter.delete(first=0,last=22)
        npaid.delete(first=0,last=22)
        hidden.config(text="\n")
        controller.show(MenuA)
        
    def calculation(self,invoicecheck,paid,left,amount,hidden):
        #checks if the invoice exists
        db = sqlite3.connect("Garage.db")
        curs = db.cursor()
        curs.execute('''SELECT Invoice FROM Bills WHERE Invoice=?''',(invoicecheck,))
        result = curs.fetchone()
        if result:
            curs.execute('''SELECT Amount,Amount_Paid FROM Bills WHERE Invoice=?''',(invoicecheck,))
            cal = curs.fetchone()
            db.commit()
            SCost = float(cal[0])
            SPaid = float(cal[1])

            total_amount_paid = float(paid.get()) + SPaid
            total_left = SCost - total_amount_paid
            curs.execute('''UPDATE Bills SET Amount_Paid=? WHERE Invoice=?''',(total_amount_paid,invoicecheck))
            left.config(text = str(total_left))
            amount.config(text = str(SCost))
            
            db.commit()
            db.close()
        else:
            hidden.config(text="Doesn't Exist\n")
            db.commit()
            db.close()

        
    def __init__(self, parent, controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Update Payment:")
        label.grid(pady=10,padx=10)
        label.config(font=("Courier", 20))

        enterl = tk.Label(self, text="Enter Invoice Number: ")
        enter = tk.Entry(self, width = 15)
        enterl.grid(row = 1)
        enter.grid(row = 1, column = 1)

        npaidl = tk.Label(self, text="Amount Paid Now: ")
        npaid = tk.Entry(self, width = 15)
        npaidl.grid(row = 2)
        npaid.grid(row = 2, column = 1)

        leftl = tk.Label(self, text="Amount Left: ")
        left = tk.Label(self, width = 15)
        leftl.grid(row = 3)
        left.grid(row = 3, column = 1)

        paidl = tk.Label(self, text="Total Paid: ")
        paid = tk.Label(self, width = 15)
        paidl.grid(row = 4)
        paid.grid(row = 4, column = 1)
        

        #buttons that call different functions when clicked
        Update = tk.Button(self, text="Update",
                        command=lambda: self.calculation(enter.get(),npaid,left,paid,hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearmenu(enter,npaid,left,paid,hidden,controller), width=8)
        clear = tk.Button(self, text="clear",
                        command=lambda: self.clearing(enter,npaid,left,paid,hidden), width=8)
        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 5, column = 1)
        menu.grid(row = 5)
        Update.grid(row = 5, column = 2)
        clear.grid(row = 6, column = 0)

        

#Manager View

class MenuM(tk.Frame):        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        title = tk.Label(self, text="Manager Menu")
        title.config(font=("Courier", 20))
        logout = tk.Button(self, text="Logout", width=15, command=lambda: controller.show(Login))
        WorkerMenu = tk.Button(self, text="Worker Menu",
                           command=lambda: controller.show(MenuW),width = 15)
        AccountMenu = tk.Button(self, text="Accountant Menu",
                           command=lambda: controller.show(MenuA),width = 15)
        registers = tk.Button(self, text="New User",
                           command=lambda: controller.show(Register),width = 15)
        
        #Positioning all widgets
        title.grid(pady=10,padx=100)
        logout.grid(row=0,column=1, sticky = "NE")
        WorkerMenu.grid(row=1,pady=10,padx=10)
        AccountMenu.grid(row=2,pady=10,padx=10)
        registers.grid(row=3,pady=10,padx=10)

class Register(tk.Frame):
    def clearing(self,last,first,pasw,paswc,hidden):
        #This removes any inputs on the screen
        last.delete(first=0,last=22)
        first.delete(first=0,last=22)
        pasw.delete(first=0,last=22)
        paswc.delete(first=0,last=22)
        hidden.config(text="\n")

    def clearmenu(self,last,first,pasw,paswc,hidden,controller):
        #This removes any inputs on the screen and returns use to main screen
        last.delete(first=0,last=22)
        first.delete(first=0,last=22)
        pasw.delete(first=0,last=22)
        paswc.delete(first=0,last=22)
        hidden.config(text="\n")
        controller.show(MenuM)

    def adduser(self,first,last,pasw,paswc,radi,hidden):
        if pasw.get() == paswc.get():
            db = sqlite3.connect("Garage.db")
            curs = db.cursor()
            curs.execute('''INSERT INTO Workers(First_Name,Last_Name,Role,Password) VALUES(?,?,?,?)''',(first.get(),last.get(),radi.get(),pasw.get()))
            db.commit()
            k = str(curs.lastrowid)
            last = "WorkerID is: \n" + k
            hidden.config(text=last)
            db.close()
        else:
            hidden.config(text = "Passwords Don't\n Match")

        
        
    def __init__(self, parent,controller):
        #Set up all the window widgets
        tk.Frame.__init__(self,parent)
        title = tk.Label(self, text="New User:")
        title.config(font=("Courier", 20))

        enterf = tk.Label(self, text="Enter First Name: ")
        enterfirst = tk.Entry(self, width = 15)
        enterf.grid(row = 1)
        enterfirst.grid(row = 1, column = 1)

        enterl = tk.Label(self, text="Enter Last Name: ")
        enterlast = tk.Entry(self, width = 15)
        enterl.grid(row = 2)
        enterlast.grid(row = 2, column = 1)

        radiovar = tk.StringVar()
        rb = tk.Radiobutton(self, text = "Worker", variable=radiovar, value = "Worker")
        rb.grid(row = 3,sticky = "W")
        rb = tk.Radiobutton(self, text = "Accountant", variable=radiovar, value = "Accountant")
        rb.grid(row = 4,sticky = "W")
        rb = tk.Radiobutton(self, text = "Managar", variable=radiovar, value = "Managar")
        rb.grid(row = 5,sticky = "W")

        enterp = tk.Label(self, text="Enter Password: ")
        enterpass = tk.Entry(self, show = "*", width = 15)
        enterp.grid(row = 6)
        enterpass.grid(row = 6, column = 1)

        enterpc = tk.Label(self, text="Confirm Password: ")
        enterpassc = tk.Entry(self, show = "*", width = 15)
        enterpc.grid(row = 7)
        enterpassc.grid(row = 7, column = 1)


        #buttons that call different functions when clicked
        add = tk.Button(self, text="Add User",
                        command=lambda: self.adduser(enterfirst,enterlast,enterpass,enterpassc,radiovar,hidden), width=8)
        menu = tk.Button(self, text = "Menu",
                         command=lambda: self.clearmenu(enterfirst,enterlast,enterpass,enterpassc,hidden,controller), width=8)
        clear = tk.Button(self, text="clear",
                        command=lambda: self.clearing(enterfirst,enterlast,enterpass,enterpassc,hidden), width=8)
        hidden = tk.Label(self, text = "\n")
        hidden.grid(row = 8, column = 1)
        menu.grid(row = 8)
        add.grid(row = 8, column = 2)
        clear.grid(row = 9, column = 0)



        
main = setup()
dir()
main.mainloop()











        
