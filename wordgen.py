from Tkinter import *
from itertools import product
from tkFileDialog import asksaveasfilename
import string

root = Tk()
class Application(Frame):

    def onKeyRelease(self,e):
        print e.__dict__
        w = e.widget
        value = w.get()
        print w.__dict__

        tov = int(w['to'])  
        fromv = int(w['from'])
        try:
            if e.keysym != 'BackSpace':
                int(value)
        except:
            w.delete(0,10)
            w.insert(0,tov)
            return

        if e.keysym != 'BackSpace':   
            if int(value) > tov:
                w.delete(0,10)
                w.insert(0,tov)
            elif int(value) < fromv:
                w.delete(0,10)
                w.insert(0,fromv)

    def generate_words(self):
        pool = ''
        file_handler = None

        if self.write_to_file.get():
            fname = asksaveasfilename(parent=root)
            if fname:
                file_handler = open(fname,'w')

        if self.alphabet.get():
            pool += string.ascii_letters
        if self.numbers.get():
            pool += string.digits
        if self.special.get():
            pool += string.punctuation
        for nb_chars in range(int(self.min_sizeSpin.get()),int(self.max_sizeSpin.get())+1):
            for w in product(pool,repeat=nb_chars):
                if file_handler is not None:
                    file_handler.write(''.join(w) + "\n")
                
                if self.output_to_console.get():
                    print w
        if self.write_to_file.get():
            self.quit()

    def change_button_and_validate_button(self):
        if self.write_to_file.get():
            self.generateBtn["text"] = "Generate to file..."
        else:
            self.generateBtn["text"] = "Generate"
        self.check_generate_validity()

    def check_generate_validity(self):
        mini = self.min_sizeSpin.get()
        maxi = self.max_sizeSpin.get()

        min_lt_max = mini < maxi
        write_or_console = (self.write_to_file.get() or self.output_to_console.get())
        pool_not_empty = self.alphabet.get() or self.numbers.get() or self.special.get()
        
        self.generateBtn["state"] = NORMAL if min_lt_max and write_or_console and pool_not_empty else DISABLED

    def createWidgets(self):
        self.pack(fill=BOTH, expand=1)
        self.rowconfigure(2)
        self.columnconfigure(1)

        self.alphabet = IntVar()
        self.numbers = IntVar()
        self.special = IntVar()
        self.write_to_file = IntVar()
        self.output_to_console = IntVar()

        self.quitBtn = Button(self)
        self.quitBtn["text"] = "QUIT"
        self.quitBtn["bg"]   = "red"
        self.quitBtn["command"] =  self.quit

        self.generateBtn = Button(self)
        self.generateBtn["text"] = "Generate",
        self.generateBtn["command"] = self.generate_words
        self.generateBtn["state"] = DISABLED


        self.alphaCb = Checkbutton(self,text="Alphabet", variable=self.alphabet, command=self.check_generate_validity)
        self.numbersCb = Checkbutton(self,text="Numbers", variable=self.numbers, command=self.check_generate_validity)
        self.specialCb = Checkbutton(self,text="Special", variable=self.special, command=self.check_generate_validity)

        self.write_fileCb = Checkbutton(self,text="Write to file", variable=self.write_to_file, command=self.change_button_and_validate_button)
        self.output_consoleCb = Checkbutton(self,text="Output to console", variable=self.output_to_console, command=self.check_generate_validity)


        self.minLabel = Label(self,text='Min')
        self.maxLabel = Label(self,text='Max')

        self.min_sizeSpin = Spinbox(self, from_=1, to=10, command=self.check_generate_validity)
        self.max_sizeSpin = Spinbox(self, from_=2, to=10, command=self.check_generate_validity)

        self.min_sizeSpin.bind("<KeyRelease>", self.onKeyRelease)
        self.max_sizeSpin.bind("<KeyRelease>", self.onKeyRelease)

        self.alphaCb.pack({"side": "right"})
        self.numbersCb.pack({"side": "right"})
        self.specialCb.pack({"side": "right"})
        self.write_fileCb.pack({"side": "right"})
        self.output_consoleCb.pack({"side": "right"})

        self.minLabel.pack({'side':'left'})
        self.min_sizeSpin.pack({'side':'left'})
        self.maxLabel.pack({'side':'left'})
        self.max_sizeSpin.pack({'side':'left'})

        self.generateBtn.pack({"side": "left"})
        self.quitBtn.pack()

        self.alphaCb.toggle()
        self.numbersCb.toggle()

        self.write_fileCb.invoke()


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

app = Application(master=root)
app.mainloop()
root.destroy()