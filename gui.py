from tkinter import *
from typing import List, Union


bg_color = "#303030"
fg_color = "#d0d0d0"
active_bg = "#404040"
active_fg = "#e0e0e0"
select_bg = "#5050f0"
default_font = ("Courier", 10)
large_font = ("Courier", 25)

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
large_label_style = {"background": bg_color,
                     "foreground": fg_color,
                     "relief": FLAT,
                     "font": large_font}
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
radio_style = {"background": active_bg,
               "foreground": active_fg,
               "activebackground": active_bg,
               "activeforeground": active_fg,
               "selectcolor": bg_color}
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

    mw: "MainWindow"

    def __init__(self, parent, mw: "MainWindow"):
        super().__init__(parent, **frame_style)
        self.mw = mw
        self.config(borderwidth=5, relief=RAISED)

    def register_event(self, trigger: str, callback, add=TRUE):
        self.bind(trigger, callback, add)

    def press(self, e=None):
        self.config(background=self.depressed_bg_color, relief=SUNKEN)

    def release(self, e=None):
        self.config(background=self.bg_color, relief=RAISED)


class Divider(Container):
    plus: Label

    def __init__(self, parent, mw):
        super().__init__(parent, mw)

        self.config(borderwidth=1)

        self.plus = Label(self, **label_style)
        self.plus.config(image=insert_img, borderwidth=4, relief=RAISED)
        self.plus.place(rely=.5, relx=.5, anchor=CENTER)

        self.register_event("<ButtonPress-1>", self.on_click)

    def on_click(self, e=None):
        pass

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.plus.bind(trigger, callback, add)

    def press(self, e=None):
        pass
        # super().press(e)
        # self.config(background=self.depressed_bg_color)
        # self.plus.config(background=self.depressed_bg_color)

    def release(self, e=None):
        pass
        # super().press(e)
        # self.config(background=self.bg_color)
        # self.plus.config(background=self.bg_color)


class PeriodDivider(Divider):
    def __init__(self, parent, mw):
        super().__init__(parent, mw)

    def on_click(self, e=None):
        self.mw.p_selection(self.index)


class EventDivider(Divider):
    parent_period: "MPeriod"

    def __init__(self, parent, parent_period: "MPeriod", mw: "MainWindow"):
        super().__init__(parent, mw)
        self.parent_period = parent_period

    def on_click(self, e=None):
        self.mw.e_selection(self.index, self.parent_period)


class MEvent(Container):  # This is the reason for the "M" prefix (M=Microscope). "Event" is already a class from tk.
    text: str
    is_dark: bool

    parent_period: "MPeriod"

    tone: Label
    label: Label
    scene_count: Label

    def __init__(self, parent, text: str, is_dark: bool, parent_period: Union["MPeriod", None], mw):
        super().__init__(parent, mw)

        self.text = text
        self.is_dark = is_dark
        self.parent_period = parent_period

        self.tone = Label(self, **label_style)
        self.tone.config(width=50, height=50)
        if self.is_dark:
            self.tone.config(image=dark_img)
        else:
            self.tone.config(image=light_img)
        self.tone.place(rely=.85, relx=.125, anchor=CENTER)

        self.label = Label(self, **label_style)
        self.label.config(text=self.text, wraplength=200)
        self.label.place(rely=.35, relx=.5, anchor=CENTER)

        self.register_event("<ButtonPress-1>", self.on_click)

    def on_click(self, e=None):
        self.mw.e_selection(self.index, self.parent_period)

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

    def release(self, e=None):
        super().release(e)
        self.tone.config(background=self.bg_color)
        self.label.config(background=self.bg_color)


class MPeriod(Container):
    text: str
    is_dark: bool

    tone: Label
    label: Label

    event_items: List[Union[MEvent, EventDivider]]

    def __init__(self, parent, text: str, is_dark: bool, mw):
        super().__init__(parent, mw)

        self.text = text
        self.is_dark = is_dark
        self.event_items = [EventDivider(self.mw.event_timeline, self, self.mw)]
        self.event_items[0].index = 0

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

        self.register_event("<ButtonPress-1>", self.on_click)

    def on_click(self, e=None):
        self.mw.p_selection(self.index)

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

    def release(self, e=None):
        super().release(e)
        self.tone.config(background=self.bg_color)
        self.label.config(background=self.bg_color)


