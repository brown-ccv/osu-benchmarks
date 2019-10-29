
import os
import h5py

# Imports an array that stores which nodes were run recently
#runHist = h5py.File('/gpfs/data/ccvstaff/osu-benchmarks/runHist.h5f5', 'a')
#preexists = "/histArray" in runHist

# TODO: create new h5py if not exists

# TODO: add something that is basically like a heat map
histArray = {}

# Get list of nodes in batch partition
nodeSteam = os.popen("sinfo --Node | grep batch | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'")
nodelist = nodeStream.read().split(',')

# TODO: save two dimensional dictionary histArray into h5py for later use


