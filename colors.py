from termcolor import colored
from consts import GREEN, YELLOW

mapping = { GREEN: 'green', YELLOW: 'yellow' }
def color(word, state):
    output = ""
    for (i, l) in enumerate(word):
        constraint = filter(lambda (p, le, c): p == i and le == l, state)
        if constraint:
            output += colored(l, mapping[constraint[0][2]])
        else:
            output += colored(l, 'white')
    return output

def magenta(word):
    return colored(word, 'magenta')