class ControlPanel(Frame):
    mw: "MainWindow"

    title_label: Label
    cur_frame: Frame = None

    p_edit_frame: Frame
    p_edit_tone: BooleanVar
    p_edit_text: Text

    e_edit_frame: Frame
    e_edit_parent_period: MPeriod
    e_edit_tone: BooleanVar
    e_edit_text: Text

    s_edit_frame: Frame
    s_edit_tone: BooleanVar
    s_edit_question: Text
    s_edit_setting: Text
    s_edit_answer: Text

    def __init__(self, parent, mw):
        super().__init__(parent, **frame_style)
        self.mw = mw

        self.config(background=active_bg)

        self.title_label = Label(self, **large_label_style)
        self.title_label.config(text="Controls Panel", width=16, background=active_bg, foreground="#f0f0f0")
        self.title_label.pack(side=TOP, fill=X)

        self.p_edit_frame = Frame(self, **frame_style)
        self.p_edit_frame.config(background=active_bg)

        p_edit_label = Label(self.p_edit_frame, **label_style)
        p_edit_label.config(text="Period Label:", background=active_bg)
        p_edit_label.pack(side=TOP, anchor=NW)

        self.p_edit_text = Text(self.p_edit_frame, **text_style)
        self.p_edit_text.config(background=bg_color, wrap=WORD, width=10, height=2)
        self.p_edit_text.pack(side=TOP, fill=BOTH, expand=TRUE, padx=3, pady=3)

        self.p_edit_tone = BooleanVar()
        p_edit_radio_light = Radiobutton(self.p_edit_frame, **radio_style)
        p_edit_radio_light.config(variable=self.p_edit_tone, value=False, text="Light")
        p_edit_radio_light.pack(side=TOP, anchor=NW)

        p_edit_radio_dark = Radiobutton(self.p_edit_frame, **radio_style)
        p_edit_radio_dark.config(variable=self.p_edit_tone, value=True, text="Dark")
        p_edit_radio_dark.pack(side=TOP, anchor=NW)
        self.p_edit_tone.set(False)

        p_edit_submit = Button(self.p_edit_frame, **button_style)
        p_edit_submit.config(background=active_bg, text="Edit Period",
                             command=lambda: self.mw.edit_period(mw.cur_selection.index, MPeriod(
                                             self.mw.period_timeline,
                                             self.p_edit_text.get("1.0", END + "- 1 chars"),
                                             self.p_edit_tone.get(),
                                             self.mw)))
        p_edit_submit.pack(side=TOP, anchor=NW)

        p_edit_delete = Button(self.p_edit_frame, **button_style)
        p_edit_delete.config(background=active_bg, text="Delete Period",
                             command=lambda: self.mw.delete_period(self.mw.cur_selection))
        p_edit_delete.pack(side=TOP, anchor=NW)

        self.e_edit_frame = Frame(self, **frame_style)
        self.e_edit_frame.config(background=active_bg)

        e_edit_label = Label(self.e_edit_frame, **label_style)
        e_edit_label.config(text="Event Label:", background=active_bg)
        e_edit_label.pack(side=TOP, anchor=NW)

        self.e_edit_text = Text(self.e_edit_frame, **text_style)
        self.e_edit_text.config(background=bg_color, wrap=WORD, width=10, height=2)
        self.e_edit_text.pack(side=TOP, fill=BOTH, expand=TRUE, padx=3, pady=3)

        self.e_edit_tone = BooleanVar()
        e_edit_radio_light = Radiobutton(self.e_edit_frame, **radio_style)
        e_edit_radio_light.config(variable=self.e_edit_tone, value=False, text="Light")
        e_edit_radio_light.pack(side=TOP, anchor=NW)

        e_edit_radio_dark = Radiobutton(self.e_edit_frame, **radio_style)
        e_edit_radio_dark.config(variable=self.e_edit_tone, value=True, text="Dark")
        e_edit_radio_dark.pack(side=TOP, anchor=NW)
        self.e_edit_tone.set(False)

        e_edit_submit = Button(self.e_edit_frame, **button_style)
        e_edit_submit.config(background=active_bg, text="Edit Event",
                             command=lambda: self.mw.edit_event(mw.cur_selection.index, MEvent(
                                             self.mw.event_timeline,
                                             self.e_edit_text.get("1.0", END + "- 1 chars"),
                                             self.e_edit_tone.get(),
                                             None, self.mw), self.e_edit_parent_period))
        e_edit_submit.pack(side=TOP, anchor=NW)

        e_edit_delete = Button(self.e_edit_frame, **button_style)
        e_edit_delete.config(background=active_bg, text="Delete Event",
                             command=lambda: self.mw.delete_event(self.mw.cur_selection, self.e_edit_parent_period))
        e_edit_delete.pack(side=TOP, anchor=NW)

    def clear_controls(self):
        if self.cur_frame is not None:
            self.cur_frame.pack_forget()

    def set_p_edit(self, p: MPeriod):
        if self.cur_frame is not None:
            self.cur_frame.pack_forget()
        self.cur_frame = self.p_edit_frame
        self.p_edit_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.p_edit_tone.set(p.is_dark)
        self.p_edit_text.delete("1.0", END)
        self.p_edit_text.insert("1.0", p.text)

    def set_e_edit(self, e: MEvent):
        if self.cur_frame is not None:
            self.cur_frame.pack_forget()
        self.cur_frame = self.e_edit_frame
        self.e_edit_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.e_edit_tone.set(e.is_dark)
        self.e_edit_text.delete("1.0", END)
        self.e_edit_text.insert("1.0", e.text)
        self.e_edit_parent_period = e.parent_period

    def set_s_edit(self):
        pass


