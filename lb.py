import random


class Student:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.hp = 100
        self.energy = 50
        self.alive = True

    def attack(self, enemy):
        if self.energy >= 10:
            damage = random.randint(15, 25)
            enemy.hp -= damage
            self.energy -= 10
            return f"{self.name} бьет {enemy.name} и наносит {damage} урона!"
        else:
            self.energy += 5
            return f"{self.name} устал и отдыхает..."

    def special_attack(self, enemy):
        if self.energy >= 25:
            damage = random.randint(30, 40)
            enemy.hp -= damage
            self.energy -= 25

            if self.role == "Технарь":
                return f" {self.name} кидает клавиатурой! {damage} урона!"
            elif self.role == "Спортсмен":
                return f" {self.name} метает тапок! {damage} урона!"
            elif self.role == "Гуманитарий":
                return f" {self.name} читает скучную лекцию! {damage} урона!"
        else:
            return "Недостаточно энергии!"

    def drink_energy(self):
        self.energy += 20
        self.hp += 10
        return f"{self.name} пьет энергетик! +20 энергии, +10 HP"

    def check_status(self):
        if self.hp <= 0:
            self.alive = False
            return f"{self.name} пал в бою..."
        return f"{self.name}: HP={self.hp}, Energy={self.energy}"


class Cockroach:
    def __init__(self, name):
        self.name = name
        self.hp = random.randint(60, 80)
        self.alive = True

    def attack(self, student):
        damage = random.randint(10, 20)
        student.hp -= damage
        attacks = [
            f"{self.name} бегает по лицу {student.name}!",
            f"{self.name} ворует еду у {student.name}!",
            f"{self.name} пугает {student.name}!"
        ]
        return f"{random.choice(attacks)} {-damage} HP"

    def check_status(self):
        if self.hp <= 0:
            self.alive = False
            return f"{self.name} уничтожен!"
        return f"{self.name}: HP={self.hp}"


class CockroachQueen:
    def __init__(self):
        self.name = "Королева Тараканов"
        self.hp = 150
        self.alive = True
        self.phase = 1

    def attack(self, student):
        if self.phase == 1:
            damage = random.randint(15, 25)
            student.hp -= damage
            return f"{self.name} атакует {student.name}! {-damage} HP"
        else:
            damage = random.randint(20, 30)
            student.hp -= damage
            return f"{self.name} В ЯРОСТИ! {-damage} HP"

    def check_status(self):
        if self.hp <= 75 and self.phase == 1:
            self.phase = 2
            return "Королева впадает в ярость! Она стала сильнее!"

        if self.hp <= 0:
            self.alive = False
            return "КОРОЛЕВА ТАРАКАНОВ ПОБЕЖДЕНА!"

        return f" {self.name}: HP={self.hp} (Фаза {self.phase})"


