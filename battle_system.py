import random
from characters import Student, Cockroach, CockroachQueen


class BattleSystem:
    def __init__(self):
        self.round = 1

    def simple_battle_3v3(self, students, cockroaches):
        """Битва 3 на 3 как в оригинальной игре"""
        print(f"\n{'=' * 50}")
        print(f"БИТВА НАЧИНАЕТСЯ!")
        print(f"{'=' * 50}")

        while any(s.alive for s in students) and any(c.alive for c in cockroaches):
            print(f"\n{'=' * 50}")
            print(f"РАУНД {self.round}")
            print(f"{'=' * 50}")

            # Показываем статусы
            print("\nСтуденты:")
            for student in students:
                if student.alive:
                    print(f"  {student.check_status()}")

            print("\nТараканы:")
            for cockroach in cockroaches:
                if cockroach.alive:
                    print(f"  {cockroach.check_status()}")

            # Ход студентов
            print(f"\n{'-' * 30}")
            print("ХОД СТУДЕНТОВ")
            print(f"{'-' * 30}")

            for student in students:
                if student.alive and any(c.alive for c in cockroaches):
                    self.student_turn(student, cockroaches)

            # Ход тараканов
            if any(c.alive for c in cockroaches):
                print(f"\n{'-' * 30}")
                print("ХОД ТАРАКАНОВ")
                print(f"{'-' * 30}")

                for cockroach in cockroaches:
                    if cockroach.alive and any(s.alive for s in students):
                        alive_students = [s for s in students if s.alive]
                        if alive_students:
                            target = random.choice(alive_students)
                            print(f"\n{cockroach.attack(target)}")
                            print(f"  {target.check_status()}")

            self.round += 1

        # Проверяем результат
        if any(s.alive for s in students):
            print(f"\n{'=' * 50}")
            print("ПОБЕДА! Студенты победили!")
            print(f"{'=' * 50}")
            return True
        else:
            print(f"\n{'=' * 50}")
            print("ПОРАЖЕНИЕ... Тараканы победили.")
            print(f"{'=' * 50}")
            return False

    def student_turn(self, student, enemies):
        """Ход одного студента"""
        print(f"\n--- Ходит {student.name} ({student.role}) ---")

        alive_enemies = [e for e in enemies if e.alive]
        if not alive_enemies:
            print("Нет целей для атаки!")
            return

        while True:
            print("\nВыбери действие:")
            print("1. Обычная атака (-10 энергии)")
            print("2. Супер-атака (-25 энергии)")
            print("3. Выпить энергетик")

            if student.artifacts:
                print("4. Использовать артефакт")
                print("5. Пропустить ход")
            else:
                print("4. Пропустить ход")

            choice = input("Твой выбор (1-5): ")

            if choice == "1":
                # Выбираем врага
                print("\nВыбери цель для атаки:")
                for i, enemy in enumerate(alive_enemies):
                    print(f"{i + 1}. {enemy.name} (HP: {enemy.hp})")

                try:
                    enemy_idx = int(input("Номер цели: ")) - 1
                    if 0 <= enemy_idx < len(alive_enemies):
                        print(f"\n{student.attack(alive_enemies[enemy_idx])}")
                    else:
                        print("Неверный выбор!")
                        continue
                except:
                    print("Ошибка ввода!")
                    continue
                break

            elif choice == "2":
                print("\nВыбери цель для супер-атаки:")
                for i, enemy in enumerate(alive_enemies):
                    print(f"{i + 1}. {enemy.name} (HP: {enemy.hp})")

                try:
                    enemy_idx = int(input("Номер цели: ")) - 1
                    if 0 <= enemy_idx < len(alive_enemies):
                        print(f"\n{student.special_attack(alive_enemies[enemy_idx])}")
                    else:
                        print("Неверный выбор!")
                        continue
                except:
                    print("Ошибка ввода!")
                    continue
                break

            elif choice == "3":
                print(f"\n{student.drink_energy()}")
                break

            elif choice == "4" and student.artifacts:
                print("\nТвои артефакты:")
                for i, artifact in enumerate(student.artifacts):
                    print(f"{i + 1}. {artifact}")

                try:
                    art_idx = int(input("Выбери артефакт: ")) - 1
                    if 0 <= art_idx < len(student.artifacts):
                        artifact = student.artifacts[art_idx]

                        # Выбираем цель для артефакта
                        if "Тапок" in artifact.name or "Ракетка" in artifact.name:
                            print("\nВыбери цель для артефакта:")
                            for i, enemy in enumerate(alive_enemies):
                                print(f"{i + 1}. {enemy.name} (HP: {enemy.hp})")

                            enemy_idx = int(input("Номер цели: ")) - 1
                            if 0 <= enemy_idx < len(alive_enemies):
                                print(f"\n{student.use_artifact(artifact, alive_enemies[enemy_idx])}")
                                # Удаляем израсходованный артефакт
                                if not artifact.can_use() and artifact.max_uses > 0:
                                    student.artifacts.pop(art_idx)
                            else:
                                print("Неверный выбор!")
                                continue
                        else:
                            print(f"\n{student.use_artifact(artifact)}")
                            # Удаляем израсходованный артефакт
                            if not artifact.can_use() and artifact.max_uses > 0:
                                student.artifacts.pop(art_idx)
                    else:
                        print("Неверный выбор!")
                        continue
                except:
                    print("Ошибка ввода!")
                    continue
                break

            elif choice == "5" or (choice == "4" and not student.artifacts):
                print(f"{student.name} пропускает ход")
                break

            else:
                print("Неверный выбор! Попробуй ещё раз.")

    def boss_battle(self, students, boss):
        """Битва с боссом"""
        print(f"\n{'=' * 50}")
        print(f"ФИНАЛЬНАЯ БИТВА С {boss.name}!")
        print(f"{'=' * 50}")

        self.round = 1

        while any(s.alive for s in students) and boss.alive:
            print(f"\n{'=' * 50}")
            print(f"РАУНД {self.round}")
            print(f"{'=' * 50}")

            # Показываем статусы
            print("\nСтуденты:")
            for student in students:
                if student.alive:
                    print(f"  {student.check_status()}")

            print(f"\nБОСС: {boss.check_status()}")

            # Ход студентов
            print(f"\n{'-' * 30}")
            print("ХОД СТУДЕНТОВ")
            print(f"{'-' * 30}")

            for student in students:
                if student.alive and boss.alive:
                    print(f"\n--- Ходит {student.name} ({student.role}) ---")

                    while True:
                        print("\nВыбери действие:")
                        print("1. Атаковать королеву (-10 энергии)")
                        print("2. Супер-атака (-25 энергии)")
                        print("3. Выпить энергетик")

                        if student.artifacts:
                            print("4. Использовать артефакт")
                            print("5. Пропустить ход")
                        else:
                            print("4. Пропустить ход")

                        choice = input("Твой выбор (1-5): ")

                        if choice == "1":
                            print(f"\n{student.attack(boss)}")
                            break

                        elif choice == "2":
                            print(f"\n{student.special_attack(boss)}")
                            break

                        elif choice == "3":
                            print(f"\n{student.drink_energy()}")
                            break

                        elif choice == "4" and student.artifacts:
                            print("\nТвои артефакты:")
                            for i, artifact in enumerate(student.artifacts):
                                print(f"{i + 1}. {artifact}")

                            try:
                                art_idx = int(input("Выбери артефакт: ")) - 1
                                if 0 <= art_idx < len(student.artifacts):
                                    artifact = student.artifacts[art_idx]
                                    print(f"\n{student.use_artifact(artifact, boss)}")

                                    # Удаляем израсходованный артефакт
                                    if not artifact.can_use() and artifact.max_uses > 0:
                                        student.artifacts.pop(art_idx)
                                else:
                                    print("Неверный выбор!")
                                    continue
                            except:
                                print("Ошибка ввода!")
                                continue
                            break

                        elif choice == "5" or (choice == "4" and not student.artifacts):
                            print(f"{student.name} пропускает ход")
                            break

                        else:
                            print("Неверный выбор! Попробуй ещё раз.")

            # Ход босса
            if boss.alive and any(s.alive for s in students):
                print(f"\n{'-' * 30}")
                print("ХОД КОРОЛЕВЫ")
                print(f"{'-' * 30}")

                print(f"\n{boss.attack(students)}")

                # Показываем урон студентам
                for student in students:
                    if student.alive:
                        print(f"  {student.check_status()}")

            self.round += 1

        # Результат битвы
        if any(s.alive for s in students):
            print(f"\n{'=' * 50}")
            print(f"ПОБЕДА! {boss.name} ПОВЕРЖЕНА!")
            print(f"{'=' * 50}")
            return True
        else:
            print(f"\n{'=' * 50}")
            print(f"ПОРАЖЕНИЕ... {boss.name} победила.")
            print(f"{'=' * 50}")
            return False

    def one_on_one_battle(self, student, cockroach):
        """Битва один на один"""
        print(f"\n{'=' * 50}")
        print(f"ДУЭЛЬ: {student.name} vs {cockroach.name}")
        print(f"{'=' * 50}")

        self.round = 1

        while student.alive and cockroach.alive:
            print(f"\n{'=' * 50}")
            print(f"РАУНД {self.round}")
            print(f"{'=' * 50}")

            print(f"\n{student.check_status()}")
            print(f"{cockroach.check_status()}")

            # Ход студента
            print(f"\n{'-' * 30}")
            print(f"ХОД {student.name}")
            print(f"{'-' * 30}")

            while True:
                print("\nВыбери действие:")
                print("1. Обычная атака (-10 энергии)")
                print("2. Супер-атака (-25 энергии)")
                print("3. Выпить энергетик")

                if student.artifacts:
                    print("4. Использовать артефакт")
                    print("5. Пропустить ход")
                else:
                    print("4. Пропустить ход")

                choice = input("Твой выбор (1-5): ")

                if choice == "1":
                    print(f"\n{student.attack(cockroach)}")
                    break

                elif choice == "2":
                    print(f"\n{student.special_attack(cockroach)}")
                    break

                elif choice == "3":
                    print(f"\n{student.drink_energy()}")
                    break

                elif choice == "4" and student.artifacts:
                    print("\nТвои артефакты:")
                    for i, artifact in enumerate(student.artifacts):
                        print(f"{i + 1}. {artifact}")

                    try:
                        art_idx = int(input("Выбери артефакт: ")) - 1
                        if 0 <= art_idx < len(student.artifacts):
                            artifact = student.artifacts[art_idx]
                            print(f"\n{student.use_artifact(artifact, cockroach)}")

                            # Удаляем израсходованный артефакт
                            if not artifact.can_use() and artifact.max_uses > 0:
                                student.artifacts.pop(art_idx)
                        else:
                            print("Неверный выбор!")
                            continue
                    except:
                        print("Ошибка ввода!")
                        continue
                    break

                elif choice == "5" or (choice == "4" and not student.artifacts):
                    print(f"{student.name} пропускает ход")
                    break

                else:
                    print("Неверный выбор! Попробуй ещё раз.")

            # Ход таракана
            if cockroach.alive:
                print(f"\n{'-' * 30}")
                print(f"ХОД {cockroach.name}")
                print(f"{'-' * 30}")

                print(f"\n{cockroach.attack(student)}")
                print(f"  {student.check_status()}")

            self.round += 1

        # Результат
        if student.alive:
            print(f"\n{'=' * 50}")
            print(f"ПОБЕДА! {student.name} победил {cockroach.name}!")
            print(f"{'=' * 50}")
            return True
        else:
            print(f"\n{'=' * 50}")
            print(f"ПОРАЖЕНИЕ... {cockroach.name} победил.")
            print(f"{'=' * 50}")
            return False