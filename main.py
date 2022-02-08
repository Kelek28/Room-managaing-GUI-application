from os import stat
import sqlite3
from tkinter import *
from tkinter import ttk
#from types import NoneType

LogedInUser = None
global DATABASE


class Staff:
    def __init__(self, ID=None, function=None, HallId=None):
        self.__ID = ID
        self.__function = function
        self.__HallId = HallId

    def getID(self):
        return self.__ID

    def setID(self, ID):
        self.__ID = ID

    def getFunction(self):
        return self.__function

    def setFunction(self, function):
        self.__function = function

    def getHall(self):
        return self.__HallId

    def setHall(self, hallID):
        self.__HallId = hallID


class lease:
    def __init__(self, roomNumber=None, leaseDuration=None, studentID=None):
        self.__roomNumber = roomNumber
        self.__leaseDuration = leaseDuration
        self.__studentID = studentID

    def getRoomNum(self):
        return self.__roomNumber

    def setRoomNum(self, roomNum):
        self.__roomNumber = roomNum

    def getLeaseDuration(self):
        return self.__leaseDuration

    def setLeaseDuration(self, lDuration):
        self.__leaseDuration = lDuration

    def getStudent(self):
        return self.__studentID

    def setStudentID(self, ID):
        self.__studentID = ID


class Student:
    def __init__(self, ID=None, name=None, lease=None, fullname=None):
        self.__ID = ID
        self.__name = name
        self.__lease = lease
        self.__fullname = fullname

    def getID(self):
        return self.__ID

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getLease(self):
        return self.__lease

    def getFullName(self):
        return self.__fullname

    def setFullName(self, name):
        self.__fullname = name

    def Apply(self, Data):
        pass


class Room:
    def __init__(self, roomNumber=None, hallNumber=None, ocupied=None, rentRate=None, cleaningStatus=None):
        self.__roomNumber = roomNumber
        self.__hallNumber = hallNumber
        self.__ocupied = ocupied
        self.__rentRate = rentRate
        self.__cleaningStatus = cleaningStatus

    def getRoomNumber(self):
        return self.__roomNumber

    def setRoomNumber(self, roomNum):
        self.__roomNumber = roomNum

    def getHallNumber(self):
        return self.__hallNumber

    def setHallNumber(self, hallNum):
        self.__hallNumber = hallNum

    def getOcupied(self):
        return self.__ocupied

    def setOccupied(self, ocupied):
        self.__ocupied = ocupied

    def getRentRate(self):
        return self.__rentRate

    def setRentRate(self, rentRate):
        self.__rentRate = rentRate

    def getCleaningStatus(self):
        return self.__cleaningStatus

    def setHallNumber(self, cleaningStatus):
        self.__cleaningStatus = cleaningStatus


class Hall:
    def __init__(self, hallNumber=None, hallName=None, address=None, telephoneNum=None):
        self.__hallNumber = hallNumber
        self.__hallName = hallName
        self.__address = address
        self.__telephoneNum = telephoneNum

    def getHallNumber(self):
        return self.__hallNumber

    def getHallName(self):
        return self.__hallName

    def getAddress(self):
        return self.__address

    def getTelephoneNum(self):
        return self.__telephoneNum

    def setHallNumber(self, hallNumber):
        self.__hallNumber = hallNumber

    def setHallName(self, HallName):
        self.__hallName = HallName

    def setHallNumber(self, address):
        self.__address = address

    def setTelephoneNum(self, telephoneNum):
        self.__telephoneNum = telephoneNum


