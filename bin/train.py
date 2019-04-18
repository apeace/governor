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

    advisor_chooser_inputs = []
    advisor_chooser_outputs = []

    print("Loading data...")
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
                states = [kingsburg.State().fromDict(s) for s in d["states"]]
                for choice in d["advisor_choices"]:
                    # Structure of each element is (advisor_influence, state_idx)
                    influence = kingsburg.AdvisorInfluence.fromDict(choice[0])
                    s = states[choice[1]]
                    base_input = training.state_to_input(s)
                    influence_input = training.advisor_choice_to_input(s, influence)
                    advisor_chooser_inputs.append(base_input + influence_input)
                    advisor_chooser_outputs.append([int(d["won"]), 1-int(d["won"])])

    print("Training...")
    advisor_chooser_model = keras.models.Sequential()
    advisor_chooser_model.add(keras.layers.Dense(1000, input_dim=516, activation="relu"))
    advisor_chooser_model.add(keras.layers.Dense(1000, activation='relu'))
    advisor_chooser_model.add(keras.layers.Dense(1000, activation='relu'))
    advisor_chooser_model.add(keras.layers.Dense(2, activation="linear", kernel_initializer="glorot_uniform"))
    advisor_chooser_model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
    advisor_chooser_model.fit(numpy.asarray(advisor_chooser_inputs), numpy.asarray(advisor_chooser_outputs), verbose=True)
    advisor_chooser_model.save(out + '_advisor_chooser')
