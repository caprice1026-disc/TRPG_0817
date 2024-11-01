from swarm import Swarm, Agent

client = Swarm()

# 英語エージェントの設定
trpg_agent = Agent(
    name="TRPG Agent",
    instructions="あなたはTRPGのGMを務めるエージェントです。",
)

# 日本語エージェントの設定
combat_agent = Agent(
    name="Combat Agent",
    instructions="あなたはTRPGの戦闘部分を担当するエージェントです。",
)

def transfer_to_combat_agent():
    """TRPG 内での戦闘エージェントにメッセージを転送する関数"""
    return combat_agent

# 英語エージェントに関数を追加
trpg_agent.functions.append(transfer_to_combat_agent)

# メッセージの設定と実行
messages = [{"role": "user", "content": "わたしは魔法使いです。山の中でゴブリンを見かけたため、即死魔法を撃ちました。"}]
response = client.run(agent=trpg_agent, messages=messages)

# 応答の出力
print(response.messages[-1]["content"])