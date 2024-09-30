from models import db, Player, Item, World
from sqlalchemy.exc import SQLAlchemyError

# models由来のメソッドを確認しておくこと

class CharacterService:
    def create_character(self, name, character_class, back_story, world_uuid):
        """新しいキャラクターを作成する"""
        try:
            world = World.query.filter_by(uuid=world_uuid).first()
            if not world:
                return {"message": "World not found"}, 404

            new_player = Player(
                name=name,
                character_class=character_class,
                back_story=back_story,
                world_uuid=world_uuid
            )
            db.session.add(new_player)
            db.session.commit()
            return {"message": "Character created successfully", "player_uuid": new_player.uuid}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error creating character", "error": str(e)}, 500

    def get_all_characters(self):
        """すべてのキャラクターを取得する"""
        try:
            players = Player.query.all()
            characters = [{
                "uuid": player.uuid,
                "name": player.name,
                "character_class": player.character_class,
                "level": player.level
            } for player in players]
            return characters
        except SQLAlchemyError as e:
            return {"message": "Error fetching characters", "error": str(e)}, 500

    def get_character(self, player_uuid):
        """指定したUUIDのキャラクターを取得する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if player:
                character = {
                    "uuid": player.uuid,
                    "name": player.name,
                    "character_class": player.character_class,
                    "level": player.level,
                    "health_points": player.health_points
                }
                return character
            else:
                return None
        except SQLAlchemyError as e:
            return {"message": "Error fetching character", "error": str(e)}, 500

    def update_character(self, player_uuid, data):
        """キャラクター情報を更新する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            # 更新可能なフィールドを順次更新
            updatable_fields = ['name', 'character_class', 'back_story', 'level', 'experience',
                                'health_points', 'mana_points', 'strength', 'agility',
                                'intelligence', 'charisma', 'dexterity', 'vitality', 'luck', 'gold']

            for key in updatable_fields:
                if key in data:
                    setattr(player, key, data[key])

            db.session.commit()
            return {"message": "Character updated successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error updating character", "error": str(e)}, 500

    def delete_character(self, player_uuid):
        """キャラクターを削除する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            db.session.delete(player)
            db.session.commit()
            return {"message": "Character deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error deleting character", "error": str(e)}, 500

    def level_up_character(self, player_uuid):
        """キャラクターのレベルを上げる"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            player.level_up()  
            db.session.commit()
            return {"message": "Character leveled up successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error leveling up character", "error": str(e)}, 500

    def character_take_damage(self, player_uuid, damage):
        """キャラクターがダメージを受ける"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            player.take_damage(damage)  
            db.session.commit()
            return {"message": f"Character took {damage} damage"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error applying damage", "error": str(e)}, 500

    def restore_character_health(self, player_uuid, amount):
        """キャラクターのHPを回復する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            player.restore_health(amount)  
            db.session.commit()
            return {"message": f"Character restored {amount} health points"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error restoring health", "error": str(e)}, 500

    def add_item_to_character(self, player_uuid, item_name, description=""):
        """キャラクターにアイテムを追加する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            new_item = Item(name=item_name, description=description)
            db.session.add(new_item)
            player.add_item(new_item)  
            db.session.commit()
            return {"message": f"Item '{item_name}' added to character"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error adding item", "error": str(e)}, 500

    def remove_item_from_character(self, player_uuid, item_uuid):
        """キャラクターからアイテムを削除する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            item = Item.query.filter_by(uuid=item_uuid).first()

            if not player or not item:
                return {"message": "Character or Item not found"}, 404

            if item in player.items:
                player.remove_item(item)  
                db.session.commit()
                return {"message": f"Item '{item.name}' removed from character"}, 200
            else:
                return {"message": "Item not associated with character"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error removing item", "error": str(e)}, 500