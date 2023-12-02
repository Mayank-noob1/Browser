# <b>JAD</b> browser.
- I have a vacation this December, so I am working on building a browser project.
- I will write progress in this README.

### Resources:
1) [How do browsers work?](https://web.dev/articles/howbrowserswork)
2) [Web browser Engineering book](https://browser.engineering)


### Target:
One chapter of the book in two days.

### How to run:
I don't know why, bs4 module is not detected by python3. Actually my settings are pretty messed up as I didn't how to setup back in my first year and I am carrying those settings around.
So how to run section is for me to remember how to run.
- #### Chapter1.py & Chapter2.py & Chapter3.py & Chapter4.py;
    - Command -> python3-intel64 Chapter<i_>.py <site_address>
    - Here site address must have http:// or https:// before URL.

### What I learnt:
Here is a section for me to remember what I learnt from the chapter.
 - #### Chapter 1:
    - Brushed up my network concepts.
    - Made a basic url request fetcher.
    - Added TLS wrap over HTTP for HTTPS.
    - SOCK_STREAM -> For a stream of data (any length) and SOCK_DGRAM for fixed-sized data.
    - Port : HTTP -> 80 , HTTPS -> 443.
- #### Chapter 2:
    - Tkinter X-position is from left to right and Y-position is from top to bottom.
    - Bind Configure Event for resizing.
    - ScrollBar is an object in Tk that can integrate to canvas or frame (Somehow it is not working for me).
- #### Chapter 3:
    - Every character has a baseline. It has an ascent and descent. So we render text by normalising all values such that no collision occurs.
    - Font caching is good for faster rendering.
- #### Chapter 4:
    - We made the parsing context sensitive by knowing implicit closing tags.
    - DOM ( Document Object Model ) converts any HTML or XML or related format to a tree. Which is helpful in parsing the document.
    - Attributes are really tricky to handle. ( Try handling attribute ).
      
### Fixes:
1) Python reinstall and clean up for modules to run.
2) Scrollbar not scrolling the canvas.
3) Touchpad event not working (if it is considered as mouse event).
4) Need to handle entities like &lt and &gt.
5) Can add support for address with no http:// or https://.
