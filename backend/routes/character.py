from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource
from services.character_service import CharacterService
from models import Player

# BlueprintとFlask-RESTxのAPIインスタンスを作成
character_bp = Blueprint('character', __name__)
api = Api(character_bp)

# サービスクラスのインスタンス化
character_service = CharacterService()

# キャラクター一覧と作成のエンドポイント
@api.route('/characters')
class CharacterListAPI(Resource):
    def get(self):
        """すべてのキャラクターを取得"""
        characters = character_service.get_all_characters()
        return jsonify(characters), 200

    def post(self):
        """新しいキャラクターを作成"""
        data = request.get_json()
        name = data.get('name')
        character_class = data.get('character_class')
        back_story = data.get('back_story')
        world_uuid = data.get('world_uuid')

        if not all([name, character_class, back_story, world_uuid]):
            return {"message": "All fields are required"}, 400

        response, status = character_service.create_character(name, character_class, back_story, world_uuid)
        return response, status

# 特定のキャラクターに対する操作
@api.route('/characters/<string:player_uuid>')
class CharacterAPI(Resource):
    def get(self, player_uuid):
        """特定のキャラクターを取得"""
        character = character_service.get_character(player_uuid)
        if character:
            return jsonify(character), 200
        return {"message": "Character not found"}, 404

    def put(self, player_uuid):
        """キャラクターを更新"""
        data = request.get_json()
        response, status = character_service.update_character(player_uuid, data)
        return response, status

    def delete(self, player_uuid):
        """キャラクターを削除"""
        response, status = character_service.delete_character(player_uuid)
        return response, status

# キャラクターのレベルアップ
@api.route('/characters/<string:player_uuid>/level-up')
class CharacterLevelUpAPI(Resource):
    def put(self, player_uuid):
        """キャラクターをレベルアップ"""
        response, status = character_service.level_up_character(player_uuid)
        return response, status

# キャラクターにダメージを与える
@api.route('/characters/<string:player_uuid>/damage')
class CharacterDamageAPI(Resource):
    def put(self, player_uuid):
        """キャラクターにダメージを与える"""
        data = request.get_json()
        damage = data.get('damage', 0)
        response, status = character_service.character_take_damage(player_uuid, damage)
        return response, status

# キャラクターのHPを回復
@api.route('/characters/<string:player_uuid>/heal')
class CharacterHealAPI(Resource):
    def put(self, player_uuid):
        """キャラクターのHPを回復"""
        data = request.get_json()
        amount = data.get('amount', 0)
        response, status = character_service.restore_character_health(player_uuid, amount)
        return response, status

# キャラクターのアイテム操作
@api.route('/characters/<string:player_uuid>/items')
class CharacterItemsAPI(Resource):
    def get(self, player_uuid):
        """キャラクターのアイテムを取得"""
        items = character_service.get_character_items(player_uuid)
        return jsonify(items), 200

    def post(self, player_uuid):
        """キャラクターにアイテムを追加"""
        data = request.get_json()
        item_name = data.get('name')
        description = data.get('description', "")
        response, status = character_service.add_item_to_character(player_uuid, item_name, description)
        return response, status

# キャラクターの特定のアイテムを削除
@api.route('/characters/<string:player_uuid>/items/<string:item_uuid>')
class CharacterItemAPI(Resource):
    def delete(self, player_uuid, item_uuid):
        """キャラクターのアイテムを削除"""
        response, status = character_service.remove_item_from_character(player_uuid, item_uuid)
        return response, status

# Blueprintを登録
def register_character_routes(app):
    app.register_blueprint(character_bp, url_prefix='/api')
