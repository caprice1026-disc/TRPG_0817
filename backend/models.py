from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# PlayerとItemの多対多のリレーションを定義
player_items = db.Table('player_items',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    dexerity = db.Column(db.Integer, default=10)
    vitality = db.Column(db.Integer, default=10)
    luck = db.Column(db.Integer, default=10)
    gold = db.Column(db.Integer, default=0)
    items = db.relationship('Item', secondary=player_items, backref=db.backref('players', lazy='dynamic'))
    
    def level_up(self):
        """レベルアップとステータスの更新、経験値リセット"""
        self.level += 1
        self.strength += 2
        self.agility += 2
        self.intelligence += 2
        self.charisma += 2
        self.dexerity += 2
        self.vitality += 2
        self.luck += 2
        self.health_points += 20
        self.mana_points += 10
        self.experience = 0  # Reset experience for new level
        db.session.commit()
    
    def __repr__(self):
        return f"<Player {self.name} (Level: {self.level})>"
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    weight = db.Column(db.Float, default=0.0)
    value = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Item {self.name} (Value: {self.value})>"


