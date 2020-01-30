
import messages
import messages.Colors as Colors

def UnknownSymbol(symbol: str, position=None):
    string = ''
    if messages.filename:
        string += f'{messages.filename}:'
    if position:
        string += f'{position.get("line")}:{position.get("column")} '

    string += f'{Colors.FAIL}UNKNOWN_SYMBOL{Colors.ENDC} - Símbolo não reconhecido pela linguagem - \'{symbol}\''

    print(string)
