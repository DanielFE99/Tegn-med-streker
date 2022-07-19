'''
Progtammet bruker en dictionary i en variabel kalt "lerret" for å lagre
linjene til tegningen. keys for dictionaryen er en (x og y) tuppel.
x og y verdiene representerer linjeformene som tegnes på skjermen.

'''
import shutil, sys

#Konstanter
OPP_NED_TEGN =  chr(9474) #'│'
VENSTRE_HØYRE_TEGN = chr(9472) #'─'
NED_HØYRE_TEGN = chr(9484) # '┌'
NED_VENSTRE_TEGN = chr(9488) #is '┐'
OPP_HØYRE_TEGN = chr(9492) #'└'
OPP_VENSTRE_TEGN = chr(9496) # is '┘'
OPP_NED_HØYRE_TEGN =  chr(9500) # is '├'
OPP_NED_VENSTRE_TEGN = chr(9508) #is '┤'
NED_VENSTRE_HØYRE_TEGN = chr(9516) # '┬'
OPP_VENSTRE_HØYRE_TEGN = chr(9524) #is '┴'
KRYSS_TEGN = chr(9532) # is '┼'

#henter størrelse på terminalen
LERRET_BREDDE, LERRET_HØYDE = shutil.get_terminal_size()
LERRET_BREDDE -= 1
#Leave room at the bottom few rows for the kommando info lines.
LERRET_HØYDE -= 5

""" KEYS for lerret er (x, y) som er en int tuppel for koordinatene,
og VALUE er et sett med bokstaver W, A, S, D som sier hvilke linje som skal
tegnes på lerrete."""
lerret = {}
markørX = 0
markørY = 0

def getCanvasString(lerretInfo, cx, cy):
    """Returnereren en multilinje streng av linjene tegnet in lerretInfo."""
    lerretStr = ''
    """lerretInfo er en dictionary med (x, y) tuppler, keys og values som er
    ett sett av 'W', 'A', 'S', eller 'D' stremger for å vise hvilken
    retning linjene er tegner for hver "x, y" koordinat."""
    #Hvis kollone og rad er like cx og cy er vi der markøren skal være
    for radNum in range(LERRET_HØYDE):
        for kolonneNum in range(LERRET_BREDDE):
            if kolonneNum == cx and radNum == cy:
                lerretStr += '*'
                continue

            '''
            Hvis ikke kolonne og rad er lik cx og cy er vi ikke ved markøren
            Og her skal linjene tegnes
            '''
            punkt = lerretInfo.get((kolonneNum, radNum))
            if punkt in (set(['W', 'S']), set(['W']), set(['S'])):
                lerretStr += OPP_NED_TEGN
            elif punkt in (set(['A', 'D']), set(['A']), set(['D'])):
                lerretStr += VENSTRE_HØYRE_TEGN
            elif punkt == set(['S', 'D']):
                lerretStr += NED_HØYRE_TEGN
            elif punkt == set(['A', 'S']):
                lerretStr += NED_VENSTRE_TEGN
            elif punkt == set(['W', 'D']):
                lerretStr += OPP_HØYRE_TEGN
            elif punkt == set(['W', 'A']):
                lerretStr += OPP_VENSTRE_TEGN
            elif punkt == set(['W', 'S', 'D']):
                lerretStr += OPP_NED_HØYRE_TEGN
            elif punkt == set(['W', 'S', 'A']):
                lerretStr += OPP_NED_VENSTRE_TEGN
            elif punkt == set(['A', 'S', 'D']):
                lerretStr += NED_VENSTRE_HØYRE_TEGN
            elif punkt == set(['W', 'A', 'D']):
                lerretStr += OPP_VENSTRE_HØYRE_TEGN
            elif punkt == set(['W', 'A', 'S', 'D']):
                lerretStr += KRYSS_TEGN
            elif punkt == None:
                lerretStr += ' '
        lerretStr += '\n'
    return lerretStr

moves = []
while True:
    #Tegn linjene basert på infoen fra lerret
    print(getCanvasString(lerret, markørX, markørY))

    print('Bruk WASD tastene for å bevege deg, H for hjelp, R for å rydde skjermen, '
    + 'F for å lagre, eller QUIT.')
    respons = input('> ').upper()

    if respons == 'QUIT':
        print('Thanks for playing!')
        sys.exit() #avslutter programmet

    elif respons == 'H':
        print('Enter W, A, S, and D characters to move the markør and')
        print('draw a line behind it as it moves. For example, ddd')
        print('draws a line going right and sssdddwwwaaa draws a box.')
        print('draws a line going right and sssdddwwwaaa draws a box.')
        print('You can save your drawing to a text fil by entering F.')
        input('Press Enter to return to the program...')
        continue
    elif respons == 'R':
        lerret = {}
        moves.append('R') #legger dette til i listen
    elif respons == 'F':
        #lagrer lerrete som en fil
        try:
            print('Skriv inn  navnet du vil lagre filn som:')
            filnavn = input('> ')

            if not filnavn.endswith('.txt'):
                filnavn += '.txt'
            with open(filnavn, 'w', encoding ='utf-8') as fil:
                fil.write(''.join(moves) + '\n')
                fil.write(getCanvasString(lerret, None, None))
        except:
            print('ERROR: kunne ikke lagre filen.')

    for kommando in respons:
        if kommando not in ('W', 'A', 'S', 'D'):
            continue
        moves.append(kommando)

        if lerret == {}:
            if kommando in ('W', 'S'):
                #Make the first line horizontal one:
                lerret[(markørX, markørY)] = set(['W', 'S'])
            elif kommando in ('A', 'D'):
                #Make the first line a vertical one:
                lerret[(markørX, markørY)] = set(['A', 'D'])

        #Oppdater x og y slik at markøren er på riktig plass
        if kommando == 'W' and markørY > 0:
            lerret[(markørX, markørY)].add(kommando)
            markørY -= 1
        elif kommando == 'S' and markørY < LERRET_HØYDE - 1:
            lerret[(markørX, markørY)].add(kommando)
            markørY += 1
        elif kommando == 'A' and markørX > 0:
            lerret[(markørX, markørY)].add(kommando)
            markørX -= 1
        elif kommando == 'D' and markørX < LERRET_BREDDE - 1:
            lerret[(markørX, markørY)].add(kommando)
            markørX += 1
        else:
            continue

        #Hvis det ikke er noe set for (markørX, markørY), legg til et tomt sett:
        if (markørX, markørY) not in lerret:
            lerret[(markørX, markørY)] = set()

        #legg til strengen som viser retning til dette settet
        #dette gjør at linjene ser sammenhengende ut når man beveger seg i en ny retning
        #uten dette ser det ut som linjene "hopper"
        if kommando == 'W':
            lerret[(markørX, markørY)].add('S')
        elif kommando == 'S':
            lerret[(markørX, markørY)].add('W')
        elif kommando == 'A':
            lerret[(markørX, markørY)].add('D')
        elif kommando == 'D':
            lerret[(markørX, markørY)].add('A')













































