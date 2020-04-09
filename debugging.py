def backward_propagation(network, inputs, targets, alpha):
    _input = list()    #
    _target = targets[0]
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

    for layer in range(2):
            for neuron in range(len(new_network_setup[layer])):
                for weight in range(len(neuron)):
                    averaged_new_network_setup[layer][neuron][weight] /= n_of_samples
    return averaged_new_network_setup
