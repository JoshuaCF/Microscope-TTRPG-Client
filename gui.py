from tkinter import *
from typing import List, Union

# insert a comment here


bg_color = "#303030"
fg_color = "#d0d0d0"
active_bg = "#404040"
active_fg = "#e0e0e0"
select_bg = "#5050f0"
small_font = ("Courier", 8)
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
radio_style = {"background": bg_color,
               "foreground": fg_color,
               "activebackground": bg_color,
               "activeforeground": fg_color,
               "selectcolor": active_bg,
               "font": default_font}
text_style = {"background": active_bg,
              "foreground": active_fg,
              "font": default_font,
              "relief": FLAT,
              "highlightthickness": 0,
              "selectbackground": select_bg,
              "insertbackground": active_fg}

dark_img: PhotoImage
small_dark_img: PhotoImage
light_img: PhotoImage
small_light_img: PhotoImage
insert_img: PhotoImage
minimize_img: PhotoImage
maximize_img: PhotoImage


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

    def press(self, _=None):
        self.config(background=self.depressed_bg_color, relief=SUNKEN)

    def release(self, _=None):
        self.config(background=self.bg_color, relief=RAISED)


class Divider(Container):
    plus: Label

    def __init__(self, parent, mw):
        super().__init__(parent, mw)

        self.config(borderwidth=1)

        self.plus = Label(self, **label_style)
        self.plus.config(image=insert_img, borderwidth=4, relief=RAISED)
        self.plus.place(rely=.5, relx=.5, anchor=CENTER)

        self.register_event("<ButtonPress-1>", self.click_down)
        self.register_event("<ButtonRelease-1>", self.click_up)

    def click_down(self, _=None):
        self.press()

    def click_up(self, _=None):
        pass

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.plus.bind(trigger, callback, add)

    def press(self, _=None):
        super().press()
        self.config(background=self.depressed_bg_color)
        self.plus.config(background=self.depressed_bg_color)

    def release(self, _=None):
        super().release()
        self.config(background=self.bg_color)
        self.plus.config(background=self.bg_color)


class PeriodDivider(Divider):
    def __init__(self, parent, mw):
        super().__init__(parent, mw)

    def click_up(self, _=None):
        self.mw.p_selection(self.index)
        self.release()


class EventDivider(Divider):
    parent_period: "MPeriod"

    def __init__(self, parent, parent_period: "MPeriod", mw: "MainWindow"):
        super().__init__(parent, mw)
        self.parent_period = parent_period

    def click_up(self, _=None):
        self.mw.e_selection(self.index, self.parent_period)
        self.release()


class SceneDivider(Divider):
    parent_event: "MEvent"

    def __init__(self, parent, parent_event: "MEvent", mw: "MainWindow"):
        super().__init__(parent, mw)
        self.parent_event = parent_event

    def click_up(self, _=None):
        self.mw.s_selection(self.index, self.parent_event)
        self.release()


class MPeriod(Container):
    text: str
    is_dark: bool

    tone: Label
    label: Label

    event_items: List[Union["MEvent", EventDivider]]

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
        self.label.config(text=self.text, wraplength=210)
        self.label.place(rely=.35, relx=.5, anchor=CENTER)

        self.register_event("<ButtonPress-1>", self.on_click)

    def on_click(self, _=None):
        self.mw.p_selection(self.index)

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.tone.bind(trigger, callback, add)
        self.label.bind(trigger, callback, add)  # It was at this point that I realized I should probably have a list
        # of child elements that I can just iterate through

        # ...eh

    def press(self, _=None):
        super().press()
        self.tone.config(background=self.depressed_bg_color)
        self.label.config(background=self.depressed_bg_color)

    def release(self, _=None):
        super().release()
        self.tone.config(background=self.bg_color)
        self.label.config(background=self.bg_color)


