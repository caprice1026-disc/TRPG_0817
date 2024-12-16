れどみというかメモ

メモ:フロントエンド側の情報保持はUsestateを使用。バックエンド側でSSEで変更を投げるようにしたい

参考文献（これを読んでswarmの理解を深める）

https://zenn.dev/dalab/articles/1d4f649c8005a0

https://qiita.com/Maki-HamarukiLab/items/addeffc7ade848a4807a

## エージェント

```mermaid
    flowchart TD

    %% エージェント定義
    U[ユーザー]
    GM_IN[ゲームマスターエージェント(入力)]
    BA[戦闘エージェント]
    CA[キャラ管理エージェント]
    IA[アイテム管理エージェント]
    WA[ワールド管理エージェント]
    GM_OUT[ゲームマスターエージェント(出力)]
    OUT[出力]

    %% 流れ定義
    U --> GM_IN

    GM_IN --> BA
    GM_IN --> CA
    GM_IN --> IA
    GM_IN --> WA

    BA --> GM_OUT
    CA --> GM_OUT
    IA --> GM_OUT
    WA --> GM_OUT

    GM_OUT --> OUT
```


TRPGを実装するために、以下のエージェントを実装

1. **ゲームマスターエージェント（GMエージェント）**
   - プレイヤーの行動に応じてストーリーを進行し、シナリオを管理する。

2. **戦闘エージェント**
   - 戦闘の処理を担当し、ダメージ計算や結果の判定を行う。

3. **キャラクター管理エージェント**
   - キャラクターの作成、レベルアップ、ステータス更新を行う。

4. **アイテム管理エージェント**
   - アイテムの追加・削除やインベントリの管理を行う。

5. **ワールドエージェント**
   - ゲーム内の世界や環境、イベントを管理する。

6. **NPCエージェント**
   - 非プレイヤーキャラクターの行動や会話を制御する。

これらのエージェントを組み合わせて、TRPGのシステムを構築する予定。

## 進捗状況
まずは各エージェント同士のワークフローを確立し、基本的な機能を実装していく。