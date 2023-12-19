# Writeup on the Multliplication Test from Automate the Boring Stuff with Python
#### The point of this project was to emulate the code provided in the book without using the provided module.

## Concepts used:
### 1. Concurrent.Futures
This is a built in module to python that deals with asynchronously executing callables.
#### ThreadPoolExecutor
Threads enqueued into the pool will execute tasks and return to the pool so they can be reused instead of dying.
```python
executor = concurrent.futures.ThreadPoolExecutor()

timer_task = executor.submit(timer)
if timer_task.result() == True:
    print('Out of time')
    break
```
#### ProcessPoolExecutor
Same as Threadpoolexecutor except that processes are used instead of threads. This allows it to side step the GIL and execute multiple things at the same time. 
```python
with concurrent.futures.ProcessPoolExecutor() as executor:
    for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
        print('%d is prime: %s' % (number, prime))
```
#### Future Objects
Future objects are whats returned from either executors. Treat futures like normal functions/variables where its what you return from the pool. So for instance if I used threadpoolexecutor to process multiple url's and scrape them for data, by calling `executor.result()` you can get the return of the function.




### 2. Shared Variables
Shared variables are something I learned about with ChatGPT's assistance. In the code i use the line `time_switch = True`. This does the following things:
* Signals to my timer function that since that variable is True, run the while loop(timer).
* Accessable by all functions since its in the global scope.
* Other functions can swap its value as required to immediately affect the timer function(threaded)
 



### 3. Returning a bool expression(ex.  return variable > 2)
Boolean values are easy to work with. That's why returning them from functions is so convinient, it's either a True, False, or null. Especailly during this project where I had to work with a threaded function. My function was giving me issues where it would TimeoutError if I just stopped it, since it wanted to run infinitely. My workaround was by putting checks in place and having the output as the objective fact on if the time was less than 8 seconds. This allowed me to change from working with numbers to a True/False value.
```python
timer_switch = True

def timer():
    time_counter = 0
    while timer_switch == True:
        time.sleep(1)
        time_counter += 1
    
    return time_counter >= 8
```



### 4. Signal Module
The signal module is a simple way to end processes which are longer by nature. As in, processes which may want to end early, or would like a definite end time. A good example of what the signal module is good at doing is saying run a function for a set amount of minutes and return the result. We don't care about completeing the process, only about seeing where the function is at after the amount of time.
#### Pros of Signal (vs multithreading/multiprocessing)
* Easy
    * Doesn't take much to learn in order to understand interupts.
    * Fast to write 
    * Reading signal code is simple
* Many different signals available to use(i.e window resize, killprocess, user input...)
* When working with timers, the Signal Module is a great way to handle the stopping of them

#### Cons of Signal (vs multithreading/multiprocessing)
* As in the name Signal, it's good at dealing with sending signals but not good at doing multiple things at once. So, while you can use multithreading to accomplish the same goal it's more difficult. And thats the good thing about these types of modules, they're sufficiently complex where they can do more than just handle the signal to stop a process or print out a specific result.




## Original Code
This code asks the user 10 multliplication questions and evaluates each question with the module created by the author. The authors challenge was to make this same program without the function which turned out to be even more difficult for me than he said. My biggest struggle was with timer for the background where I ended up using threading/threadpoolexecutor.
```python
import pyinputplus as pyip
import time, random

numberOfQuestions = 10
correctAnswers = 0

for questionNumber in range(numberOfQuestions):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    prompt = '#%s: %s x %s = ' % (questionNumber, num1, num2)

    try:
        pyip.inputStr(prompt, allowRegexes=['^%s$' % (num1 * num2)], 
                    blockRegexes=[('.*', 'Incorrect!')], 
                    timeout=8, 
                    limit=3)
        
    except pyip.TimeoutException:
        print("Out of time")
    except pyip.RetryLimitException:
        print("Out of tries!")
    else:
        print("Correct")
        correctAnswers += 1
    time.sleep(1)

print('Score: %s / %s' % (correctAnswers, numberOfQuestions))
```
### Pyinputplus
A general input module that strictly builds onto the existing input function. Includes support of addresses, bools, choice, date, datetime etc. Has quite a few powerful features like timeout which refers back to the signal module. This feature in the inputs allows you to only give the user a number of seconds before the input is invalid. Other than that theres also defaults, limits, and strips that are availible to users.
```python
import pyinputplus as pyip
```





