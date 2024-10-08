from models import db, Player, Item, World
from sqlalchemy.exc import SQLAlchemyError

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

    def get_character(self, player_uuid):
        """指定したUUIDのキャラクターを取得する"""
        player = Player.query.filter_by(uuid=player_uuid).first()
        if player:
            return player
        else:
            return None

    def update_character(self, player_uuid, data):
        """キャラクター情報を更新する"""
        try:
            player = Player.query.filter_by(uuid=player_uuid).first()
            if not player:
                return {"message": "Character not found"}, 404

            # 更新可能なフィールドを順次更新
            for key, value in data.items():
                if hasattr(player, key):
                    setattr(player, key, value)

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

            player.level_up()  # models.pyで定義したメソッドを呼び出し
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

            player.take_damage(damage)  # models.pyで定義したメソッドを呼び出し
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

            player.restore_health(amount)  # models.pyで定義したメソッドを呼び出し
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
            player.items.append(new_item)
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
                player.items.remove(item)
                db.session.commit()
                return {"message": f"Item '{item.name}' removed from character"}, 200
            else:
                return {"message": "Item not associated with character"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Error removing item", "error": str(e)}, 500