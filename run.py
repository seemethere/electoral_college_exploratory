import csv


def read_electoral_college(filename):
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            yield line.strip().split('\t')


def read_population_data(filename):
    for line in csv.DictReader(open(filename, 'r')):
        yield line

def print_table(myDict, colList=None):
   """ Pretty print a list of dictionnaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList:
       colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict:
       myList.append([str(item[col] or '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList:
       print(formatStr.format(*item))

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
print_table(
    country,
    ['name',
     'difference',
     'electoral_percentage',
     'population_percentage',
     'electoral_votes',
     'population'])
