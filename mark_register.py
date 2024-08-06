
###############

# prerequisites:-

# pip install mysql-connector-python

# pip install PySimpleGUI

# pip install tabulate

# http://www.mediafire.com/folder/xwg4hy0mdnwz5/Python+and+Mysql

###############

import time

import multiprocessing

import pickle

from tabulate import tabulate

from sys import exc_info

from sys import exit

import random

import PySimpleGUI as sg

import mysql.connector


intro = """

  ███╗░░░███╗░█████╗░██████╗░██╗░░██╗  ██████╗░███████╗░██████╗░██╗░██████╗████████╗███████╗██████╗░  
  ████╗░████║██╔══██╗██╔══██╗██║░██╔╝  ██╔══██╗██╔════╝██╔════╝░██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗  
  ██╔████╔██║███████║██████╔╝█████═╝░  ██████╔╝█████╗░░██║░░██╗░██║╚█████╗░░░░██║░░░█████╗░░██████╔╝  
  ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗░  ██╔══██╗██╔══╝░░██║░░╚██╗██║░╚═══██╗░░░██║░░░██╔══╝░░██╔══██╗  
  ██║░╚═╝░██║██║░░██║██║░░██║██║░╚██╗  ██║░░██║███████╗╚██████╔╝██║██████╔╝░░░██║░░░███████╗██║░░██║  
  ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝  ╚═╝░░╚═╝╚══════╝░╚═════╝░╚═╝╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  

  """


def check_empty_and_add(databases):
    try:
        if databases == []:
           
            while True:
                db = sg.popup_get_text(
                    "Welcome! Enter A Class Name To Get Started.", title="Mark Registry", keep_on_top=True)
                
                if db == None:
                    exit()
                
                elif db == "":
                    continue
                
                else:
                    break
            
            db = db.replace("-", "_")
            db = db.replace(" ", "_")
            cursor.execute(f"CREATE DATABASE {prefx + db};")
            class_init(db, cursor)
            databases.append(db.lower())
    
    except mysql.connector.errors.ProgrammingError:
        sg.PopupError("Syntax Not Supported", keep_on_top=True)
        check_empty_and_add(databases)


def create_class_select_window(cur_database=""):
    
    if databases == []:
        check_empty_and_add(databases)
        create_class_select_window()
    layout = [[sg.Text(intro, relief=sg.RELIEF_RIDGE, font=("Helvetica", 5), key="intro1")], [
        sg.Text("    Select a Class    ", pad=(0, (10, 5)), relief=sg.RELIEF_SUNKEN)]]
    
    for a in databases:
        if a == cur_database:
            layout.append(
                [sg.Radio((a), "RADIO1", default=True, enable_events=True)])
        else:
            layout.append(
                [sg.Radio((a), "RADIO1", enable_events=True)])
    
    if cur_database:
        layout.append([sg.Submit(f"Use Class {cur_database}", tooltip='Click to Add/Edit Tests'), sg.Submit(f"Edit Class {cur_database}"), sg.Submit(f"Delete Class {cur_database}")])
    layout.append([sg.Submit(
        "Add Class"), sg.Button("Change Theme"), sg.Cancel("Quit")])
    return sg.Window('Mark Registry', layout, keep_on_top=True, resizable=True, disable_close=True, element_justification="c")


def change_theme_window(theme):
    layout = [[]]
    for a in themes_temp:
        data = []
        for b in a:
            if b == theme:
                data.append(
                    [sg.Radio(b, "Radio2", key=b, enable_events=True, default=True)])
            else:
                data.append([sg.Radio(b, "Radio2", key=b, enable_events=True)])
        layout[0].append(sg.Column(data))
        layout[0].append(sg.VerticalSeparator())
    layout = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True)]]
    layout.append([sg.Column([[sg.Button("Save Changes"), sg.Button(
        "Discard Changes")]], element_justification="l")])
    return sg.Window("Change Theme", layout, keep_on_top=True)


def exit_popup():
    window2 = yes_or_no_popup(
        "Do you wanna quit?             ",
        "Caution")
   
    if window2 == "Yes":
        exit()


def yes_or_no_popup(text, title):
    layout = [
        [sg.Text(text)],
        [sg.Submit("Yes"), sg.Cancel("NO")]
    ]
    popup1 = sg.Window(title, layout, resizable=True,
                       font="Courier 10", keep_on_top=True)
    event, values = popup1.read(close=True)
    
    if event in (sg.WIN_CLOSED, "NO"):
        return "No"
    
    else:
        return "Yes"


