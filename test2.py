# Importing Modules

import pygame
from   pygame import mixer
import random
import time

# Initializing pygame
import numpy
import qiskit
from qiskit import *
from qiskit import Aer, QuantumCircuit
from qiskit import execute

#from qiskit_aer import Aer
from controls.circuit_grid import CircuitGrid
from data import globals
from model.circuit_grid_model import CircuitGridModel
pygame.init()
pygame.display.set_caption("Ludo")
screen = pygame.display.set_mode((1200, 875))

import matplotlib.pyplot as plt

from qiskit_aer import AerSimulator
from qiskit.circuit.library import *
from qiskit_aer.noise import (NoiseModel, depolarizing_error)

# Define the noise model
def noise():
    i_error = depolarizing_error(0.3, 1)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(i_error, "i_with_error")
    return noise_model

# Define the noisy gate
def noise_circuit():
    # This should be qc = QuantumCircuit(1)
    # Measuring for demostration purposes
    qc = QuantumCircuit(1)
    i_gate = IGate(label="i_with_error")
    qc.append(i_gate, [0])
    return qc

# 3 qubit encoding circuit
def encoding_circuit():
    qc = QuantumCircuit(3)
    qc.cx(0,1)
    qc.cx(0,2)
    return qc
# 3 qubit decoding circuit
def decoding_circuit():
    qc = QuantumCircuit(3)
    qc.cx(0,1)
    qc.cx(0,2)
    qc.ccx(2, 1, 0)   
    return qc

# 3 qubit hadamard addition
def phase_correction():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    return qc

def error_correcting_circuit():
    qc = QuantumCircuit(9)
    
    qc = qc.compose(encoding_circuit(), [0,3,6])
    qc = qc.compose(phase_correction(), [0,3,6])
    
    qc = qc.compose(encoding_circuit(), [0,1,2])
    qc = qc.compose(encoding_circuit(), [3,4,5])
    qc = qc.compose(encoding_circuit(), [6,7,8])
    
    qc.barrier()
    qc = qc.compose(noise_circuit(), [0])
    qc.barrier()

    
    qc = qc.compose(decoding_circuit(), [0,1,2])
    qc = qc.compose(decoding_circuit(), [3,4,5])
    qc = qc.compose(decoding_circuit(), [6,7,8])
        
    qc = qc.compose(phase_correction(), [0,3,6])
    qc = qc.compose(decoding_circuit(), [0,3,6])
    
    return qc
# Quantum Dice
def quantum_dice():
    #circuit
    #simulator = Aer.get_backend('statevector_simulator')
    circuit = circuit_grid.circuit_grid_model.compute_circuit()
    

    full_circuit = QuantumCircuit(27,3)
    full_circuit = full_circuit.compose(circuit, [0,9,18])
    full_circuit = full_circuit.compose(error_correcting_circuit(), range(9))
    full_circuit = full_circuit.compose(error_correcting_circuit(), range(9,18))
    full_circuit = full_circuit.compose(error_correcting_circuit(), range(18, 27))
    full_circuit.measure(0,0)
    full_circuit.measure(9,1)
    full_circuit.measure(18,2)

    full_circuit.draw()


    
    simulator = AerSimulator(noise_model = noise())
    transpiled_circuit = qiskit.transpile(full_circuit, simulator)
    dict_count = simulator.run(transpiled_circuit, shots = 100).result().get_counts()




    """
    # Get the magnitudes of the statevector
    magnitudes = numpy.abs(statevector)**2
    # Ignore the last two elements of the magnitudes
    epsilon = 1e-7
    magnitudes = magnitudes + epsilon

    # Normalize the magnitudes so they sum to 1
    magnitudes = magnitudes / numpy.sum(magnitudes)

    print(magnitudes)

    # Create a list of possible dice rolls
    dice_rolls = list(range(0, 8))

    # Choose a dice roll based on the magnitudes as probabilities
    dice_roll = numpy.random.choice(dice_rolls, p=magnitudes)

    # Return the list of dice rolls
    """
    return dict_count

def createGrid():

    circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT, CircuitGridModel(globals.NUM_QUBITS,16))
    circuit_grid.handle_input(pygame.K_h)
    circuit_grid.handle_input(pygame.K_s)
    circuit_grid.handle_input(pygame.K_h)
    circuit_grid.handle_input(pygame.K_s)
    circuit_grid.handle_input(pygame.K_h)
    circuit_grid.handle_input(pygame.K_w)
    circuit_grid.handle_input(pygame.K_w)
    circuit_grid.handle_input(pygame.K_d)
    globals.GATE_COUNT=5
    return circuit_grid


circuit_grid = createGrid()
print(quantum_dice())