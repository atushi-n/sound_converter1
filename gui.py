import tkinter as tk

class Template(tk.Tk):
    def __init__(self, **kwargs):
        super(Template, self).__init__()
        self.title(kwargs.get("title", "radio"))
        self.geometry("+{}+{}".format(*kwargs.get("pos", (500, 500))))
        self.resizable(*kwargs.get("resize", (1, 1)))
        try:
            self.iconbitmap(kwargs.get("icon", None))
        except:
            if kwargs.get("icon", None) is not None:
                icon_name = kwargs.get("icon")
                icon_img = ImageTk.PhotoImage(file=icon_name)
                self.tk.call("wm", "iconphoto", self._w, icon_img)

    def run(self):
        self.mainloop()