def notif_popup(text, title, extra=None):
    layout = [
        [sg.Text(text)],
        [sg.Submit("Ok")]
    ]
    popup1 = sg.Window(title, layout, resizable=True,
                       font="Courier 10", keep_on_top=True)
    popup1.read(close=True)


def add_class(databases, cursor):
    
    while True:
        global window
        
        db = sg.popup_get_text(
            "Enter Class Name", title="Add Class", keep_on_top=True)
        
        if db:
            if db not in databases:
                db = db.replace("-", "_")
                cursor.execute(f"CREATE DATABASE {prefx + db};")
                class_init(db, cursor)
                databases.append(db.lower())
                break
            else:
                sg.popup_error("Class Already Exists",
                               title="Error", keep_on_top=True)
                continue
        
        elif db == None:
            break
        
        elif db.strip() == "":
            continue


def delete_class(databases, cursor):
    global window
    global cur_database
    for x, y in values.items():
       
        if y:
            cur_database = databases[x]
            choice = yes_or_no_popup(f"Class {cur_database} will be Erased.\nDo you Want to Proceed?", "Caution!")
            
            if choice == "Yes":
                cursor.execute(f"DROP DATABASE {prefx + cur_database};")
                databases.remove(cur_database)
                cur_database = ''
                window.close()
            break


def create_test_select_window(tests, cur_test):
    layout = [[sg.Text(intro, relief=sg.RELIEF_RIDGE, font=("Helvetica", 5), key="intro2")]]
    table = [tests[i:i+2] for i in range(0, len(tests), 2)]
    if tests:
        layout.append( [sg.Text("    Select a Test    ", pad=(0, (10, 5)), relief=sg.RELIEF_SUNKEN)])
    for a in table:
        layout.append([])
        for b in a:
            
            if b == cur_test:
                layout[-1].append(sg.Radio((b), "RADIO1",
                                           enable_events=True, default=True))
            
            else:
                layout[-1].append(sg.Radio((b), "RADIO1",
                                           enable_events=True))
    if cur_test:
        layout += [
            [sg.Button(f"View Statistics of {cur_test}"), sg.Submit(f"Add/Edit Marks of {cur_test}"), sg.Button(f"Remove {cur_test}")], [sg.Button("Add A New Test"),
                                                                                                                                         sg.Button("Go Back"), sg.Button("Quit")]]

    else:
        layout += [
            [sg.Button("Add A New Test"),
             sg.Button("Go Back"), sg.Button("Quit")]]

    return sg.Window(cur_database, layout, disable_close=True, element_justification="c", keep_on_top=True)


