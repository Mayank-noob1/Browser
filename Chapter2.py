from Chapter1 import *
import tkinter
import tkinter.font

WIDTH = 1400
HEIGHT = 800
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
    return text
        
def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if (c == '\n'):
            display_list.append((cursor_x, cursor_y, c))
            cursor_y += VSTEP//9
        else:
            display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.scroll = 0
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
        )
        self.data= ""
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Configure>",self.resize)
        self.window.bind_all("<MouseWheel>",self.onMouseScroll)

        self.vbar = tkinter.Scrollbar(self.window,orient="vertical")
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.vbar.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=1)

    def load(self, url):
        headers, body = request(url)
        self.data = lex(body)
        self.display_list = layout(self.data)
        self.draw()
        print(self.data)

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y-self.scroll, text=c)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        self.scroll -= SCROLL_STEP
        self.draw()
    
    def resize(self,e):
        global HEIGHT,WIDTH
        HEIGHT = self.window.winfo_height()
        WIDTH = self.window.winfo_width()
        self.display_list = layout(self.data)
        self.draw()

    def onMouseScroll(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.draw()



if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()