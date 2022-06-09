from tkinter import END, INSERT, font



class AppMethods:
    def __init__(self, display_words, word_list, word_pos=0, user_input_string=""):
        """ Show the words and highlight the word and the character that are being written """
        # Arguments
        self.text_display = display_words
        self.word_list = word_list
        self.main_word_pos = word_pos
        self.user_input_string = user_input_string
        # Display Preparation
        # Clear the Display Words
        self.text_display["state"] = "normal"
        self.text_display.delete("1.0", "end")
        self.text_display["state"] = "disabled"
        # Display Parameters
        self.font_family = "Courier New"
        self.text_display.config(font=(font.families()[font.families().index(self.font_family)], 30))
        self.text_display.tag_configure("empty")
        self.text_display.tag_configure('main', background='cyan', relief='raised')
        self.text_display.tag_configure('main_chr_correct', background='green', relief='raised')
        self.text_display.tag_configure('main_chr_wrong', background='red', relief='raised')
        # Show the words in the Display Area
        self.max_chr_per_line = self.max_chr_per_line()
        self.show_words()

    def show_words(self):
        """ organise the words in the display frame """
        # Make the text_display widget state normal
        self.text_display["state"] = "normal"
        # Insert the next four words
        self.text_display.insert(INSERT, "\n")
        words_to_write = ""
        for n in range(self.main_word_pos, self.main_word_pos+5):
            remaining_space = self.max_chr_per_line - len(self.word_list[n])
            if len(self.word_list[n]) % 2 == 0:
                empty_side = " " * round(remaining_space / 2)
                comb_string = empty_side + self.word_list[n] + empty_side + "\n"
            else:
                empty_side = " " * round((remaining_space - 1) / 2)
                comb_string = empty_side + self.word_list[n] + empty_side + " " + "\n"
            words_to_write += comb_string
        self.text_display.insert(INSERT, words_to_write)
        # Highlight the main word and the character that is being written
        self.search_main_word(self.text_display, self.word_list[self.main_word_pos], "main")

        # Disable the text_display widget state
        self.text_display["state"] = "disabled"

    def search_main_word(self, text_widget, keyword, tag_word):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag_word, idx, pos)
            # Check if the input string is equal to the main word
            if len(self.user_input_string) <= len(keyword):
                for i in range(0, len(self.user_input_string)):
                    pos_chr = '{}+{}c'.format(idx, i+1)
                    if i <= len(keyword):
                        if self.user_input_string[i] == keyword[i]:
                            text_widget.tag_add("main_chr_correct", idx, pos_chr)
                        else:
                            text_widget.tag_add("main_chr_wrong", idx, pos_chr)
            else:
                text_widget.tag_add("main_chr_wrong", idx, pos)

    def max_chr_per_line(self):
        """ Obtain the maximum number of character that can fit on one line """
        self.text_display.update_idletasks()
        total_width_pixel = self.text_display.winfo_width()
        text_font = font.Font(family=self.font_family, size=30)

        count_chr = -1
        text_try = "A"
        text_try_pixel = text_font.measure(text_try)
        while text_try_pixel < total_width_pixel:
            text_try_pixel = text_font.measure(text_try)
            text_try += "A"
            count_chr += 1
        return count_chr




# Create a list of lists where in each inter list you save the length of each word

# --- START THE GAME --- #
            # When the timer is zero -> send information to the result window