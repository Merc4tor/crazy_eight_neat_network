        for player in result:
            if len(player.hand) != 0:   
                player.genome[0].fitness += 1 - (-1 / (len(player.hand)) + 1)