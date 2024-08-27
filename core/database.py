import os
import json
from pathlib import Path
from pymongo import MongoClient
from core.logger import logger 
from core.config import configs
from urllib.parse import quote_plus

config = configs.mongodb


class MongoDB:
    def __init__(self):
        # 기본 설정값
        host = config["host"]
        # port = config["port"]         # atlas로 관리하여 제외
        db = config.get("database", None)

        username = quote_plus(os.getenv(config["userKey"], ""))
        password = quote_plus(os.getenv(config["pwdKey"], ""))
        
        # URI 생성
        # uri = f"mongodb://{username}:{password}@{host}:{port}/{db}"         # atlas로 관리하여 제외
        uri = f"mongodb+srv://{username}:{password}@{host}"
        
        # 클라이언트 유효성 검사
        try:
            # 클라이언트 생성
            self.client = MongoClient(uri)
            self.db_list = self.client.list_database_names()
            
            # db, collection 생성
            self.db = self._get_db(db)
            
            # 로거
            logger.info(f"클라이언트 생성 완료")
        except:
            logger.error("연결정보가 올바르지 않습니다. URI 정보들을 다시 확인해주세요.(format=mongodb+srv://{username}:{password}@{host})")

    def _get_db(self, db_name):
        try:
            db = self.client[db_name]
            self.collection_list = db.list_collection_names()
        except:
            logger.error(f"데이터베이스 목록을 다시 확인하세요 - {self.db_list}")
        
        return db

    def connect_collection(self, collection_name):
        if collection_name in self.collection_list:
            # 컬렉션 연결
            self.collection = self.db[collection_name]

            return self.collection
        else:
            logger.error(f"컬렉션 이름이 목록에 존재하지 않습니다 - {self.collection_list}")

mongo = MongoDB()