# ACES

Through this project, we attempted to implement the method for scalable noise metrology of quantum circuits that improves upon randomized benchmarking, interleaved RB and simulataneous RB. The theory behind ACES is linked here: [Averaged circuit eigenvalue sampling](https://arxiv.org/pdf/2108.05803.pdf) is developed by Steven T. Flammia.

##### General Problem:

The error rates of a general Pauli channel can be reinterpreted by examining the error rates of the Pauli-twirl of that channel.

##### Method: 

1) Generate a random noisy circuit.
- ```generateCliffordCircuit```: generate a random Clifford circuit with single and double qubit gates. This function takes the single and double qubit Clifford gate sets as the input. Then it randomly generate a ```qiskit``` circuit with single and double qubit gates layer by layer.
2) Generate the "A" matrix: To continue, we build a matrix A, constructed to build to full rank. Each row in matrix A represents in independent sampling of the quauntum circuit, meant to capture the frequency of errors for each operation on each Pauli input.
3) Solve the "A" matrix for Pauli Error rates: Given a matrix A, we solve the equation Ax=b for x, where x corresponds to the Pauli eigenvalues of the twirled channel.
4) From Lambda to Error Probabilities: We take the eigenvalues of the individual gates and Hadamard transform them to find the probability of an errors for a general Pauli Channel at the each gate level.