class Database():
    def __init__(self):
        self.__dataBaseName = "myDB.db"

    def get_rooms_from_hall(self, hallId):
        return self.sqlExecute("SELECT RoomNumber,HallNumber,Occupied,RentRate,CleaningStatus FROM RoomTable WHERE HallNumber = {}".format(hallId))

    def get_all_rooms(self):
        results = self.sqlExecute(
            "SELECT RoomNumber,HallNumber,Occupied,RentRate,CleaningStatus FROM RoomTable")
        AllRooms = [Room(*x) for x in results]
        return AllRooms

    #  def fill_table(self):
    #     results = self.sqlExecute("SELECT r.RoomNumber, r.HallNumber, r.Occupied, r.CleaningStatus, l.LeaseId, l.StudentId  FROM RoomTable AS r LEFT JOIN LeaseTable AS l ON r.RoomId = l.RoomId")
    #     return results

    def get_All_Students(self):
        result = self.sqlExecute(
            "SELECT FullName,StudentId  FROM StudentTable Where not FullName = '' and Lease = 0; ")
        return [x for x in result]

    def get_Table_data(self):
        results = self.sqlExecute(
            "SELECT  LeaseTable.LeaseId, HallTable.HallName, HallNumber,RoomNumber,StudentTable.FullName,Occupied,CleaningStatus FROM RoomTable LEFT JOIN LeaseTable  ON RoomTable.RoomId = LeaseTable.RoomId  LEFT JOIN StudentTable  ON LeaseTable.StudentId= StudentTable.StudentId  LEFT JOIN HallTable ON RoomTable.HallNumber = HallTable.IdHall ORDER BY HallNumber")
        AllRooms = [x for x in results]
        return AllRooms

    def get_Table_data_warden(self, hallId):
        results = self.sqlExecute(
            """SELECT  LeaseTable.LeaseId, HallTable.HallName,
            HallNumber, RoomNumber, StudentTable.FullName, Occupied, CleaningStatus FROM RoomTable
            LEFT JOIN LeaseTable  ON RoomTable.RoomId=LeaseTable.RoomId
            LEFT JOIN StudentTable  ON LeaseTable.StudentId=StudentTable.StudentId
            INNER JOIN HallTable ON RoomTable.HallNumber=HallTable.IdHall and HallTable.IdHall={}
            ORDER BY HallNumber """.format(hallId))
        AllRooms = [x for x in results]
        return AllRooms

    def get_possible_position(self):
        options = self.sqlExecute("""SELECT IdHall
                        FROM HallTable
                        WHERE NOT EXISTS
                        (SELECT *
                         FROM StaffMemberTable
                         WHERE HallTable.IdHall=StaffMemberTable.IdHall) """)
        options = [x[0] for x in options]
        return options

    def register(self, login, password, type):
        error = False
        userExist = self.sqlExecute(
            "SELECT count(StudentTable.userName) FROM StudentTable Where UserName='{}' UNION all SELECT Count(StaffMemberTable.UserName) FROM StaffMemberTable WHERE UserName='{}'".format(login, login))
        UserExist = not not sum([x[0] for x in userExist])
        print(UserExist)
        if UserExist:
            error = True

        if type == "Student" and error != True:
            result = self.sqlExecute(
                ' SELECT max(StudentId) FROM StudentTable')[0]
            studentId = result[0]
            if studentId == None:
                studentId = 1
            else:
                studentId = studentId + 1
            self.sqlExecute('INSERT INTO StudentTable VALUES ({},"{}",{},"{}","{}")'.format
                            (studentId, login, 0, password, ""))
            return error
        result = self.sqlExecute(
            "SELECT max(StaffId) FROM StaffMemberTable")[0]
        memberId = result[0]
        if memberId == None:
            memberId = 1
        else:
            memberId = memberId + 1
        if "Manager" in type and error != True:
            hallId = None
            self.sqlExecute('INSERT INTO StaffMemberTable VALUES({},"{}","{}","{}","{}")'.format(
                memberId, password, type, hallId, login))
            return error
        if error != True:
            hallId = type.split(".")[1]
            self.sqlExecute('INSERT INTO StaffMemberTable VALUES({},"{}","{}",{},"{}")'.
                            format(memberId, password, type.split()[0], hallId, login))
        return error

    def login(self, login, password):
        global LogedInUser
        StudentQuery = self.sqlExecute(
            "SELECT StudentId,UserName,Lease,FullName From StudentTable WHERE UserName = '{}' and Password = '{}'".format(login, password))
        if StudentQuery:
            LogedInUser = Student(*StudentQuery[0])
            return LogedInUser
        StaffMemberQuery = self.sqlExecute(
            "SELECT  StaffId, Function, IdHall from StaffMemberTable WHERE UserName='{}' and Password='{}'".format(
                login, password)
        )
        if StaffMemberQuery:
            LogedInUser = Staff(*StaffMemberQuery[0])
            return LogedInUser
        return LogedInUser

    def userUpdate(self, User):
        self.sqlExecute("UPDATE StudentTable set FullName = '{}' WHERE StudentId = {}".format(
            User.getFullName(), User.getID()))

    def sqlExecute(self, sql):
        try:
            con = sqlite3.connect(self.__dataBaseName)
            cur = con.cursor()
            cur.execute(sql)
            if sql.split()[0].upper() in ["UPDATE", "INSERT", "DELETE"]:
                con.commit()
            result = cur.fetchall()
        except con.Error as err:
            print("operation is failed", err)
        finally:
            if con:
                con.close()
                return result


