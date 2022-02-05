import yaml
from random import uniform, randint

with open("yaml/settings.yaml", encoding="UTF-8") as f:
    data = yaml.safe_load(f.read())

with open("yaml/locale.yaml", encoding="UTF-8") as f:
    locale = yaml.safe_load(f.read())


class Game:
    def __init__(self):
        global rock, paper, scissors
        rock = Kanobu("rock")
        paper = Kanobu("paper")
        scissors = Kanobu("scissors")
        self.playerchoice = 0
        self.botchoice = 0

    def menu(self):
        while True:
            print("""
  _                         _                     
 | | __ __ _  _ __    ___  | |__   _   _ 
 | |/ // _` || '_ \  / _ \ | '_ \ | | | |
 |   <| (_| || | | || (_) || |_) || |_| |
 |_|\_ \__,_||_| |_| \___/ |_.__/  \__,_|
      ___  ___   ___        ___ 
     | _ \| _ \ / __| __ __|_  )
     |   /|  _/| (_ | \ V / / / 
     |_|_\|_|   \___|  \_/ /___|.0.0
            """)
            print(locale["menu"])
            choice = input(">>> ")

            if choice in ("1", "2", "3"):
                game.menu_choice(int(choice))
                
            break

    def menu_choice(self, choice: int):
        if choice == 1:
            game.battle()
        if choice == 2:
            game.check_kanobu()
        if choice == 3:
            game.settings()

    def settings(self):
        while True:
            print()
            print(locale["settings"])

            choice = input(">>> ")
            if choice in ["1"]:
                if int(choice) == 1:
                    game.regenerate_team()
            else:
                break

    def check_kanobu(self):
        list = [rock, paper, scissors]
        for x in list:
            if x.health <= 0:
                x.health = 0
                status_ = "[МЕРТВ] "
            else:
                status_ = ""
            print(locale["check"].format(
                status=status_,
                name=x.name,
                max_health=x.maxhealth,
                health=x.health,
                min_attack=x.minattack,
                max_attack=x.maxattack,
                defence=x.defence,
                level=x.level,
                levelup_exp=x.levelup_exp,
                exp=round(x.exp, 1)
            ))

    def init_enemy(self):
        global rock_enemy, paper_enemy, scissors_enemy

        rock_enemy = Kanobu("rock")
        paper_enemy = Kanobu("paper")
        scissors_enemy = Kanobu("scissors")

    def battle(self):
        self.init_enemy()
        items = [rock, scissors, paper]

        botitems = [rock_enemy, scissors_enemy, paper_enemy]
        teamlevel = rock.level + paper.level + scissors.level
        botlevel = rock_enemy.level + paper_enemy.level + scissors_enemy.level

        print(locale["battle"]["started"].format(
            team_level=teamlevel,
            bot_level=botlevel)
        )

        while True:
            for item in botitems:
                if item.health <= 0:
                    botitems.remove(item)

            # начало боя и вывод текста
            print(locale["battle"]["choice_text"])
            for i, item in enumerate(items, start=1):
                print(locale["battle"]["choice_element"].format(
                    i=i,
                    player=item.name,
                    health=item.health)
                )

            # выбор игрокв
            if len(items) == 0:
                self.lose()
                break

            while True:
                choice = input(">>> ")
                if int(choice)-1 in range(len(items)):
                    self.playerchoice = items[int(choice) - 1]
                    break

            # выбор бота
            if len(botitems) == 0:
                self.win()
                break

            try:
                self.botchoice = botitems[randint(0, len(botitems)-1)]
            except:
                self.win()
                break

            print(f"{self.playerchoice.name} | {self.botchoice.name}")
            self.step("attack")

            if len(botitems) == 1 and self.botchoice.health <= 0:
                self.win()
                break

            self.step("defence")
            try:
                for i in items:
                    if i.health <= 0:
                        items.remove(i)
            except:
                self.lose()

    def checkweakness(self, turn):
        weakness = [
            [rock, scissors],
            [scissors, paper],
            [paper, rock]
        ]

        for item in weakness:
            if turn == "player":
                if item == [self.botchoice.type, self.playerchoice.type]:
                    print(locale["battle"]["not_effective"])
                    return 0.6
                else:
                    return 1
            elif turn == "bot":
                if item == [self.playerchoice.type, self.botchoice.type]:
                    return 0.6
                else:
                    return 1

    def step(self, action):
        if action == "attack":
            source_damage = randint(self.playerchoice.minattack,
                                    self.playerchoice.maxattack)

            damage = source_damage * self.checkweakness("player") - self.botchoice.defence

            if damage <= 0:
                damage = 1

            self.botchoice.health -= damage

            print(locale["battle"]["damage"].format(damage=damage))

            if self.botchoice.health <= 0:
                exp = ((4 + 1.3 * (self.playerchoice.level * 0.7) + (0.7 * randint(1, 5))) * uniform(0.8, 1.5)) * 0.9

                self.playerchoice.exp += exp

                print(locale["level"]["get_exp"].format(
                    player=self.playerchoice.name,
                    exp=round(exp, 1))
                )

        elif action == "defence":
            source_damage = randint(self.botchoice.minattack,
                                    self.botchoice.maxattack)

            damage = source_damage * self.checkweakness("bot") - self.playerchoice.defence
            if damage <= 0:
                damage = 1
            self.playerchoice.health -= damage
            print(locale["battle"]["attack"].format(
                player_choice=self.playerchoice.name.lower(),
                damage=damage
            ))

    def win(self):
        items = [rock, scissors, paper]
        print("\n\033[32mПобеда!\033[0m")
        print("Получено опыта:")
        for i in items:
            exp = i.exp * data["modifications"]["expirience"]["win"]
            print("  " + locale["level"]["get_exp_win"].format(
                player=i.name,
                exp=round(exp - i.exp, 1),
                old_exp=round(i.exp, 1),
                new_exp=round(exp, 1))
            )
        for i in items:
            i.level_up()

    def lose(self):
        items = [rock, scissors, paper]
        print("\n\033[31mПоражение...\033[0m")
        print("Потеряно опыта:")
        for i in items:
            exp = i.exp * data["modifications"]["expirience"]["lose"]
            print("  " + locale["level"]["lose_exp"].format(
                player=i.name,
                exp=round(exp - i.exp, 1),
                old_exp=round(i.exp, 1),
                new_exp=round(exp, 1))
            )
            i.level_up()

    def regenerate_team(self):
        items = [rock, paper, scissors]
        for x in items:
            x.health = x.maxhealth
        print(locale["health"])


