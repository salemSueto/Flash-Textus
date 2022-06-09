from tkinter import Tk, Label, Frame
from tkmacosx import Button


class GameResult():
    def __init__(self, raw_cpm, correct_cpm):
        # --- Arguments --- #
        self.raw_cpm = raw_cpm
        self.correct_cpm = correct_cpm
        # --- GUI --- #
        # Window
        self.window = Tk()
        self.window.title('Results Summary')
        self.window.minsize(width=300, height=150)
        self.window.resizable(False, False)
        self.window.attributes('-topmost', 1)

        # Frame
        frame_info = Frame(self.window, highlightthickness=0)
        frame_info.pack()

        # Labels
        label_percentile = Label(frame_info, text="Percentile", anchor='w', width=30)
        label_raw_cpm = Label(frame_info, text="Raw CPM", anchor='w', width=30)
        label_cpm = Label(frame_info, text="Corrected CPM",  anchor='w', width=30)
        label_wpm = Label(frame_info, text="WPM",  anchor='w', width=30)

        label_percentile.grid(row=0, column=0, pady=3)
        label_raw_cpm.grid(row=1, column=0, pady=3)
        label_cpm.grid(row=2, column=0, pady=3)
        label_wpm.grid(row=3, column=0, pady=3)

        # Results
        label_percentile_res = Label(frame_info, text=self.user_percentile(self.correct_cpm), anchor='w', width=30)
        label_raw_cpm_res = Label(frame_info, text=self.raw_cpm, anchor='w', width=30)
        label_cpm_res = Label(frame_info, text=self.correct_cpm, anchor='w', width=30)
        label_wpm_res = Label(frame_info, text=self.correct_cpm/4, anchor='w', width=30)

        label_percentile_res.grid(row=0, column=1, pady=3)
        label_raw_cpm_res.grid(row=1, column=1, pady=3)
        label_cpm_res.grid(row=2, column=1, pady=3)
        label_wpm_res.grid(row=3, column=1, pady=3)

        btn_ok = Button(self.window, text='Ok', command=self.close_window)
        btn_ok.pack(expand=True)

        self.window.mainloop()

    # Find the Percentile
    def user_percentile(self, correct_cpm):
        # STATS -> https://typing-speed-test.aoeu.eu/
        cpm_stats = {
            "30": 0, "40": 0, "50": 1, "60": 1, "70": 3, "80": 4, "90": 6, "100": 8, "110": 11, "120": 14, "130": 17,
            "140": 21, "150": 25, "160": 28, "170": 32, "180": 36, "190": 40, "200": 44, "210": 47, "220": 51,
            "230": 54, "240": 57, "250": 60, "260": 63, "270": 66, "280": 69, "290": 71, "300": 73, "310": 76,
            "320": 78, "330": 80, "340": 82, "350": 83, "360": 85, "370": 86, "380": 88, "390": 89, "400": 90,
            "410": 91, "420": 92, "430": 93, "440": 94, "450": 95, "460": 95, "470": 96, "480": 97, "490": 97,
            "500": 97, "510": 98, "520": 98, "530": 98, "540": 99, "550": 99, "560": 99, "570": 99, "580": 99,
            "590": 100, "600": 100, "610": 100, "620": 100, "630": 100, "640": 100, "650": 100, "660": 100, "670": 100,
            "680": 100, "690": 100, "700": 100
        }

        min_diff = 1000
        min_diff_key = ""
        for n in cpm_stats.keys():
            if abs(correct_cpm - int(n)) < min_diff:
                min_diff = abs(correct_cpm - int(n))
                min_diff_key = n

        return cpm_stats[min_diff_key]

    # Close window
    def close_window(self):
        self.window.destroy()
        self.window.quit()
