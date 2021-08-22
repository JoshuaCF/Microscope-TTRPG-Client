from tkinter import *
from typing import List, Union


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
canvas_style = {"background": bg_color,
                "borderwidth": 0,
                "highlightthickness": 0}
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

    id: int  # For use with canvas
    index: int  # For use with MainWindow

    def __init__(self, parent):
        super().__init__(parent, **frame_style)
        self.config(borderwidth=5, relief=RAISED)

    def register_event(self, trigger: str, callback, add=TRUE):
        self.bind(trigger, callback, add)

    def press(self, e=None):
        self.config(background=self.depressed_bg_color, relief=SUNKEN)

    def release(self, e=None):
        self.config(background=self.bg_color, relief=RAISED)


class Divider(Container):
    plus: Label

    def __init__(self, parent):
        super().__init__(parent)

        self.config(borderwidth=0)

        self.plus = Label(self, **label_style)
        self.plus.config(image=insert_img, borderwidth=4, relief=RAISED)
        self.plus.place(rely=.5, relx=.5, anchor=CENTER)

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.plus.bind(trigger, callback, add)

    def press(self, e=None):
        super().press(e)
        self.plus.config(background=self.depressed_bg_color)

    def release(self, e=None):
        super().press(e)
        self.plus.config(background=self.bg_color)


class Period(Container):
    text: str
    is_dark: bool

    tone: Label
    label: Label

    def __init__(self, parent, text: str, is_dark: bool):
        super().__init__(parent)

        self.text = text
        self.is_dark = is_dark

        self.tone = Label(self, **label_style)
        self.tone.config(width=50, height=50)
        if self.is_dark:
            self.tone.config(image=dark_img)
        else:
            self.tone.config(image=light_img)
        self.tone.place(rely=.85, relx=.5, anchor=CENTER)

        self.label = Label(self, **label_style)
        self.label.config(text=self.text, wraplength=170)
        self.label.place(rely=.35, relx=.5, anchor=CENTER)

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.tone.bind(trigger, callback, add)
        self.label.bind(trigger, callback, add)  # It was at this point that I realized I should probably have a list
        # of child elements that I can just iterate through

        # ...eh

    def press(self, e=None):
        super().press(e)
        self.tone.config(background=self.depressed_bg_color)
        self.label.config(background=self.depressed_bg_color)
        print(e)

    def release(self, e=None):
        super().release(e)
        self.tone.config(background=self.bg_color)
        self.label.config(background=self.bg_color)


class MainWindow:
    window: Tk

    period_frame: Frame

    period_timeline: Canvas

    period_x = 200
    period_y = 300
    period_spacing_x = 70
    period_items: List[Union[Divider, Period]] = []

    other_scroll: Scrollbar

    def __init__(self):
        self.window = Tk()

        global dark_img, light_img, insert_img  # There's probably a better way to do this, but I don't know it
        dark_img = PhotoImage(name="dark", file="Dark.png")
        light_img = PhotoImage(name="light", file="Light.png")
        insert_img = PhotoImage(name="insert", file="Insert.png")

        self.window.config(background=bg_color)
        self.window.title("Microscope TTRPG")

        self.period_frame = Frame(self.window, **frame_style)

        self.period_timeline = Canvas(self.period_frame, **canvas_style)
        self.other_scroll = Scrollbar(self.period_frame)
        self.period_timeline.config(width=800, height=self.period_y, xscrollcommand=self.other_scroll.set)
        self.period_timeline.pack(side=TOP, expand=TRUE, fill=X)

        self.other_scroll.config(orient=HORIZONTAL, command=self.period_timeline.xview)
        self.other_scroll.pack(side=TOP, expand=FALSE, fill=X)

        self.period_frame.pack(side=TOP, expand=FALSE, fill=X, padx=8, pady=8)

        self.period_items.append(Divider(self.period_timeline))
        self.period_items[0].id = self.period_timeline.create_window(0, 0, window=self.period_items[0])
        self.period_items[0].index = 0

        self.insert_period(Period(self.period_timeline,
                                  "The Rise of Machine Learning, Algorithmic Solutions to Humanity's Problems (START)",
                                  False), 0)

        self.insert_period(Period(self.period_timeline, "An Age of Prosperity, AIs Solve Major World Issues", False), 2)

        self.insert_period(Period(self.period_timeline, "Value Drift Causes Breakdown of World Infrastructure, "
                                                        "Self-Replicating Machines Threaten Humanity", True), 4)

        self.insert_period(Period(self.period_timeline, "Machines Decide to Study and Learn from Humanity, "
                                                        "all Humans Are Uploaded into an Eternal Simulation, "
                                                        "Effective Immortality (END)", False), 6)

    def insert_period(self, period: Period, index: int):
        self.period_items.insert(index, Divider(self.period_timeline))
        self.period_items.insert(index+1, period)

        self.period_items[index].id = self.period_timeline.create_window(0, 0, window=self.period_items[index])
        self.period_items[index+1].id = self.period_timeline.create_window(0, 0, window=self.period_items[index+1])

        for i in range(len(self.period_items)):
            self.period_items[i].index = i
        self.update_period_canvas()

    def delete_period(self, period: Period):
        pass

    def update_period_canvas(self):
        period_item_size = len(self.period_items)
        running_width = 0
        for i in range(period_item_size):
            if i == 0 or i == period_item_size-1:
                self.period_items[i].config(width=self.period_spacing_x / 2, height=self.period_y)
                self.period_timeline.moveto(self.period_items[i].id, running_width, 0)

                running_width += self.period_spacing_x / 2
            elif i % 2 == 0:
                self.period_items[i].config(width=self.period_spacing_x, height=self.period_y)
                self.period_timeline.moveto(self.period_items[i].id, running_width, 0)

                running_width += self.period_spacing_x
            else:
                self.period_items[i].config(width=self.period_x, height=self.period_y)
                self.period_timeline.moveto(self.period_items[i].id, running_width, 0)

                running_width += self.period_x

        self.period_timeline.config(scrollregion=self.period_timeline.bbox("all"))
        print(self.period_timeline.config("scrollregion"))