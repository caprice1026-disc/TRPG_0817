from flask_restx import Resource
from models import db, Player

class CharacterAPI(Resource):
    def setcharacter(self):
        # キャラクター情報を取得するロジックを追加する予定
        pass

    def CreateCharacter(self, name, character_class, back_story):
        # キャラクターを作成するロジックを追加する予定
        #新しいPlayerインスタンスを作成（Playerクラスはmodels.pyで定義、各値は引数で渡す）
        new_player = Player(name=name, character_class=character_class, back_story=back_story)
        #新しいPlayerインスタンスをデータベースに追加
        db.session.add(new_player)
        pass
    
