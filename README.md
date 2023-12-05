# <b>JAD</b> browser
- I have a vacation this December, so I am working on building a browser project.
- I will write progress in this README.

### Resources:
1) [How do browsers work?](https://web.dev/articles/howbrowserswork)
2) [Web browser Engineering book](https://browser.engineering)


### Target:
One chapter of the book in two days.

### How to run:
This for me to remember and fix my environment variables and all the packages installed.
- Command -> python3-intel64 Chapter<i_>.py <site_address>
- Here site address must have http:// or https:// before URL.

### What I learned:
Here is a section for me to remember what I learned from the chapter.
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
- #### Chapter 5:
    - We finally made a render tree. We created a render tree on the HTML tree.
    - We created two heterogenous nodes for the tree. One type of node is the head which doesn't have any parent and the second type of node which is the main/recursive node.
    - Rendering is done with relative position from the parent node.
    - Rectangle/Frame is laid first then the text is rendered.
    - In the recursive pass we first evaluate horizontal width then in the return of function we get the vertical height of each node.
 - #### Chapter 6:
    - Digital Principle: produce maximally conformant output but accept even minimally conformant input.
    - We added CSS support.
    - Css statments are of the form <selector_tag> {[PROPERTY:VALUE;]*}
    - We have to take care of normal and relative url.
    - We stored each node's property in one pass and then painted node.
      
### Fixes:
1) Python reinstall and clean up for modules to run.
2) Scrollbar not scrolling as it is written on canvas. Need to add a frame and put the whole tree into the frame?.
3) Touchpad event not working (if it is considered as a mouse event).
4) Need to handle entities like &lt and &gt.
5) Can add support for address with no http:// or https://.
6) Add support for list items by bullet points and indentation.

### Need to read again:
- Chapter 6
