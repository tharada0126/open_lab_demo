import numpy as np
import copy

test_problem = [
    { "name": "ベーコン", "price": 250, "value": 80, "category": "肉類" },
    { "name": "チキン", "price": 300, "value": 90, "category": "肉類" },
    { "name": "ハンバーグ", "price": 350, "value": 100, "category": "肉類" },
    { "name": "フィッシュ", "price": 280, "value": 70, "category": "肉類" },
    { "name": "てりやきソース", "price": 50, "value": 60, "category": "ソース類" },
    { "name": "マヨネーズソース", "price": 40, "value": 70, "category": "ソース類" },
    { "name": "マスタードソース", "price": 45, "value": 80, "category": "ソース類" },
    { "name": "オーロラソース", "price": 55, "value": 60, "category": "ソース類" },
    { "name": "ブラウンソース", "price": 60, "value": 50, "category": "ソース類" },
    { "name": "ケチャップソース", "price": 30, "value": 80, "category": "ソース類" },
    { "name": "タルタルソース", "price": 70, "value": 80, "category": "ソース類" },
    { "name": "目玉焼き", "price": 130, "value": 90, "category": "その他トッピング" },
    { "name": "ピクルス", "price": 85, "value": 70, "category": "その他トッピング" },
    { "name": "トマト", "price": 90, "value": 80, "category": "その他トッピング" },
    { "name": "レタス", "price": 70, "value": 60, "category": "その他トッピング" },
    { "name": "玉ねぎ", "price": 75, "value": 75, "category": "その他トッピング" },
    { "name": "アボカド", "price": 150, "value": 80, "category": "その他トッピング" },
    { "name": "キャベツ", "price": 65, "value": 50, "category": "その他トッピング" },
    { "name": "チーズ", "price": 140, "value": 30, "category": "その他トッピング" }
]

class Problem:
    def __init__(self, problem, budget):
        self.problem = self._convert_problem(problem)
        self.num_meet = len(self.problem['meet'])
        self.num_sauce = len(self.problem['sauce'])
        self.num_topping = len(self.problem['topping'])
        self.dim = 2 + self.num_topping
        self.budget = budget
    
    def _convert_problem(self, problem):
        key_dict = {"肉類": "meet", "ソース類": "sauce", "その他トッピング": "topping"}
        return {
            key_dict[category]: [item for item in problem if item['category'] == category]
            for category in set(item['category'] for item in problem)
        }

    def generate_individual(self):
        ind = []
        ind.append(np.random.randint(0, self.num_meet))
        ind.append(np.random.randint(0, self.num_sauce))
        for _ in range(self.num_topping):
            ind.append(np.random.randint(0, 2))
        return ind

    def evaluation(self, ind):
        sum_price = 0
        sum_value = 0
        meet = self.problem['meet'][ind[0]]
        sum_price += meet['price']
        sum_value += meet['value']
        sauce = self.problem['sauce'][ind[1]]
        sum_price += sauce['price']
        sum_value += sauce['value']
        for i in range(self.num_topping):
            if ind[i+2] == 1:
                topping = self.problem['topping'][i]
                sum_price += topping['price']
                sum_value += topping['value']
        return sum_price, sum_value
    
    def show_selected_items(self, ind):
        meet = self.problem['meet'][ind[0]]
        print(meet)
        sauce = self.problem['sauce'][ind[1]]
        print(sauce)
        toppings = [self.problem['topping'][i] for i in range(self.num_topping) if ind[i+2] == 1]
        for topping in toppings:
            print(topping)
    
    def get_selected_items(self, ind):
        meet = self.problem['meet'][ind[0]]
        sauce = self.problem['sauce'][ind[1]]
        toppings = [self.problem['topping'][i] for i in range(self.num_topping) if ind[i+2] == 1]
        res = [meet, sauce] + toppings
        return res

def initialization(population_size, problem):
    return [problem.generate_individual() for _ in range(population_size)]

def one_point_crossover(ind1, ind2):
    point = np.random.randint(1, len(ind1))
    return ind1[:point] + ind2[point:], ind2[:point] + ind1[point:]

def mutation(ind, mutation_rate, problem):
    for i in range(len(ind)):
        if np.random.rand() < mutation_rate:
            if i == 0:
                ind[i] = np.random.randint(0, problem.num_meet)
            elif i == 1:
                ind[i] = np.random.randint(0, problem.num_sauce)
            else:
                ind[i] = np.random.randint(0, 2)
    return ind

def calculate_fitness(ind, problem):
    price, value = problem.evaluation(ind)
    return value - max(0, price - problem.budget) * 10

def tournament_selection(population, fitnesses, problem, tournament_size=2):
    selected = []
    for _ in range(tournament_size):
        candidates = np.random.choice(len(population), tournament_size, replace=False)
        best_cand = np.argmax([fitnesses[cand] for cand in candidates])
        selected.append(copy.deepcopy(population[candidates[best_cand]]))
        
    return selected

def genetic_algorithm(population_size, problem, generation, crossover_rate, mutation_rate):
    population = initialization(population_size, problem)
    fitnesses = [calculate_fitness(ind, problem) for ind in population]
    best_idx = np.argmax(fitnesses)
    best_ind = population[best_idx]
    best_fit = fitnesses[best_idx]
    best_price, best_value = problem.evaluation(best_ind)
    for gen in range(generation):
        next_population = []
        for _ in range(population_size // 2):
            ind1, ind2 = tournament_selection(population, fitnesses, problem)
            if np.random.rand() < crossover_rate:
                ind1, ind2 = one_point_crossover(ind1, ind2)
            ind1 = mutation(ind1, mutation_rate, problem)
            ind2 = mutation(ind2, mutation_rate, problem)
            next_population.extend([ind1, ind2])
        next_fitnesses = [calculate_fitness(ind, problem) for ind in next_population]
        elites = np.argsort(fitnesses)[-2:]
        next_population.extend([population[elite] for elite in elites])
        next_fitnesses.extend([fitnesses[elite] for elite in elites])
        sort_idx = np.argsort(next_fitnesses)[::-1]
        population = [next_population[idx] for idx in sort_idx]
        fitnesses = [next_fitnesses[idx] for idx in sort_idx]
        best_idx = np.argmax(fitnesses)
        if fitnesses[best_idx] > best_fit:
            best_ind = population[best_idx]
            best_fit = fitnesses[best_idx]
            best_price, best_value = problem.evaluation(best_ind)
        print(f"Generation {gen+1}: Best Fitness {best_fit}, Best Price {best_price}, Best Value {best_value}")
    return best_ind, best_price, best_value, problem.get_selected_items(best_ind)

if __name__ == "__main__":
    problem = Problem(test_problem, 500)
    best_ind, best_price, best_value, selected_items = genetic_algorithm(100, problem, 100, 1.0, 1.0/problem.dim)
    print(f"Best Price: {best_price}, Best Value: {best_value}")
    print("Selected Items")
    for item in selected_items:
        print(item)