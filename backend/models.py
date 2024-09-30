from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

# Worldクラスの定義
class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    chaos_level = db.Column(db.Integer, default=0)
    description = db.Column(db.String(200))
    setting = db.Column(db.String(200))

# Itemクラスの定義
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    value = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Item {self.name} (UUID: {self.uuid})>"

# PlayerとItemの多対多のリレーションを定義
player_items = db.Table('player_items',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

# Playerクラスの定義
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    character_class = db.Column(db.String(50), nullable=False)
    back_story = db.Column(db.String(500), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    health_points = db.Column(db.Integer, default=100)
    mana_points = db.Column(db.Integer, default=50)
    strength = db.Column(db.Integer, default=10)
    agility = db.Column(db.Integer, default=10)
    intelligence = db.Column(db.Integer, default=10)
    charisma = db.Column(db.Integer, default=10)
    dexterity = db.Column(db.Integer, default=10)
    vitality = db.Column(db.Integer, default=10)
    luck = db.Column(db.Integer, default=10)
    gold = db.Column(db.Integer, default=0)
    world_uuid = db.Column(db.String(36), db.ForeignKey('world.uuid'))
    world = db.relationship('World', backref=db.backref('players', lazy=True))
    items = db.relationship('Item', secondary='player_items', backref=db.backref('players', lazy='dynamic'))

    def level_up(self):
        """レベルアップとステータスの更新、経験値リセット"""
        self.level += 1
        self.strength += 2
        self.agility += 2
        self.intelligence += 2
        self.charisma += 2
        self.dexterity += 2
        self.vitality += 2
        self.luck += 2
        self.experience = 0  # 経験値をリセット

    def take_damage(self, damage):
        """ダメージを受けた際にプレイヤーのHPを減少させる"""
        self.health_points -= damage
        if self.health_points <= 0:
            self.health_points = 0  # プレイヤーのHPが0以下にならないようにする
            # プレイヤーが死亡した場合の処理をここに追加

    def restore_health(self, amount):
        """プレイヤーのHPを回復させる"""
        self.health_points += amount
        if self.health_points > 100:  # 最大HPを100と仮定
            self.health_points = 100

    def __repr__(self):
        """プレイヤーの情報を文字列で返す"""
        return f"<Player {self.name} (UUID: {self.uuid})>"

    def add_item(self, item):
        """プレイヤーのアイテムを追加する"""
        self.items.append(item)

    def remove_item(self, item):
        """プレイヤーのインベントリからアイテムを削除"""
        if item in self.items:
            self.items.remove(item)