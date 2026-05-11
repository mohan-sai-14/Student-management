
import tkinter as tk
from tkinter import ttk, messagebox
import random

# Large question bank including Indian-centric and general knowledge questions
QUESTION_BANK = [
    # Indian History & Geography
    {"question": "Who was the first Prime Minister of India?", "options": ["Jawaharlal Nehru", "Indira Gandhi", "Rajendra Prasad", "Subhash Chandra Bose"], "answer": 0},
    {"question": "What is the capital of Tamil Nadu?", "options": ["Chennai", "Mumbai", "Kolkata", "Hyderabad"], "answer": 0},
    {"question": "Which river is known as the 'Ganges of the South'?", "options": ["Godavari", "Krishna", "Kaveri", "Narmada"], "answer": 2},
    {"question": "In which year did India gain independence?", "options": ["1945", "1947", "1950", "1939"], "answer": 1},
    {"question": "Who was the last Governor-General of independent India?", "options": ["Lord Mountbatten", "C. Rajagopalachari", "Rajendra Prasad", "Liaquat Ali Khan"], "answer": 1},
    {"question": "Which Indian state is known as the 'Land of Five Rivers'?", "options": ["Punjab", "Haryana", "Rajasthan", "Uttar Pradesh"], "answer": 0},
    {"question": "The Ajanta Caves are located in which state?", "options": ["Maharashtra", "Gujarat", "Rajasthan", "Uttar Pradesh"], "answer": 0},
    {"question": "Who founded the Maurya Empire?", "options": ["Ashoka", "Bindusara", "Chandragupta Maurya", "Harsha"], "answer": 2},
    {"question": "What is the national animal of India?", "options": ["Elephant", "Tiger", "Lion", "Peacock"], "answer": 1},
    {"question": "Which Indian festival is known as the 'Festival of Lights'?", "options": ["Holi", "Diwali", "Eid", "Pongal"], "answer": 1},

    # Indian Politics & Current Affairs
    {"question": "Who is the current President of India? (2025)", "options": ["Droupadi Murmu", "Ram Nath Kovind", "Pranab Mukherjee", "Narendra Modi"], "answer": 0},
    {"question": "What is the upper house of Indian Parliament called?", "options": ["Lok Sabha", "Rajya Sabha", "Vidhan Sabha", "Gram Sabha"], "answer": 1},
    {"question": "Which city is the capital of India?", "options": ["Mumbai", "New Delhi", "Chennai", "Bangalore"], "answer": 1},
    {"question": "Who is known as the 'Iron Man of India'?", "options": ["Jawaharlal Nehru", "Sardar Vallabhbhai Patel", "Bhagat Singh", "Subhash Chandra Bose"], "answer": 1},
    {"question": "Which is the largest political party in India by membership?", "options": ["BJP", "Congress", "Aam Aadmi Party", "CPI"], "answer": 0},

    # Indian Science & Technology
    {"question": "Who is known as the father of the Indian nuclear program?", "options": ["Homi J. Bhabha", "C.V. Raman", "Vikram Sarabhai", "A.P.J. Abdul Kalam"], "answer": 0},
    {"question": "Which Indian satellite was the first to be launched?", "options": ["INSAT-1A", "Aryabhata", "Rohini", "GSAT-6"], "answer": 1},
    {"question": "What is the name of India’s Mars Orbiter Mission?", "options": ["Vikram", "Chandrayaan", "Mangalyaan", "Rohini"], "answer": 2},
    {"question": "Who was the first Indian astronaut to go to space?", "options": ["Rakesh Sharma", "Sunita Williams", "Kalpana Chawla", "Srinivasa Ramanujan"], "answer": 0},
    {"question": "The Indian Space Research Organisation (ISRO) is headquartered in which city?", "options": ["Mumbai", "Hyderabad", "Bangalore", "New Delhi"], "answer": 2},

    # Indian Culture & Literature
    {"question": "Who wrote the epic 'Mahabharata'?", "options": ["Valmiki", "Vyasa", "Kalidasa", "Tulsidas"], "answer": 1},
    {"question": "Which dance form is native to Kerala?", "options": ["Bharatanatyam", "Kathak", "Kathakali", "Odissi"], "answer": 2},
    {"question": "What language is the script 'Devanagari' used for?", "options": ["Tamil", "Sanskrit", "Gujarati", "Punjabi"], "answer": 1},
    {"question": "Which festival celebrates the arrival of spring in India?", "options": ["Diwali", "Holi", "Eid", "Raksha Bandhan"], "answer": 1},
    {"question": "Rabindranath Tagore won the Nobel Prize for Literature in which year?", "options": ["1913", "1921", "1930", "1947"], "answer": 0},

    # General Knowledge
    {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Gd", "Go"], "answer": 0},
    {"question": "Which planet is closest to the sun?", "options": ["Venus", "Earth", "Mercury", "Mars"], "answer": 2},
    {"question": "Who painted the Mona Lisa?", "options": ["Vincent Van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "answer": 2},
    {"question": "What is the hardest natural substance on Earth?", "options": ["Gold", "Diamond", "Iron", "Silver"], "answer": 1},
    {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"], "answer": 2},

    # More Indian Geography & Miscellaneous
    {"question": "Which is the largest desert in India?", "options": ["Thar Desert", "Rann of Kutch", "Sundarbans", "Deccan Plateau"], "answer": 0},
    {"question": "Which Indian state has the largest area?", "options": ["Maharashtra", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh"], "answer": 1},
    {"question": "Which mountain range is called the 'Water Tower of India'?", "options": ["Aravalli", "Himalayas", "Western Ghats", "Vindhyas"], "answer": 1},
    {"question": "India shares its longest border with which country?", "options": ["China", "Pakistan", "Bangladesh", "Nepal"], "answer": 2},
    {"question": "Which city is known as the 'Pink City' of India?", "options": ["Jaipur", "Udaipur", "Jodhpur", "Ajmer"], "answer": 0},

    # Indian Sports
    {"question": "Who is known as the 'Master Blaster' in Indian cricket?", "options": ["Virat Kohli", "MS Dhoni", "Sachin Tendulkar", "Rahul Dravid"], "answer": 2},
    {"question": "Where were the first Asian Games held in India?", "options": ["Chennai", "New Delhi", "Kolkata", "Mumbai"], "answer": 1},
    {"question": "Which Indian badminton player won the World Championship in 2022?", "options": ["P.V. Sindhu", "Saina Nehwal", "Kidambi Srikanth", "Prakash Padukone"], "answer": 0},
    {"question": "In which sport does India hold the Hockey World Cup titles?", "options": ["Cricket", "Football", "Hockey", "Badminton"], "answer": 2},
    {"question": "Who was India's first Olympic gold medalist?", "options": ["Abhinav Bindra", "K.D. Jadhav", "Norman Pritchard", "Leander Paes"], "answer": 2},

    # Indian Economy & Society
    {"question": "What is the currency of India?", "options": ["Dollar", "Rupee", "Yen", "Euro"], "answer": 1},
    {"question": "Which is India's largest bank?", "options": ["State Bank of India", "HDFC Bank", "ICICI Bank", "Punjab National Bank"], "answer": 0},
    {"question": "Which Indian city is known as the 'Silicon Valley of India'?", "options": ["Hyderabad", "Pune", "Bangalore", "Chennai"], "answer": 2},
    {"question": "Which sector contributes the most to India’s GDP?", "options": ["Agriculture", "Industry", "Services", "Manufacturing"], "answer": 2},
    {"question": "What is the literacy rate of India as per 2021 data (approx)?", "options": ["70%", "77%", "85%", "90%"], "answer": 1},

    # Indian Constitution & Law
    {"question": "Who is known as the 'Father of the Indian Constitution'?", "options": ["Jawaharlal Nehru", "Dr. B.R. Ambedkar", "Sardar Patel", "Rajendra Prasad"], "answer": 1},
    {"question": "What type of government does India have?", "options": ["Monarchy", "Federal Parliamentary Democratic Republic", "Dictatorship", "Socialist State"], "answer": 1},
    {"question": "How many fundamental rights are there in the Indian Constitution?", "options": ["5", "6", "7", "8"], "answer": 2},
    {"question": "What is the maximum age for election as President of India?", "options": ["30 years", "35 years", "40 years", "45 years"], "answer": 1},
    {"question": "Who appoints the Chief Justice of India?", "options": ["Prime Minister", "President", "Parliament", "Supreme Court"], "answer": 1},
]

QUIZ_SIZE = 10  # Number of questions per quiz

class QuizApp(tk.Tk):
    def __init__(self, question_bank, quiz_size=10):
        super().__init__()
        self.title("Quiz App - Indian & General Knowledge")
        self.geometry("700x450")
        self.resizable(False, False)

        self.question_bank = question_bank
        self.quiz_size = quiz_size

        self.prepare_quiz()
        self.current_index = 0
        self.user_answers = [None] * self.quiz_size

        self.create_widgets()
        self.display_question()

    def prepare_quiz(self):
        self.questions = random.sample(self.question_bank, self.quiz_size)

    def create_widgets(self):
        # Question Label
        self.question_label = ttk.Label(self, text="", wraplength=650, font=("Arial", 16))
        self.question_label.pack(pady=20)

        # Options (Radio Buttons)
        self.selected_option = tk.IntVar(value=-1)
        self.option_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self, text="", variable=self.selected_option, value=i)
            rb.pack(anchor=tk.W, padx=60, pady=5)
            self.option_buttons.append(rb)

        # Navigation Buttons Frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=20)

        self.prev_btn = ttk.Button(nav_frame, text="Previous", command=self.prev_question)
        self.prev_btn.grid(row=0, column=0, padx=15)

        self.next_btn = ttk.Button(nav_frame, text="Next", command=self.next_question)
        self.next_btn.grid(row=0, column=1, padx=15)

        self.submit_btn = ttk.Button(self, text="Submit Quiz", command=self.submit_quiz)
        self.submit_btn.pack()

        # Status Label
        self.status_label = ttk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def display_question(self):
        q = self.questions[self.current_index]
        self.question_label.config(text=f"Q{self.current_index + 1}: {q['question']}")
        self.selected_option.set(-1 if self.user_answers[self.current_index] is None else self.user_answers[self.current_index])
        for i, option_text in enumerate(q["options"]):
            self.option_buttons[i].config(text=option_text)

        # Disable prev on first, next on last
        self.prev_btn.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_index < self.quiz_size - 1 else tk.DISABLED)

        self.status_label.config(text=f"Question {self.current_index + 1} of {self.quiz_size}")

    def save_answer(self):
        selected = self.selected_option.get()
        if selected >= 0:
            self.user_answers[self.current_index] = selected

    def next_question(self):
        self.save_answer()
        if self.current_index < self.quiz_size - 1:
            self.current_index += 1
            self.display_question()

    def prev_question(self):
        self.save_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.display_question()

    def submit_quiz(self):
        self.save_answer()
        if None in self.user_answers:
            if not messagebox.askyesno("Confirm Submit", "You have unanswered questions. Submit anyway?"):
                return
        score = sum(1 for i, ans in enumerate(self.user_answers) if ans == self.questions[i]["answer"])
        total = self.quiz_size
        messagebox.showinfo("Quiz Result", f"Your Score: {score} / {total}\n\nThank you for playing!")
        if messagebox.askyesno("Restart Quiz", "Do you want to restart the quiz?"):
            self.restart_quiz()
        else:
            self.destroy()

    def restart_quiz(self):
        self.prepare_quiz()
        self.user_answers = [None] * self.quiz_size
        self.current_index = 0
        self.display_question()

if __name__ == "__main__":
    app = QuizApp(QUESTION_BANK, QUIZ_SIZE)
    app.mainloop()
