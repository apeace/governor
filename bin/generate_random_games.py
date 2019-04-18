import sys
import os
import errno
import json
import time
import datetime
import random

import kingsburg
import engine
import logger
import game

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def ident():
    d = datetime.datetime.now()
    unix = time.mktime(d.timetuple())
    rand = random.randint(10000, 99990)
    return str(unix) + "-" + str(rand)

# TODO should start games at a random state rather than beginning
# TODO in addition to this, test the effect of having more than one output
# TODO maybe look at under/over fitting as well
# TODO does randomplayer ever need to pass unnecessarily? it may on buildings, not on influence

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:")
        print("python -m bin.generate_random_games <num> <batchsize> <dir>")
        sys.exit(1)

    num = int(sys.argv[1])
    batchsize = int(sys.argv[2])
    dir = sys.argv[3]

    mkdir_p(dir)

    output = ""
    for i in range(1, num+1):
        l = logger.SilentLogger()
        eng = engine.TrainingDataEngine(l)
        state = kingsburg.State()
        g = game.Game(eng, kingsburg.State())
        g.play()
        game_json = json.dumps({
            "states": [state.toDict() for state in eng.states],
            "advisor_choices": [[choice[0].toDict(), choice[1]] for choice in eng.advisor_choices],
            "won": eng.won(g.state)
        })
        output += game_json + "\n"
        if i % batchsize == 0:
            filename = dir + "/" + ident()
            f = open(filename, "w")
            f.write(output)
            f.close()
            output = ""
        print(i)