def select_class(cursor, cur_database):
    load = multiprocessing.Process(target=loading)
    cursor.execute(f"USE {prefx + cur_database}")
    cursor.execute(f"SELECT testname FROM tests;")
    data = cursor.fetchall()
    tests = [data[i][0] for i in range(len(data))]

    cursor.execute(f"SELECT * FROM subjects;")
    data_fetched = cursor.fetchall()
    subs = [data_fetched[i][0] for i in range(len(data_fetched))]
    cursor.execute(f"SELECT * FROM students;")
    data_fetched = cursor.fetchall()
    studs = [data_fetched[i][0] for i in range(len(data_fetched))]

    if not studs and not subs:
        notif_popup(
            "Start By Adding Students and Subjects\nto Your class Using The 'Edit Class' Option", ":)")
        return
   
    elif not studs:
        notif_popup(
            "To Proceed, Add Students To Your\nClass Using The 'Edit Class' Option", ":)")
        return
    
    elif not subs:
        notif_popup(
            "To Proceed, Add Subjects To Your\nClass Using The 'Edit Class' Option", ":)")
        return

    cur_test = ""

    window = create_test_select_window(tests, cur_test)

    while True:
        event, values = window.read()

        if event == f"View Statistics of {cur_test}":
            window.close()
            load.start()
            time1 = time.time()
            cursor.execute(f'select {",".join([f"avg({x})" for x in subs])} from {cur_test}')
            avg_subs = cursor.fetchall()[0]
            avg_subs = [round(x, 2) if x else "NULL" for x in avg_subs]
            cursor.execute(f"select maxmark,description from tests where testname = '{cur_test}'")
            data = cursor.fetchall()
            desc = data[0][1].replace("-n-", "\n")
            max_marks = data[0][0]
            cursor.execute(f"select studentname,{','.join(subs)} from {cur_test}")
            table_data = cursor.fetchall()
            table_data = [list(a) for a in table_data]
            for a in range(len(table_data)):
                for b in range(len(table_data[a])):
                    if table_data[a][b] == None:
                        table_data[a][b] = "NULL"

            if desc.strip().replace("\n", ""):
                layout = [
                    [sg.Frame("Class Summary", layout=[
                        [sg.Column([
                            [sg.Text(f"Student Count:- {len(studs)}")], [sg.Text(f"Subject Count:- {len(subs)}")], [sg.Text(f"Maximum Marks:- {max_marks}")]], pad=(0, 0)),
                            sg.VerticalSeparator(),
                            sg.Text(f"Class Description:-\n\n{desc}")],
                        [sg.Text("Subject Average Scored By Class:-\n")],
                        [sg.Column([[sg.Text(tabulate([avg_subs], headers=subs, tablefmt="psql"), font="Courier 10", justification="c")]], justification="c")]]), sg.VerticalSeparator(),
                        sg.Column([[sg.Text(tabulate(table_data, headers=["Student Name"]+subs, tablefmt="psql"),
                                            font="Courier 10", justification="c")], [sg.Button("Go Back")]], element_justification="r")
                     ]]
            else:
                layout = [
                    [sg.Frame("Class Summary", layout=[
                        [sg.Column([
                            [sg.Text(f"Student Count:- {len(studs)}")], [sg.Text(f"Subject Count:- {len(subs)}")], [sg.Text(f"Maximum Marks:- {max_marks}")]], pad=(0, 0))],
                        [sg.Text("Subject Average Scored By Class:-\n")],
                        [sg.Column([[sg.Text(tabulate([avg_subs], headers=subs, tablefmt="psql"), font="Courier 10", justification="c")]], justification="c")]]), sg.VerticalSeparator(),
                        sg.Column([[sg.Text(tabulate(table_data, headers=["Student Name"]+subs, tablefmt="psql"),
                                            font="Courier 10", justification="c")], [sg.Button("Go Back")]], element_justification="r")
                     ]]
            
            timecheck(time1)
            load.terminate()
            load = multiprocessing.Process(target=loading)
            sg.Window(title=f"{cur_test}", layout=layout, element_justification="c", keep_on_top=True).read(close=True)

        elif event == f"Add/Edit Marks of {cur_test}":
            window.close()
            load.start()
            time1 = time.time()
            cursor.execute(f"select maxmark from tests where testname = '{cur_test}'")
            maxmark = int(cursor.fetchall()[0][0])
            layout = [[sg.Column([[sg.Text("Student Name", justification="c", size=(
                20, None), relief=sg.RELIEF_RIDGE)]])]]
            for a in subs:
                layout[0].append(sg.Column([[sg.Text(a, justification="c", size=(
                    8, 1), relief=sg.RELIEF_RIDGE, pad=((1, 11), 0))]]))

            data = ["studentname"] + subs.copy()
            cursor.execute(f"Select {','.join(data)} from {cur_test};")
            data2 = cursor.fetchall()
            data3 = {x[0]: {subs[b]: x[b+1]
                            for b in range(len(subs))} for x in data2}

            layout_mini = []
            
            for a in studs:
                layout_mini.append(
                    [sg.Text(a.replace("_", " ").capitalize(), justification="c", size=(20, None))])
                
                for b in subs:
                    layout_mini[-1].append(sg.Input(data3[a][b], size=(10, 1), enable_events=True, justification="c", key=f"{b} {a}", pad=(8, 0), 
                        tooltip="Use Arrow Keys To Navigate Between Fields"))
                
                layout_mini.append(
                    [sg.Text("_" * (24 + (len(subs)*11)), justification="c", pad=(0, (0, 15)))])

            layout_mini.pop(-1)
            layout.append([sg.Column(layout_mini, element_justification="c", size=(
                (191 + (len(subs)*90)), 300), key="col1", scrollable=True, vertical_scroll_only=True)])
            layout.append([sg.Column([[sg.Text("+" * 20, visible=False, key="Caution")]], justification="l"),
                           sg.Column([[sg.Button("Save Changes"), sg.Button("Discard Changes")]], justification="r")])
            timecheck(time1)
            load.terminate()
            load = multiprocessing.Process(target=loading)
            wind = sg.Window(f"Edit Marks From {cur_test}", layout, keep_on_top=True, disable_close=True, use_default_focus=True, return_keyboard_events=True)
            
            while True:
                event, values = wind.read()

                if event == "Save Changes":
                    wind.close()
                    load.start()
                    time1 = time.time()
                    data = {}
                    for a in studs:
                        data[a] = []
                    for x, y in values.items():
                        x2, x1 = x.split()
                        if y:
                            data[x1].append(x2 + "=" + y)
                        else:
                            data[x1].append(x2 + "=NULL")
                    for x in data:
                        cursor.execute(f"UPDATE {cur_test} SET {' , '.join(data[x])} WHERE studentname='{x}';")
                        cnx.commit()
                    timecheck(time1)
                    load.terminate()
                    load = multiprocessing.Process(target=loading)
                    break
                
                elif event == "Discard Changes":
                    wind.close()
                    break
                
                elif event.split(":")[0] == "Up":
                    x, y = recent_focus.split()
                    x1 = studs.index(y)
                    if x1:
                        wind[f"{x} {studs[x1-1]}"].SetFocus()
                elif event.split(":")[0] == "Down":
                    x, y = recent_focus.split()
                    x1 = studs.index(y)
                    if x1 != len(studs)-1:
                        wind[f"{x} {studs[x1+1]}"].SetFocus()

                elif event.split(":")[0] == "Right":
                    x, y = recent_focus.split()
                    y1 = subs.index(x)
                    if y1 != len(subs)-1:
                        wind[f"{subs[y1 + 1]} {y}"].SetFocus()

                elif event.split(":")[0] == "Left":
                    x, y = recent_focus.split()
                    y1 = subs.index(x)
                    if y1:
                        wind[f"{subs[y1 - 1]} {y}"].SetFocus()

                elif event != " " and " " in event:
                    recent_focus = event
                    if values[event]:
                        if values[event][-1] not in ('0123456789'):
                            wind[event].update(values[event][:-1])
                            values[event] = values[event][:-1]
                        elif values[event][-1] == "0" and len(values[event]) == 1:
                            wind[event].update(values[event][:-1])
                            values[event] = values[event][:-1]
                        elif int(values[event]) > maxmark:
                            wind["Caution"].update(f"Max Marks is {maxmark}", visible=True)
                            wind[event].update(values[event][:-1])
                            values[event] = values[event][:-1]
                        elif int(values[event]) < 200:
                            wind["Caution"].update(visible=False)

        elif event == f"Remove {cur_test}":
            if yes_or_no_popup(f"All Entries In {cur_test} will be Removed.\nDo you Want To Proceed?", "Caution") == "Yes":
                cursor.execute(f'delete from tests where testname="{cur_test}"')
                cursor.execute(f'DROP TABLE {cur_test}')
                tests.remove(cur_test)
                cur_test = ""

        elif event == "Add A New Test":
            window.close()
            layout = [
                [sg.Text("Enter Test Name:- ", size=(12, None)),
                 sg.Input(key='-IN2-', enable_events=True)],
                [sg.Text("Enter Maximum Marks:- ", size=(12, None)), sg.Input(tooltip="Max Marks is 200.", size=(10, None), key='-IN-',
                                                                              enable_events=True), sg.Text("Max Marks is 200               ", font="Courier 9", visible=False, key="Caution", pad=(0, 10))],
                [sg.Text("Description:- \n(Optional)", size=(12, None)),
                 sg.Multiline(size=(30, 7))],
                [sg.Button("Add Test", key="SubmitButton",
                           button_color="red on white"), sg.Button("Cancel")]
            ]

            sub_window = sg.Window(f"Add Test To {cur_database}", layout, keep_on_top=True)

            while True:
                event, values = sub_window.read()

                if event == "SubmitButton":
                   
                    if values["-IN-"] and values["-IN2-"]:
                       
                        if values["-IN2-"] not in tests and values["-IN2-"] not in ["tests", "students", "subjects"]:
                            sub_window.close()
                            load.start()
                            time1 = time.time()
                            values[0] = values[0].replace("\n", "-n-")
                            temp = "(\"" + "\",\"".join(values.values()) + "\")"
                            cursor.execute(f'INSERT INTO tests VALUES{temp}')

                            data = ""
                            for a in subs:
                                data += a + " varchar(50)"
                                if a != subs[-1]:
                                    data += ", "
                            tests.append(values["-IN2-"])
                            cursor.execute(f'CREATE TABLE {values["-IN2-"]}(studentname varchar(50), {data})')

                            data = "('" + "'),('".join(studs) + "')"
                            cursor.execute(f'insert into {values["-IN2-"]}(studentname) values{data};')
                            cnx.commit()
                            timecheck(time1)
                            load.terminate()
                            load = multiprocessing.Process(target=loading)
                            return

                       
                        elif values["-IN2-"] in tests:
                            sub_window["Caution"].update(
                                "Test Already Exists", visible=True)
                        
                        elif values["-IN2-"] in ["tests", "students", "subjects"]:
                            sub_window["Caution"].update(
                                "Table Name Not Supported", visible=True)

                elif event == '-IN2-' and values['-IN2-']:
                    
                    if values['-IN2-'][-1] in ' !@#$%^&*()<>?/;:-}{|+-=`~*[]\',."':
                        sub_window['-IN2-'].update(values['-IN2-'][:-1]+"_")
                        values['-IN2-'] = values['-IN2-'][:-1]+"_"
                    
                    elif values['-IN2-'][-1] in ("0123456789") and len(values['-IN2-']) == 1:
                        sub_window['-IN2-'].update(values['-IN2-'][:-1]+"_")
                        values['-IN2-'] = values['-IN2-'][:-1]+"_"
                    
                    if values["-IN2-"] in tests:
                        sub_window["Caution"].update(
                            "Test Already Exists", visible=True)
                    
                    elif values["-IN2-"] in ["tests", "students", "subjects"]:
                        sub_window["Caution"].update(
                            "Table Name Not Supported", visible=True)
                    
                    else:
                        sub_window["Caution"].update(visible=False)
                    values['-IN2-'] = values['-IN2-'].lower()
                    sub_window['-IN2-'].update(values['-IN2-'].lower())

                
                elif event == '-IN-' and values['-IN-']:
                    
                    if values['-IN-'][-1] not in ('0123456789'):
                        sub_window['-IN-'].update(values['-IN-'][:-1])
                        values['-IN-'] = values['-IN-'][:-1]
                    
                    elif values['-IN-'][-1] == "0" and len(values['-IN-']) == 1:
                        sub_window['-IN-'].update(values['-IN-'][:-1])
                        values['-IN-'] = values['-IN-'][:-1]
                    
                    elif int(values["-IN-"]) > 200:
                        sub_window["Caution"].update(
                            "Max Marks is 200", visible=True)
                        sub_window['-IN-'].update(values['-IN-'][:-1])
                        values['-IN-'] = values['-IN-'][:-1]
                    
                    elif int(values["-IN-"]) < 200:
                        sub_window["Caution"].update(visible=False)
                
                elif event in (None, "Cancel"):
                    sub_window.close()
                    break

                if values["-IN-"] and values["-IN2-"] and values["-IN2-"] not in tests and values["-IN2-"] not in ["tests", "students", "subjects"]:
                    sub_window["SubmitButton"].update(
                        button_color=("white on red"))
                
                else:
                    sub_window["SubmitButton"].update(
                        button_color=("red on white"))

        
        elif event == "Go Back":
            window.close()
            break
       
        elif event == "Quit":
            exit_popup()
        
        elif event in range(0, len(tests)):
            cur_test = tests[event]
            window.Refresh()

        window.close()
        window = create_test_select_window(tests, cur_test)


