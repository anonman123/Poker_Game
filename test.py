import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image



import random

path=['Images1','Images2','Images3','Images4']

Images=('mountain.jpg')
class Example(Frame):

    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open(Images)
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

    def change_image(self, file):
        """Change background image of the window."""
        size = (self.winfo_width(), self.winfo_height())
        self.image = Image.open(file).resize(size)
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

cards=['A','2','3','4','5','6','7','8','9','10','J','Q','K']

card_types=['♠', '♦', '♥', '♣']

card_faces={'J':'11','Q':'12','K':'13','A':'14','♠':'16','♦':'17','♥':'18','♣':'19'}

win_names={1:'Straight Flush',2:'4 of a kind',3:'full house',4:'Flush',5:'straight',6:'3 of a kind',7:'2 pair',8:'1 pair'}


players_winnings=[100,100,100,100]
players=[[],[],[],[]]
players_hand=[[],[],[],[]]
number_of_players=int(input('how many players are at the table?'))
pot=0
def hand_setup():
    """ setups the hand, everyone gets a rnadom assortment of 5 cards from the deck (no card types) """
    global players
    global players_hand
    for i in range(number_of_players):
        players[i].append((random.choice(cards))+' '+ random.choice(card_types) + ' ' + random.choice(cards)+' '+ random.choice(card_types) + ' ' + random.choice(cards)+' '+ random.choice(card_types) + ' ' +
        random.choice(cards)+' '+ random.choice(card_types) + ' ' + random.choice(cards) + ' ' + random.choice(card_types))
        players_hand[i]+=[y for x in players[i] for y in x.split(' ')]

def betting():
    """First round of betting, here you may also exchange your cards if you wish and go through a 2nd round of betting"""
    global pot
    global players_winnings
    pot_round_1=input(f'How much money would you like to bet\n Current Amount: {players_winnings[0]} ')
    for i in range(number_of_players):
        players_winnings[i]-=int(pot_round_1)
    pot+=(int(pot_round_1))*number_of_players
    trade_hands=input('if there are any cards you would like to exchange, type the index of the cards e.g. 01234 (otherwise, click enter): ')
    if trade_hands != '':
        for i in trade_hands:
            players_hand[0][(int(i)*2)]=random.choice(cards)
            players_hand[0][(int(i)*2+1)]=random.choice(card_types)
        print(f'New Hand\n{["".join(x) for x in zip(*[iter(players_hand[0])]*2)]}')
        print(f'Current Pot {pot}')
        pot_round_2=input(f'How much money would you like to bet\n Current Amount: {players_winnings[0]} ')
        pot+=(int(pot_round_2))*number_of_players
        for i in range(number_of_players):
            players_winnings[i]-=int(pot_round_2)


check_list=[[],[],[],[]]
def convert_hand():
    """To simplify the analysis of your hand, all face cards are converted to numbers using the above dict"""
    global check_list
    converted_list=[[],[],[],[]]
    adding_one_1=0
    for i in range(number_of_players):
        for x in players_hand[i]:
            if x == ' ':
                continue
            try:
                if x == 'A':
                    adding_one_1+=1
                    if adding_one_1<2:
                        converted_list[i].append(1)
                converted_list[i].append(int(card_faces[x]))
            except:
                converted_list[i].append(int(x))
        check_list[i].append(sorted(converted_list[i]))

doubles=[]
triples=[]
quads=[]
straight=[]
winning_hands=[]
highest_card=[]
card_type=[]
def analyze_hand():
    """The hand is then analyzed, and you look for doubles, triples, quads, etc. These are given a numberical value to determine who has the best hand"""
    global doubles
    global triples
    global quads
    global straight
    global winning_hands
    global highest_card
    global card_type
    current=[]
    for i in range(number_of_players):
        counter=0
        first_value=0
        current.clear()
        straight.clear()
        quads.clear()
        doubles.clear()
        triples.clear()
        flattened_check_list=[item for sublist in check_list[i] for item in sublist]
        highest_card.append(max(flattened_check_list[0:5]))
        for numbers in flattened_check_list:
            first_value+=1
            if first_value<2:
                current.append(numbers)
                straight.append(numbers)
                continue
            else:
                if numbers>15:
                    card_type.append(numbers)
                    continue
                if numbers == (current[0]+1):
                    straight.append(numbers)
                if numbers == current[0]:
                    counter+=1
                    if counter == 1:
                        doubles+=(current+[numbers])
                        current.clear()
                        current.append(numbers)
                        continue
                    if counter == 2:
                        triples+=(doubles[0:2]+[numbers])
                        current.clear()
                        doubles.clear()
                        current.append(numbers)
                        continue
                    if counter == 3:
                        quads+=(triples[0:3]+[numbers])
                        current.clear()
                        current.append(numbers)
                        continue
                else:
                    counter=0
                    current.clear()
                    current.append(numbers)
        print(f'player{i+1} has\n{["".join(x) for x in zip(*[iter(players_hand[i])]*2)]}')
        if len(straight) == 5 and card_type[0] == ((sum(card_type)/len(card_type))):
            winning_hands.append(1)
        elif len(quads) == 4:
            winning_hands.append(2)
        elif (len(doubles)+len(triples)) == 5:
            winning_hands.append(3)
        elif card_type[0] == ((sum(card_type)/len(card_type))):
            winning_hands.append(4)
        elif len(straight) == 5:
            winning_hands.append(5)
        elif len(triples) == 3:
            winning_hands.append(6)
        elif len(doubles) == 4:
            winning_hands.append(7)
        elif len(doubles) == 2:
            winning_hands.append(8)
        else:
            winning_hands.append(9)

