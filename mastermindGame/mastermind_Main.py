def introduction_text(): #function for printing the whole starting text
    print('\nWelcome to the digital version of the board game Master Mind.')
    print('In this game, you will have to guess the right colours in the correct positions.\n')
    print('The Instructions:')
    print('1. The game will generate four random colours from a list of possible colors.\nYou have to guess all four of them in the correct sequences/positions to complete\nthe game.')
    print('2. The game can generate the same colours in different positions.\nFor example, "violet", "blue", "violet", "red".')
    print('3. All commands/inputs into this game are case-insensitive.')
    print('4. You may enter your guessed colours(inputs) partially or fully.\nYou must start with the first letter.\nExample, "R", "ReD", "rE" are valid inputs, while "rad" and "redd" are invalid inputs.')
    print('5. You may exit the game at anytime by entering "exit".')
    print('6. If you wish to display the answers while playing, you may\nenter "Answer" before starting the game.\n')
    print('The possible colours are:')
    print('RED ', 'ORANGE ', 'YELLOW ', 'GREEN ', 'BLUE ', 'INDIGO ', 'VIOLET\n')

def debug_answer(answer, assign): #function to display your guesses and the answers in terms of number, mostly use for debugging
    print('\n-----------------------------------------------------------------------------------------------')
    print('\nYour Guesses and Answers:')
    print('List : RED-0 ', 'ORANGE-1 ', 'YELLOW-2 ', 'GREEN-3 ', 'BLUE-4 ', 'INDIGO-5 ', 'VIOLET-6') #each color correspond to a value
    print('\nInput 1:', assign[0])
    print('Input 2:', assign[1])
    print('Input 3:', assign[2])
    print('Input 4:', assign[3], '\n')
    print('Answer 1:', answer[0])
    print('Answer 2:', answer[1])
    print('Answer 3:', answer[2])
    print('Answer 4:', answer[3])
    print('\n-----------------------------------------------------------------------------------------------')

def assign_value(): #function to take user inputs and convert them into numbers based on the sequence of the colors, example, "yel" to "2"
    colors = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'INDIGO', 'VIOLET', '0'] #each color correspond to a value from 0 to 6
    number = ['First', 'Second', 'Third', 'Fourth']
    assigned = [0, 0, 0, 0] #initialize assigned list
    count = 0
    while count < 4: #this while loop takes user inputs, find the value correspond to the color selected by user, assign that value to the assigned list
        print("\nInput your", number[count], "Color Guess:") 
        in_put = input("").upper() + '9' #user selects a color by inputing a color string
        if in_put == 'EXIT9': #decides if the user has entered "Exit" from in_put, exit the function with string 'EXIT'
            return 'EXIT'
        count2 = 0
        repeat = 0

        while in_put[0] != colors[count2][0]: #this nested while loop compares the first letter of user input with first letter of each color
            if count2 == 7: #decides if all the comparison for the first letter is done but none of them are equal, show error and exit the current loop
                print('\nInvalid Color/Input : Please enter one of the colours from the given possible list of colours.')
                print('                      You can enter partially or fully. You must start with the first letter.')
                print('                      Example, "R", "ReD", "rE" are valid inputs, while "rad" and "redd" are invalid inputs.')
                count = count - 1 #allow repeating of the whole while loop with the same counter
                repeat = 1
                break
            count2 = count2 + 1
       #when the first nested while loop is done, the final value of count2 correspond to the selected color by user
       #if there was an input error, skip the following nested loop

        count3 = 0
        while count3 < len(in_put) - 1 and count2 != 7: #this nested while loop checks user input error by comparing the user input with the selected color
            if in_put[count3] != colors[count2][count3] or len(in_put) - 1 > len(colors[count2]): #decides if all the letters has been compared but one of them is not equal, show error and exit the current loop
                print('\nInvalid Color/Input : Please enter one of the colours from the given possible list of colours.')
                print('                      You may enter partially or fully starting with the first letter. Example, "R", "ReD", "rE" are valid inputs, while "rad" and "redd" are invalid inputs.')
                count = count - 1 #allow repeating of the whole while loop with the same counter
                repeat = 1
                break
            count3 = count3 + 1

        if repeat == 0: #decides if user has not made an input error, assign the value of the selected color to the assigned list
            assigned[count] = count2
        count = count + 1
    return assigned


def correct_position(answer, assign, attempts): 
    correct = 0
    for count in range(0,4): #count number of correct colours in the correct place
        if assign[count] == answer[count]:
            correct = correct + 1
    if correct == 4: 
        print('\nCongrats! You guessed all colours with correct positions correctly.')
        print('Your total number of attempts is ', attempts)
    return correct

def wrong_position(answer, assign):
    wrong = 0
    for count in range(0,4): #count the number of correct colours in right or wrong place
        for count2 in range(0,4):
            if answer[count] == assign[count2]:
                assign[count2] = ' ' #assign any value other than 0 to 6 so that it doesn't check the same answer again
                wrong = wrong + 1
                break
    return wrong

#----------------------------------------------------------------PROGRAM STARTS HERE---------------------------------------------------------------------------

import random

introduction_text() #starts program by displaying the instruction texts
display_answer = 0

while True: #infinity loop until users choose to input "Yes" to start the game or "Exit" the program
    play = input('Start the game? (Yes/Exit/Answer)\n').upper()
    correct = 0

    if play == 'ANSWER': 
        display_answer = 1
        print('\nAnswers Display is enabled. Restart the program to reset it back to disabled.')
        continue
    elif play != 'EXIT' and play != 'YES':
        print('\nInvalid Input : Please enter one of the given options in the parenthesis.')
        continue
    elif play == 'EXIT':
        break

    while True: #infinity loop until users choose to input "Yes" to play again or "Exit" the program
        answer = [0, 0 , 0, 0] #initialize a list
        answer[0] = 4 #random.randint(0,6) #assign random value from 0 to 6 
        answer[1] = 0 #random.randint(0,6) #note that each value correspond to a color
        answer[2] = 4 #random.randint(0,6) # RED-0, ORANGE-1, YELLOW-2, GREEN-3, BLUE-4, INDIGO-5, VIOLET-6
        answer[3] = 6 #random.randint(0,6)
        attempts= 0 #starts from 0 attempts

        while play == 'YES': #if the users input "YES" after completion, the game is restarted
            print('\n-----------------------------------------------------------------------------------')
            print('\nThe possible colours are:')
            print('RED ', 'ORANGE ', 'YELLOW ', 'GREEN ', 'BLUE ', 'INDIGO ', 'VIOLET')
            assign = assign_value() #takes user inputs and return a list of selected colors (in values)
            if assign == 'EXIT': #decides if user has entered 'Exit' from assign_value function, exit the current loop
                print('\nExiting the game....')
                break
            if display_answer == 1: #decides if user had entered "answer", display the answers with debug_answer function
                debug_answer(answer, assign)
            attempts = attempts + 1 #count number of attempts
            correct = correct_position(answer, assign, attempts) #count the correct number of colours in the correct places
            wrong = wrong_position(answer, assign) - correct #minus right places to calculate the number of correct colour but in the wrong place
            if correct != 4:
                print("\nNumber of correct colour in the correct place: ", correct)
                print("Number of correct colour but in the wrong place: ", wrong)
            else: 
                break

        play = input('\nDo you want to start over? (Yes/Exit)\n').upper()

        if play != 'EXIT' and play != 'YES':
            print('\nInvalid Input : Please enter one of the given options in the parenthesis.')
        elif play == 'EXIT':
            break
    break