def edit_class(cursor, cur_database):
    cursor.execute(f"USE {prefx + cur_database}")
    cursor.execute(f"SELECT * FROM subjects;")
    data = cursor.fetchall()
    subs = [data[i][0] for i in range(len(data))]

    cursor.execute(f"SELECT * FROM students;")
    data = cursor.fetchall()
    studs = [data[i][0] for i in range(len(data))]

    layout_edit_class = [[sg.Text(tabulate([[len(subs), len(studs)]], headers=("Count of Subjects", "Count Of Students"), tablefmt="github"), font="Courier 10")], [sg.Text("_"*60)], [sg.Button("Add Subjects"),sg.Button("Add Students")]]
                                                                                                                                                                                       

    if subs and not studs:
        layout_edit_class.append([sg.Button("Remove Subjects",
                                            button_color="white on red")])
    if studs and not subs:
        layout_edit_class.append([sg.Button("Remove Students",
                                            button_color="white on red")])

    if studs and subs:
        layout_edit_class.append([sg.Button("Remove Subjects", 
                                            button_color="white on red"),
                                            sg.Button("Remove Students", 
                                            button_color="white on red")])

    window3 = sg.Window(cur_database, layout_edit_class,
                        element_justification="c", 
                        resizable=True, 
                        keep_on_top=True)
    event3, values3 = window3.read()

    if event3 == "Add Students":
        add_students(values, cur_database)

    elif event3 == "Add Subjects":
        add_subjects(values, cur_database)

    elif event3 == "Remove Students":
        remove_students(values, cur_database)

    elif event3 == "Remove Subjects":
        remove_subjects(values, cur_database)
    
    window3.close()