def determine_winner():
    """The lowest the number, the better the win. If no one has a set, then the highest card wins. If a tie, then everyone in the tie wins, and the pot is split"""
    global pot
    global highest_card
    global winning_hands
    global player_number
    #print(f'\n\n{straight}\n\n')
    winner=min(winning_hands)
    winner_list=[]
    indexer=0
    if winner == 9:
        highest_card_win=max(highest_card)
        highest_card_win_player=highest_card.index(highest_card_win)
        print(f'\nplayer {highest_card_win_player+1} won with {highest_card_win}')
        players_winnings[highest_card_win_player]+=pot
    else:
        for i in winning_hands:
            if i == winner:
                winner_list.append(indexer)
            indexer+=1
        if len(winner_list)>1:
            print('tie')
            new_pot=0
            new_pot+=(pot/len(winner_list))
            pot=new_pot
            for player_number in winner_list:
                print(f'\nplayer{player_number+1} won with {win_names[winner]}')
                players_winnings[player_number]+=pot
        else:
            winning_player=winning_hands.index(winner)
            print(f'\nplayer{(winning_player)+1} won with {win_names[winner]}')
            players_winnings[winning_player]+=pot

def reset():
    """All variables are reset to start the next round"""
    global doubles
    global triples
    global quads
    global straight
    global winning_hands
    global highest_card
    global pot
    global check_list
    global players
    global players_hand
    global card_type
    pot=0
    card_type.clear()
    doubles.clear()
    triples.clear()
    quads.clear()
    straight.clear()
    winning_hands.clear()
    highest_card.clear()
    check_list=[[],[],[],[]]
    players=[[],[],[],[]]
    players_hand=[[],[],[],[]]

def main(e,image_folder):
    global Images
    global players_winnings
    count=0
    """Main loop, you go until you or the other players run out of money"""
    while players_winnings[0]>1 and players_winnings[0]<400:
        if players_winnings[0]<=100 and count==0:
            count+=1
            e.destroy()
            Images=image_folder+'/'+'image1.jpg'
            e = Example(root)
            e.pack(fill=BOTH, expand=YES)
            root.update_idletasks()
        hand_setup()
        print(f'Your hand\n{["".join(x) for x in zip(*[iter(players_hand[0])]*2)]}')
        betting()
        print(f'Current Pot {pot}')
        convert_hand()
        analyze_hand()
        determine_winner()
        reset()
        if players_winnings[0]>100 and count==1:
            count+=1
            e.destroy()
            Images=image_folder+'/'+'image2.jpg'
            e = Example(root)
            e.pack(fill=BOTH, expand=YES)
            root.update_idletasks()
        if players_winnings[0]>200 and count==2:
            count+=1
            e.destroy()
            Images=image_folder+'/'+'image3.jpg'
            e = Example(root)
            e.pack(fill=BOTH, expand=YES)
            root.update_idletasks()
        if players_winnings[0]>300 and count==3:
            count+=1
            e.destroy()
            Images=image_folder+'/'+'image4.jpg'
            e = Example(root)
            e.pack(fill=BOTH, expand=YES)
            root.update_idletasks()
        print('\nNext round\n')
    if players_winnings[0]<1:
        print('You have run out of money, you lose')
    else:
        print('Other players have run out of money, you win!')
        e.destroy()
        Images=image_folder+'/'+'image5.jpg'
        e = Example(root)
        e.pack(fill=BOTH, expand=YES)
        root.update_idletasks()

def main_loop2(e):
    global players_winnings
    while True:
        quest=input('would you like to play again? (y/n)')
        if quest == 'n':
            break
        image_folder=random.choice(path)
        players_winnings=[100,100,100,100]
        main(e,image_folder)

root = tk.Tk()
root.geometry('600x800')
e=Example(root)
root.update_idletasks()
main_loop2(e)
root.mainloop()
