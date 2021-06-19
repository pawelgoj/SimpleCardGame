# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 10:19:17 2021

@author: pagoj

Prosta gra karciana typu poker, założenia:
    1. Urzytkownik gra przeciw komputerowni 
    2. Wyniki z porzednich rozgrywek są zapisywane 
    3. Gracz może w karzdej chwili podglądnąć zasady

Zasady gry w piku: game_rules.txt
            
"""

from enum import IntEnum 
import random 
import datetime

'''User interface key words:
    r - Show_game_rules
    1 - Draw_card_1
    2 - Draw_card_2
    3 - Draw_card_3
    4 - Draw_card_4
    c - Continue
    s - Save_game_resoult
    sc - Show_earlier_results
    cr - Clear_result_table
    e - Exit
    '''
    
game_options_dictionary = {'r':1, '1':2, '2':3, '3':4, '4':5, 'c':6, 's':7, 'sc':8, 'cr':9, 'e':10}

Options = IntEnum('Options', 'Show_game_rules Draw_card Draw_2_cards Draw_3_cards\
                  Draw_cards Continue Save_game_resoult Show_earlier_results Clear_result_table Exit')
                  
Results = {'win':1,'draw':2, 'lose':3}

User_decizions = {'c':1, 'r':2, 'e':3}

'''Pokaż zasady gry'''
def show_game_rules():
    with open("game_rules.txt", 'r', encoding='UTF-8') as file:
        print(file.read(), '\n') 
    return 

'''Zapisz wczesniejsze wyniki'''
def save_game_result(score):
    with open("game_resoults.txt", 'a+', encoding='UTF-8') as file:
        if score > 2:
            won_not_won = 'wygrał.'
        else:
            won_not_won = 'nie wygrał.'
            
        date = datetime.datetime.now()
        string = str(date) + ' gracz zgadnął ' + str(score) + ' na 5 wyników i ' + str(won_not_won) + ' \n'
        file.write(string) 
        print(' \n wynik zapisany \n')
    return

'''Pokaż wczesniejsze wyniki'''
def show_game_results():
    try:
        with open("game_resoults.txt", 'r', encoding='UTF-8') as file:
            results = file.read()
            if results == '': 
                print('Brak wcześniejszych wyników')
            else: 
                print(results)
    except:
        print(' \n Nie ma zapisanych wyników. \n')
    return

'''Wyczyść wcześniejsze wyniki'''
def clear_game_results(): 
    with open("game_resoults.txt", 'w', encoding='UTF-8') as file:  
        file.write('')
    print('Wyniki wyczyszczone! \n')
    return 

'''Tasowanie i rozdanie kart'''
def shuffling_and_dealing(dealing, list_of_cards): 
    random.shuffle(list_of_cards)
    list_of_cards, user_cards = dealing(list_of_cards, 4)
    list_of_cards, computer_cards = dealing(list_of_cards, 4)
    return user_cards, computer_cards

'''Wymień karty graczowi'''
def card_exchange(dealing, list_of_cards, user_cards, card_numbers):
    for card in card_numbers:
        list_of_cards, clist  = dealing(list_of_cards, 1)
        user_cards[int(card) -1] = clist[0]
    return user_cards

'''Rozdaj karty'''
def dealing(list_of_cards, Number_of_cards):
    new_list_of_cards = []
    for card in range(Number_of_cards):
         new_list_of_cards.append(list_of_cards.pop())
    return list_of_cards, new_list_of_cards


'''Licz ilosć punktów'''
def count_points(cards):
    
    combination_of_cards = {'Król': 0, 'Żmija': 0, 'Kret': 0, 'Mysz': 0}
    
    combination_of_cards['Król'] = cards.count('Król')
    combination_of_cards['Żmija'] = cards.count('Żmija')
    combination_of_cards['Kret'] = cards.count('Kret')
    combination_of_cards['Mysz'] = cards.count('Mysz')
    
    points = 0 
    
    for value in combination_of_cards.values():
        if value == 4: 
            points = 4 
            break 
        
        elif value == 3: 
            points = 3
            break
        
        elif value == 2: 
            points += 1
    
    return points

'''Sprawwdź kto wygrał'''
def check_it_out(count_points, user_cards, computer_cards):
    user_points = count_points(user_cards)
    computer_points = count_points(computer_cards)
    
    if user_points > computer_points:
        result = 'win'
    elif user_points < computer_points:
        result = 'lose'     
    elif user_points == computer_points:
        result = 'draw'
            
    return result



list_of_cards = ['Król', 'Król', 'Król', 'Król', 'Żmija', 'Żmija', 'Żmija', 'Żmija', 'Kret', 'Kret', 'Kret', 'Kret', 'Mysz', 'Mysz', 'Mysz', 'Mysz']

while True:
    user_input = input('''
                       ----MENU---------
                       Co chcesz zrobić? 
                       c - zagraj 
                       r - pokaz zasady gry 
                       sc - pokaż wczeniejsze wyniki 
                       cr - wyczyść tabelę z wynikami 
                       e - wyjdź z gry 
''')

    try:                       
        Option = game_options_dictionary[user_input]     
               
        if Option == Options.Continue:
            game_round = int(1)
            
            points = 0
            
            while game_round < 6:
                print('\n Runda nr', game_round, '\n')
                
                Option = game_options_dictionary[input('''
                           Co chcesz zrobić? 
                           c - tasuj i rozdaj karty  
                           r - pokaz zasady gry  
                           e - cofnij się do MENU \n''')]
                           
                if Option == Options.Continue:
                    deck_in_the_hand = list_of_cards.copy()
                    user_cards, computer_cards = shuffling_and_dealing(dealing, deck_in_the_hand)
                    game_round += 1
                    print(' \n Karty na twojej rence: \n', '\n', 'Nr karty:   1    2    3    4 \n',\
                          '           ', user_cards[0], user_cards[1], user_cards[2], user_cards[3], '\n')
                    Option = game_options_dictionary[input('''
                           Czy chcesz wymienić karty? 
                           c - Tak   
                           e - Nie \n''')]
                    if Option == Options.Continue:
                        card_numbers = input('\n Które karty chcesz wymienić, wpisz ich numery? \n \n' + 'Nr karty:   1    2    3    4 \n'\
                              '           ' + user_cards[0] +' '+ user_cards[1] +' ' +  user_cards[2] +' ' + user_cards[3] + '\n').split()
                        user_cards = card_exchange(dealing, deck_in_the_hand, user_cards, card_numbers)
                    elif Option == Options.Exit:
                        pass 
                    
                elif Option == Options.Show_game_rules:
                    show_game_rules()
                    continue
                elif Option == Options.Exit:
                    break  
                 
                print('\n Karty na twojej rence: \n', '\n', 'Nr karty:   1    2    3    4 \n',\
                          '           ', user_cards[0], str(user_cards[1]), str(user_cards[2]), str(user_cards[3]), '\n')
                Option = User_decizions[input('''
                           Zgadnij kto ma więcej punktów z kart Ty czy komputer? 
                           c - Ja 
                           r - remis
                           e - komputer \n''')]
                result = check_it_out(count_points, user_cards, computer_cards)
                           
                if Option == Results[result]:
                    print(' \n Wygrywasz rundę !!! \n')
                    points +=1
                else:
                    print('\n', 'Nie zgadłeś :( \n')
                print('Twoje karty:', str(user_cards[0]), str(user_cards[1]), str(user_cards[2]), str(user_cards[3]),\
                      '\nKarty komputera: ', str(computer_cards[0]), str(computer_cards[1]), str(computer_cards[2]), str(computer_cards[3]), '\n')
                           
            print('\n', 'Twoeje punkty: ', points, '\n')
            if points >= 3: 
                print('\n Wygrywasz rozgrywkę!!!! \n    Gratulacje!!!! \n')
            else: 
                print('\n Niestety się nie udało :( \n')
                
            if game_round > 5: 
                Option = game_options_dictionary[input('''
                                Czy chcesz zapisać wynik do tabeli wyników? 
                                c - Tak  
                                e - cofnij się do MENU \n''')]
                                
                if Option == Options.Continue:
                    save_game_result(points)
                    print('\n Wynik zapisany. \n')
                elif  Option == Options.Exit:
                    pass
                else:
                    raise
                
        elif Option == Options.Show_game_rules:
            show_game_rules()
        elif Option == Options.Show_earlier_results:
            show_game_results()
        elif Option == Options.Clear_result_table:
            clear_game_results()
        elif Option == Options.Exit:
            print('\n Do widzenia! \n')
            break
    except:
        print(' \n Nie ma takiej opcji!!! \n')
    