def class_init(class_name, cursor):
    cursor.execute(f"CREATE TABLE {prefx + class_name}.subjects(subjectname char(50));")
    cursor.execute(f"CREATE TABLE {prefx + class_name}.students(studentname char(50));")
    cursor.execute(f"CREATE TABLE {prefx + class_name}.tests(testname varchar(50), maxmark int, description text);")


def add_subjects(values, cur_database):
    cursor.execute(f"USE {prefx + cur_database}")
    cursor.execute(f"SELECT * FROM subjects;")
    data = cursor.fetchall()
    subs = [data[i][0] for i in range(len(data))]
    added = []
   
    while True:
        temp = (subs+added).copy()
        l = len(subs+added)
        layout2 = [[sg.Text("Existing Subjects:-\n\n"+tabulate([subs[i:i+4] for i in range(0, len(subs), 4)]), font="Courier 10")],
                   [sg.Text("Added Subjects:-\n\n"+tabulate([added[i:i+4]
                                                             for i in range(0, len(added), 4)]), font="Courier 10")],
                   [sg.InputText()],
                   [sg.Submit("Add Subject"), sg.Submit("Confirm"), sg.Submit("Undo"), sg.Cancel()]]
        window2 = sg.Window('Mark Registry', layout2,
                            resizable=True, disable_close=True, 
                            use_default_focus=True, keep_on_top=True)
        event2, values2 = window2.read()
        
        if event2 == "Cancel":
            window2.close()
            return "Quit"
        
        elif event2 == "Add Subject" and values2[0].strip() != "":
            
            if values2[0].lower().replace(" ", "_") not in (added+subs):
                added.append(values2[0].lower().replace(" ", "_"))
            
            else:
                notif_popup(
                    values2[0].lower()+" already added/exists.           ", "Title Exists")
        
        elif event2 == "Undo" and added:
            added.pop(-1)
        
        elif event2 == "Confirm":
            
            if added:
                temp = "(\"" + "\"),(\"".join(added) + "\")"
                cursor.execute(f"USE {prefx + cur_database};")
                cursor.execute(f"insert into subjects values{temp};")

                cursor.execute(f"select testname from tests;")
                data_fetched = cursor.fetchall()
                tests = [data_fetched[i][0] for i in range(len(data_fetched))]
                cmds = "ADD COLUMN " + \
                    " varchar(50), ADD COLUMN ".join(added) + " varchar(50);"
                for a in tests:
                    cursor.execute(f"ALTER TABLE {a} {cmds}")

                cnx.commit()
                window2.close()
                break
            
            else:
                notif_popup("Enter A Name to Proceed", "Empty Input")
        
        window2.close()


