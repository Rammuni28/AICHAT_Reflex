# state.py
import reflex as rx
import openai
import os



openai.api_key = os.getenv("OPENAI_API_KEY")

class State(rx.State):
    question: str
    chat_history: list[tuple[str, str]]



    def handle_key_press(self, event):
        if event == 'Enter':
          return  self.answer()

            


    def answer(self):
        session = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self.question}
            ],
            stop=None,
            temperature=0.7,
            stream=True,
        )
        answer = ""
        self.chat_history.append((self.question, answer))
        self.question = ""
        yield

        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
            yield
             