class SimpleBattle:
    def __init__(self):
        self.students = [
            Student("Саша", "Технарь"),
            Student("Маша", "Гуманитарий"),
            Student("Коля", "Спортсмен")
        ]
        self.enemies = [
            Cockroach("Таракан-солдат"),
            Cockroach("Таракан-разведчик"),
            Cockroach("Таракан-мутант")
        ]
        self.boss = CockroachQueen()
        self.round = 1

    def show_status(self):
        print(f"\n{'=' * 40}")
        print(f"РАУНД {self.round}")
        print("Студенты:")
        for student in self.students:
            if student.alive:
                print(f" {student.check_status()}")

        print("\nТараканы:")
        for enemy in self.enemies:
            if enemy.alive:
                print(f"  {enemy.check_status()}")

        print(f"\nБОСС: {self.boss.check_status()}")

    def student_turn(self, student):
        if not student.alive:
            return

        print(f"\n--- Ходит {student.name} ({student.role}) ---")
        print("1 - Атака (-10 энергии)")
        print("2 - Супер-атака (-25 энергии)")
        print("3 - Выпить энергетик")
        print("4 - Пропустить ход")

        try:
            choice = input("Выбери действие: ")

            alive_enemies = [e for e in self.enemies if e.alive]
            target = None

            if choice == "1":
                if alive_enemies:
                    target = random.choice(alive_enemies)
                    print(student.attack(target))
                else:
                    print("Нет целей для атаки!")

            elif choice == "2":
                if alive_enemies:
                    target = random.choice(alive_enemies)
                    print(student.special_attack(target))
                else:
                    print("Нет целей для атаки!")

            elif choice == "3":
                print(student.drink_energy())

            elif choice == "4":
                print(f"{student.name} пропускает ход")

            else:
                print("Неверный выбор! Пропускаю ход...")

        except:
            print("Ошибка! Пропускаю ход...")

        if target:
            print(target.check_status())

    def enemy_turn(self):
        alive_students = [s for s in self.students if s.alive]
        if not alive_students:
            return

        for enemy in self.enemies:
            if enemy.alive and alive_students:
                target = random.choice(alive_students)
                print(f"\n{enemy.attack(target)}")
                print(target.check_status())

    def boss_turn(self):
        alive_students = [s for s in self.students if s.alive]
        if alive_students and self.boss.alive:
            target = random.choice(alive_students)
            print(f"\n{self.boss.attack(target)}")
            print(target.check_status())

    def check_win_condition(self):
        students_alive = any(s.alive for s in self.students)
        enemies_alive = any(e.alive for e in self.enemies)
        boss_alive = self.boss.alive

        if not students_alive:
            return "lose"

        if not enemies_alive and not boss_alive:
            return "win"

        return "continue"

    def start_battle(self):
        print("БИТВА ЗА ОБЩАГУ НАЧИНАЕТСЯ!")
        print("Студенты против тараканов!")

        while any(e.alive for e in self.enemies) and any(s.alive for s in self.students):
            self.show_status()

            for student in self.students:
                if student.alive:
                    self.student_turn(student)

                    if not any(e.alive for e in self.enemies):
                        break

            if any(e.alive for e in self.enemies):
                self.enemy_turn()

            self.round += 1

        if any(s.alive for s in self.students):
            print("\n" + "=" * 50)
            print("Все обычные тараканы побеждены!")
            print("Но появляется КОРОЛЕВА ТАРАКАНОВ!")
            input("Нажми Enter чтобы продолжить...")

            while self.boss.alive and any(s.alive for s in self.students):
                self.show_status()

                for student in self.students:
                    if student.alive:
                        print(f"\n--- Ходит {student.name} ---")
                        print("1 - Атаковать королеву (-10 энергии)")
                        print("2 - Супер-атака (-25 энергии)")
                        print("3 - Выпить энергетик")

                        try:
                            choice = input("Выбери действие: ")

                            if choice == "1":
                                print(student.attack(self.boss))
                            elif choice == "2":
                                print(student.special_attack(self.boss))
                            elif choice == "3":
                                print(student.drink_energy())
                            else:
                                print("Пропускаю ход...")
                        except:
                            print("Ошибка! Пропускаю ход...")

                        print(self.boss.check_status())

                        if not self.boss.alive:
                            break

                if self.boss.alive:
                    self.boss_turn()

                self.round += 1

        print("\n" + "=" * 50)
        if any(s.alive for s in self.students):
            print("ПОБЕДА! Студенты отстояли общагу!")
            print("Тараканы повержены! Можно спокойно готовиться к сессии!")
        else:
            print("ПОРАЖЕНИЕ... Тараканы захватили общагу!")
            print("Придется ночевать в библиотеке...")


if __name__ == "__main__":
    print("Добро пожаловать в ОБЩАЖНУЮ ДУЭЛЬ!")
    print("Студенты vs Тараканы - битва за выживание!")

    battle = SimpleBattle()
    battle.start_battle()

    input("\nНажми Enter чтобы выйти...")