def add_students(values, cur_database):
    cursor.execute(f"USE {prefx + cur_database}")
    cursor.execute(f"SELECT * FROM students;")
    data = cursor.fetchall()
    subs = [data[i][0] for i in range(len(data))]
    added = []
    
    while True:
        temp = (subs+added).copy()
        l = len(subs+added)
        layout2 = [[sg.Text("Existing Students:-\n\n"+tabulate([subs[i:i+4] for i in range(0, len(subs), 4)]), font="Courier 10")],
                   [sg.Text("Added Students:-\n\n"+tabulate([added[i:i+4]
                                                             for i in range(0, len(added), 4)]), font="Courier 10")],
                   [sg.InputText()],
                   [sg.Submit("Add Student"), sg.Submit("Confirm"), sg.Submit("Undo"), sg.Cancel()]]
        window2 = sg.Window('Mark Registry', layout2,
                            resizable=True, disable_close=True, use_default_focus=True, keep_on_top=True)
        event2, values2 = window2.read()
        
        if event2 == "Cancel":
            window2.close()
            return "Quit"
       
        elif event2 == "Add Student" and values2[0].strip() != "":
            
            if values2[0].lower().replace(" ", "_") not in (added+subs):
                added.append(values2[0].lower().replace(" ", "_"))
            
            else:
                notif_popup(
                    values2[0].lower().replace(" ", "_")+" already added/exists.          ", "Title Exists")
        
        elif event2 == "Undo" and added:
            added.pop(-1)
            window2.close()
        
        elif event2 == "Confirm":
            
            if added:
                
                temp = "(\"" + "\"),(\"".join(added) + "\")"
                cursor.execute(f"USE {prefx + cur_database};")
                cursor.execute(f"insert into students values{temp};")
                cursor.execute(f"select testname from tests;")
                data_fetched = cursor.fetchall()
                tests = [data_fetched[i][0] for i in range(len(data_fetched))]
                cmds = "('" + "'),('".join(added) + "')"
                
                for a in tests:
                    cursor.execute(f'insert into {a}(studentname) values{cmds};')

                cnx.commit()
                window2.close()
                break
            
            else:
                notif_popup("Enter A Name to Proceed            ",
                            "Empty Input")
        window2.close()


