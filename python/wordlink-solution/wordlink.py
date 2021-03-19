import sys
import enchant
import itertools
import traceback

'''
Ohidur Rahman Bappy
https://ohidur.com
https://github.com/ohidurbappy

Usage:
    python wordlink.py <letters>
Example:
    python wordlink.py potato
'''

def main():
    try:
        d = enchant.Dict("en_US")

        if len(sys.argv) < 2:
            letters=input("Input a word:")
        else:
            letters = sys.argv[1]
        
        letters_size = len(letters)

        for size in range(2, letters_size + 1):
            print("Length", size)
            permutations = [''.join(p) for p in list(
                itertools.permutations(letters, size))]
            matches = [word for word in permutations if d.check(word) == True]
            print("\t", dedupe(matches))

        main()
    except KeyboardInterrupt:
            print("KEYBOARD INTERRUPT DETECTED. CLOSING PROGRAM")
            sys.exit(1)
    except Exception:
            traceback.print_exc()
            pass

def dedupe(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


if __name__ == '__main__':
    print("Wordlink Solution")
    print("Press CTRL+C to quit.")
    main()