class WardenTabView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.WardenTab = ttk.Frame(self.parent, width=400,
                                   height=280, name="wardenFrame")

        self.WardenTab.pack(fill='both', expand=True)
        self.parent.add(self.WardenTab, text="Warden")
        self.currentlySelected = StringVar()
        self.LeaseNumberEntry = StringVar()
        self.HallNameEntry = StringVar()
        self.HallNumberEntry = StringVar()
        self.RoomNumberEntry = StringVar()
        self.StudentNameEntry = StringVar()
        self.OcuupancyEntry = StringVar()
        self.CleaningEntry = StringVar()
        self.StudentID = StringVar()
        trvWarden = ttk.Treeview(self.WardenTab, selectmode="browse")
        trvWarden.grid(row=0, column=0)
        trScrolbr = ttk.Scrollbar(
            self.WardenTab, orient="vertical", command=trvWarden.yview)
        trScrolbr.grid(row=0, column=1, columnspan=4)

        trvWarden.configure(xscrollcommand=trScrolbr.set)
        # Defining number of columns
        trvWarden["columns"] = ('1', '2', '3', '4', '5', '6', '7')

        # Defining heading
        trvWarden = self.tabulateObject(
            trvWarden, DATABASE.get_Table_data_warden(LogedInUser.getHall()))
        trvWarden['show'] = 'headings'
        headings = [
            "Lease Number",
            "Hall Name",  # Prev Hall name
            "Hall Number",  # Prev Hall name
            "Room Number",  # prev Lease Num
            "Student name",
            "Occupancy Status",  # prev Hall Num
            "Cleaning Status",  # Prev Room Num
            # Prev Student Name, Occupancy Status, Cleaning Status
        ]
        for num, text in enumerate(headings, start=1):
            trvWarden.column(str(num), width=120, anchor="c")
            trvWarden.heading(str(num), text=text)
        trvWarden.bind("<Button-1>",
                       lambda event, widget=trvWarden: self.select_item(widget))

        # retrieveing data from users table and inserting into the treeview
        lf = ttk.Labelframe(self.WardenTab, text='Lease Information')
        lf.grid(row=1, column=0, columnspan=4)
        DatabaseAccess = Database()
        Label(lf, text="Hall Name").grid(row=0, column=0)
        Entry(lf, textvariable=self.HallNameEntry,
              state=DISABLED).grid(row=0, column=1)
        Label(lf, text="Lease Number").grid(row=0, column=2)
        Entry(lf, textvariable=self.LeaseNumberEntry,
              state=DISABLED).grid(row=0, column=3)

        Label(lf, text="Hall Number").grid(row=1, column=0)
        Entry(lf, textvariable=self.HallNumberEntry,
              state=DISABLED).grid(row=1, column=1)
        Label(lf, text="Student Name").grid(row=1, column=2)
        Entry(lf, textvariable=self.StudentNameEntry,
              state=DISABLED).grid(row=1, column=3)
        Label(lf, text="Room Number").grid(row=2, column=0)
        Entry(lf, textvariable=self.RoomNumberEntry,
              state=DISABLED).grid(row=2, column=1)
        Button(lf, text="Room is Clean",
               command=lambda: self.update_Item("Clean")).grid(row=3, column=2)
        Button(lf, text="Room is Dirty", command=lambda: self.update_Item("Dirty")).grid(
            row=3, column=3)  # command used to be update_item
        Button(lf, text="Room is Offline", command=lambda: self.update_Item("Offline")).grid(
            row=3, column=1)  # command used to be update_item

    def tabulateObject(self, tr, results):
        for item in tr.get_children():
            tr.delete(item)
        i = 1
        for row in results:
            txt = "L"+str(i)
            i += 1
            tr.insert("", 'end', text=txt, values=(
                tuple([x if x else "" for x in row])))

        return tr

    def select_item(self, tk):

        data = [self.LeaseNumberEntry,     self.HallNameEntry,
                self.HallNumberEntry,
                self.RoomNumberEntry,
                self.StudentNameEntry,
                self.OcuupancyEntry, self.CleaningEntry]
        selected = tk.focus()
        self.currentlySelected.set(tk.item(selected, "values"))
        for count, var in enumerate(tk.item(selected, "values")):
            data[count].set(var)

    # Template for Update Item
    def update_Item(self, state):
        if self.RoomNumberEntry.get():
            RoomId = int(str(self.RoomNumberEntry.get()) +
                         str(self.HallNumberEntry.get()))
            DATABASE.sqlExecute("UPDATE RoomTable set CleaningStatus = '{}' WHERE RoomId={}".format(
                state, RoomId))
            self.reload_window(self.parent)
            return PopUp(f"Room {self.RoomNumberEntry.get()} is now {state}")
        return PopUp(f"Room not selected")

    def reload_window(self, parent):
        self.WardenTab.destroy()
        WardenTabView(parent)

