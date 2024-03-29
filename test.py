from general_functions import *
import time
import mysql.connector
import json
import argparse
from spacy.vocab import Vocab

parser = argparse.ArgumentParser(description='Paso de parámetros')
parser.add_argument("-MUID", dest="p_MUID", help="MUID to fetch")
params = parser.parse_args()
global_time = time.time()

c = open("config.json")
config = json.load(c)
#MUID = 'asoter_1_hashtagTop_9_cec6fcb9'
MUID = params.p_MUID
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
    #cursor.execute("SELECT * FROM data_media WHERE MUID IN ('%s') " % (MUID))
    #sql_detected = "UPDATE data_media SET hashtag_detection = %s WHERE id = %s"
    cursor.execute("SELECT * FROM data_media WHERE (MUID IN ('%s') AND hashtag_detection is null)" % (MUID))
    posts = cursor.fetchall()
    print("MUID found :", len(posts))

    #post_list = []
    #for post in posts:
        #post_list.append(post[11])
        #feel slower

    #print (post_list)
    #for doc in nlp.pipe(post_list):
    #for doc in nlp.pipe(texts, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
        #assert doc.has_annotation("DEP")
    #    print(doc)
    i=0
    for post in posts:
        start_time = time.time()
        # cl.login("betitoprendido3", "challenge/action/1")
        #s = """#SanDiegoBenching #TlajoGraff #ScottAirForceOne
        #cherokeetag#NorthPekin#SanFrancisco#SanSebastianelGrande#BuenaVista#WestlakeVillage 
        #winnipegbench #graffiticholula #graffititoluca #canadabench#jaliscograffiti#benchguadalajara#bombasguadalajaramistrik#jasdjaws 
        #jawscaminojalisco#tlajomulco#guadalajaragraffiti"""
        s = post[11]
        s = re.sub(r'#', r' #', s)
        print("Stripping hashtags and looking for entities at: ",s)
        doc = nlp(s)
        print(doc)
        #clean array in
        token_detected_dict = []
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
                    if token._.is_city:
                        #falta agregar lat-long
                        print("----------- City Hashtag -", token._.geo_hashtag, "countrycode -", token._.geo_countrycode)
                        token_detected_dict.append((token_hashtag, "city", token._.geo_hashtag, token._.geo_countrycode))
                    if token._.is_graffiti_lingo:
                        print("----------- Graffiti Hashtag -", token._.graffiti_hashtag)
                        token_detected_dict.append((token_hashtag, "graffiti_lingo", token._.graffiti_hashtag))
                    if token._.is_railroad_lingo:
                        print("----------- Railroad Hashtag -", token._.railroad_hashtag)
                        token_detected_dict.append((token_hashtag, "railroad_lingo", token._.railroad_hashtag))
                    if token._.is_custom_entity:
                        print("----------- Entity Hashtag -", token._.custom_entity_cat, token._.custom_entity_text )
                        token_detected_dict.append((token_hashtag, "entity", token._.custom_entity_cat, token._.custom_entity_text ))
                elif token._.is_mention:
                    token_mention = re.sub(r'@', r'', token.text)
                    # if cl.user_info_by_username(token_mention):
                    # print(token.text, " - ", cl.user_info_by_username(token_mention).biography)
                    # time.sleep(5)
                    print(token.text, " - arroba ")
        print("----------- Hashtag detected :")
        print(token_detected_dict)
        token_detected_json = json.dumps(token_detected_dict)
        print(token_detected_json)
        cnx.reconnect()
        innercursor = cnx.cursor()
        sql_detected = "UPDATE data_media SET hashtag_detection = %s WHERE id = %s"
        val = (token_detected_json, post[0])
        innercursor.execute(sql_detected, val)
        cnx.commit()
        cnx.close()
        print("post time --- %s seconds ---" % (time.time() - start_time))

print("total time --- %s seconds ---" % (time.time() - global_time))