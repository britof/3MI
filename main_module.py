#importa os módulos de mapeamento cartesiano, tomada de decisão e integração com hardware
import cartesius, neural_network, machine

#função principal
def main(ROUTE, operation_mode, machine):
    
    if(operation_mode == 'standard'):
        #inicialização (ponto zero)
        matched_points = 0

        #enquanto o botão de ligar estiver pressionado (sinal = 1)
        while(machine.input.ON_OFF()):

            #escanear ambiente
            SCAN = neural_network.run(machine.input.scan())

            #enquanto a rede neural não indicar rota de colisão
            while(SCAN != 0):
                
                #seguir a rota armazenada
                machine.output.move(ROUTE.nextStep(matched_points)
                matched_points = matched_points + 1

            #desviar da rota de colisão
            wrong_segment = machine.output.moveWithDeviation(SCAN)

            #corrigir o desvio efetuado                        
            machine.output.move(ROUTE.setRight(matched_points, wrong_segment))
            matched_points = matched_points + 1                                    

    if(operation_mode == 'learning'):
        #enquanto a rota não for salva                                    
        while(machine.input.save_route == False):

            #adicionar segmento à rota
            ROUTE.appendSegment(machine.input.lastSegment())

if(__name__ == '__main__'):
    main()
