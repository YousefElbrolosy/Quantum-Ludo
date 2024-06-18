# Quantum Ludo

We added a twist to the famous Ludo game by making the dice controllable by a quantum circuit! This allows you to bias your dice into probabilities you favor, only if you know the right quantum circuit for it ;)

This game aims to help people familiarize themselves with how quantum circuits are constructed in a fun and creative environment.

## Features

- **Controllable Quantum Dice:** The dice in the game are controlled by a quantum circuit, allowing you to bias the outcomes if you know how to set up the circuit correctly.
- **Quantum Error Correction:** Under the hood, we apply quantum error correction algorithms to two out of our three qubits. Noise is added to the circuit and then removed using the famous quantum error correction algorithm, which adds more qubits in a certain way to produce one noiseless (logical) qubit.
- **Qiskit Integration:** All qubit simulations are done using Qiskit on IBM's quantum simulators. While these simulations can be replaced by real quantum computers on the cloud, we opted to use simulators for speed purposes to avoid waiting in a queue for runtime of our circuits.

## Getting Started

### Prerequisites

To run this project, you need to have the following installed:

- Python 3.7+
- Qiskit

You can install Qiskit using pip:

```sh
pip install qiskit
```

To install the game locally
```
$ git clone https://github.com/YousefElbrolosy/Quantum-Ludo.git
```


This code uses [Sahaj Mistry's](https://github.com/i-sahajmistry/Ludo.git) Classical version of Ludo as well as James Weaver's quantum-circuit-pygame [package](https://github.com/JavaFXpert/quantum-circuit-pygame).