## Breakdown of project

### Initial File (multi_test.py)
```python
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
```
#### Goals
1. Break up the code into core functions (question, validate answer, and timer)
2. Call code inside of `if __name__ == '__main__'`
3. Provide overview of code easy to read and understand flow from single block

#### Control Flow
1. Define question function: Ask question and return the answer given by the user and what the correct answer is
2. Define validation function: Use the returns from the question function to evaluate if the answer was correct
3. Define timer function: Make an 8 second timer which will stop the question once completed
4. Bring everything together and establish asking 10 questions

#### Shortcomings
* With using threading using the line `time.sleep(8)` won't work as intended. Multithreading relys on I/O bound stoppages to process other code. And in this case it would take 8 seconds for the timer to finish meaning that each question would take that long regardless of how fast the answer was inputted.
* Also I didn't know how to use threading which ended up with me creating an entire side project just to explore multithreading and queues. So I was trying to use threading but i had no clue.
* I was returning multiple variables which isnt horrible, just messy from the question function. Those could've been handled on the global score so anyone can interact with the information instead of having to 'handshake' it back and forth.

#### What happened after these shortcomings
With all these breakpoints, I decided to make the Process Orders project and come back after I understood threading better. Also I had to clean code and find a better way to work with the timer. So in V2 that's exactly what I did.




### V2 File (multi_test_V2.py)

#### Timer Function
The improved Timer function uses a global variable and per second sleeps and checks if the global variable is still True. But after a question is answered its changed to False which stops the timer. This function is asynchronous which was one of my goals.
```python
timer_switch = True

def timer():
    time_counter = 0
    while timer_switch == True:
        time.sleep(1)
        time_counter += 1
    
    return time_counter >= 8
```
#### Ask Question Function
After providing which question the program is on, generates a question as well as its answer. And since we return the question and answer we can continue to repeat the same question over and over without making a new question. That was because one of my constraints with this project was that everything had to be exactly the same as with the original project. So if the inputted answer was incorrect it would use the same question to ask again.
```python
def ask_question(question_no):
    num1 = random.randint(0,9)
    num2 = random.randint(0,9)
    answ = num1 * num2

    user_input = f'#{question_no}: {num1} x {num2} = '
    
    return user_input, answ
```
#### Validate Question Function
This function is very simple, just checking if its true or false. I did include exception handling incase someone enters something i wouldn't even imagine. Also this code returns either a True or a False. The purpose of having it return like this was to make it easy to handle the tries variable. You get up to 3 tries to answer the question correctly, but I wanted that to be handled in the main function rather than adding an additional function or code to this function.
```python
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
```

#### Control Flow
1. Define number of questions in test, set variable for correct answers
2. Initialize ThreadPoolExecutor
3. Loop for each question
    * Access global variables, and set current tries
    * Initialize question
    * Start timer as thread
    * Ask question
    * Flip timer switch once user responds
    * Validate out of time
    * Validate if answer was correct
    * If incorrect restart from the Start timer as thread step
4. Print score

#### Main Function
Following with the control flow, this function was designed to be a top down look at whats going on.
```python
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
```
## Summary
This project taught me a lot of helpful concepts for python. It built on my problem solving skills as well as my intuition since when I couldn't solve the original problem I thought of what I needed to learn and then built on it with two projects. This project was difficult conceptually but quite easy to write for the basic lines. The main things stopping me from just completeing it in an afternoon was thanks to the timer. Now I know I could've saved myself a lot of time with the signal module, but my time wasn't wasted regardless.