class MainWindow(Tk):
    controls: ControlPanel

    period_timeline: Canvas
    event_timeline: Canvas

    # The game is meant to be played with index cards. To me, index cards are normally oriented with the long side
    # horizontal. Consider the width to be the long side and the height to be the short side of an index card.
    card_height = 200
    card_width = 260

    # A lot of these assignments are somewhat redundant and I could easily mix around the variables in the code itself,
    # but I do it like this in hopes that it will be clear to myself and others where the numbers come from.
    period_x = card_height
    period_y = card_width
    period_spacing_x = card_width - card_height
    period_items: List[Union[PeriodDivider, MPeriod]] = []

    event_x = card_width
    event_y = card_height
    event_spacing_y = card_width - card_height

    primary_scroll: Scrollbar

    cur_selection: Union[MPeriod, MEvent] = None

    def __init__(self):
        super().__init__()

        global dark_img, light_img, insert_img  # There's probably a better way to do this, but I don't know it
        dark_img = PhotoImage(name="dark", file="Dark.png")
        light_img = PhotoImage(name="light", file="Light.png")
        insert_img = PhotoImage(name="insert", file="Insert.png")

        self.config(background=bg_color)
        self.title("Microscope TTRPG")

        self.controls = ControlPanel(self, self)
        self.controls.pack(side=RIGHT, fill=Y)

        self.period_frame = Frame(self, **frame_style)

        self.period_timeline = Canvas(self, **canvas_style)
        self.primary_scroll = Scrollbar(self)
        self.period_timeline.config(width=800, height=self.period_y, xscrollcommand=self.primary_scroll.set)
        self.period_timeline.pack(side=TOP, expand=FALSE, fill=X)

        self.period_items.append(PeriodDivider(self.period_timeline, self))
        self.period_items[0].id = self.period_timeline.create_window(0, 0, window=self.period_items[0])
        self.period_items[0].index = 0

        self.event_timeline = Canvas(self, **canvas_style)
        self.event_timeline.config(xscrollcommand=self.primary_scroll.set, yscrollincrement=1)
        self.event_timeline.bind("<MouseWheel>", self.vertical_scroll)
        self.event_timeline.pack(side=TOP, expand=TRUE, fill=BOTH)

        self.primary_scroll.config(orient=HORIZONTAL, command=self.horizontal_scroll)
        self.primary_scroll.pack(side=TOP, expand=FALSE, fill=X)

        self.update_canvases()

    def horizontal_scroll(self, start, end):
        self.period_timeline.xview(start, end)
        self.event_timeline.xview(start, end)

    def vertical_scroll(self, e):
        if self.event_timeline.yview() != (0, 1):
            self.event_timeline.yview_scroll(-e.delta, "units")

    def p_selection(self, index: int):
        if self.cur_selection is not None:
            self.cur_selection.release()
        self.cur_selection = self.period_items[index]

        if isinstance(self.cur_selection, PeriodDivider):
            self.insert_period(index, MPeriod(self.period_timeline, "New Period", False, self))
            self.controls.clear_controls()
        elif isinstance(self.cur_selection, MPeriod):
            self.cur_selection.press()
            self.controls.set_p_edit(self.cur_selection)

    def edit_period(self, index: int, period: MPeriod):
        self.period_timeline.delete(self.period_items[index].id)
        old_events = self.period_items[index].event_items
        self.period_items[index] = period
        self.period_items[index].id = self.period_timeline.create_window(0, 0, window=self.period_items[index])
        self.period_items[index].index = index
        self.period_items[index].event_items = old_events

        self.update_canvases()

    def insert_period(self, index: int, period: MPeriod):
        self.period_items.insert(index, PeriodDivider(self.period_timeline, self))
        self.period_items.insert(index+1, period)

        self.period_items[index].id = self.period_timeline.create_window(0, 0, window=self.period_items[index])
        self.period_items[index+1].id = self.period_timeline.create_window(0, 0, window=self.period_items[index+1])

        self.period_items[index+1].event_items[0].id = \
            self.event_timeline.create_window(0, 0, window=self.period_items[index+1].event_items[0])
        self.period_items[index + 1].event_items[0].register_event("<MouseWheel>", self.vertical_scroll)

        for i in range(len(self.period_items)):
            self.period_items[i].index = i

        self.update_canvases()

    def delete_period(self, period: MPeriod):
        index = self.period_items.index(period)
        self.period_timeline.delete(self.period_items[index].id)
        self.period_timeline.delete(self.period_items[index+1].id)

        period_event_size = len(period.event_items)
        for i in range(period_event_size):
            self.event_timeline.delete(period.event_items[i].id)

        del self.period_items[index:index+2]

        for i in range(len(self.period_items)):
            self.period_items[i].index = i

        self.update_canvases()

    def e_selection(self, index: int, period: MPeriod):
        if self.cur_selection is not None:
            self.cur_selection.release()
        self.cur_selection = period.event_items[index]

        if isinstance(self.cur_selection, EventDivider):
            self.insert_event(index, MEvent(self.event_timeline, "New Event", False, period, self), period)
            self.controls.clear_controls()
        elif isinstance(self.cur_selection, MEvent):
            self.cur_selection.press()
            self.controls.set_e_edit(self.cur_selection)

    def edit_event(self, index: int, event: MEvent, period: MPeriod):
        event.parent_period = period
        self.event_timeline.delete(period.event_items[index].id)
        period.event_items[index] = event
        period.event_items[index].register_event("<MouseWheel>", self.vertical_scroll)
        period.event_items[index].id = self.event_timeline.create_window(0, 0, window=period.event_items[index])
        period.event_items[index].index = index

        self.update_canvases()

    def insert_event(self, index: int, event: MEvent, period: MPeriod):
        period.event_items.insert(index, EventDivider(self.event_timeline, period, self))
        period.event_items.insert(index+1, event)

        period.event_items[index].id = self.event_timeline.create_window(0, 0, window=period.event_items[index])
        period.event_items[index+1].id = self.event_timeline.create_window(0, 0, window=period.event_items[index+1])
        period.event_items[index].register_event("<MouseWheel>", self.vertical_scroll)
        period.event_items[index+1].register_event("<MouseWheel>", self.vertical_scroll)

        for i in range(len(period.event_items)):
            period.event_items[i].index = i

        self.update_canvases()

    def delete_event(self, event: MEvent, period: MPeriod):
        index = period.event_items.index(event)
        self.event_timeline.delete(period.event_items[index].id)
        self.event_timeline.delete(period.event_items[index+1].id)

        del period.event_items[index:index+2]

        for i in range(len(period.event_items)):
            period.event_items[i].index = i

        self.update_canvases()

    def update_canvases(self):
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

                event_items = self.period_items[i].event_items
                event_item_size = len(event_items)

                running_height = 0
                event_x_pos = running_width - self.period_spacing_x / 2 - self.period_x

                for j in range(event_item_size):
                    if j == 0 or j == event_item_size-1:
                        event_items[j].config(width=self.event_x, height=self.event_spacing_y / 2)
                        self.event_timeline.moveto(event_items[j].id, event_x_pos, running_height)

                        running_height += self.event_spacing_y / 2
                    elif j % 2 == 0:
                        event_items[j].config(width=self.event_x, height=self.event_spacing_y)
                        self.event_timeline.moveto(event_items[j].id, event_x_pos, running_height)

                        running_height += self.event_spacing_y
                    else:
                        event_items[j].config(width=self.event_x, height=self.event_y)
                        self.event_timeline.moveto(event_items[j].id, event_x_pos, running_height)

                        running_height += self.event_y

        self.period_timeline.config(scrollregion=self.period_timeline.bbox("all"))
        self.event_timeline.config(scrollregion=self.event_timeline.bbox("all"))