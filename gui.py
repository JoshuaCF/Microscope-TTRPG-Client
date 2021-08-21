from tkinter import *


class MainWindow:
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

    window: Tk

    period_frame: Frame

    period_timeline: Text
    period_scroll: Scrollbar

    def __init__(self):
        self.window = Tk()
        self.window.config(background=self.bg_color)
        self.window.title("Microscope TTRPG")

        self.period_frame = Frame(self.window, **self.frame_style)

        self.period_timeline = Text(self.period_frame, **self.text_style)
        self.period_scroll = Scrollbar(self.period_frame)
        self.period_timeline.config(width=4, height=1, font=("Courier", 170), wrap=NONE, state=DISABLED,
                                    xscrollcommand=self.period_scroll.set)
        self.period_timeline.pack(side=TOP, expand=TRUE, fill=X)

        self.period_scroll.config(orient=HORIZONTAL, command=self.period_timeline.xview)
        self.period_scroll.pack(side=TOP, expand=FALSE, fill=X)

        self.period_frame.pack(side=TOP, expand=FALSE, fill=X, padx=8, pady=8)

        add_period = Button(self.period_timeline, **self.button_style)
        add_period.config(text="Add Period")

        self.period_timeline.window_create(END, window=add_period, align=CENTER, stretch=TRUE)