def remove_subjects(values, cur_database):
    cursor.execute(f"USE {prefx + cur_database}")
    cursor.execute(f"SELECT * FROM subjects;")
    data = cursor.fetchall()
    subs = [data[i][0] for i in range(len(data))]
    
    if subs:
        layout = [[sg.Text("Select Subjects To Remove")], ]
        for a in range(4):
            layout.append([])
            for b in range(a, len(subs), 4):
                layout[-1].append(sg.Checkbox(subs[b], size=(12, 1)))
        layout.append([sg.Submit(), sg.Cancel()])
    window = sg.Window("Remove Subjects", layout, keep_on_top=True)
    
    while True:
        event1, values1 = window.read()
       
        if event1 == "Submit" and (True in values1.values()):
            names = []
            i = 0
            for a in range(4):
                for b in range(a, len(subs), 4):
                    if values1[i]:
                        names.append(subs[b])
                    i += 1
            choice = yes_or_no_popup("The Following subjects Marks Will Be Dropped.\n\n"+tabulate(
                [names[i:i+4] for i in range(0, len(names), 4)]), "Confirm")
            
            if choice == "Yes":
                cursor.execute(f"USE {prefx + cur_database};")
                cursor.execute(f"DELETE FROM subjects WHERE subjectname IN {str(names).replace('[','(').replace(']',')')};")
                cursor.execute(f"select testname from tests;")
                data_fetched = cursor.fetchall()
                tests = [data_fetched[i][0] for i in range(len(data_fetched))]
                cmds = "DROP " + " , DROP ".join(names)
                for a in tests:
                    cursor.execute(f"ALTER TABLE {a} {cmds};")
                window.close()
                break
            
            else:
                continue
        
        elif event1 in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return


def remove_students(values, cur_database):
    cursor.execute(f"USE {prefx + cur_database}")
    cursor.execute(f"SELECT * FROM students;")
    data = cursor.fetchall()
    subs = [data[i][0] for i in range(len(data))]
    
    if subs:
        layout = [[sg.Text("Select Students To Remove")], ]
        layout_mini = []
        temp = [subs[i:i+2] for i in range(0, len(subs), 2)]
        for a in temp:
            layout_mini.append([])
            for b in a:
                layout_mini[-1].append(sg.Checkbox(b, size=(12, 1)))

        layout.append(
            [sg.Column(layout_mini, size=(245, 115), scrollable=True, vertical_scroll_only=True)])
        layout.append([sg.Submit(), sg.Cancel()])
    
    else:
        notif_popup(f"No Students Found in {cur_database}                ", "No Students Found")
        return
    window = sg.Window("Remove Students", layout, keep_on_top=True)
    
    while True:
       
        event1, values1 = window.read()
        if event1 == "Submit" and (True in values1.values()):
            names = []
            for x, y in values1.items():
                if y:
                    names.append(subs[x])
            choice = yes_or_no_popup(("The Following Students Marks Will Be Dropped.\nDo You Want To Proceed?\n\n"+tabulate(
                [names[i:i+4] for i in range(0, len(names), 4)])), "Confirm")

            if choice == "Yes":
                cursor.execute(f"USE {prefx + cur_database};")
                cursor.execute(f"DELETE FROM students WHERE studentname IN {str(names).replace('[','(').replace(']',')')};")
                cursor.execute(f"select testname from tests;")
                data_fetched = cursor.fetchall()
                tests = [data_fetched[i][0] for i in range(len(data_fetched))]
                cmds = "('" + "'),('".join(names) + "')"
                for a in tests:
                    cursor.execute(f"delete from {a} WHERE studentname IN {str(names).replace('[','(').replace(']',')')};")
                window.close()
                break
            else:
                continue
        elif event1 in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return


def timecheck(time1, i=3):
    while time.time() - time1 < i:
        time.sleep(0.1)
        pass


def loading():
    imgdata = b'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'
    layout = [[sg.Text("Loading...", 
        pad=(0, 0), 
        background_color="White", 
        text_color="black", 
        size=(20, 1), 
        justification="c")], 
    [sg.Image(data=imgdata, 
        key=f"Prog_bar", 
        pad=(0, 0))]]

    window4 = sg.Window("title", layout, 
        keep_on_top=True, 
        no_titlebar=True, 
        margins=(2, 2), 
        element_justification="c", 
        background_color="White")

    time1=time.time()
    while time.time() - time1 < 6:
        event, values = window4.Read(timeout=80)
        window4.FindElement(f"Prog_bar").UpdateAnimation(imgdata, time_between_frames=80)
    
    window4.Close()


