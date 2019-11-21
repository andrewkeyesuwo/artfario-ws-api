import json
import logging
import pymysql
import sys

db_host = "artfario.cxflsnmivaqh.us-east-2.rds.amazonaws.com"
db_user = "admin"
db_password = ""
db_database = "artfario"

'''
Input: Response of previous images shown
Output: Two new images to show, one is the main, the next is the on deck_image
'''

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    logger.info(event)
    request_body = json.loads(event['body'])
    logger.info(request_body)

    user_cookie = ""
    if(request_body.get('userID') is not None):
        user_cookie = request_body.get('userID').split("=")[1]

    if(request_body.get('action') is not None and request_body['action'] == 'first_visit'):
        with conn.cursor() as cur:
                if(user_cookie != ""):
                    insert_query = "INSERT INTO `user` (`iduser`, `cookie`) VALUES ((SELECT MAX(u.iduser) FROM `user` as u)+1, '"+user_cookie+"');"
                    cur.execute(insert_query)
                    conn.commit()

    if(request_body.get('artworkid') is not None and user_cookie != ""):
        artwork_id = request_body.get('artworkid')
        with conn.cursor() as cur:
            insert_response_query = "INSERT INTO `artfario`.`responses` (`id`, `time`, `response`, `userid`, `artworkid`) VALUES ((SELECT MAX(u.id) FROM `responses` as u)+1, DATE(), 0, (SELECT iduser FROM `user` WHERE cookie = '"+user_cookie+"'), "+str(artwork_id)+");"
            cur.execute(insert_response_query)
            conn.commit()

    records = []
    with conn.cursor() as cur:

        select_query = 'SELECT * FROM artwork  WHERE idartwork NOT IN ( SELECT artworkid FROM responses INNER JOIN user ON responses.userid = user.iduser WHERE cookie = \''+ '' +'\') LIMIT 2;'
        cur.execute(select_query)
        conn.commit()

        for row in cur:
            record = {
                'id': row[0],
                'url': row[1],
                'name': row[2],
                'description': row[3]
            }
            records.append(record)

    response_body = {
        'main_image': records[0]
    }

    return {
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'statusCode': 200,
        'body': json.dumps(response_body)
    }