import threading, time, random
import concurrent.futures

# create two random numbers inside of the main so they can be accessed by everyone

timer_switch = True

def timer():
    time_counter = 0
    while timer_switch == True:
        time.sleep(1)
        time_counter += 1
    
    return time_counter >= 8

def ask_question(question_no):
    num1 = random.randint(0,9)
    num2 = random.randint(0,9)
    answ = num1 * num2

    user_input = f'#{question_no}: {num1} x {num2} = '
    
    return user_input, answ

def validate_question(user_response, answer):
    try:
        if int(user_response) != answer:
            # validate timer first
            print('Incorrect')
            return False
        
        elif int(user_response) == answer:
            print('Correct')
            time.sleep(1)
            return True
        else:
            print('AnswerError')
    except ValueError:
        print("Please input a number")

def main():
    number_of_questions = 10
    correct_answers = 0
    executor = concurrent.futures.ThreadPoolExecutor()

    for question_no in range(number_of_questions):
        global timer_switch
        tries = 0
        current_question, answer = ask_question(question_no) # ask question
        
        while tries < 3:
            timer_switch = True
            timer_task = executor.submit(timer)
            user_response = input(current_question)
            timer_switch = False
        
            if timer_task.result() == True:
                print('Out of time')
                break
            elif timer_task.result() == False:
                question_response_validated = validate_question(user_response, answer)
                if question_response_validated == False:
                    tries += 1
                elif question_response_validated == True:
                    correct_answers += 1
                    break
            else:
                print('TimerError')
    print(f'Score: {correct_answers} / {number_of_questions}')

    

if __name__ == '__main__':
    main()
