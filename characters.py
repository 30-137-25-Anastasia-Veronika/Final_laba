import random


# ==================== КЛАСС ИГРОКА ====================
class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.current_location = "вход"
        self.progress = 0
        self.artifacts = []
        self.hp = 100
        self.energy = 100

    def save_to_dict(self):
        """Создает словарь для сохранения данных игрока"""
        artifacts_data = []
        for artifact in self.artifacts:
            artifacts_data.append({
                "name": artifact.name,
                "power": artifact.power,
                "description": artifact.description,
                "max_uses": artifact.max_uses,
                "current_uses": artifact.current_uses
            })

        return {
            "username": self.username,
            "current_location": self.current_location,
            "progress": self.progress,
            "artifacts": artifacts_data,
            "hp": self.hp,
            "energy": self.energy
        }

    def load_from_dict(self, data, vault):
        """Загружает данные игрока из словаря"""
        self.current_location = data["current_location"]
        self.progress = data["progress"]
        self.hp = data["hp"]
        self.energy = data["energy"]

        # Загружаем артефакты
        self.artifacts = []
        for art_data in data["artifacts"]:
            artifact = vault.get_artifact_by_name(art_data["name"])
            if artifact:
                artifact.current_uses = art_data["current_uses"]
                self.artifacts.append(artifact)

    def add_artifact(self, artifact):
        """Добавляет артефакт игроку"""
        self.artifacts.append(artifact)
        print(f"Ты получил артефакт: {artifact}")

    def show_artifacts(self):
        """Показывает артефакты игрока"""
        if not self.artifacts:
            print("У тебя пока нет артефактов.")
            return

        print("\nТвои артефакты:")
        for i, artifact in enumerate(self.artifacts, 1):
            print(f"{i}. {artifact}")

    def has_artifact(self, artifact_name):
        """Проверяет, есть ли у игрока артефакт"""
        for artifact in self.artifacts:
            if artifact.name == artifact_name:
                return True
        return False

    def __str__(self):
        return f"Игрок: {self.username}, Прогресс: {self.progress}%, HP: {self.hp}, Энергия: {self.energy}"


# ==================== КЛАСС АРТЕФАКТА ====================
class Artifact:
    def __init__(self, name, power, description, max_uses=-1):
        self.name = name
        self.power = power
        self.description = description
        self.max_uses = max_uses  # -1 означает бесконечное использование
        self.current_uses = max_uses if max_uses > 0 else -1

    def use(self):
        """Использует артефакт, возвращает True если можно использовать дальше"""
        if self.max_uses > 0:
            if self.current_uses > 0:
                self.current_uses -= 1
                return True
            return False
        return True

    def can_use(self):
        """Проверяет, можно ли использовать артефакт"""
        return self.max_uses == -1 or self.current_uses > 0

    def __str__(self):
        if self.max_uses > 0:
            return f"{self.name} (+{self.power}): {self.description} (осталось: {self.current_uses})"
        return f"{self.name} (+{self.power}): {self.description}"


