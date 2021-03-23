import shelve

fs = shelve.open('filesystem.fs', writeback=True)
current_dir = []

def install(fs):
    # create root and others
    username = input('What do you want your username to be? ')

    fs[""] = {"System": {}, "Users": {username: {}}}

def current_dictionary():
    """Return a dictionary representing the files in the current directory"""
    d = fs[""]
    for key in current_dir:
        d = d[key]
    return d

def ls(args):
    print ('Contents of directory', "/" + "/".join(current_dir) + ':')
    for i in current_dictionary():
        print (i)

def cd(args):
    if len(args) != 1:
        print ("Usage: cd <directory>")
        return

    if args[0] == "..":
        if len(current_dir) == 0:
            print ("Cannot go above root")
        else:
            current_dir.pop()
    elif args[0] not in current_dictionary():
        print ("Directory " + args[0] + " not found")
    else:
        current_dir.append(args[0])


def mkdir(args):
    if len(args) != 1:
        print ("Usage: mkdir <directory>")
        return
    # create an empty directory there and sync back to shelve dictionary!
    d = current_dictionary()[args[0]] = {}
    fs.sync()

COMMANDS = {'ls' : ls, 'cd': cd, 'mkdir': mkdir}

install(fs)

while True:
    raw = input('> ')
    cmd = raw.split()[0]
    if cmd in COMMANDS:
        COMMANDS[cmd](raw.split()[1:])

#Use break instead of exit, so you will get to this point.
input('Press the Enter key to shutdown...')