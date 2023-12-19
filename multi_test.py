# lesson
# The goal of this project is to replicate 'multiplication_test.py' without using the pyinputplus module

# for loop 10x and put each question inside of a while loop for x < 3 and time < 8 seconds

import time, random, threading

numberOfQuestions = 10
correctAnswers = 0

def question_input(question_number: int, num1: int, num2: int) -> int:
    num1 = random.randint(0,9)
    num2 = random.randint(0,9)
    response = input(f'#{question_number}: {num1} x {num2} = ')
    answer = num1 * num2
    return answer, response

def input_validate(correct_answer: int, user_input: int) -> bool|str:
    if user_input == correct_answer:
        print('Correct!')
        time.sleep(1)
        return True
    elif user_input != correct_answer:
        print('Incorrect!')
    else:
        print('error')

def timer():
    time.sleep(8)
    return 

if __name__ == '__main__':
    for i in range(10):
        answer_count = 0
        while answer_count < 3:
            # thread1 = threading.Thread(target=timer)
            answer, response = question_input(question_number=i, num1=0, num2=0)
            input_validate(answer, response)
            answer_count += 1
            if input_validate == True:
                break
            
            