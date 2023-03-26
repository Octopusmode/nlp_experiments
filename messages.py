# Telegram data parser

import pandas as pd
import json
from tqdm import tqdm
import emoji
import logging
from datetime import datetime
from pathlib import Path
import re

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

data_file = Path(r'source_test\result.json')

TEXT_TYPES = ['plain', 'bold', 'italic', 'code', 'underline']

messages = []
participants = {}
last_nick_id = None

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)


def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')


def extract_id(id_str):
    return re.findall("\d+", id_str)[0]


def get_user_id(usr_name, user_list=participants):
    if usr_name in participants:
        return participants[usr_name]
    return None


def extract_content(msg):
    def parse_text(txt_ent):
        txt = []
        mnt_ids = []
        for item in txt_ent:
            if item['type'] in TEXT_TYPES:
                if item['text']:
                    content = item['text'] + '\n'
                    txt.append(content)

                if 'mention' in item:
                    usr_name = item['text']
                    usr_id = get_user_id(usr_name)
                    mnt_ids.append(usr_id)
                else:
                    mnt_ids = None
        return txt, mnt_ids

    mention_ids = []
    rep_id = None
    text_content = None
    # Извлекаем из сообщения нужные нам данные
    msg_id = msg['id']
    text_entities = msg.get('text_entities', [])
    user, user_id = (msg['from'], int(extract_id(msg['from_id'])))
    date = msg['date_unixtime']
    text_content, mentions = parse_text(text_entities)
    if "reply_to_message" in msg:
        rep_id = msg['reply_to_message']
    return msg_id, user_id, text_content, mentions, date, rep_id


for message in tqdm(data['messages'], desc='Добавляем участников...'):
    if 'from' in message and 'from_id' in message:
        participants[message['from']] = int(extract_id(message['from_id']))

for message in tqdm(data['messages'][:10], desc='Обрабатываем сообщения...'):
    # Пропускаем запись если это оне сообщение от участника
    if message['type'] != 'message' and len(message['text_entities']) == 0:
        continue

    # Если предыдущий отправитель не равен текущему или прошло больше 5 минут, то
    # Создаём переменную с необходимыми полями:
    # message_id, from_id, text, mention_ids, timestamp, reply_id

    message_id, from_id, text, mentions_ids, timestamp, reply_id = extract_content(message)

    logging.debug(extract_content(message))
    # TODO Фиксируем предыдущего отправителя
    previous_from_id = from_id
    logging.debug(previous_from_id)
