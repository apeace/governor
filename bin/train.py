import sys
import os
import json

import keras
import numpy

import kingsburg
import training

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:")
        print("python -m bin.train <num> <out> <dir>")
        sys.exit(1)

    num = int(sys.argv[1])
    out = sys.argv[2]
    dir = sys.argv[3]

    files = os.listdir(dir)
    files = [dir + "/" + f for f in files if os.path.isfile(dir + "/" + f)]

    states = []
    wins = []

    stop = False
    count = 0
    for file in files:
        if stop:
            break
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if count == num:
                    stop = True
                    break
                d = json.loads(line)
                for state in d["states"]:
                    s = kingsburg.State().fromDict(state)
                    input = training.state_to_input(s)
                    assert len(input) == 167
                    states.append(input)
                    wins.append(d["won"])
                count += 1

    model = keras.models.Sequential()
    model.add(keras.layers.Dense(200, input_dim=167, activation="relu"))
    model.add(keras.layers.Dense(1, activation="linear", kernel_initializer="glorot_uniform"))
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
    model.fit(numpy.asarray(states), numpy.asarray(wins), verbose=False)
    model.save(out)
