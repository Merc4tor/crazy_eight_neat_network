
import neat
import pesten_ai


def eval_genomes(genomes, config):
    # genome.fitness = 4.0

    game = pesten_ai.Game(False)
        
    genomes_with_net = [(genome[1], neat.nn.FeedForwardNetwork.create(genome[1], config)) for genome in genomes]

    for genome in genomes:
        genome[1].fitness = 0

    for i in range(4):
        manager = pesten_ai.GameManager(0, genomes=genomes_with_net, game=game)

        result = manager.play()
    
        for player in result:
            player.genome[0].fitness += len(player.hand) / max([len(player.hand) for player in result])



# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(False))

# Run until a solution is found.
winner = p.run(eval_genomes)

# Display the winning genome.
print('\nBest genome:\n{!s}'.format(winner))

# Show output of the most fit genome against training data.
print('\nOutput:')
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
# for xi, xo in zip(xor_inputs, xor_outputs):
#     output = winner_net.activate(xi)
#     print("  input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))