from tkinter import Tk, Frame, Label, Entry, DISABLED, Text, CENTER, StringVar, NORMAL
from tkmacosx import Button
from PIL import Image, ImageTk
from app_methods import AppMethods
from game_result import GameResult
from english_words import english_words_lower_alpha_set
import random


class App(Tk):
    def __init__(self):
        super().__init__()
        # CountDown
        self.total_sec = 60
        self.start_again_countdown = False
        # English Words Selection
        self.num_words = 5000
        self.english_dic = list(english_words_lower_alpha_set)
        self.words_selected = []
        # Display Words
        self.word_pos = 0
        # Result Parameters
        self.raw_CPM = 0
        self.correct_CPM = 0

        # --- GUI --- #
        width, height = 860, 350

        self.geometry('{}x{}'.format(width, height))
        self.resizable(False, False)
        self.title('Flash-Textus')

        # Background Image
        bg_img = ImageTk.PhotoImage(Image.open("./aldebaran.png").resize((width, height), Image.Resampling.LANCZOS))
        lbl = Label(self, image=bg_img)
        lbl.img = bg_img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.

        # Frame Information #
        frame_info = Frame(self, highlightthickness=0)
        frame_info.pack()

        # Character Per Minute (CPM)
        label_cpm = Label(frame_info, text="Corrected CPM:")
        label_cpm.grid(row=0, column=0, pady=3)

        self.entry_cpm = Entry(frame_info, width=5, bg="white", fg="red")
        self.entry_cpm.insert(2, "?")
        self.entry_cpm["state"] = DISABLED
        self.entry_cpm.grid(row=0, column=1)

        # Words Per Minute (WPM)
        label_wpm = Label(frame_info, text="WPM:")
        label_wpm.grid(row=0, column=2, pady=3)

        self.entry_wpm = Entry(frame_info, width=5, bg="white", fg="red")
        self.entry_wpm.insert(2, "?")
        self.entry_wpm["state"] = DISABLED
        self.entry_wpm.grid(row=0, column=3)

        # Time Left
        label_time = Label(frame_info, text="Time left:")
        label_time.grid(row=0, column=4, pady=3)

        self.time_text = StringVar()
        self.time_text.set("00:60")
        self.entry_time = Entry(frame_info, width=5, bg="white", fg="red", textvariable=self.time_text)
        self.entry_time.grid(row=0, column=5)
        self.entry_time["state"] = DISABLED

        # Start/Restart Button
        self.btn_start = Button(frame_info, bg="#FAC213", width=100, text='Start', command=lambda: self.start_game())
        self.btn_start.grid(row=0, column=6)

        # Frame Display Words -> The frame does not change size based on the input text #
        frame_display_words = Frame(self, width=836, height=270, highlightthickness=0)
        frame_display_words.pack_propagate(False)
        self.text_display_words = Text(frame_display_words, width=1, height=1, bg="white", fg="black",
                                       state="disabled", highlightthickness=0)
        self.text_display_words.pack(fill="both", expand=True, padx=0, pady=0)
        frame_display_words.pack()

        # Frame User Input Words #
        frame_input = Frame(self, highlightthickness=0)
        frame_input.pack()

        self.entry_input_words = Entry(frame_input, width=55, font=('Times New Roman', 30, 'bold'), justify=CENTER)
        self.entry_input_words.insert(0, "Click 'Start' & Type the words here...")
        self.entry_input_words["state"] = "disabled"
        self.entry_input_words.bind("<ButtonRelease-1>", lambda event: self.clean_input())
        self.entry_input_words.bind("<space>", lambda event: self.next_input())
        self.entry_input_words.bind("<KeyRelease>", lambda event: self.update_display())
        self.entry_input_words.grid(row=0, column=5)

    def update_results(self):
        keyword = self.words_selected[self.word_pos]
        user_input = self.entry_input_words.get().strip()
        # Raw CPM
        self.raw_CPM += len(user_input)
        # Correct CPM
        for n in range(0, len(keyword)):
            if keyword[n] == user_input[n]:
                self.correct_CPM += 1
        # Info Stats
        self.entry_cpm["state"] = NORMAL
        self.entry_cpm.delete(0, "end")
        self.entry_cpm.insert(2, f"{self.correct_CPM}")
        self.entry_cpm["state"] = DISABLED

        self.entry_wpm["state"] = NORMAL
        self.entry_wpm.delete(0, "end")
        self.entry_wpm.insert(2, f"{self.correct_CPM/4}")
        self.entry_wpm["state"] = DISABLED

    def next_input(self):
        """ Move to the next word when the user click the space bar """
        # Update the results
        self.update_results()
        # Update the next word
        self.word_pos += 1
        self.entry_input_words.delete(0, "end")
        self.update_display()

    def update_display(self):
        """ Update the Display Text everytime a key is released """
        AppMethods(self.text_display_words, self.words_selected, self.word_pos, self.entry_input_words.get().strip())

    def clean_input(self):
        """ Remove the temporary text in the input entry & Starts the countdown """
        if self.entry_input_words.get():
            self.entry_input_words.delete(0, "end")
            self.total_sec = 60
            self.start_again_countdown = False
            self.countdown()

    def countdown(self):
        """ refresh the content of the Timer Entry Widget every second """
        self.total_sec -= 1    # decrease the time
        mins, secs = divmod(self.total_sec, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # display the new time
        self.time_text.set(timer)
        # request tkinter to call self.refresh after 1s
        if self.start_again_countdown is False:
            if self.total_sec >= 0:
                self.entry_time.after(1000, self.countdown)
            else:
                self.time_text.set("00:00")
                self.show_result()
                return
        else:
            self.time_text.set("00:60")

    def show_result(self):
        """ Show the result window """
        print(f"Raw CPM: {self.raw_CPM} - Correct CPM: {self.correct_CPM} - WPM: {self.correct_CPM/5}")
        window_result = GameResult(self.raw_CPM, self.correct_CPM)

    def start_game(self):
        """ Start/Restart the game """
        # # Clear the Display Words
        self.text_display_words["state"] = "normal"
        self.text_display_words.delete("1.0", "end")
        self.text_display_words["state"] = "disabled"
        # Change message inside the user input
        self.entry_input_words.delete(0, "end")
        self.entry_input_words.insert(0, "Type the words here...")
        self.entry_input_words["state"] = "normal"
        # Stop the timer & Set it back to 60 seconds
        self.start_again_countdown = True
        # Change the Button Text
        self.btn_start['text'] = 'Restart'
        # Start the Game mechanics
        self.words_selected = random.sample(self.english_dic, self.num_words)    # Random selection of words
        AppMethods(self.text_display_words, self.words_selected)
