import random

def roll_d100():
    """1D100のダイスロールをシミュレートする"""
    return random.randint(1, 100)

def roll_3d6():
    """3D6のダイスロールをシミュレートする"""
    return sum(random.randint(1, 6) for _ in range(3))

def roll_2d6():
    """2D6のダイスをシミュレートする"""
    return sum(random.randint(1, 6) for _ in range(2))