# ==================== КЛАСС СТУДЕНТА ====================
class Student:
    def __init__(self, name, role, hp=100, energy=50):
        self.name = name
        self.role = role
        self.hp = hp
        self.energy = energy
        self.alive = True
        self.artifacts = []
        self.special_used = False

    def get_total_attack_bonus(self):
        """Вычисляет общий бонус от артефактов"""
        bonus = 0
        for artifact in self.artifacts:
            # Только артефакты с именем "Милость" дают постоянный бонус
            if "Милость" in artifact.name:
                bonus += artifact.power
        return bonus

    def attack(self, enemy):
        """Обычная атака"""
        if self.energy >= 10:
            base_damage = random.randint(10, 20)
            bonus = self.get_total_attack_bonus()
            damage = base_damage + bonus
            enemy.hp -= damage
            self.energy -= 10
            return f"{self.name} атакует {enemy.name}! {damage} урона! (+{bonus} от артефактов)"
        else:
            self.energy += 5
            return f"{self.name} устал и отдыхает... +5 энергии"

    def special_attack(self, enemy):
        """Специальная атака"""
        if self.energy >= 25:
            base_damage = random.randint(30, 40)
            bonus = self.get_total_attack_bonus() * 2
            damage = base_damage + bonus
            enemy.hp -= damage
            self.energy -= 25

            if self.role == "Технарь":
                return f"{self.name} кидает клавиатурой! {damage} урона!"
            elif self.role == "Спортсмен":
                return f"{self.name} метает тапок! {damage} урона!"
            elif self.role == "Гуманитарий":
                return f"{self.name} читает скучную лекцию! {damage} урона!"
            else:
                return f"{self.name} использует супер-атаку! {damage} урона!"
        else:
            return "Недостаточно энергии!"

    def drink_energy(self):
        """Выпить энергетик"""
        self.energy += 20
        self.hp += 10
        if self.hp > 150:  # Максимальное HP
            self.hp = 150
        return f"{self.name} пьет энергетик! +20 энергии, +10 HP"

    def use_artifact(self, artifact, enemy=None):
        """Использовать артефакт"""
        if artifact.can_use():
            if artifact.use():
                if "Тапок" in artifact.name:
                    enemy.hp -= artifact.power
                    return f"{self.name} кидает {artifact.name} в {enemy.name}! {-artifact.power} HP"
                elif "Ракетка" in artifact.name:
                    enemy.hp -= artifact.power
                    return f"{self.name} бьёт {artifact.name} по {enemy.name}! {-artifact.power} HP"
                elif "Кружка" in artifact.name:
                    self.hp += artifact.power
                    return f"{self.name} пьёт из {artifact.name}! +{artifact.power} HP"
                elif "Энергетик" in artifact.name:
                    self.energy += artifact.power
                    return f"{self.name} пьёт {artifact.name}! +{artifact.power} энергии"
                else:
                    # Для других артефактов (Милость и т.д.)
                    return f"{self.name} использует {artifact.name}! Эффект активен."
            else:
                return f"{artifact.name} израсходован!"
        return f"{artifact.name} нельзя использовать!"

    def check_status(self):
        """Проверяет статус студента"""
        if self.hp <= 0:
            self.alive = False
            return f"{self.name} пал в бою..."

        artifact_info = ""
        if self.artifacts:
            artifact_info = f", Артефакты: {len(self.artifacts)}"
            for art in self.artifacts:
                if "Милость" in art.name:
                    artifact_info += f" [+{art.power}]"

        return f"{self.name} ({self.role}): HP={self.hp}, Энергия={self.energy}{artifact_info}"

    def __str__(self):
        return f"{self.name} ({self.role})"


# ==================== СПЕЦИАЛЬНЫЕ ПЕРСОНАЖИ ====================
class Nika(Student):
    def __init__(self):
        super().__init__("Ника", "житель 2209", 90, 60)
        self.drank_potion = False

    def special_attack(self, enemy):
        if not self.special_used and self.energy >= 30:
            self.energy -= 30
            self.special_used = True

            if not self.drank_potion:
                self.hp += 100
                self.drank_potion = True
                return f"{self.name} выпила 'Деревеньку'! +100 HP!"
            else:
                self.hp = 0
                self.alive = False
                return f"{self.name} выпила вторую 'Деревеньку'... выбывает из боя!"
        return "Недостаточно энергии или способность уже использована!"


class Nastya(Student):
    def __init__(self):
        super().__init__("Настя", "житель 2209", 110, 40)
        self.rag_used = False

    def special_attack(self, enemy):
        if not self.rag_used and self.energy >= 40:
            self.energy -= 40
            self.rag_used = True
            enemy.hp = 0
            enemy.alive = False
            return f"{self.name} ударила тряпкой! {enemy.name} уничтожен!"
        return "Недостаточно энергии или способность уже использована!"


class Masha(Student):
    def __init__(self):
        super().__init__("Маша", "житель 2209", 100, 50)

    def special_attack(self, allies):
        if self.energy >= 25:
            self.energy -= 25
            for ally in allies:
                if ally.alive:
                    ally.hp += 25
                    if ally.hp > 150:
                        ally.hp = 150
            return f"{self.name} играет на саксофоне! Все союзники получают +25 HP!"
        return "Недостаточно энергии!"


class Alexander(Student):
    def __init__(self):
        super().__init__("Александр", "Легенда инноватики", 80, 70)

    def special_attack(self, enemies):
        if self.energy >= 35:
            self.energy -= 35
            damage = random.randint(20, 30)
            for enemy in enemies:
                if enemy.alive:
                    enemy.hp -= damage
            return f"{self.name} решает интеграл! Все тараканы теряют {-damage} HP от сложности!"
        return "Недостаточно энергии!"

    def delivery_attack(self, enemy):
        if self.energy >= 15:
            damage = random.randint(15, 25)
            enemy.hp -= damage
            self.energy -= 15
            return f"{self.name} кидает доширак! {damage} урона!"
        return "Недостаточно энергии!"