# STUDENT Widget


class StudentTabView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.StudentTab = ttk.Frame(self.parent, width=250,
                                    height=280, name="studentFrame")
        self.parent.add(self.StudentTab, text="Student")
        # Tab for student which tries to submit application
        if not LogedInUser.getFullName() and not LogedInUser.getLease():
            Label(self.StudentTab, text="Welcome to UWE!").grid(row=0, column=0)
            Label(self.StudentTab, text="Full Name").grid(
                row=1, column=0)
            appli = StringVar()
            Entry(self.StudentTab, textvariable=appli).grid(row=1, column=1)
            Button(self.StudentTab, text="Submit Application", command=lambda: self.submit_application(self.parent, appli.get())).grid(
                row=1, column=2)
            Button(self.StudentTab, text="Quit", command=self.parent.destroy).grid(
                row=4, column=2, sticky=W)
        if not LogedInUser.getLease() and LogedInUser.getFullName():
            # Tab after submiting aplication
            Label(self.StudentTab, text="Congratulation form submited correctly!\nYour application is under consideration ").grid(
                row=0, column=0)
        if LogedInUser.getFullName() and LogedInUser.getLease():
            # Tab after being accepted
            resultName = ["RentRate", "RoomNumber", "LeaseTable.LeaseDuration", "LeaseTable.LeaseId",
                          "HallTable.HallAddress", "HallNumber", "HallTable.Telephone"]
            resultValues = DATABASE.sqlExecute("""SELECT RentRate, RoomNumber, LeaseTable.LeaseDuration, LeaseTable.LeaseId, HallTable.HallAddress, HallNumber, HallTable.Telephone
                                from RoomTable inner join LeaseTable on RoomTable.RoomId=LeaseTable.RoomId INNER JOIN HallTable ON RoomTable.HallNumber=HallTable.IdHall WHERE LeaseTable.StudentId={}""".format(LogedInUser.getID()))
            result = dict(zip(resultName, resultValues[0]))
            message = f"""Accepted!
            Room number {result['RoomNumber']} in hall {result['HallNumber']} on {result['HallTable.HallAddress']}. \nIt is yours for the next 12 months for the price of {result['RentRate']}£. \nIf you have any questions you can contact us on {result['HallTable.Telephone']} quoting your rental reference number {result['HallTable.Telephone']}
            """
            Label(self.StudentTab, text=message).grid(
                row=0, column=0)

    def submit_application(self, parent, name):
        if name:
            LogedInUser.setFullName(name)
            DATABASE.userUpdate(LogedInUser)
            self.reload_window(parent)
            return PopUp("Form submited correctly!")
        return PopUp("Field is empty")

    def reload_window(self, parent):
        self.StudentTab.destroy()
        StudentTabView(parent)

