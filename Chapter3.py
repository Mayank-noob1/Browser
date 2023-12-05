from Chapter1 import *
import tkinter
import tkinter.font

WIDTH = 1400
HEIGHT = 800
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
weight_ = "normal"
style_ = "roman"
FONTS = {}

class Text:
    def __init__(self, text):
        self.text = text

class Tag:
    def __init__(self, tag):
        self.tag = tag

def lex(body):
    out = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text: out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))
    return out

def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight, slant=slant)
        FONTS[key] = font
    return FONTS[key]

class Layout:
    def __init__(self,tokens):
        self.display_list=[]
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.line = []
        for tok in tokens:
            self.token(tok)
        self.flush() 

    def flush(self):
        if not self.line: return

        max_ascent = max([font.metrics("ascent") for (x, word, font) in self.line])
        baseline = self.cursor_y + 1.25 * max_ascent

        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))

        max_descent = max([font.metrics("descent") for (x, word, font) in self.line])

        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP
        self.line = []
    
    def word(self,word):
        font = get_font(size=self.size, weight=self.weight, slant=self.style)    
        w = font.measure(text=word)
        if self.cursor_x + w > WIDTH - HSTEP:
            self.flush()
        self.line.append((self.cursor_x,word,font))
        self.cursor_x += w + font.measure(' ')

    def token(self,tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size += 2
        elif tok.tag == "/small":
            self.size -= 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Jad Browser")
        self.scroll = 0
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )

        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Configure>",self.resize)
        self.window.bind("<MouseWheel>",self.onMouseScroll)

        self.vbar = tkinter.Scrollbar(self.window,orient="vertical")
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.vbar.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=1)

        self.bi_times = tkinter.font.Font(
            family="Times",
            size=16,
            weight="bold",
            slant="italic",
        )

    def load(self, url):
        headers, body = URL(url).request()
        self.source = body
        self.tokens = lex(body)
        self.display_list = Layout(self.tokens).display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c, f in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + f.metrics("linespace") < self.scroll: continue
            self.canvas.create_text(x, y-self.scroll, text=c,font=f,anchor="nw")

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
        self.display_list = Layout(self.tokens).display_list
        self.draw()

    def onMouseScroll(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.draw()

if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()
