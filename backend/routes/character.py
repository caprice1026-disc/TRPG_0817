# routes/character.py
from flask_restx import Resource
from models import db, Character

class CharacterAPI(Resource):
    def get(self):
        # キャラクター情報を取得するロジックを追加
        pass

    def create_character(self ,character_name, character_class, back_story):
        """キャラクターを作成する"""
        character = Character(character_name, character_class, back_story)
        db.session.add(character)
        db.session.commit()
        return {"message": "Character created successfully"}
