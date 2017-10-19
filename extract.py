import pymysql.cursors
import json
import datetime

# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='info',
    password='aut',
    db='infoaut',
    charset='utf8mb4',
    # cursorclass=pymysql.cursors.DictCursor
)

def to_dict(id, title, alias, catid, published, introtext, fulltext, video, gallery, extra_fields, extra_fields_search, created, created_by, created_by_alias, checked_out, checked_out_time, modified, modified_by, publish_up, publish_down, trash, access, ordering, featured, featured_ordering, image_caption, image_credits, video_caption, video_credits, hits, params, metadesc, metadata, metakey, plugins, language):
    return {
        "id": id,
        "title": title,
        "alias": alias,
        "catid": catid,
        "published": published,
        "introtext": introtext,
        "fulltext": fulltext,
        "video": video,
        "gallery": gallery,
        "extra_fields": extra_fields,
        "extra_fields_search": extra_fields_search,
        "created": created,
        "created_by": created_by,
        "created_by_alias": created_by_alias,
        "checked_out": checked_out,
        "checked_out_time": checked_out_time,
        "modified": modified,
        "modified_by": modified_by,
        "publish_up": publish_up,
        "publish_down": publish_down,
        "trash": trash,
        "access": access,
        "ordering": ordering,
        "featured": featured,
        "featured_ordering": featured_ordering,
        "image_caption": image_caption,
        "image_credits": image_credits,
        "video_caption": video_caption,
        "video_credits": video_credits,
        "hits": hits,
        "params": params,
        "metadesc": metadesc,
        "metadata": metadata,
        "metakey": metakey,
        "plugins": plugins,
        "language": language,
    }

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `xs8ea_finder_links`"
        cursor.execute(sql)
        rs = cursor.fetchall()
        all_zuzamment = []
        for result in rs:
            result = [a if type(a) == str else a for a in result]
            result = [a.isoformat() if isinstance(a, datetime.datetime) else a for a in result]
            renny = to_dict(*result)
            all_zuzamment.append(renny)
        
        print(len(all_zuzamment))

        with open('posts.json', 'w') as f:
            json.dump(all_zuzamment, f)
        
finally:
    connection.close()



def to_dict(link_id,url,route,title,description,indexdate,md5sum,published,state,access,language,publish_start_date,publish_end_date,start_date,end_date,list_price,sale_price,type_id,object):
    return {
        "link_id": link_id,
        "url": url,
        "route": route,
        "title": title,
        "description": description,
        "indexdate": indexdate,
        "md5sum": md5sum,
        "published": published,
        "state": state,
        "access": access,
        "language": language,
        "publish_start_date": publish_start_date,
        "publish_end_date": publish_end_date,
        "start_date": start_date,
        "end_date": end_date,
        "list_price": list_price,
        "sale_price": sale_price,
        "type_id": type_id,
        "object": object,
    }

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `xs8ea_finder_links`"
        cursor.execute(sql)
        rs = cursor.fetchall()
        all_zuzamment = []
        for result in rs:
            for a in result:
                print(type(a))
            result = [str(a, 'utf-8') if type(a) == bytes else a for a in result]
            result = [a.isoformat() if isinstance(a, datetime.datetime) else a for a in result]
            renny = to_dict(*result)
            all_zuzamment.append(renny)
        
        print(len(all_zuzamment))

        with open('links.json', 'w') as f:
            json.dump(all_zuzamment, f)
        
finally:
    connection.close()


def to_dict(id, parent_id, lft, rgt, level, name, title, rules):
    return {
        "id": id,
        "parent_id": parent_id,
        "lft": lft,
        "rgt": rgt,
        "level": level,
        "name": name,
        "title": title,
        "rules": rules,
    }

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `xs8ea_assets`"
        cursor.execute(sql)
        rs = cursor.fetchall()
        all_zuzamment = []
        for result in rs:
            for a in result:
                print(type(a))
            result = [str(a, 'utf-8') if type(a) == bytes else a for a in result]
            result = [a.isoformat() if isinstance(a, datetime.datetime) else a for a in result]
            renny = to_dict(*result)
            all_zuzamment.append(renny)
        
        print(len(all_zuzamment))

        with open('assets.json', 'w') as f:
            json.dump(all_zuzamment, f)
        
finally:
    connection.close()