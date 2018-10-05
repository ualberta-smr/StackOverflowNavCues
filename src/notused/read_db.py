import pdb
import time 
import sqlite3 

def get_unique_labels():
    conn = sqlite3.connect('Witt.db')
    cursor = conn.cursor()
    res = {}
    index = {}
    main = []
    techs = list(cursor.execute("select * from technologies").fetchall())
    for tech in techs:
        if not tech[2] in res:
            res[tech[2]] = set()

        if not tech[0] in index:
            index[tech[0]] = tech[1]

        res[tech[2]].add(tech[1])

        if tech[2] == 1:
            main.append(tech[0])

    # for g_id, children in res.items():
    #     print("{}:{}".format(index[g_id], children))

    reverse_index = {v:k for k, v in index.items()}
    
    vals = []
    for item in main:
        vals.append(index[item])
        print(index[item])

    # pdb.set_trace()


def get_all_tags():
    QUERY = 'select distinct C.Tag, A.Tech from (select id, Tech from technologies) as A join (select Tag, Tech from tagstotechs) as B join tags as C on A.id=B.Tech and B.Tag=C.id where A.Tech != "(no category)";'

    conn = sqlite3.connect('Witt.db')
    cursor = conn.cursor()
    tags = list(cursor.execute(QUERY).fetchall())

    tags_dict = {}
    for tag in tags:
        tags_dict[tag[0]] = tag[1]
   
    return tags_dict

if __name__=="__main__":
    res = get_all_tags()
    pdb.set_trace()
    # get_unique_labels()