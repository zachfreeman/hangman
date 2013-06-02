import random

class HangGame(object):
    def __init__(self, address):
        self.address = address
        self.answer = self.return_word().upper()
        self.answer = self.answer.strip()
        self.allGuesses = []
        self.wrongGuesses = []
        self.rightGuesses = []
        baseStrngList = []
        self.baseBlanks = self.create_base()
        self.picDict = self.build_picDict()
        self.title = "H A N G M A N"
        self.end_game = [False, None]
        self.answerCount = len(set(self.answer))
        self.picPieces = [(2,5,'O'), (3,5,'|'), (3,4,'/'), (3,6,'\\'), (4,5,'|'), (5,4,'/'), (5,6,'\\'),
                          (5,3,'_'), (5,7,"_")]
        """
             O    2,5
            /|\   3,4 3,5 3,6
             |    4,5
           _/ \_  5,3 5,4 5,6 5,7
        """

    def create_base(self):
        """ Creates the underline-based blank template for guesses
        """
        baseStrngList = []
        for i in range(len(self.answer)):
            baseStrngList.append('_')
            baseStrngList.append(' ')
        return baseStrngList[:-1]

    def update_base(self,guess):
        """ Takes a guess already determined to be in the answer
            Updates the base string appropriately
        """
        for i in range(len(self.answer)):
            if self.answer[i] == guess:
                self.baseBlanks[i*2] = guess
        return self.baseBlanks

    def build_picDict(self):
        picDict = {}
        baseRow, picDict[6], = [],[]

        for i in range(15):
            baseRow.append(' ')
        picDictBase, picDict[0], picDict[1] = list(baseRow), list(baseRow), list(baseRow)
        picDictBase[11] = '|'

        picDict[0][5], picDict[0][11] = '+', '+'
        picDict[0][6], picDict[0][7], picDict[0][8], picDict[0][9], picDict[0][10] = '-', '-', '-', '-', '-'
        picDict[1][5], picDict[1][11], = '|','|'
        for i in range(2,6):
            picDict[i] = list(picDictBase)
        for i in range(15):
            picDict[6].append('=')

        return picDict

    def update_pic(self):
        row = self.picPieces[len(self.wrongGuesses)][0]
        col = self.picPieces[len(self.wrongGuesses)][1]
        glyph = self.picPieces[len(self.wrongGuesses)][2]
        self.picDict[row][col] = glyph

    def print_pic(self):
        """ Prints the hangman picture in its current state
        """
        for i in range(7):
            print reduce(self.smush,self.picDict[i])

    def guess_letter(self,letter):
        """ Used to determine whether or not a guessed letter is in the answer and
            Take appropriate action
        :param letter:
        """
        if str(letter).upper() not in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ') or len(str(letter)) != 1:
            print '"%s" is not a valid guess - guess must be a single alpha character - guess again' % (letter)
            return False
        else:
            letter = letter.upper()

        if letter in self.allGuesses:
            print 'You have already guessed letter "%s" - guess again' % (letter)
            return False
        else:
            self.allGuesses.append(letter)
            if letter in self.answer:
                # do some stuff related to updating self.baseBlanks, self.rightGuesses
                print 'You got letter %s right!' % (letter)
                self.rightGuesses.append(letter)
                self.update_base(letter)
                # check if game is over
                if len(self.rightGuesses) == self.answerCount:
                    self.end_game[0], self.end_game[1] = True, 'won'
                return True
            else:
                # do some stuff related to updating self.wrongGuesses and sorting
                self.update_pic()
                self.wrongGuesses.append(letter)
                self.wrongGuesses.sort()
                print 'You got letter %s wrong!' % (letter)
                # check if game is over
                if len(self.wrongGuesses) == len(self.picPieces):
                    self.end_game[0], self.end_game[1] = True, 'lost'
                return True

    def return_missed(self):
        baseStrng = ''
        for letter in self.wrongGuesses:
            baseStrng = baseStrng + letter + " "
        return baseStrng[:-1]

    def return_base(self):
        return reduce(self.smush, self.baseBlanks)

    def play(self):
        print self.title
        print
        roundCounter = 0
        while True:
            roundCounter += 1
            print '----Round %s----' % (roundCounter)
            self.print_pic()
            print 'Missed letters:',self.return_missed()
            print self.return_base()
            if self.end_game[0]:
                print "You %s!" % (self.end_game[1])
                if self.end_game[1] == 'lost':
                    print 'The correct answer is %s' % (self.answer)
                break
            while True:
                print 'Guess a letter.'
                guess = raw_input('Guess: ')
                if self.guess_letter(guess):
                    break
            print

    def return_word(self, max_word = 113809):
        """
        Takes a source composed of words delimited by line breaks, and a max value, and
        returns a random word located in the file before the max value
        :param address: a source file containing words, by default a text file
        :param max_word: the maximum line number to use in search for words
        :return:
        """
        with open(self.address) as f:
            counter = 0
            word_num = random.randint(1,max_word)
            for line in f:
                counter += 1
                if counter == word_num:
                    break
            return line

    def smush(self,x,y):
        return x + y

start = 'Y'
answer = ''
gameCounter = 0
# UPDATE THE 'address' variable to a file of your choosing
address = "C:\Users\Owner\Dropbox\PyProgs\Games\hangman\words.txt"
while answer.upper() == 'Y' or start == 'Y':
    start, answer = '', ''
    gameCounter += 1
    print
    print 'GAME NUMBER ' + str(gameCounter) + ' OF... '
    curHang = HangGame(address)
    result = curHang.play()
    while answer.upper() not in ('Y','N'):
        answer = raw_input('Play again (y/n): ')