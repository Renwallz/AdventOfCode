START = 'cqjxjnds'
ALPHABET = 'abcdefghjkmnpqrstuvwxyz'

def increment(string):
    r = []
    for i,c in enumerate(string[::-1]):
        if c != ALPHABET[-1]:
            r.append(ALPHABET[ALPHABET.index(c)+1])
            r.append(string[:len(string)-i-1])
            break
        else:
            r.append(ALPHABET[0])
    return ''.join(r[::-1])
    

def rule1(string):
    """
    Passwords must include one increasing straight of at least 
    three letters, like abc, bcd, cde, and so on, up to xyz. 
    They cannot skip letters; abd doesn't count.
    
    Returns True if string complies, False otherwise
    """
    triplets = (''.join((a,b,c)) for a,b,c in zip(string, string[1:], string[2:]))
    for trip in triplets:
        if trip in ALPHABET:
            return True
    return False
    
#rule2 is handled by ALPHABET, assuming no banned 
#letters are in the starting string


def rule3(string):
    """
    Passwords must contain at least two different, non-overlapping 
    pairs of letters, like aa, bb, or zz.
    
    Returns True if string complies, False otherwise
    """
    
    pairs = [a for a,b in zip(string, string[1:]) if a == b]
    return len(pairs) >= 2 and pairs[0] != pairs[1]
    
password = START
while(not rule3(password) or not rule1(password)):
    password = increment(password)

print(password)