class MEvent(Container):  # This is the reason for the "M" prefix (M=Microscope). "Event" is already a class from tk.
    text: str
    is_dark: bool

    parent_period: MPeriod

    tone: Label
    label: Label
    scene_count: Label

    scene_items: List[Union["MScene", SceneDivider]]

    def __init__(self, parent, text: str, is_dark: bool, parent_period: Union[MPeriod, None], mw):
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

        self.scene_count = Label(self, **label_style)
        self.scene_count.config(font=large_font)

        self.label = Label(self, **label_style)
        self.label.config(text=self.text, wraplength=260)
        self.label.place(rely=.35, relx=.5, anchor=CENTER)

        self.register_event("<ButtonPress-1>", self.on_click)

        self.scene_items = []
        self.scene_items.append(SceneDivider(self.mw.scene_timeline, self, self.mw))
        self.scene_items[0].index = 0

    def on_click(self, _=None):
        self.mw.e_selection(self.index, self.parent_period)

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.tone.bind(trigger, callback, add)
        self.label.bind(trigger, callback, add)
        self.scene_count.bind(trigger, callback, add)

    def press(self, _=None):
        super().press()
        self.tone.config(background=self.depressed_bg_color)
        self.label.config(background=self.depressed_bg_color)
        self.scene_count.config(background=self.depressed_bg_color)

    def release(self, _=None):
        super().release()
        self.tone.config(background=self.bg_color)
        self.label.config(background=self.bg_color)
        self.scene_count.config(background=self.bg_color)

    def update_scene_count(self):
        if len(self.scene_items) // 2 > 0:
            if len(self.scene_items) // 2 == 1:
                self.scene_count.config(text="1 scene")
            elif len(self.scene_items) // 2 > 1:
                self.scene_count.config(text="{} scenes".format(len(self.scene_items) // 2))
            self.scene_count.place(rely=.85, relx=.25, anchor=W)
        else:
            self.scene_count.place_forget()


class MScene(Container):
    question: str
    setting: str
    answer: str
    is_dark: bool

    parent_event: MEvent

    tone: Label
    question_lbl: Label
    setting_lbl: Label
    answer_lbl: Label

    def __init__(self, parent, question: str, setting: str, answer: str, is_dark: bool,
                 parent_event: Union[MEvent, None], mw):
        super().__init__(parent, mw)

        self.question = question
        self.setting = setting
        self.answer = answer
        self.is_dark = is_dark
        self.parent_event = parent_event

        self.tone = Label(self, **label_style)
        self.tone.config(width=30, height=30)
        if self.is_dark:
            self.tone.config(image=small_dark_img)
        else:
            self.tone.config(image=small_light_img)
        self.tone.place(rely=.91, relx=.88, anchor=CENTER)

        self.question_lbl = Label(self, **label_style)
        self.question_lbl.config(font=small_font, text=self.question, wraplength=220)
        self.question_lbl.place(relx=.5, rely=.15, anchor=CENTER)

        divider1 = Frame(self, **frame_style)
        divider1.config(width=220, height=2, background=active_fg)
        divider1.place(relx=.5, rely=.30, anchor=CENTER)

        self.setting_lbl = Label(self, **label_style)
        self.setting_lbl.config(font=small_font, text=self.setting, wraplength=220)
        self.setting_lbl.place(relx=.5, rely=.45, anchor=CENTER)

        divider2 = Frame(self, **frame_style)
        divider2.config(width=220, height=2, background=active_fg)
        divider2.place(relx=.5, rely=.60, anchor=CENTER)

        self.answer_lbl = Label(self, **label_style)
        self.answer_lbl.config(font=small_font, text=self.answer, wraplength=220)
        self.answer_lbl.place(relx=.5, rely=.75, anchor=CENTER)

        self.register_event("<ButtonPress-1>", self.on_click)

    def on_click(self, _=None):
        self.mw.s_selection(self.index, self.parent_event)

    def register_event(self, trigger: str, callback, add=TRUE):
        super().register_event(trigger, callback, add)
        self.tone.bind(trigger, callback, add)
        self.question_lbl.bind(trigger, callback, add)
        self.setting_lbl.bind(trigger, callback, add)
        self.answer_lbl.bind(trigger, callback, add)

    def press(self, _=None):
        super().press()
        self.tone.config(background=self.depressed_bg_color)
        self.question_lbl.config(background=self.depressed_bg_color)
        self.setting_lbl.config(background=self.depressed_bg_color)
        self.answer_lbl.config(background=self.depressed_bg_color)

    def release(self, _=None):
        super().release()
        self.tone.config(background=self.bg_color)
        self.question_lbl.config(background=self.bg_color)
        self.setting_lbl.config(background=self.bg_color)
        self.answer_lbl.config(background=self.bg_color)


class ControlPanel(Frame):
    mw: "MainWindow"

    title_label: Label
    cur_frame: Frame = None

    p_edit_frame: Frame
    p_edit_text: Text
    p_edit_tone: BooleanVar

    e_edit_frame: Frame
    e_edit_parent_period: MPeriod
    e_edit_text: Text
    e_edit_tone: BooleanVar

    s_edit_frame: Frame
    s_edit_parent_event: MEvent
    s_edit_question: Text
    s_edit_setting: Text
    s_edit_answer: Text
    s_edit_tone: BooleanVar

    def __init__(self, parent, mw):
        super().__init__(parent, **frame_style)
        self.mw = mw

        self.title_label = Label(self, **large_label_style)
        self.title_label.config(text="Controls Panel", width=16, foreground="#f0f0f0")
        self.title_label.pack(side=TOP, fill=X)

        self.p_edit_frame = Frame(self, **frame_style)

        p_edit_label = Label(self.p_edit_frame, **label_style)
        p_edit_label.config(text="Period Label:")
        p_edit_label.pack(side=TOP, anchor=NW)

        self.p_edit_text = Text(self.p_edit_frame, **text_style)
        self.p_edit_text.config(wrap=WORD, width=10, height=2)
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
        p_edit_submit.config(text="Edit Period",
                             command=lambda: self.mw.edit_period(mw.cur_selection.index, MPeriod(
                                             self.mw.period_timeline,
                                             self.p_edit_text.get("1.0", END + "- 1 chars"),
                                             self.p_edit_tone.get(),
                                             self.mw)))
        p_edit_submit.pack(side=TOP, anchor=NW)

        p_edit_delete = Button(self.p_edit_frame, **button_style)
        p_edit_delete.config(text="Delete Period",
                             command=lambda: self.mw.delete_period(self.mw.cur_selection))
        p_edit_delete.pack(side=TOP, anchor=NW)

        self.e_edit_frame = Frame(self, **frame_style)

        e_edit_label = Label(self.e_edit_frame, **label_style)
        e_edit_label.config(text="Event Label:")
        e_edit_label.pack(side=TOP, anchor=NW)

        self.e_edit_text = Text(self.e_edit_frame, **text_style)
        self.e_edit_text.config(wrap=WORD, width=10, height=2)
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
        e_edit_submit.config(text="Edit Event",
                             command=lambda: self.mw.edit_event(mw.cur_selection.index, MEvent(
                                             self.mw.event_timeline,
                                             self.e_edit_text.get("1.0", END + "- 1 chars"),
                                             self.e_edit_tone.get(),
                                             None, self.mw), self.e_edit_parent_period))
        e_edit_submit.pack(side=TOP, anchor=NW)

        e_edit_delete = Button(self.e_edit_frame, **button_style)
        e_edit_delete.config(text="Delete Event",
                             command=lambda: self.mw.delete_event(self.mw.cur_selection, self.e_edit_parent_period))
        e_edit_delete.pack(side=TOP, anchor=NW)

        self.s_edit_frame = Frame(self, **frame_style)

        s_question_label = Label(self.s_edit_frame, **label_style)
        s_question_label.config(text="Scene Question:")
        s_question_label.pack(side=TOP, anchor=NW)

        self.s_edit_question = Text(self.s_edit_frame, **text_style)
        self.s_edit_question.config(wrap=WORD, width=6, height=2)
        self.s_edit_question.pack(side=TOP, fill=BOTH, expand=TRUE, padx=3, pady=3)

        s_setting_label = Label(self.s_edit_frame, **label_style)
        s_setting_label.config(text="Scene Setting:")
        s_setting_label.pack(side=TOP, anchor=NW)

        self.s_edit_setting = Text(self.s_edit_frame, **text_style)
        self.s_edit_setting.config(wrap=WORD, width=6, height=2)
        self.s_edit_setting.pack(side=TOP, fill=BOTH, expand=TRUE, padx=3, pady=3)

        s_answer_label = Label(self.s_edit_frame, **label_style)
        s_answer_label.config(text="Scene Answer:")
        s_answer_label.pack(side=TOP, anchor=NW)

        self.s_edit_answer = Text(self.s_edit_frame, **text_style)
        self.s_edit_answer.config(wrap=WORD, width=6, height=2)
        self.s_edit_answer.pack(side=TOP, fill=BOTH, expand=TRUE, padx=3, pady=3)

        self.s_edit_tone = BooleanVar()
        s_edit_radio_light = Radiobutton(self.s_edit_frame, **radio_style)
        s_edit_radio_light.config(variable=self.s_edit_tone, value=False, text="Light")
        s_edit_radio_light.pack(side=TOP, anchor=NW)

        s_edit_radio_dark = Radiobutton(self.s_edit_frame, **radio_style)
        s_edit_radio_dark.config(variable=self.s_edit_tone, value=True, text="Dark")
        s_edit_radio_dark.pack(side=TOP, anchor=NW)
        self.s_edit_tone.set(False)

        s_edit_submit = Button(self.s_edit_frame, **button_style)
        s_edit_submit.config(text="Edit Scene", command=lambda:
                             self.mw.edit_scene(mw.scene_selection.index,
                                                MScene(self.mw.scene_timeline,
                                                       self.s_edit_question.get("1.0", END + "- 1 chars"),
                                                       self.s_edit_setting.get("1.0", END + "- 1 chars"),
                                                       self.s_edit_answer.get("1.0", END + "- 1 chars"),
                                                       self.s_edit_tone.get(), None, self.mw),
                                                self.mw.cur_selection))
        s_edit_submit.pack(side=TOP, anchor=NW)

        s_edit_delete = Button(self.s_edit_frame, **button_style)
        s_edit_delete.config(text="Delete Scene",
                             command=lambda: self.mw.delete_scene(self.mw.scene_selection, self.s_edit_parent_event))
        s_edit_delete.pack(side=TOP, anchor=NW)

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

    def set_s_edit(self, s: MScene):
        if self.cur_frame is not None:
            self.cur_frame.pack_forget()
        self.cur_frame = self.s_edit_frame
        self.s_edit_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.s_edit_tone.set(s.is_dark)
        self.s_edit_question.delete("1.0", END)
        self.s_edit_question.insert("1.0", s.question)
        self.s_edit_setting.delete("1.0", END)
        self.s_edit_setting.insert("1.0", s.setting)
        self.s_edit_answer.delete("1.0", END)
        self.s_edit_answer.insert("1.0", s.answer)
        self.s_edit_parent_event = s.parent_event


class MainWindow(Tk):
    controls: ControlPanel

    padding_frame: Frame
    upper_frame: Frame
    lower_frame: Frame
    minimize_frame: Frame  # This has content that can be minimized to make more room in the GUI

    minimize_control_button: Button
    is_minimized: bool = True

    event_frame: Frame
    scene_frame: Frame

    period_timeline: Canvas
    event_timeline: Canvas
    scene_timeline: Canvas

    # The game is meant to be played with index cards. To me, index cards are normally oriented with the long side
    # horizontal. Consider the width to be the long side and the height to be the short side of an index card.
    card_height = 240
    card_width = 280

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
    scene_scroll: Scrollbar

    cur_selection: Union[MPeriod, MEvent] = None
    scene_selection: MScene = None

    def __init__(self):
        super().__init__()

        # There's probably a better way to do this, but I don't know it
        global dark_img, small_dark_img, light_img, small_light_img, insert_img, minimize_img, maximize_img
        dark_img = PhotoImage(name="dark", file="Dark.png")
        small_dark_img = PhotoImage(name="small_dark", file="SmallDark.png")
        light_img = PhotoImage(name="light", file="Light.png")
        small_light_img = PhotoImage(name="small_light", file="SmallLight.png")
        insert_img = PhotoImage(name="insert", file="Insert.png")
        minimize_img = PhotoImage(name="minimize", file="Minimize.png")
        maximize_img = PhotoImage(name="maximize", file="Maximize.png")

        self.config(background=active_bg)
        self.title("Microscope TTRPG")

        self.padding_frame = Frame(self, **frame_style)
        self.padding_frame.config(background=active_bg)

        self.upper_frame = Frame(self.padding_frame, **frame_style)
        self.upper_frame.config(background=active_bg)

        self.controls = ControlPanel(self.upper_frame, self)
        self.controls.pack(side=RIGHT, fill=Y, padx=4, pady=4)

        self.period_frame = Frame(self.upper_frame, **frame_style)

        self.event_frame = Frame(self.upper_frame, **frame_style)
        self.event_frame.config(background=active_bg)

        self.period_timeline = Canvas(self.upper_frame, **canvas_style)
        self.primary_scroll = Scrollbar(self.event_frame)
        self.period_timeline.config(width=800, height=self.period_y, xscrollcommand=self.primary_scroll.set)
        self.period_timeline.pack(side=TOP, expand=FALSE, fill=X, padx=4, pady=4)

        self.period_items.append(PeriodDivider(self.period_timeline, self))
        self.period_items[0].id = self.period_timeline.create_window(0, 0, window=self.period_items[0])
        self.period_items[0].index = 0

        self.event_timeline = Canvas(self.event_frame, **canvas_style)
        self.event_timeline.config(xscrollcommand=self.primary_scroll.set, yscrollincrement=1)
        self.event_timeline.bind("<MouseWheel>", self.vertical_scroll)
        self.event_timeline.pack(side=TOP, expand=TRUE, fill=BOTH)

        self.primary_scroll.config(orient=HORIZONTAL, command=self.horizontal_scroll)
        self.primary_scroll.pack(side=TOP, expand=FALSE, fill=X)

        self.event_frame.pack(side=TOP, expand=TRUE, fill=BOTH, padx=4, pady=4)

        self.upper_frame.pack(side=TOP, expand=TRUE, fill=BOTH)

        self.lower_frame = Frame(self.padding_frame, **frame_style)
        self.lower_frame.config(background=active_bg)

        self.minimize_control_button = Button(self.lower_frame, **button_style)
        self.minimize_control_button.config(image=maximize_img, command=self.minimize_control)
        self.minimize_control_button.pack(side=RIGHT, anchor=N, padx=4, pady=4)

        self.minimize_frame = Frame(self.lower_frame, **frame_style)
        self.minimize_frame.config(background=active_bg)

        self.scene_frame = Frame(self.minimize_frame, **frame_style)
        self.scene_frame.config(background=active_bg)

        self.scene_scroll = Scrollbar(self.scene_frame)
        self.scene_timeline = Canvas(self.scene_frame, **canvas_style)
        self.scene_timeline.config(height=self.period_y, xscrollcommand=self.scene_scroll.set)
        self.scene_timeline.pack(side=TOP, expand=FALSE, fill=X)

        self.scene_scroll.config(orient=HORIZONTAL, command=self.scene_timeline_scroll)
        self.scene_scroll.pack(side=TOP, expand=FALSE, fill=X)

        self.scene_frame.pack(side=TOP, expand=FALSE, fill=X, padx=4, pady=4)

        self.lower_frame.pack(side=TOP, expand=FALSE, fill=X)

        self.padding_frame.pack(side=TOP, expand=TRUE, fill=BOTH, padx=8, pady=8)

        self.update_canvases()

    def horizontal_scroll(self, start, end):
        self.period_timeline.xview(start, end)
        self.event_timeline.xview(start, end)

    def vertical_scroll(self, e):
        if self.event_timeline.yview() != (0, 1):
            self.event_timeline.yview_scroll(int(-e.delta * .4), "units")

    def scene_timeline_scroll(self, start, end):
        self.scene_timeline.xview(start, end)

    def p_selection(self, index: int):
        if self.cur_selection is not None:
            self.cur_selection.release()
        self.cur_selection = self.period_items[index]
        if self.scene_selection is not None:
            self.scene_selection.release()

        self.update_scene_timeline()

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

        self.controls.clear_controls()

        self.update_canvases()

    def e_selection(self, index: int, period: MPeriod):
        if self.cur_selection is not None:
            self.cur_selection.release()
        self.cur_selection = period.event_items[index]
        if self.scene_selection is not None:
            self.scene_selection.release()

        if isinstance(self.cur_selection, EventDivider):
            self.insert_event(index, MEvent(self.event_timeline, "New Event", False, period, self), period)
            self.controls.clear_controls()
            self.update_scene_timeline()
        elif isinstance(self.cur_selection, MEvent):
            self.cur_selection.press()
            self.controls.set_e_edit(self.cur_selection)
            self.update_scene_timeline(self.cur_selection)

    def edit_event(self, index: int, event: MEvent, period: MPeriod):
        event.parent_period = period
        self.event_timeline.delete(period.event_items[index].id)
        old_scenes = period.event_items[index].scene_items
        period.event_items[index] = event
        period.event_items[index].register_event("<MouseWheel>", self.vertical_scroll)
        period.event_items[index].id = self.event_timeline.create_window(0, 0, window=period.event_items[index])
        period.event_items[index].index = index
        period.event_items[index].scene_items = old_scenes

        event.update_scene_count()

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

        self.controls.clear_controls()

        self.update_canvases()

    def s_selection(self, index: int, event: MEvent):
        if self.scene_selection is not None:
            self.scene_selection.release()
        self.scene_selection = event.scene_items[index]

        if isinstance(self.scene_selection, SceneDivider):
            self.insert_scene(index, MScene(self.scene_timeline, "New Scene Question", "New Scene Setting",
                                            "New Scene Answer", False, self.cur_selection, self), self.cur_selection)
            self.controls.clear_controls()
        elif isinstance(self.scene_selection, MScene):
            self.scene_selection.press()
            self.controls.set_s_edit(self.scene_selection)
            self.update_scene_timeline(self.cur_selection)

    def edit_scene(self, index: int, scene: MScene, event: MEvent):
        scene.parent_event = event
        self.scene_timeline.delete(event.scene_items[index].id)
        event.scene_items[index] = scene
        event.scene_items[index].id = self.scene_timeline.create_window(0, 0, window=event.scene_items[index])
        event.scene_items[index].index = index

        if event is self.cur_selection:
            self.update_scene_timeline(event)

    def insert_scene(self, index: int, scene: MScene, event: MEvent):
        event.scene_items.insert(index, SceneDivider(self.scene_timeline, event, self))
        event.scene_items.insert(index + 1, scene)

        for i in range(len(event.scene_items)):
            event.scene_items[i].index = i

        if self.cur_selection is event:
            self.update_scene_timeline(event)
        event.update_scene_count()

    def delete_scene(self, scene: MScene, event: MEvent):
        index = event.scene_items.index(scene)
        self.scene_timeline.delete(event.scene_items[index].id)
        self.scene_timeline.delete(event.scene_items[index+1].id)

        del event.scene_items[index:index+2]

        for i in range(len(event.scene_items)):
            event.scene_items[i].index = i

        self.controls.clear_controls()

        if event is self.cur_selection:
            self.update_scene_timeline(event)
        event.update_scene_count()

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

    def update_scene_timeline(self, event: MEvent = None):
        self.scene_timeline.delete("all")

        if event is not None:
            for scene_item in event.scene_items:
                scene_item.id = self.scene_timeline.create_window(0, 0, window=scene_item)

            running_width = 0
            scene_item_size = len(event.scene_items)
            for i in range(scene_item_size):
                if i == 0 or i == scene_item_size - 1:
                    event.scene_items[i].config(width=self.period_spacing_x / 2, height=self.period_y)
                    self.scene_timeline.moveto(event.scene_items[i].id, running_width, 0)

                    running_width += self.period_spacing_x / 2
                elif i % 2 == 0:
                    event.scene_items[i].config(width=self.period_spacing_x, height=self.period_y)
                    self.scene_timeline.moveto(event.scene_items[i].id, running_width, 0)

                    running_width += self.period_spacing_x
                else:
                    event.scene_items[i].config(width=self.period_x, height=self.period_y)
                    self.scene_timeline.moveto(event.scene_items[i].id, running_width, 0)

                    running_width += self.period_x

        self.scene_timeline.config(scrollregion=self.scene_timeline.bbox("all"))

    def minimize_control(self):
        if self.is_minimized:
            self.is_minimized = False
            self.minimize_frame.pack(side=TOP, expand=FALSE, fill=X)
            self.minimize_control_button.config(image=minimize_img)
        else:
            self.is_minimized = True
            self.minimize_frame.pack_forget()
            self.minimize_control_button.config(image=maximize_img)