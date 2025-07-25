import pandas as pd
import customtkinter as ctk
import random

def load_data() -> pd.DataFrame:
    try:
        data = pd.read_csv('resources/question_pool.csv')
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return pd.DataFrame()

class QuestionCache:
    cache = set()

    @classmethod
    def load_cache(cls, ttl_questions):
        cls.cache = set(range(1, ttl_questions + 1))

    @classmethod
    def remove_item(cls, question_number: int):
        cls.cache.discard(question_number)

    @classmethod
    def return_cache_options(cls):
        return cls.cache

    @classmethod
    def pick_question_number(cls) -> int:
        if not cls.cache:
            return None
        picked_id = random.choice(list(cls.cache))
        cls.remove_item(picked_id)
        return picked_id

def return_question_dictionary(data, question_number):
    df = data[data['id'] == question_number]
    if df.empty:
        return None
    return df.iloc[0].to_dict()

def submit_answer(selected_option, correct_answer, result_label, score_label, state):
    if state["first_attempt_made"]:
        return  # Only count the first attempt

    selected = selected_option.get()
    if not selected:
        return  # No option selected

    state["first_attempt_made"] = True
    state["total_answered"] += 1

    if selected == correct_answer:
        state["correct_on_first_try"] += 1
        result_label.configure(text="✅ Correct!", text_color="green")
    else:
        result_label.configure(text="❌ Incorrect.", text_color="red")

    percent = round((state["correct_on_first_try"] / state["total_answered"]) * 100)
    score_label.configure(text=f"{state['correct_on_first_try']}/{state['total_answered']} answered – {percent}%")

def main():
    question_pool = load_data()
    if question_pool.empty:
        print("No data loaded.")
        return

    question_pool['id'] = question_pool['id'].astype(int)
    ttl_questions = int(question_pool['id'].max())
    QuestionCache.load_cache(ttl_questions)

    app = ctk.CTk()
    app.geometry("600x700")
    app.title("PMP Questionnaire")

    # Shared state dictionary
    state = {
        "first_attempt_made": False,
        "total_answered": 0,
        "correct_on_first_try": 0
    }

    # UI elements
    selected_option = ctk.StringVar()
    radio_buttons = {}
    result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=14))
    question_label = ctk.CTkLabel(app, text="", wraplength=450, font=ctk.CTkFont(size=16, weight="bold"))
    score_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=14, weight="bold"))

    def load_new_question():
        state["first_attempt_made"] = False
        selected_option.set("")
        result_label.configure(text="")

        question_id = QuestionCache.pick_question_number()
        if question_id is None:
            question_label.configure(text="🎉 All questions completed!")
            for rb in radio_buttons.values():
                rb.pack_forget()
            submit_btn.configure(state="disabled")
            next_btn.configure(state="disabled")
            return

        data = return_question_dictionary(question_pool, question_id)
        question_label.configure(text=f"Question {data['id']}: {data['question_text']}")
        for key in ['a', 'b', 'c', 'd']:
            radio_buttons[key].configure(text=f"{key.upper()}: {data[key]}")
        submit_btn.configure(command=lambda: submit_answer(
            selected_option, data['answer'], result_label, score_label, state
        ))

    # Layout
    question_label.pack(pady=20)

    for key in ['a', 'b', 'c', 'd']:
        rb = ctk.CTkRadioButton(app, text="", variable=selected_option, value=key)
        rb.pack(anchor='w', padx=40, pady=5, fill='x') 
        radio_buttons[key] = rb

    submit_btn = ctk.CTkButton(app, text="Submit")
    submit_btn.pack(pady=5)

    next_btn = ctk.CTkButton(app, text="Next", command=load_new_question)
    next_btn.pack(pady=5)

    result_label.pack(pady=10)
    score_label.pack(pady=10)

    load_new_question()

    app.mainloop()

if __name__ == '__main__':
    main()