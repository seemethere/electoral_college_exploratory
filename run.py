import csv


def read_electoral_college(filename):
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            yield line.strip().split('\t')


def read_population_data(filename):
    for line in csv.DictReader(open(filename, 'r')):
        yield line

country = {item[0]: {'electoral_votes': int(item[1]), 'name': item[0]}
           for item in read_electoral_college(
               'data/electoral_college_allocation')}

for item in read_population_data('data/population.csv'):
    state = country.get(item['NAME'], None)
    if not state:
        continue
    state['population'] = int(item['POPESTIMATE2015'])

total_population = sum(
    state['population'] for _, state in country.items())
total_electoral_votes = sum(
    state['electoral_votes'] for _, state in country.items())

for _, state in country.items():
    state['population_percentage'] = (
        (state['population'] / total_population) * 100)
    state['electoral_percentage'] = (
        (state['electoral_votes'] / total_electoral_votes) * 100)
    state['difference'] = (
        state['electoral_percentage']) - state['population_percentage']

country = sorted(country.values(), key=lambda item: item['difference'])
