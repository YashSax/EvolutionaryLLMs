https://www.reddit.com/r/MachineLearning/comments/1aji7np/d_microsoft_researchs_evoprompt_evolutionary/

Genes:
    - Attributes:
        - Content -> either some piece of code or some text
        - Fitness -> a single number that represents how good this gene is
        - Characteristics -> String description of the content
    - Methods:
        - Mutate -> apply a random mutation to the gene
        - Combine -> combines two genes using the 

Population:
    - Attributes:
        - Organisms -> List of Genes
        - Generation # -> Current generation
        - Best organism
    - Methods
        - Init -> Size of the population
        - Run Generation:
            - Calculate the fitness of all of the genes
            - Only keep the top N or top K %
            - Mutate and combine them
        - Something to initialize the genes?

Evaluator:
    - Function that takes a gene and returns the fitness
    - Potentially could also return feedback

Mutator:
    - Init -> some prompt
    - Mutates genes in one way or another

Breeder: (the correct term is Crossover but I think Breeder is funnier)
    - Init -> some prompt
    - Combines the characteristics of two genes

"# EvolutionaryLLMs" 
