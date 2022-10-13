from PatternOmatic.api import find_patterns
import time
import mysql.connector
import json

global_time = time.time()

c = open("config.json")
config = json.load(c)
MUID = 'fr8heaven_1_hashtagRecent_6_3708ca94'
try:
    cnx = mysql.connector.connect(user=config["SQL"]["username"],
                                  password=config["SQL"]["password"],
                                  host=config["SQL"]["hostname"],
                                  database=config["SQL"]["database"],
                                  )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Looking for caption in MUID:", MUID)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM data_media WHERE MUID IN ('%s') " % (MUID))
    posts = cursor.fetchall()
    print("MUID found :", len(posts))

    post_list_str = ""
    for post in posts:
        print(post[11])
        post_list_str += post[11]
        #feel slower

    print (post_list_str)
    start_time = time.time()
    # cl.login("betitoprendido3", "challenge/action/1")
    s = """#SanDiegoBenching #TlajoGraff #ScottAirForceOne 
            #cherokeetag#NorthPekin#SanFrancisco#SanSebastianelGrande#BuenaVista#WestlakeVillage 
            #winnipegbench #graffiticholula #graffititoluca #canadabench#jaliscograffiti#benchguadalajara#bombasguadalajaramistrik#jasdjaws 
            #jawscaminojalisco#tlajomulco#guadalajaragraffiti"""
    s = post_list_str
    s = re.sub(r'#', r' #', s)
    doc = nlp(s)

samples = ['I am a cat!', 'You are a dog!', 'She is an owl!']

patterns_found, _ = find_patterns(samples)

print(f'Patterns found: {patterns_found}')