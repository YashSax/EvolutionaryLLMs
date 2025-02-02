from typing import List, Tuple
from tqdm import tqdm
import random
from abc import ABC, abstractmethod


class Gene(ABC):
    pass

class Evaluation(ABC):
    @abstractmethod
    def __lt__(self, other):
        pass

class Evaluator(ABC):
    @abstractmethod
    def evaluate(gene: Gene) -> Evaluation:
        pass


class Mutator(ABC):
    @abstractmethod
    def mutate(gene: Gene) -> Gene:
        pass


class Breeder(ABC):
    @abstractmethod
    def breed(gene_1: Gene, gene_2: Gene) -> Gene:
        pass


class Population:
    def __init__(
        self,
        num_organisms: List[Gene],
        initial_gene: Gene,
        evaluator: Evaluator,
        mutator: Mutator,
        breeder: Breeder,
        selection_criteria="topk",
        top_k=5,
    ):
        assert (
            top_k <= num_organisms
        ), f"Top k must be lower than the number of organisms, but it's {top_k}"
        self.num_organisms = num_organisms
        self.evaluator = evaluator
        self.mutator = mutator
        self.breeder = breeder

        self.selection_criteria = selection_criteria
        self.topk = top_k

        self.organisms = []
        self.init_genes(initial_gene)

        self.best_gene = None
        self.best_fitness = -1e99

        self.mutate_probability = 0.5

    def init_genes(self, initial_gene):
        """Takes the default gene and mutate it self.num_organisms times."""
        self.organisms = [
            self.mutator.mutate(initial_gene) for _ in range(self.num_organisms)
        ]

    def run_generations(self, num_generations, show_progress=False):
        generation_iterator = (
            tqdm(range(num_generations)) if show_progress else range(num_generations)
        )
        for generation_num in generation_iterator:
            print(f"Running Generation {generation_num}")

            gene_fitnesses = [
                (gene, self.evaluator.evaluate(gene)) for gene in self.organisms
            ]
            best_gene_in_generation, best_generation_fitness = max(
                gene_fitnesses, key=lambda x: x[1]
            )
            if best_generation_fitness > self.best_fitness:
                self.best_fitness = best_generation_fitness
                self.best_gene = best_gene_in_generation

            surviving_genes = self.kill_the_weak(gene_fitnesses)

            # Mutate with probability self.mutate_probability
            # Otherwise we want to breed -> randomly choose two surviving genes
            #   - Maybe we want to select based off the fitnesses? Like higher fitnesses are more likely to breed?
            for _ in range(self.num_organisms - self.topk):
                if random.random() <= self.mutate_probability:
                    random_gene = random.choice(surviving_genes)
                    surviving_genes.append(self.mutator.mutate(random_gene))
                else:
                    parents = random.sample(surviving_genes, 2)
                    surviving_genes.append(self.breeder.breed(*parents))
            self.organisms = surviving_genes

        return self.organisms

    def kill_the_weak(self, genes: List[Tuple[Gene, float]]):
        genes.sort(lambda x: x[1])
        return genes[: self.top_k]
