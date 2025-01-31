from flask_sqlalchemy import SQLAlchemy
import uuid


db = SQLAlchemy()

# Worldクラスの定義
class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # プライマリキーとして整数型
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # UUIDをセカンダリキーとして使用
    chaos_level = db.Column(db.Integer, default=0)  # カオス度 (0-100) 不確実性
    description = db.Column(db.String(200))  # 世界観の説明 (200文字以内)
    setting = db.Column(db.String(200))  # 舞台の説明 (200文字以内)

# Itemクラスの定義
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # プライマリキーとして整数型
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # UUIDをセカンダリキーとして使用
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
    id = db.Column(db.Integer, primary_key=True)  # プライマリキーとして整数型
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # UUIDをセカンダリキーとして使用
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
    dexterity = db.Column(db.Integer, default=10)  # タイポ修正
    vitality = db.Column(db.Integer, default=10)
    luck = db.Column(db.Integer, default=10)
    gold = db.Column(db.Integer, default=0)
    world_uuid = db.Column(db.String(36), db.ForeignKey('world.uuid'))  # UUIDを外部キーとして使用
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
        db.session.commit()

    def take_damage(self, damage):
        """ダメージを受けた際にプレイヤーのHPを減少させる"""
        self.health_points -= damage
        if self.health_points <= 0:
            self.health_points = 0  # プレイヤーのHPが0以下にならないようにする
            # プレイヤーが死亡した場合の処理を書く
        db.session.commit()

    def restore_health(self, amount):
        """プレイヤーのHPを回復させる"""
        self.health_points += amount
        if self.health_points > 100:  # HPの上限を100に設定
            self.health_points = 100
        db.session.commit()

    def __repr__(self):
        """プレイヤーの情報を文字列で返す"""
        return f"<Player {self.name} (UUID: {self.uuid})>"

    def add_item(self, item_name, description=""):
        """プレイヤーのアイテムを追加する"""
        existing_item = Item.query.filter_by(name=item_name).first()
        if not existing_item:
            new_item = Item(name=item_name, description=description)
            db.session.add(new_item)
            self.items.append(new_item)
        else:
            self.items.append(existing_item)
        db.session.commit()

    def remove_item(self, item):
        """プレイヤーのインベントリからアイテムを削除"""
        if item in self.items:
            self.items.remove(item)
            db.session.commit()