class Kanobu:
    def __init__(self, kanobu):
        self.type = kanobu
        self.name = locale["kanobu"][kanobu]
        self.init_stats()

    def init_stats(self):
        self.maxhealth = data["stats"][self.type]["health"]
        self.health = self.maxhealth
        self.minattack = data["stats"][self.type]["damage"]["min"]
        self.maxattack = data["stats"][self.type]["damage"]["max"]
        self.defence = data["stats"][self.type]["defence"]
        self.level = 1
        self.exp = 0
        self.levelup_exp = data["stats"][self.type]["levelup_exp"]

    def level_up(self):
        while True:
            if self.exp >= self.levelup_exp:
                self.exp -= self.levelup_exp
                self.level += 1

                statsup = data["modifications"]["statsup"]

                health_up = randint(statsup["health"]["min"],
                                    statsup["health"]["max"])

                minattack_up = randint(statsup["attack"]["min"],
                                       statsup["attack"]["max"])

                maxattack_up = randint(statsup["attack"]["min"],
                                       statsup["attack"]["max"])

                defence_up = randint(statsup["defence"]["min"],
                                     statsup["defence"]["max"])

                levelexp_up = randint(statsup["exp"]["min"],
                                      statsup["exp"]["max"])

                self.maxhealth += health_up
                self.minattack += minattack_up
                self.maxattack += maxattack_up
                self.defence += defence_up
                self.levelup_exp += levelexp_up

                print(locale["stats"]["level_up"].format(
                    player=self.name,
                    level=self.level)
                )

                print(locale["stats"]["health"].format(
                    health=self.maxhealth - health_up,
                    new_health=self.maxhealth)
                )

                print(locale["stats"]["min_attack"].format(
                    min_attack=self.minattack - minattack_up,
                    new_min_attack=self.minattack)
                )

                print(locale["stats"]["max_attack"].format(
                    max_attack=self.maxattack - maxattack_up,
                    new_max_attack=self.maxattack)
                )

                print(locale["stats"]["defence"].format(
                    defence=self.defence - defence_up,
                    new_defence=self.defence)
                )

                print(locale["stats"]["exp"].format(
                    level=self.level+1,
                    exp=self.levelup_exp - levelexp_up,
                    new_exp=self.levelup_exp)
                )

                if self.minattack > self.maxattack:
                    self.minattack = self.maxattack
            else:
                break


game = Game()

while True:
    game.menu()
