from tkinter import *


bg_color = "#303030"
fg_color = "#d0d0d0"
active_bg = "#404040"
active_fg = "#e0e0e0"
select_bg = "#5050f0"
default_font = ("Courier", 10)

button_style = {"background": bg_color,
                "foreground": fg_color,
                "activebackground": active_bg,
                "activeforeground": active_fg,
                "relief": RAISED,
                "font": default_font}
label_style = {"background": bg_color,
               "foreground": fg_color,
               "relief": FLAT,
               "font": default_font}
frame_style = {"background": bg_color,
               "borderwidth": 0}
listbox_style = {"background": active_bg,
                 "foreground": active_fg,
                 "font": default_font,
                 "relief": FLAT,
                 "highlightthickness": 0,
                 "selectbackground": select_bg}
text_style = {"background": active_bg,
              "foreground": active_fg,
              "font": default_font,
              "relief": FLAT,
              "highlightthickness": 0,
              "selectbackground": select_bg,
              "insertbackground": active_fg}

dark_img: PhotoImage
light_img: PhotoImage
insert_img: PhotoImage


class Container(Frame):

    bg_color: str = bg_color
    depressed_bg_color: str = "#282828"

    def __init__(self, parent):
        super().__init__(parent, **frame_style)
        self.config(borderwidth=5, relief=RAISED)

        self.bind("<ButtonPress-1>", self.press)
        self.bind("<ButtonRelease-1>", self.release)

    def press(self, e=None):
        self.config(background=self.depressed_bg_color, relief=SUNKEN)

    def release(self, e=None):
        self.config(background=self.bg_color, relief=RAISED)


class Divider(Container):
    def __init__(self, parent, small=False):
        super().__init__(parent)

        self.config(borderwidth=0)

        size = 70
        if small:
            self.config(width=size/2)
        else:
            self.config(width=size)

        plus = Label(self, **label_style)
        plus.config(image=insert_img, borderwidth=4, relief=RAISED)
        plus.place(rely=.5, relx=.5, anchor=CENTER)


class Period(Container):
    text: str
    is_dark: bool

    tone: Label
    label: Label

    def __init__(self, parent, text: str, is_dark: bool):
        super().__init__(parent)

        self.text = text
        self.is_dark = is_dark

        self.config(width=190)

        self.tone = Label(self, **label_style)
        self.tone.config(width=50, height=50)
        if self.is_dark:
            self.tone.config(image=dark_img)
        else:
            self.tone.config(image=light_img)
        self.tone.place(rely=.85, relx=.5, anchor=CENTER)

        self.tone.bind("<ButtonPress-1>", self.press)
        self.tone.bind("<ButtonRelease-1>", self.release)

        self.label = Label(self, **label_style)
        self.label.config(text=self.text, wraplength=170)
        self.label.place(rely=.35, relx=.5, anchor=CENTER)

        self.label.bind("<ButtonPress-1>", self.press)
        self.label.bind("<ButtonRelease-1>", self.release)

    def press(self, e=None):
        super().press(e)
        self.tone.config(background=self.depressed_bg_color)
        self.label.config(background=self.depressed_bg_color)

    def release(self, e=None):
        super().release(e)
        self.tone.config(background=self.bg_color)
        self.label.config(background=self.bg_color)


class MainWindow:
    window: Tk

    period_frame: Frame

    period_timeline: Text
    event_timeline: Text
    other_scroll: Scrollbar

    def __init__(self):
        self.window = Tk()

        global dark_img, light_img, insert_img
        dark_img = PhotoImage(name="dark", file="Dark.png")
        light_img = PhotoImage(name="light", file="Light.png")
        insert_img = PhotoImage(name="insert", file="Insert.png")

        self.window.config(background=bg_color)
        self.window.title("Microscope TTRPG")

        self.period_frame = Frame(self.window, **frame_style)

        self.period_timeline = Text(self.period_frame, **frame_style)
        self.other_scroll = Scrollbar(self.period_frame)
        self.period_timeline.config(width=4, height=1, font=("Courier", 170), wrap=NONE, state=DISABLED,
                                    xscrollcommand=self.other_scroll.set)
        self.period_timeline.pack(side=TOP, expand=TRUE, fill=X)

        self.other_scroll.config(orient=HORIZONTAL, command=self.period_timeline.xview)
        self.other_scroll.pack(side=TOP, expand=FALSE, fill=X)

        self.period_frame.pack(side=TOP, expand=FALSE, fill=X, padx=8, pady=8)

        div = Divider(self.period_timeline, True)
        self.period_timeline.window_create(END, window=div, align=CENTER, stretch=TRUE)

        period = Period(self.period_timeline,
                        "The Rise of Machine Learning, Algorithmic Solutions to Humanity's Problems (START)", False)
        self.period_timeline.window_create(END, window=period, align=CENTER, stretch=TRUE)

        div = Divider(self.period_timeline)
        self.period_timeline.window_create(END, window=div, align=CENTER, stretch=TRUE)

        period = Period(self.period_timeline,
                        "An Age of Prosperity, AIs Solve Major World Issues", False)
        self.period_timeline.window_create(END, window=period, align=CENTER, stretch=TRUE)

        div = Divider(self.period_timeline)
        self.period_timeline.window_create(END, window=div, align=CENTER, stretch=TRUE)

        period = Period(self.period_timeline,
                        "Value Drift Causes Breakdown of World Infrastructure, "
                        "Self-Replicating Machines Threaten Humanity", True)
        self.period_timeline.window_create(END, window=period, align=CENTER, stretch=TRUE)

        div = Divider(self.period_timeline)
        self.period_timeline.window_create(END, window=div, align=CENTER, stretch=TRUE)

        period = Period(self.period_timeline,
                        "Machines Decide to Study and Learn from Humanity, all Humans Are Uploaded into an "
                        "Eternal Simulation, Effective Immortality (END)", False)
        self.period_timeline.window_create(END, window=period, align=CENTER, stretch=TRUE)

        div = Divider(self.period_timeline, True)
        self.period_timeline.window_create(END, window=div, align=CENTER, stretch=TRUE)

        # add_period = Button(self.period_timeline, **self.button_style)
        # add_period.config(width=25, text="Add Period", command=self.insert_period)
        #
        # self.period_timeline.window_create(END, window=add_period, align=CENTER, stretch=TRUE)

    # def insert_period(self):
    #     new_period = Button(self.period_timeline, **self.button_style)
    #     new_period.config(width=25, text="THIS IS A NEW PERIOD")
    #
    #     self.period_timeline.window_create(END + " - 2 chars", window=new_period, align=CENTER, stretch=TRUE)