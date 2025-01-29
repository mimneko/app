import json

class Species:
    """
    ポケモンの種族を表すクラス。
    """
    def __init__(self, name, dex_number, base_stats, learnable_moves, abilities):
        self.name = name
        self.dex_number = dex_number
        self.base_stats = base_stats
        self.learnable_moves = learnable_moves
        self.abilities = abilities


class Individual:
    """
    ポケモンの個体を表すクラス。
    """
    def __init__(self, species, ability, nature, ivs=None, evs=None, moves=None, level=50, item=None):
        """
        :param species: Species オブジェクト
        :param ability: 実際の特性 (str)
        :param nature: 性格の辞書 (dict: {"up": str, "down": str})
        :param ivs: 個体値の辞書
        :param evs: 努力値の辞書
        :param moves: 覚えている技のリスト
        :param level: レベル (int)
        :param item: 持ち物 (str)
        """
        self.species = species
        self.ability = ability
        if self.ability not in self.species.abilities:
            raise ValueError(f"{self.ability}は{self.species.name}の特性候補ではありません。")
        self.nature = nature
        self.ivs = ivs if ivs else {"h": 0, "a": 0, "b": 0, "c": 0, "d": 0, "s": 0}
        self.evs = evs if evs else {"h": 0, "a": 0, "b": 0, "c": 0, "d": 0, "s": 0}
        self.moves = moves if moves else []
        self.level = level
        self.item = item
        self.actual_stats = self.calculate_stats()

    def calculate_stats(self):
        """
        実数値を計算する。
        :return: 実数値の辞書 (dict: {"h": int, "a": int, "b": int, "c": int, "d": int, "s": int})
        """
        actual_stats = {}
        base = self.species.base_stats
        nature_up = self.nature["up"]
        nature_down = self.nature["down"]

        for stat in ["h", "a", "b", "c", "d", "s"]:
            if stat == "h":
                actual_stats[stat] = ((base[stat] * 2 + self.ivs[stat] + self.evs[stat] // 4) * self.level) // 100 + self.level + 10
            else:
                stat_value = ((base[stat] * 2 + self.ivs[stat] + self.evs[stat] // 4) * self.level) // 100 + 5
                if stat == nature_up:
                    stat_value = int(stat_value * 1.1)
                elif stat == nature_down:
                    stat_value = int(stat_value * 0.9)
                actual_stats[stat] = stat_value

        return actual_stats

    def learn_move(self, move):
        """
        技を覚える処理。
        :param move: 技名 (str)
        """
        if move in self.species.learnable_moves:
            if len(self.moves) < 4:
                self.moves.append(move)
            else:
                print(f"{self.species.name}は技を4つ覚えています！ 技を忘れさせてから追加してください。")
        else:
            print(f"{self.species.name}は{move}を覚えることができません。")


# JSONファイルからポケモンの種族を読み込む
def load_species_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {species['name']: Species(**species) for species in data['species']}


# 使用例
species = load_species_from_json('species.json')

tapu_lele = Individual(
    species=species["カプ・テテフ"],
    ability="サイコメイカー",
    nature={"up": "c", "down": "a"},  # 性格: ひかえめ (特攻↑ 攻撃↓)
    ivs={"h": 31, "a": 0, "b": 31, "c": 31, "d": 31, "s": 31},
    evs={"h": 0, "a": 0, "b": 4, "c": 252, "d": 0, "s": 252},
    moves=["サイコキネシス", "ムーンフォース", "シャドーボール", "10まんボルト"],
    level=50,
    item="こだわりスカーフ"
)

mimikyu = Individual(
    species=species["ミミッキュ"],
    ability="ばけのかわ",
    nature={"up": "a", "down": "c"},  # 性格: いじっぱり (攻撃↑ 特攻↓)
    ivs={"h": 31, "a": 31, "b": 31, "c": 0, "d": 31, "s": 31},
    evs={"h": 4, "a": 252, "b": 0, "c": 0, "d": 0, "s": 252},
    moves=["じゃれつく", "シャドークロー", "かげうち", "つるぎのまい"],
    level=50,
    item="フェアリーZ"
)

garchomp = Individual(
    species=species["ガブリアス"],
    ability="さめはだ",
    nature={"up": "s", "down": "c"},  # 性格: ようき (素早さ↑ 特攻↓)
    ivs={"h": 31, "a": 31, "b": 31, "c": 0, "d": 31, "s": 31},
    evs={"h": 0, "a": 252, "b": 0, "c": 0, "d": 4, "s": 252},
    moves=["じしん", "げきりん", "つるぎのまい", "がんせきふうじ"],
    level=50,
    item="きあいのタスキ"
)

# 出力例
pokemons = [tapu_lele, mimikyu, garchomp]
print("-" * 30)
for pokemon in pokemons:
    print(f"ポケモン名: {pokemon.species.name}")
    print(f"持ち物: {pokemon.item}")
    print(f"特性: {pokemon.ability}")
    print(f"実数値: {pokemon.actual_stats}")
    print(f"覚えている技: {pokemon.moves}")
    print("-" * 30)