## Módulo de Tomada de Decisão do 3MI
## Autor: Joás de Brito
#
#Possui funções que criam, treinam e executam FFNNs com uma camada oculta
#
#A rede neural é representada como uma lista de camadas;
#Cada camada é representada como uma lista de neurônios;
#Cada neurônio é representado como uma lista de pesos;
#Cada peso é representado como um número real.
#
#neuron  == weights list
#layer   == neurons list
#network == layers list
#
#

from math import exp
import random

#retorna uma lista de listas no formato network = [[hidden_layer], [output_layer]]
#os pesos são inicializados aleatoriamente no range [0,1]
#os biases são inicializados como b = 0
def generate_network(in_n, hid_n, out_n):  #número de neurônios nas camadas
    hidden_layer = []
    for h_neuron in range(hid_n):
        neuron = []

        for h_weight in range(in_n):            
            neuron.append(random.random())
        neuron.append(0) #bias weight
        hidden_layer.append(neuron)

    output_layer = []
    for o_neuron in range(out_n):
        neuron = []
        for o_weight in range(hid_n):
            neuron.append(random.random())
        neuron.append(0) #bias weight
        output_layer.append(neuron)

    network = [hidden_layer, output_layer]
    print("HIDDEN Layer: ")
    print(hidden_layer)
    print("OUTPUT Layer: ")
    print(output_layer)
    return network

#calcula a entrada de um dado neurônio 
def weighted_sum(weights, inputs):
    output = weights[-1] #bias
    for i in range(len(weights)-1):
        output += inputs[i] * weights[i]
    return output

def sigmoid(x):
    return 1/(1+exp(-x))

#calcula a saída de uma rede para uma dada entrada
def forward_propagation(network, inputs):
    h_output = []
    for neuron in network[0]:
        h_output.append(sigmoid(weighted_sum(neuron, inputs)))
    output = []
    for neuron in network[1]:
        output.append(sigmoid(weighted_sum(neuron, h_output)))
    return output

#backpropagation: para uma FFNN de arquitetura AxBxC, retorna uma nova configuração de pesos e biases
def backward_propagation(network, inputs, targets, alpha):
    n_of_samples = len(targets)
    _h_in = list()    #
    _h_out = list()    #variaveis
    _o_in = list()    #
    _o_out = list()    #
    _err = list()    #

    _w_ih = network[0]    #input_to_hidden weights
    _w_ho = network[1]    #hidden_to_output weights
    counter = 0

    new_network_setup = network

    for _target in targets: #para cada sample do batch
        _input = inputs[counter]
        outputs = forward_propagation(network, _input)
        for neuron in network[0]:
            weighted_sum = weighted_sum(neuron, _input)
            _h_in.append(weighted_sum)
            _h_out.append(sigmoid(weighted_sum))

        for neuron in network[1]:
            weighted_sum = weighted_sum(neuron, _h_out)
            output = sigmoid(weighted_sum)
            _o_in.append(weighted_sum)
            _o_out.append(output)

        for i in range(len(_target)):
            _err.append(error_function(_o_out[i], _target[i], i))
            print("Output Neuron ",i ,"Error: ", _err[i])

        print("Total network output error: ", error_function(forward_propagation(network, _input), _target))

        #output layer
        j_range = len(_o_out)
        k_range = len(network[1][0])
        for j in range(j_range): #six neurons
            for k in range(k_range): #eleven weights
                partial_derivative_E_ho = (_o_out[j] - _target[j])*(_o_out[j]*(1-_o_out[j]))*(_h_out[j]) #hidden_to_output weights
                new_network_setup[1][j][k] -= alpha * partial_derivative_E_ho #weight update

        #hidden layer
        j_range = len(_h_out)
        k_range = len(network[0][0])
        l_range = len(network[1]) #six output neurons == six weights
        partial_derivative_E_ih = 0.0
        for j in range(j_range): #ten hidden neurons
            for k in range(k_range): #thirty weights
                aux = (_h_out[j] * (1-_h_out[j]) * weighted_sum(_w_ih[j], ))
                o_sum = 0.0
                for l in range(l_range):
                    o_sum += (_o_out[l]-_target[l])*(_o_out[l]*(1 - _o_out[l]))*(_w_ho[j][l])
                partial_derivative_E_ih = aux * o_sum 
                new_network_setup[0][j][k] -= alpha * partial_derivative_E_ih #weight update

        for layer in range(2):
            for neuron in range(len(new_network_setup[layer])):
                for weight in range(len(neuron)):
                    averaged_new_network_setup[layer][neuron][weight] += new_network_setup[layer][neuron][weight]

        counter = counter + 1

    for layer in range(2):
            for neuron in range(len(new_network_setup[layer])):
                for weight in range(len(neuron)):
                    averaged_new_network_setup[layer][neuron][weight] /= n_of_samples
        
    return averaged_new_network_setup

#squared error function
def error_function(output, target, index):
    error = 0.0
    for i in range(len(output)):
        if(index == i and index != -1):
            return pow((output[i] - target[i]), 2)/2
        error += pow((output[i] - target[i]), 2)/2

def train(network, dataset, alpha, epochs):
    batch = 0
    new_network = network
    print("Training with alpha = ", alpha)

    for epoch in range(epochs):
        for batch in range(len(dataset)):
            print("batch: ", epoch)
            inputs = dataset[batch][0]
            targets = dataset[batch][1]
            new_network = backward_propagation(new_network, inputs, targets, alpha) 
    print("Training completed!")
    return new_network
