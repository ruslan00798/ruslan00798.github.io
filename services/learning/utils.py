#utils.py

def check_answer(
    user_answer: str,
    correct_answer: str,
)-> bool:
    
    return (
        user_answer.strip().lower()
        ==
        correct_answer.strip().lower()
    )