# MANAGER WIDGET


class ManagerTabView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        currentlySelected = StringVar()
        self.ManagerTab = ttk.Frame(self.parent, width=400,
                                    height=280, name="managerFrame")

        self.ManagerTab.pack(fill='both', expand=True)
        self.parent.add(self.ManagerTab, text="Manager")
        self.currentlySelected = StringVar()
        self.LeaseNumberEntry = StringVar()
        self.HallNameEntry = StringVar()
        self.HallNumberEntry = StringVar()
        self.RoomNumberEntry = StringVar()
        self.StudentNameEntry = StringVar()
        self.OcuupancyEntry = StringVar()
        self.CleaningEntry = StringVar()
        self.StudentID = StringVar()
        trvManager = ttk.Treeview(self.ManagerTab, selectmode="browse")
        trvManager.grid(row=0, column=0)
        trScrolbr = ttk.Scrollbar(
            self.ManagerTab, orient="vertical", command=trvManager.yview)
        trScrolbr.grid(row=0, column=1, columnspan=4)

        trvManager.configure(xscrollcommand=trScrolbr.set)
        # trvManager.bind("<Double-Button-1>", select_item)
        # Defining number of columns
        trvManager["columns"] = ('1', '2', '3', '4', '5', '6', '7')

        # Defining heading
        trvManager = self.tabulateObject(
            trvManager, DATABASE.get_Table_data())
        trvManager['show'] = 'headings'
        headings = [
            "Lease Number",
            "Hall Name",  # Prev Hall name
            "Hall Number",  # Prev Hall name
            "Room Number",  # prev Lease Num
            "Student Name",
            "Occupancy Status",  # prev Hall Num
            "Cleaning Status",  # Prev Room Num
            # Prev Student Name, Occupancy Status, Cleaning Status
        ]
        for num, text in enumerate(headings, start=1):
            trvManager.column(str(num), width=120, anchor="c")
            trvManager.heading(str(num), text=text)
        trvManager.bind("<Button-1>",
                        lambda event, widget=trvManager: self.select_item(widget))

        # retrieveing data from users table and inserting into the treeview
        lf = ttk.Labelframe(self.ManagerTab, text='Lease Information')
        lf.grid(row=1, column=0, columnspan=4)
        DatabaseAccess = Database()
        Label(lf, text="Hall Name").grid(row=0, column=0)
        Entry(lf, textvariable=self.HallNameEntry,
              state=DISABLED).grid(row=0, column=1)
        Label(lf, text="Lease Number").grid(row=0, column=2)
        Entry(lf, textvariable=self.LeaseNumberEntry,
              state=DISABLED).grid(row=0, column=3)

        Label(lf, text="Hall Number").grid(row=1, column=0)
        Entry(lf, textvariable=self.HallNumberEntry,
              state=DISABLED).grid(row=1, column=1)
        Label(lf, text="Student Name").grid(row=1, column=2)
        self.allStudents = dict(DATABASE.get_All_Students())
        studentNamCB = ttk.Combobox(lf, values=list(self.allStudents.keys(
        )), justify="center", textvariable=self.StudentID)
        studentNamCB.grid(row=1, column=3)

        Label(lf, text="Room Number").grid(row=2, column=0)
        Entry(lf, textvariable=self.RoomNumberEntry,
              state=DISABLED).grid(row=2, column=1)
        Label(lf, text="Occupancy").grid(row=2, column=2)
        ttk.Entry(lf, textvariable=self.OcuupancyEntry,
                  state=DISABLED,).grid(row=2, column=3)
        Button(lf, text="Remove Student From Room",
               command=self.delete).grid(row=3, column=2)
        Button(lf, text="Assign Room", command=self.update_Item).grid(
            row=3, column=3)

    def tabulateObject(self, tr, results):
        for item in tr.get_children():
            tr.delete(item)
        i = 1
        for row in results:
            txt = "L"+str(i)
            i += 1
            tr.insert("", 'end', text=txt, values=(
                tuple([x if x else "" for x in row])))

        return tr

    def select_item(self, tk):

        data = [self.LeaseNumberEntry,     self.HallNameEntry,
                self.HallNumberEntry,
                self.RoomNumberEntry,
                self.StudentNameEntry,
                self.OcuupancyEntry, self.CleaningEntry]
        selected = tk.focus()
        self.currentlySelected.set(tk.item(selected, "values"))
        for count, var in enumerate(tk.item(selected, "values")):
            data[count].set(var)

    def update_Item(self):
        if self.RoomNumberEntry.get():
            if self.StudentID.get():
                if(self.CleaningEntry.get() != "Offline"):
                    if self.OcuupancyEntry.get() == "Occupied":
                        return PopUp("This room is not Free")
                    if self.OcuupancyEntry.get() == "Free":
                        NextLeaseId = DATABASE.sqlExecute(
                            "SELECT MAX(LeaseId) FROM LeaseTable")
                        if NextLeaseId[0][0]:
                            NextLeaseId = NextLeaseId[0][0]+1
                        else:
                            NextLeaseId = 1001
                        RoomId = int(str(self.RoomNumberEntry.get()) +
                                     str(self.HallNumberEntry.get()))
                        DATABASE.sqlExecute("INSERT INTO LeaseTable Values ({},{},{},{})".format(
                            NextLeaseId, RoomId, 12, self.allStudents[self.StudentID.get()]))
                        DATABASE.sqlExecute("UPDATE StudentTable set Lease=12 where StudentId = {} ".format(
                            int(self.allStudents[self.StudentID.get()])))
                        DATABASE.sqlExecute("UPDATE RoomTable set Occupied='Occupied' where RoomId = {} ".format(
                            "{}{}".format(self.RoomNumberEntry.get(), self.HallNumberEntry.get())))
                        self.reload_window(self.parent)
                        return PopUp(f"Room is assign to {self.StudentID.get()}")
                    return PopUp(f"That room is occupied by {self.StudentID.get()}")

                return PopUp("Room is offline unable to change")
            return PopUp("Student name not selected")
        return PopUp("Room not selected")

    def delete(self):
        if self.LeaseNumberEntry.get():
            if self.CleaningEntry.get() != "Offline":
                StudentId = DATABASE.sqlExecute(
                    "SELECT StudentId FROM LeaseTable wHERE LeaseId={}".format(self.LeaseNumberEntry.get()))[0][0]
                DATABASE.sqlExecute("DELETE FROM LeaseTable WHERE LeaseId={}".format(
                    self.LeaseNumberEntry.get()))
                DATABASE.sqlExecute("UPDATE StudentTable set Lease=0 where StudentId = {} ".format(
                    StudentId))
                DATABASE.sqlExecute("UPDATE RoomTable set Occupied='Free' where RoomId = {} ".format(
                    "{}{}".format(self.RoomNumberEntry.get(), self.HallNumberEntry.get())))
                self.reload_window(self.parent)
                return PopUp("Student removed from room")
            return PopUp("Room is offline unable to unasign user")
        return PopUp("Room is already empty")

    def reload_window(self, parent):
        self.ManagerTab.destroy()
        ManagerTabView(parent)


