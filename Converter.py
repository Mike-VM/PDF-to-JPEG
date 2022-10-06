import tkinter as tk
import fitz
import PySimpleGUI as sg
import os.path


def preview(file):  # Provides cover page preview for the right UI pane
    doc = fitz.open(file)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=55)
    pix.save("page-%i.jpeg" % page.number)
    pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
    imgdata = pix1.tobytes("ppm")
    return tk.PhotoImage(data=imgdata)


def convert_to_jpeg(file):
    output = sg.popup_get_file("", save_as=True, no_window=True)
    doc = fitz.open(file)
    while True:
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            pix.save(output + '-%i.jpeg' % page.number)
        sg.popup_notify("Done!")
        break


# --------------------------------- Layout ---------------------------------

left_col = [[sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-FILE LIST-')],
            [sg.Button("Convert", enable_events=True, key='-CONVERT-')]]

images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40, 1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]

# ----- Full layout -----
layout = [
    [sg.Column(left_col, element_justification='c'), sg.VSeperator(), sg.Column(images_col, element_justification='c')]]

# --------------------------------- Window ---------------------------------

window = sg.Window('PDF to JPEG Converter', layout, resizable=True)

# --------------------------------- Event Loop ---------------------------------

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-FOLDER-':
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith(".pdf")]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':  # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            window['-IMAGE-'].update(data=preview(filename))
        except Exception as E:
            print(f'** Error {E} **')
            pass
    if event == '-CONVERT-':
        try:
            convert_to_jpeg(filename)
        except:
            sg.popup_notify(
                "Please select a file first")  # in case the user did not select anything and pressed convert

window.close()