class Andrey(Student):
    def __init__(self):
        super().__init__("Андрей", "Человек-удача", 150, 30)

    def special_attack(self, enemy):
        if self.energy >= 50:
            self.energy -= 50
            if random.random() > 0.5:  # 50% шанс на успех
                damage = 50
                enemy.hp -= damage
                return f"{self.name} удачно бьёт! {damage} урона!"
            else:
                self.hp -= 20
                return f"{self.name} промахивается и падает! -20 HP"
        return "Недостаточно энергии!"


class Zakhar(Student):
    def __init__(self):
        super().__init__("Захар", "Житель 2519", 70, 80)

    def special_attack(self, enemy):
        if self.energy >= 20:
            damage = random.randint(15, 25) * 2  # Двойной урон от интеллекта
            enemy.hp -= damage
            self.energy -= 20
            return f"{self.name} использует знания! {damage} урона!"
        return "Недостаточно энергии!"


class Timur(Student):
    def __init__(self):
        super().__init__("Тимур", "Житель 2519", 140, 40)

    def special_attack(self, enemy):
        if self.energy >= 30:
            damage = random.randint(35, 45)
            enemy.hp -= damage
            self.energy -= 30
            return f"{self.name} бьёт со всей силы! {damage} урона!"
        return "Недостаточно энергии!"


class Barisbiy(Student):
    def __init__(self):
        super().__init__("Барисбий", "Житель 2519", 100, 60)

    def special_attack(self, enemy):
        if self.energy >= 25:
            damage = random.randint(25, 35)
            enemy.hp -= damage
            self.energy -= 25
            return f"{self.name} очаровывает и бьёт! {damage} урона!"
        return "Недостаточно энергии!"


# ==================== КЛАССЫ ТАРАКАНОВ ====================
class Cockroach:
    def __init__(self, name, hp=60):
        self.name = name
        self.hp = hp
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


class CockroachIntellectual(Cockroach):
    def __init__(self):
        super().__init__("Таракан-интеллектуал", 75)
        self.questions = [
            ("Как зовут героя общаги Икар, который случайно зашёл в душ к девочкам?", "Клим"),
            (
            "Почему самолёт летает?\n1. Потому что так сказали на ВАРКТе\n2. Потому что в самолёте всегда есть тот самый человек, который молится богу\n3. Потому что молекулы воздуха толкают крылышки самолёта и тот не падает",
            "3"),
            ("Как зовут преподавателя информатики на инноватике (ФИО)?", "Александрова Светлана Сергеевна")
        ]


class CockroachQueen:
    def __init__(self):
        self.name = "КОРОЛЕВА ТАРАКАНОВ"
        self.hp = 200
        self.alive = True
        self.phase = 1

    def attack(self, students):
        alive_students = [s for s in students if s.alive]
        if not alive_students:
            return "Нет целей для атаки!"

        if self.phase == 1:
            damage = random.randint(15, 25)
            target = random.choice(alive_students)
            target.hp -= damage
            return f"{self.name} атакует {target.name}! {-damage} HP"
        else:
            damage = random.randint(20, 35)
            for student in alive_students:
                student.hp -= damage // 2
            return f"{self.name} В ЯРОСТИ! Атакует всех! Каждый теряет {-damage // 2} HP"

    def check_status(self):
        if self.hp <= 100 and self.phase == 1:
            self.phase = 2
            return "Королева впадает в ярость! Она стала сильнее!"
        if self.hp <= 0:
            self.alive = False
            return "КОРОЛЕВА ТАРАКАНОВ ПОБЕЖДЕНА!"
        return f"{self.name}: HP={self.hp} (Фаза {self.phase})"


# ==================== КОПИЛКА АРТЕФАКТОВ ====================
class ArtifactVault:
    def __init__(self):
        self.all_artifacts = self.load_artifacts()

    def load_artifacts(self):
        artifacts = [
            Artifact("Тапок Барисбия", 50, "Однократный супер-удар по таракану", 1),
            Artifact("Теннисная ракетка Маши", 30, "Мощный удар ракеткой", 3),
            Artifact("Милость Ольги Васильевны", 25, "Постоянный бонус к силе"),
            Artifact("Кружка 2205", 10, "Восстанавливает 10 HP каждый ход"),
            Artifact("Браслет Тимура", 20, "Защита от атак тараканов"),
        ]
        return artifacts

    def get_artifact_by_name(self, name):
        for artifact in self.all_artifacts:
            if artifact.name == name:
                # Создаем новый экземпляр артефакта
                return Artifact(artifact.name, artifact.power,
                                artifact.description, artifact.max_uses)
        return None

    def create_new_artifacts(self):
        """Создает новые артефакты, если все были собраны"""
        self.all_artifacts = self.load_artifacts()
        print("В копилке появились новые артефакты!")