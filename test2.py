from general_functions import *
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

    for token in doc:
        if not token.is_space:
            print(token.text, token.lemma_, token.pos_)
            if token._.is_hashtag:
                print(token.text, " - hashtag")
                token_hashtag = re.sub(r'#', r'', token.text)
                # print( len(cl.hashtag_info(token_hashtag)) )
                # try:
                # cl.hashtag_info(token_hashtag)
                # print(token.text, " - ", cl.hashtag_info(token_hashtag).media_count)
                # time.sleep(5)
                # except:
                # print("An exception occurred")
                if token._.is_geo:
                    print("Countrycode -", token._.geo_countrycode)
                    print("Lemma hashtag -", token._.geo_hashtag)
            elif token._.is_mention:
                token_mention = re.sub(r'@', r'', token.text)
                # if cl.user_info_by_username(token_mention):
                # print(token.text, " - ", cl.user_info_by_username(token_mention).biography)
                # time.sleep(5)
                print(token.text, " - arroba ")
    print("post time --- %s seconds ---" % (time.time() - start_time))

print("total time --- %s seconds ---" % (time.time() - global_time))