import PySimpleGUI as sg
from pathlib import Path
import subprocess as sp
import csv
from sudoku import sudoku

sg.Window._move_all_windows = True
DEFAULT_MASK_RATE = 0.7


def makewindow(theme=None):
    if theme:
        sg.theme(theme)
    sg.set_options(font=("Microsoft JhengHei", 16))
    layout = [
        [sg.Text('code difference console', size=(80, 1), justification='center', font=("Helvetica", 25),
                 relief=sg.RELIEF_RIDGE)],
        [sg.B('Change Theme'), sg.B('sudoku')],
        [
            [sg.Combo(sorted(sg.user_settings_get_entry('-filenames1-', [])),
                      default_value=sg.user_settings_get_entry('-last filename1-', ''), size=(50, 1),
                      key='-FILENAME1-'),
             sg.FileBrowse(file_types=(("ALL Files", "*.*"),)), sg.B('Clear History1')],
            [sg.Combo(sorted(sg.user_settings_get_entry('-filenames2-', [])),
                      default_value=sg.user_settings_get_entry('-last filename2-', ''), size=(50, 1),
                      key='-FILENAME2-'),
             sg.FileBrowse(file_types=(("ALL Files", "*.*"),)), sg.B('Clear History2')],
        ],
        [sg.MLine(default_text='first code', key='file1', size=(60, 15)),
         sg.MLine(default_text='Second code', key='file2', size=(60, 15))],
        [sg.Button('Ok', bind_return_key=True), sg.Button('Exit'), sg.Button('Highlight')],
        [
            sg.Text('auto judge result', size=(15, 1), justification='left', font=("Helvetica", 25),
                    relief=sg.RELIEF_RIDGE),
            sg.InputText('', key='-judge-'),
            sg.B('get judge result')
        ],
        [sg.Text("User confirm"), sg.CBox("yes", key='-yeskey-'), sg.CBox("no", key='-nokey-'), sg.B('confirm')],
        [sg.Text("final result"),
         sg.InputText(' ', size=(20, 1), key='-final-', justification='left', font=("Helvetica", 25))]
    ]
    return sg.Window('201840009tys', layout, finalize=True, keep_on_top=True, grab_anywhere=False,
                     transparent_color=sg.theme_background_color(), no_titlebar=False)


def title_bar(title, text_color, background_color):
    bc = background_color
    tc = text_color
    font = 'Helvetica 12'

    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0),
                   background_color=bc),
            sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, font=font, key='-MINIMIZE-'),
                     sg.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]],
                   element_justification='r', key='-C-', grab=True,
                   pad=(0, 0), background_color=bc)]


def main():
    top_window = makewindow("Dark Blue 2")
    filename0 = ""
    filename1 = ""
    filename2 = ""
    font2 = ('Courier New', 15, 'bold')
    multiline1 = top_window['file1']
    widget1 = multiline1.Widget
    widget1.tag_config('HIGHLIGHT', foreground='white', background='blue', font=font2)
    multiline2 = top_window['file2']
    widget2 = multiline2.Widget
    widget2.tag_config('HIGHLIGHT', foreground='white', background='blue', font=font2)
    while True:
        event, values = top_window.read()
        # if event == sg.WINDOW_CLOSED:
        #     break
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        if event == 'Ok':
            filename1 = values['-FILENAME1-']
            filename2 = values['-FILENAME2-']
            # filename0 = values['-FILENAME0-']
            if Path(filename1).is_file() and Path(filename2).is_file():
                try:
                    with open(filename1, "rt", encoding='utf-8') as f:
                        text = f.read()
                        top_window['file1'].update("".join(text))
                except Exception as e:
                    print("Error: ", e)

                try:
                    with open(filename2, "rt", encoding='utf-8') as f:
                        text = f.read()
                        top_window['file2'].update("".join(text))
                except Exception as e:
                    print("Error: ", e)

            sg.user_settings_set_entry('-filenames1-',
                                       list(set(sg.user_settings_get_entry('-filenames1-', []) + [
                                           values['-FILENAME1-'], ])))
            sg.user_settings_set_entry('-filenames2-',
                                       list(set(sg.user_settings_get_entry('-filenames2-', []) + [
                                           values['-FILENAME2-'], ])))
            sg.user_settings_set_entry('-last filename1-', values['-FILENAME1-'])
            sg.user_settings_set_entry('-last filename2-', values['-FILENAME2-'])
            top_window['-FILENAME1-'].update(values=list(set(sg.user_settings_get_entry('-filenames1-', []))),
                                             value=values['-FILENAME1-'])
            top_window['-FILENAME2-'].update(values=list(set(sg.user_settings_get_entry('-filenames2-', []))),
                                             value=values['-FILENAME2-'])
            # with open('in.txt', 'w') as f:
            #     f.write(filename0)
            #     f.write('\n')
            #     f.write(filename1[0:-4] + '.out')
            #     f.write('\n')
            #     f.write(filename2[0:-4] + '.out')

            f.close()

        if event == 'Clear History1':
            sg.user_settings_set_entry('-filenames1-', [])
            sg.user_settings_set_entry('-last filename1-', '')
            top_window['-FILENAME1-'].update(values=[], value='')

        if event == 'Clear History2':
            sg.user_settings_set_entry('-filenames2-', [])
            sg.user_settings_set_entry('-last filename2-', '')
            top_window['-FILENAME2-'].update(values=[], value='')

        if event == 'get judge result':
            with open("equal.csv", 'r') as equ:
                reader = csv.reader(equ)
                flag = 0
                for row in reader:
                    pro1 = filename1[42:len(filename1)]
                    pro2 = filename2[42:len(filename2)]
                    # print(row)
                    # print(pro1 + " " + pro2)
                    # print(pro2 + " " + pro1)
                    if pro1 + " " + pro2 in row or pro2 + " " + pro1 in row:
                        # print(row)
                        # print(pro1+" "+pro2)
                        # print(pro2+" "+pro1)
                        print("yes")
                        top_window['-judge-'].update("yes")
                        flag = 1
                        break
                if flag == 0:
                    print("no")
                    top_window['-judge-'].update("no")

        if event == "confirm":
            if values['-yeskey-'] == True:
                top_window['-final-'].update("equal")
            elif values['-nokey-'] == True:
                top_window['-final-'].update("inequal")

        if event == 'Change Theme':  # Theme button clicked, so get new theme and restart window
            event, values = sg.Window('Choose Theme', [
                [sg.Combo(sg.theme_list(), readonly=True, k='-THEME LIST-'), sg.OK(), sg.Cancel()]]).read(close=True)
            print(event, values)
            if event == 'OK':
                top_window.close()
                top_window = makewindow(values['-THEME LIST-'])

        if event == 'sudoku':
            sudoku(DEFAULT_MASK_RATE)

        if event == 'Highlight':
            # widget1.tag_add('HIGHLIGHT','1.2','1.7')
            with open(filename1, 'rb') as file1:
                with open(filename2, 'rb') as file2:
                    a = file1.readlines()
                    b = file2.readlines()

                for i in range(0,len(a),1):
                    if a[i]!=b[i]:
                        widget1.tag_add('HIGHLIGHT', str(i+1)+'.0', str(i+1)+'.'+str(len(a[i])))
                        widget2.tag_add('HIGHLIGHT', str(i + 1) + '.0', str(i + 1) + '.' + str(len(b[i])))


    top_window.close()


if __name__ == '__main__':
    main()
