import tkinter as tk
from tkinter import ttk, messagebox
import random

class TambolaTicketFrame(ttk.Frame):
    def __init__(self, master, ticket_numbers, player_num, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.ticket_numbers = ticket_numbers  # 3x9 grid with 0 for blanks
        self.player_num = player_num
        self.labels = []
        self.marked_numbers = set()

        self.jaldi5_done = False
        self.first_line_done = False
        self.second_line_done = False
        self.third_line_done = False
        self.housie_done = False

        ttk.Label(self, text=f"Player {player_num}", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=9, pady=5)

        for r in range(3):
            row_labels = []
            for c in range(9):
                num = ticket_numbers[r][c]
                if num == 0:
                    lbl = tk.Label(self, text="", width=4, height=2, relief=tk.FLAT, bg="white")
                else:
                    lbl = tk.Label(self, text=str(num), width=4, height=2, relief=tk.RIDGE, bg="white",
                                   font=("Helvetica", 10, "bold"))
                lbl.grid(row=r+1, column=c, padx=1, pady=1)
                row_labels.append(lbl)
            self.labels.append(row_labels)

    def mark_number(self, number):
        for r in range(3):
            for c in range(9):
                if self.ticket_numbers[r][c] == number:
                    self.labels[r][c].config(bg="lightgreen")
                    self.marked_numbers.add(number)

    def check_jaldi5(self):
        if not self.jaldi5_done and len(self.marked_numbers) >= 5:
            self.jaldi5_done = True
            return True
        return False

    def check_line(self, row):
        if (row == 0 and self.first_line_done) or \
           (row == 1 and self.second_line_done) or \
           (row == 2 and self.third_line_done):
            return False  # already done

        count_marked = 0
        for c in range(9):
            num = self.ticket_numbers[row][c]
            if num != 0 and num in self.marked_numbers:
                count_marked += 1
        if count_marked == 5:
            if row == 0:
                self.first_line_done = True
            elif row == 1:
                self.second_line_done = True
            else:
                self.third_line_done = True
            return True
        return False

    def check_housie(self):
        if self.housie_done:
            return False
        if len(self.marked_numbers) == 15:
            self.housie_done = True
            return True
        return False


def generate_ticket():
    col_ranges = [
        range(1, 10), range(10, 20), range(20, 30), range(30, 40),
        range(40, 50), range(50, 60), range(60, 70), range(70, 80), range(80, 91)
    ]

    ticket_nums = [[] for _ in range(9)]
    for c, crange in enumerate(col_ranges):
        num = random.choice(list(crange))
        ticket_nums[c].append(num)

    remaining_numbers_needed = 15 - 9
    while remaining_numbers_needed > 0:
        c = random.randint(0, 8)
        if len(ticket_nums[c]) < 3:
            possible_numbers = set(col_ranges[c]) - set(ticket_nums[c])
            if possible_numbers:
                num = random.choice(list(possible_numbers))
                ticket_nums[c].append(num)
                remaining_numbers_needed -= 1

    for c in range(9):
        ticket_nums[c].sort()

    rows = [[0]*9 for _ in range(3)]
    for c in range(9):
        nums = ticket_nums[c]
        positions = random.sample(range(3), len(nums))
        for r, num in zip(positions, nums):
            rows[r][c] = num

    for r in range(3):
        count = sum(1 for x in rows[r] if x != 0)
        while count != 5:
            if count < 5:
                for c in range(9):
                    if rows[r][c] == 0:
                        for rr in range(3):
                            if rr != r and rows[rr][c] != 0 and sum(1 for x in rows[rr] if x != 0) > 5:
                                rows[r][c], rows[rr][c] = rows[rr][c], 0
                                count += 1
                                break
                        if count == 5:
                            break
            else:
                for c in range(9):
                    if rows[r][c] != 0:
                        for rr in range(3):
                            if rr != r and rows[rr][c] == 0 and sum(1 for x in rows[rr] if x != 0) < 5:
                                rows[rr][c], rows[r][c] = rows[r][c], 0
                                count -= 1
                                break
                        if count == 5:
                            break

    return rows


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=500)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class TambolaGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tambola / Housie / Bingo Game")
        self.geometry("1100x650")
        self.resizable(False, False)

        self.num_tickets = 0
        self.tickets_frames = []
        self.tickets_window = None

        self.drawn_numbers = []
        self.remaining_numbers = []

        self.prizes_announced = {
            "jaldi5": set(),
            "first_line": set(),
            "second_line": set(),
            "third_line": set(),
            "housie": set(),
        }

        self.create_widgets()

    def create_widgets(self):
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Number of Tickets (Players):").grid(row=0, column=0, padx=5)
        self.ticket_count_entry = ttk.Entry(control_frame, width=5)
        self.ticket_count_entry.grid(row=0, column=1, padx=5)
        self.ticket_count_entry.insert(0, "1")

        self.start_button = ttk.Button(control_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=2, padx=10)

        self.draw_button = ttk.Button(control_frame, text="Draw Number", command=self.draw_number, state=tk.DISABLED)
        self.draw_button.grid(row=0, column=3, padx=10)

        self.reset_button = ttk.Button(control_frame, text="Reset Game", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=4, padx=10)

        winner_frame = ttk.LabelFrame(self, text="Prize Announcements", padding=10)
        winner_frame.pack(pady=10, fill=tk.X, padx=20)

        self.winner_text = tk.Text(winner_frame, height=7, state=tk.DISABLED, font=("Helvetica", 11))
        self.winner_text.pack(fill=tk.X)

        drawn_frame = ttk.LabelFrame(self, text="Drawn Numbers", padding=10)
        drawn_frame.pack(pady=10, fill=tk.BOTH, expand=False, padx=20)

        numbers_frame = ttk.Frame(drawn_frame)
        numbers_frame.pack()

        self.drawn_number_labels = {}
        for i in range(1, 91):
            row = (i-1)//9
            col = (i-1)%9
            lbl = tk.Label(numbers_frame, text=str(i), width=4, height=2, relief=tk.RIDGE, bg="white",
                           font=("Helvetica", 10))
            lbl.grid(row=row, column=col, padx=2, pady=2)
            self.drawn_number_labels[i] = lbl

        self.last_number_var = tk.StringVar(value="Last Drawn: None")
        self.last_number_label = ttk.Label(self, textvariable=self.last_number_var,
                                           font=("Helvetica", 18, "bold"))
        self.last_number_label.pack(pady=10)

    def start_game(self):
        try:
            count = int(self.ticket_count_entry.get())
            if count < 1:
                raise ValueError
            self.num_tickets = count
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for number of tickets.")
            return

        self.remaining_numbers = list(range(1, 91))
        random.shuffle(self.remaining_numbers)
        self.drawn_numbers = []

        self.prizes_announced = {
            "jaldi5": set(),
            "first_line": set(),
            "second_line": set(),
            "third_line": set(),
            "housie": set(),
        }

        # If old tickets window exists, destroy it
        if self.tickets_window and self.tickets_window.winfo_exists():
            self.tickets_window.destroy()

        # Create new tickets window
        self.tickets_window = tk.Toplevel(self)
        self.tickets_window.title("Tickets")
        self.tickets_window.geometry("1000x600")
        self.tickets_window.resizable(False, False)

        container = ScrollableFrame(self.tickets_window)
        container.pack(fill="both", expand=True)

        self.tickets_frames.clear()
        for i in range(1, self.num_tickets + 1):
            ticket_nums = generate_ticket()
            ticket_frame = TambolaTicketFrame(container.scrollable_frame, ticket_nums, i, relief=tk.GROOVE, borderwidth=2)
            ticket_frame.pack(padx=5, pady=5, fill="x", anchor="n")
            self.tickets_frames.append(ticket_frame)

        # Reset drawn number board
        for lbl in self.drawn_number_labels.values():
            lbl.config(bg="white")

        self.last_number_var.set("Last Drawn: None")
        self.draw_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.ticket_count_entry.config(state=tk.DISABLED)

        self.clear_winner_text()

    def draw_number(self):
        if not self.remaining_numbers:
            messagebox.showinfo("Game Over", "All numbers have been drawn!")
            self.draw_button.config(state=tk.DISABLED)
            return

        number = self.remaining_numbers.pop(0)
        self.drawn_numbers.append(number)
        self.last_number_var.set(f"Last Drawn: {number}")

        self.drawn_number_labels[number].config(bg="lightgreen")

        for ticket in self.tickets_frames:
            ticket.mark_number(number)

        self.check_prizes()

    def check_prizes(self):
        announcements = []

        for idx, ticket in enumerate(self.tickets_frames, start=1):
            if ticket.check_jaldi5() and idx not in self.prizes_announced["jaldi5"]:
                self.prizes_announced["jaldi5"].add(idx)
                announcements.append(f"Player {idx} got Jaldi 5!")

            if ticket.check_line(0) and idx not in self.prizes_announced["first_line"]:
                self.prizes_announced["first_line"].add(idx)
                announcements.append(f"Player {idx} completed 1st Line!")

            if ticket.check_line(1) and idx not in self.prizes_announced["second_line"]:
                self.prizes_announced["second_line"].add(idx)
                announcements.append(f"Player {idx} completed 2nd Line!")

            if ticket.check_line(2) and idx not in self.prizes_announced["third_line"]:
                self.prizes_announced["third_line"].add(idx)
                announcements.append(f"Player {idx} completed 3rd Line!")

            if ticket.check_housie() and idx not in self.prizes_announced["housie"]:
                self.prizes_announced["housie"].add(idx)
                announcements.append(f"Player {idx} got Housie! 🎉")

        if announcements:
            self.append_winner_text("\n".join(announcements))
            if any("Housie" in a for a in announcements):
                messagebox.showinfo("Game Over", "Housie won! Game Over.")
                self.draw_button.config(state=tk.DISABLED)

    def append_winner_text(self, text):
        self.winner_text.config(state=tk.NORMAL)
        self.winner_text.insert(tk.END, text + "\n")
        self.winner_text.see(tk.END)
        self.winner_text.config(state=tk.DISABLED)

    def clear_winner_text(self):
        self.winner_text.config(state=tk.NORMAL)
        self.winner_text.delete("1.0", tk.END)
        self.winner_text.config(state=tk.DISABLED)

    def reset_game(self):
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            if self.tickets_window and self.tickets_window.winfo_exists():
                self.tickets_window.destroy()
            self.tickets_frames.clear()

            for lbl in self.drawn_number_labels.values():
                lbl.config(bg="white")

            self.drawn_numbers.clear()
            self.remaining_numbers.clear()

            self.prizes_announced = {
                "jaldi5": set(),
                "first_line": set(),
                "second_line": set(),
                "third_line": set(),
                "housie": set(),
            }

            self.last_number_var.set("Last Drawn: None")
            self.start_button.config(state=tk.NORMAL)
            self.draw_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            self.ticket_count_entry.config(state=tk.NORMAL)

            self.clear_winner_text()


if __name__ == "__main__":
    app = TambolaGame()
    app.mainloop()
