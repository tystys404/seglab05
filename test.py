import PySimpleGUI as sg

text = """
This program is designed to turn a black and white image into a double-knit template.
If your image doesn't display as desired, adjusting the contrast might help.
""".strip()

lines = text.split('\n')
index1 = lines[0].index("image")
index2 = lines[1].index("image")
indexes = [(f'1.{index1}', f'1.{index1+5}'), (f'2.{index2}', f'2.{index2+5}')]

sg.theme('DarkBlue3')
font1 = ('Courier New', 10)
font2 = ('Courier New', 10, 'bold')
sg.set_options(font=font1)

layout = [
    [sg.Multiline(text, size=(40, 8), key='-MULTILINE')],
    [sg.Push(), sg.Button('Highlight'), sg.Button('Remove')],
]
window = sg.Window('Title', layout, finalize=True)
multiline = window['-MULTILINE']
widget = multiline.Widget
widget.tag_config('HIGHLIGHT', foreground='white', background='blue', font=font2)
# widget.tag_config('HIGHLIGHT', foreground=multiline.BackgroundColor, background=multiline.TextColor, font=font2)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'Highlight':
        for index1, index2 in indexes:
            widget.tag_add('HIGHLIGHT', index1, index2)
        window['Highlight'].update(disabled=True)
    elif event == 'Remove':
        for index1, index2 in indexes:
            widget.tag_remove('HIGHLIGHT', index1, index2)
        window['Highlight'].update(disabled=False)

window.close()