class PopUp():
    def __init__(self, message, *args):
        win = Toplevel()
        win.wm_title("Window")

        l = ttk.Label(win, text=message)
        l.grid(row=0, column=0)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)


class LoginPage(ttk.Frame):
    global DATABASE

    def __init__(self, parent, *args, **kwargs):
        self.loginWindow = Toplevel(name="loginPage")
        self.parent = parent
        self.loginWindow.title("Tab Widget")
        tabControl = ttk.Notebook(self.loginWindow)

        loginTab = ttk.Frame(tabControl)
        registerTab = ttk.Frame(tabControl)

        tabControl.add(loginTab, text='Login')
        tabControl.add(registerTab, text='Register')
        tabControl.pack(expand=1, fill="both")

        uName = StringVar()
        uPass = StringVar()
        uType = StringVar()

        # Tab 1 development starts from here

        Label(loginTab, text="User Name").grid(row=0, column=0)
        Entry(loginTab, textvariable=uName).grid(row=0, column=1)

        Label(loginTab, text="Password").grid(row=1, column=0)
        Entry(loginTab, textvariable=uPass, show='*').grid(row=1, column=1)

        Button(loginTab, text="Login", command=lambda: self.login(loginTab,
                                                                  uName, uPass)).grid(row=4, column=0, sticky=W)
        Button(loginTab, text="Exit", command=self.parent.destroy).grid(
            row=4, column=1, sticky=W)
        # Tab 2 development starts from here

        Label(registerTab, text="User Name:").grid(
            row=0, column=0, padx=10, pady=10)
        Entry(registerTab, textvariable=uName).grid(row=0, column=1)
        Label(registerTab, text="Password:").grid(
            row=1, column=0, padx=10, pady=10)
        Entry(registerTab, textvariable=uPass, show='*').grid(row=1, column=1)
        Label(registerTab, text="User Type:").grid(
            row=2, column=0,  padx=10, pady=10)

        # Entry(registerTab, textvariable=uType).grid(row=2,column=1)

        uType.set("Student")
        optionsRegisterFinal = ["Student", "Manager"] + [
            "Warden Hall nr.{}".format(x) for x in DATABASE.get_possible_position()]
        OptionMenu(registerTab, uType, *optionsRegisterFinal).grid(
            row=2, column=1,  padx=10, pady=10)

        Button(registerTab, text="Save", command=lambda: self.save(
            uName, uPass, uType)).grid(row=4, column=0)

    def login(self, tk, username, password):
        if DATABASE.login(username.get(), password.get()):
            self.loginWindow.destroy()
            GUI(self.parent).pack(side="top", fill="both", expand=True)
        else:
            Label(tk, text="").grid(
                row=5, column=0)  # , sticky=W)
            Label(tk, text="Login failed", fg='red').grid(
                row=5, column=1)  # , sticky=W)

    def save(self, login, password, type):
        if login.get() and password.get():
            if not DATABASE.register(login.get(), password.get(), type.get()):
                return PopUp("Congratulations!\nUser created")
            return PopUp("Error try again!")
        return PopUp("Login or password field is empty")


class GUI(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        global LogedInUser
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        if not LogedInUser:
            self.parent.withdraw()
            LoginPageWindow = LoginPage(self.parent)
        if LogedInUser:
            self.parent.title("UWE Bristol Accommodation System")
            n = ttk.Notebook(parent)
            n.pack(pady=10, expand=True)
            self.parent.deiconify()
            # Display only student tab
            if LogedInUser.__class__.__name__ == "Student":
                StudentPageWindow = StudentTabView(n)
            else:
                if LogedInUser.getFunction() == "Manager":
                    ManagerPageWindow = ManagerTabView(n)
                if LogedInUser.getFunction() == "Warden":
                    WardenPageWindow = WardenTabView(n)


if __name__ == "__main__":
    root = Tk()
    DATABASE = Database()
    GUI(root).pack(side="top", expand=True)
    root.mainloop()
