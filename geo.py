import geonamescache
import spacy
import re

gc = geonamescache.GeonamesCache()

# gets nested dictionary for countries
countries = gc.get_countries()

# gets nested dictionary for cities
cities = gc.get_cities()

def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)


# Python program to convert a list
# to string using join() function

# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = "|"

    # return string
    return (str1.join(s).lower())


cities = [*gen_dict_extract(cities, 'name')]
countries = [*gen_dict_extract(countries, 'name')]

#print(cities)
#print(countries)

#nlp = spacy.load("en_core_web_trf")
s = """#pegados#etiquetas#otraetiqueta @rrrmn2 #hashtags #🦫 REPUS 🦫
#Have a good day, humans of Guadalajara Mexico Jalisco Winnipeg Bench MX GDL México Mejico Estados Unidos America USA España Spain!
#
#repus #repusgraffiti #repusbeaver #hoppergraffiti #fr8painting #fr8traingraffiti #fr8porn #benching #benchingtrains #trainbenching #winnipegbench #canadabench #albanypark"""
s = re.sub(r'#', r' #', s)
s = s.lower()
#doc = nlp(s)

#doc= nlp('Resilience Engineering Institute, Tempe, AZ, United States; Naval Postgraduate School, Department of Operations Research, Monterey, CA, United States; Arizona State University, School of Sustainable Engineering and the Built Environment, Tempe, AZ, United States; Arizona State University, School for the Future of Innovation in Society, Tempe, AZ, United States')


#Convierte en lista diccionario uno
wordList = '''cdmx winnipeg guadalajara guadalajara albany park guadalajara park'''.lower()
wordList = wordList.split()
wordOr = '|'.join(wordList)


s = s.lower()
s_list = s.split()

# Driver code
cities_str = listToString(cities)
#wordOr = cities_str

print(cities_str)
#p = re.compile(r'(?:[a-z0-9]{1,4}:+){3,5}[a-z0-9]{1,4}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def splitHashTag(hashTag):
    p = r'(?:' + wordOr + ')+'
    for wordSequence in re.findall(p, hashTag):
        print("encontró algo")
        print(type(wordSequence))
        print(wordSequence)

for hashTag in s_list:
    print('###', hashTag)
    splitHashTag(hashTag)