if __name__ == "__main__":
    
    try:
        themes = list(sg.LOOK_AND_FEEL_TABLE.keys())
        
        try:
            with open("CONFIG", "rb") as f:
                dict1 = pickle.load(f)
                theme = dict1["theme"]
        
        except FileNotFoundError:
            theme = random.choice(themes)
            with open("CONFIG", "wb") as f:
                dict1 = {"theme": theme, "username": "",
                         "host": "", "password": ""}
                pickle.dump(dict1, f)

        sg.ChangeLookAndFeel(theme)
        themes.insert(0, "Random")
        prefx = "markdb_"

        while True:
            
            if dict1["username"]:
                try:
                    cnx = mysql.connector.connect(
                        user=dict1["username"], password=dict1["password"], host=dict1["host"])
                    cursor = cnx.cursor()
                    break
                except:
                    pass
            
            while True:
                layout = [[sg.Text(intro, relief=sg.RELIEF_RIDGE, font=("Helvetica", 5), key="intro1")],
                          [sg.Column([[sg.Text("Username:- ")], [sg.Text("Host:- ")], [sg.Text("Password:- ")]]), sg.Column(
                              [[sg.Input("root")], [sg.Input("localhost")], [sg.Input(password_char="*")]])],
                          [sg.Button("Login", bind_return_key=True,
                                     pad=(10, 0)), sg.Button("Quit")]
                          ]
                event, values = sg.Window(
                    "Login", layout, disable_close=True).read(close=True)

                if event == "Login":
                    load = multiprocessing.Process(target=loading)
                    load.start()
                    time1 = time.time()
                    try:
                        cnx = mysql.connector.connect(
                            user=values[0], password=values[2], host=values[1])
                        cursor = cnx.cursor()
                        with open("CONFIG", "wb") as file:
                            dict1["username"] = values[0]
                            dict1["password"] = values[2]
                            dict1["host"] = values[1]
                            pickle.dump(dict1, file)
                    
                    except mysql.connector.Error as err:
                        load.terminate()
                        notif_popup(
                            "Login Failed... Try again...", "ʕっ•́ᴥ•̀ʔっ")
                    else:
                        timecheck(time1)
                        load.terminate()
                        break

                elif event == "Quit":
                    exit_popup()

        cursor.execute("show databases;")
        databases = cursor.fetchall()
        databases = [databases[i][0].replace(prefx, "") for i in range(
            len(databases)) if prefx in databases[i][0]]

        check_empty_and_add(databases)

        window = create_class_select_window()
        cur_database = ""
        load = multiprocessing.Process(target=loading)
        
        while True:
            event, values = window.read()

            if event == "Quit":
                cnx.commit()
                exit_popup()
                continue

            elif event == "Add Class":
                window.close()
                add_class(databases, cursor)

            elif event == f"Delete Class {cur_database}":
                window.close()
                delete_class(databases, cursor)

            elif event == f"Use Class {cur_database}":
                window.close()
                select_class(cursor, cur_database)

            elif event == f"Edit Class {cur_database}":
                window.close()
                edit_class(cursor, cur_database)

            elif event in range(len(databases)):
                if cur_database in databases and int(event) == databases.index(cur_database):
                    continue
                cur_database = databases[event]
                window.close()
            
            elif event == "Change Theme":
                window.close()
                themes_temp = [themes[i::4] for i in range(4)]
                wind = change_theme_window(theme)
                
                while True:
                    event, values = wind.read()
                    
                    if event == "Save Changes":
                        theme = theme2
                        with open("CONFIG", "rb") as f:
                            dict1 = pickle.load(f)
                        dict1["theme"] = theme
                        with open("CONFIG", "wb") as f:
                            pickle.dump(dict1, f)
                        wind.close()
                        break
                    
                    elif event == "Discard Changes" or event == sg.WIN_CLOSED:
                        sg.ChangeLookAndFeel(theme)
                        wind.close()
                        break
                    
                    else:
                        wind.close()
                        del wind
                        load.start()
                        time1 = time.time()
                        if event == "Random":
                            event = random.choice(themes)
                        sg.ChangeLookAndFeel(event)
                        wind = change_theme_window(event)
                        theme2 = event
                        timecheck(time1, 2)
                        load.terminate()
                        load = multiprocessing.Process(target=loading)
            else:
                window.close()
                continue

            window = create_class_select_window(cur_database)
   
    except:
        sg.change_look_and_feel("Darkpurple")
        
        if str(exc_info()[0]) != "<class 'SystemExit'>":
            sg.popup_error(exc_info()[1], title="Unexpected Error")
