import random
import numpy as np
import csv

class GeneticSelector:

    def __init__(self, score_provider, elite_size, sample_size, population_size, mutation_rate, gene_range, 
                    gene_length, crossover_rate, crossover_probability, tmp_population_size, generations_number, verbose=False, log=False, log_file = None):
        
        assert(sample_size <= population_size)
        assert(gene_length <= gene_range)
        assert(population_size <= tmp_population_size)
        assert(elite_size <= population_size)
        
        self.score_provider = score_provider
        self.sample_size = sample_size
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.gene_range = gene_range
        self.gene_length = gene_length
        self.crossover_rate = crossover_rate
        self.crossover_probability = crossover_probability
        self.tmp_population_size = tmp_population_size   
        self.generations_number = generations_number
        self.elite_size = elite_size
        self.verbose = verbose
        self.log = log
        self.log_file = log_file

        if self.log:
            with open(self.log_file, 'w') as f:
                log_writer = csv.writer(f)
                log_writer.writerow(['iteration', 'max', 'min', 'mean', 'std', 'best'])

    def tournament_selection(self, scores, genes):
        selected_indexes = random.sample(range(self.population_size), self.sample_size)
        selected_scores=scores[selected_indexes]        
        return genes[np.where(scores == np.max(selected_scores))[0][0]]

    def mutate_gene(self, gene):         
        n = min(self.gene_length, self.gene_range - self.gene_length)
        mutation_options = random.sample(set(range(self.gene_range)).difference(set(gene)), n) 

        for i in range(n):
            if random.random() < self.mutation_rate:
                gene[i] = mutation_options[i]
    
        random.shuffle(gene)
        return gene

    def crossover(self, gene_a, gene_b):
        unique_a = list(set(gene_a).difference(set(gene_b)))
        unique_b = list(set(gene_b).difference(set(gene_a)))
        common = list(set(gene_a).intersection(set(gene_b)))

        for i in range(len(unique_a)):
            if random.random() < self.crossover_rate:
                tmp = unique_a[i]
                unique_a[i] = unique_b[i]
                unique_b[i] = tmp

        new_gene_a = unique_a + common
        new_gene_b = unique_b + common
        random.shuffle(new_gene_a)
        random.shuffle(new_gene_b)       
        
        return [new_gene_a, new_gene_b]

    def generate_new_pair(self, genes, scores):
        gene_a = self.tournament_selection(scores, genes)
        gene_b = self.tournament_selection(scores, genes)

        if random.random() < self.crossover_probability:
            gene_pair = self.crossover(gene_a, gene_b)

        else:
            gene_pair = [gene_a, gene_b]

        gene_pair[0] = self.mutate_gene(gene_pair[0])
        gene_pair[1] = self.mutate_gene(gene_pair[1])
        
        return gene_pair

    def generate_new_population(self, genes, scores):
        new_population = []
        for _ in range(self.tmp_population_size//2):
            gene_pair = self.generate_new_pair(genes, scores)            
            new_population.extend(gene_pair)

        return new_population

    def search(self):
        new_genes = []
        for _ in range(self.tmp_population_size):
            new_genes.append(random.sample(range(self.gene_range), self.gene_length))

        scores = self.score_provider.compute_score(new_genes)
        scores_order = np.flip(np.argsort(scores), 0)[:self.population_size]        
        genes = [new_genes[i] for i in scores_order]

        for i in range(self.generations_number):            
            elite_genes =[gene.copy() for gene in genes[:self.elite_size]]            

            new_genes = self.generate_new_population(genes, scores)
            new_genes.extend(elite_genes)
            scores = self.score_provider.compute_score(new_genes)            
           
            scores_order = np.flip(np.argsort(scores), 0)[:self.population_size]
            genes = [new_genes[i] for i in scores_order]

            if self.verbose:
                print(f'Iteration: {i}, max score: {scores[scores_order[0]]}, best gene: {genes[0]}')    
                
            if self.log:
                with open(self.log_file, 'a') as f:
                    log_writer = csv.writer(f)
                    log_writer.writerow([str(i), str(scores[scores_order[0]]), str(scores[scores_order[-1]]), str(np.mean(scores[scores_order])), str(np.std(scores[scores_order])), '-'.join(str(i) for i in genes[0])])

        return (genes[0], scores[scores_order[0]])



        
