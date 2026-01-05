import os
import json
import time
import sys
from characters import *
from battle_system import BattleSystem


# ==================== СИСТЕМА РЕГИСТРАЦИИ ====================
class RegistrationSystem:
    def __init__(self):
        self.players_file = "players.txt"
        self.current_player = None

    def register_player(self):
        print("\n" + "=" * 60)
        print("Ты достаёшь паспорт и протягиваешь его Валентину...")
        print("=" * 60)

        username = input("Валентин записывает в журнал твоё имя: ")
        password = input("Придумай секретное слово для пропуска: ")

        if os.path.exists(self.players_file):
            with open(self.players_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if username in line:
                        print("Валентин хмурится: 'Такой пропуск уже есть!'")
                        return False

        with open(self.players_file, 'a', encoding='utf-8') as f:
            f.write(f"{username}:{password}\n")

        print(f"\nВалентин протягивает тебе пропуск: 'Добро пожаловать в Икар, {username}!'")
        self.current_player = Player(username, password)
        return True

    def login_player(self):
        print("\n" + "=" * 60)
        print("Ты показываешь свой пропуск Валентину...")
        print("=" * 60)

        username = input("Твоё имя на пропуске: ")
        password = input("Секретное слово: ")

        if not os.path.exists(self.players_file):
            print("Валентин: 'Никого ещё не пропускал сегодня!'")
            return False

        with open(self.players_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    saved_user, saved_pass = parts
                    if saved_user == username and saved_pass == password:
                        print(f"\nВалентин кивает: 'Проходи, {username}, помни правила!'")
                        self.current_player = Player(username, password)
                        self.load_game()
                        return True

        print("Валентин качает головой: 'Неверный пропуск или секретное слово!'")
        return False

    def save_game(self):
        if self.current_player:
            if not os.path.exists("saves"):
                os.makedirs("saves")

            save_file = f"saves/{self.current_player.username}_save.json"

            # Сохраняем артефакты
            artifacts_data = []
            for artifact in self.current_player.artifacts:
                artifacts_data.append({
                    "name": artifact.name,
                    "power": artifact.power,
                    "description": artifact.description,
                    "max_uses": artifact.max_uses,
                    "current_uses": artifact.current_uses
                })

            save_data = {
                "username": self.current_player.username,
                "current_location": self.current_player.current_location,
                "progress": self.current_player.progress,
                "artifacts": artifacts_data,
                "hp": self.current_player.hp,
                "energy": self.current_player.energy,
                "completed_stories": getattr(self.current_player, 'completed_stories', []),
                "secret_room_visited": getattr(self.current_player, 'secret_room_visited', False)
            }

            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)

            print("\nИгра сохранена!")

    def load_game(self):
        if not self.current_player:
            return False

        save_file = f"saves/{self.current_player.username}_save.json"

        if os.path.exists(save_file):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)

                self.current_player.current_location = save_data["current_location"]
                self.current_player.progress = save_data["progress"]
                self.current_player.hp = save_data["hp"]
                self.current_player.energy = save_data["energy"]

                # Загружаем артефакты
                vault = ArtifactVault()
                self.current_player.artifacts = []

                for art_data in save_data["artifacts"]:
                    artifact = vault.get_artifact_by_name(art_data["name"])
                    if artifact:
                        artifact.current_uses = art_data["current_uses"]
                        self.current_player.artifacts.append(artifact)

                # Загружаем пройденные сюжеты
                self.current_player.completed_stories = save_data.get("completed_stories", [])
                # Загружаем посещение секретной комнаты
                self.current_player.secret_room_visited = save_data.get("secret_room_visited", False)

                print(f"Загружено сохранение. Прогресс: {self.current_player.progress}%")
                return True
            except Exception as e:
                print(f"Не удалось загрузить сохранение: {e}")
                return False

        return False


# ==================== ОСНОВНАЯ ИГРА ====================
class IkarGame:
    def __init__(self):
        self.reg_system = RegistrationSystem()
        self.vault = ArtifactVault()
        self.battle_system = BattleSystem()
        self.story_completed = False

    def print_slow(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def show_ending(self):
        """Показывает финальную надпись при любом завершении игры"""
        print("\n" + "*" * 80)
        print("ВСЕ ИМЕНА И СОБЫТИЯ ВЫМЫШЛЕНЫ,")
        print("ЛЮБЫЕ СОВПАДЕНИЯ С РЕАЛЬНЫМИ ЛЮДЬМИ И СОБЫТИЯМИ СЛУЧАЙНЫ")
        print("ИГРА ЗАВЕРШИЛАСЬ.")
        print("*" * 80)
        input("\nНажми Enter для выхода...")
        sys.exit(0)

    def show_intro(self):
        print("\n" + "=" * 60)
        self.print_slow("Привет, дорогой друг! Ты попал в общагу 'Икар'.")
        self.print_slow("Это не просто 5-ти этажный домик для студентов, а общага самого лучшего вуза на свете -")
        self.print_slow("Межгалактической Алкогольной Империи (МАИ).")
        print()
        self.print_slow("Именно здесь обитают будущие гении, миллиардеры, плэйбои, филантропы.")
        self.print_slow("Именно в этом месте днём можно увидеть, как решают по 600 интегралов заключённые 311 кафедры,")
        self.print_slow("а ночью можно услышать, как разливаются животворящие жидкости по бокалам.")
        print()
        self.print_slow("Именно в этом месте тебе откроется завеса всех тайн студенческой жизни!")
        print()
        self.print_slow("Только будь осторожен... в общаге живут не только студенты,")
        self.print_slow("но ещё и их вечные враги - тараканы.")
        self.print_slow("Они способны вызвать ужас в глазах любого студента,")
        self.print_slow("завладеть их едой, вещами, а иногда даже выжить их из собственных постелей.")
        print()
        self.print_slow("Только сильнейшие доживают до 4-го курса.")
        self.print_slow("Но не переживай! Мы уверены, именно тебе под силу одолеть этих мелких,")
        self.print_slow("но до жути хитрых тараканов, и завоевать своё место под солнцем!")
        print()
        self.print_slow("С богом, дорогой друг!")
        print("=" * 60)
        input("\nНажми Enter чтобы переступить порог общаги...")

    def main_menu(self):
        while True:
            print("\n" + "=" * 60)
            print("Ты переступил порог этого чудесного заведения!")
            print("На проходной ты встречаешь охранника Валентина,")
            print("который не может пропустить тебя просто так:")
            print("=" * 60)
            print("1. Получить пропуск (если первый раз в нашей общаге)")
            print("2. Показать пропуск (уже бывал здесь раньше)")
            print("3. Зашёл не в ту дверь (выход)")
            print("=" * 60)

            choice = input("Твои действия (1-3): ")

            if choice == "1":
                if self.reg_system.register_player():
                    self.start_story()
            elif choice == "2":
                if self.reg_system.login_player():
                    self.start_story()
            elif choice == "3":
                print("\nВалентин машет рукой: 'До свидания!'")
                self.show_ending()
            else:
                print("Валентин смотрит на тебя с недоумением...")

    def start_story(self):
        player = self.reg_system.current_player

        # Инициализируем список пройденных сюжетов, если его нет
        if not hasattr(player, 'completed_stories'):
            player.completed_stories = []

        # Инициализируем посещение секретной комнаты
        if not hasattr(player, 'secret_room_visited'):
            player.secret_room_visited = False

        print("\n" + "=" * 60)
        self.print_slow(f"Ты входишь в общагу 'Икар', {player.username}!")
        self.print_slow("Перед тобой длинный коридор, пахнет чем-то знакомым...")
        self.print_slow("это запах свободы, молодости и... немного плесени.")
        print()
        self.print_slow("Куда отправишься в первую очередь?")
        print("=" * 60)

        while not self.story_completed:
            print("\nТвой выбор:")
            print("1. Пойти заниматься в коворкинг")
            print("2. Присоединиться к чаепитию в 2205")
            print("3. Пойти отдыхать в самую любимую комнату - 2209")
            print("4. Тайная комната (только один раз!)")
            print(
                "5. Подняться на 5-й этаж для финальной битвы" if player.progress >= 66 else "5. (Заблокировано - пройди другие пути)")
            print("6. Выйти из общаги (сохранить и выйти)")
            print("=" * 60)

            choice = input("Что выбираешь? (1-6): ")

            if choice == "1":
                if "коворкинг" not in player.completed_stories:
                    self.coworking_story()
                else:
                    print("Ты уже проходил эту сюжетную линию!")
            elif choice == "2":
                if "чай_2205" not in player.completed_stories:
                    self.tea_party_story()
                else:
                    print("Ты уже проходил эту сюжетную линию!")
            elif choice == "3":
                if "комната_2209" not in player.completed_stories:
                    self.room_2209_story()
                else:
                    print("Ты уже проходил эту сюжетную линию!")
            elif choice == "4":
                self.secret_room_story()
            elif choice == "5" and player.progress >= 66:
                self.final_battle()
                break
            elif choice == "6":
                self.exit_option()
                break
            else:
                print("Такого варианта нет... попробуй ещё раз.")

    def secret_room_story(self):
        """Тайная комната для восстановления сил"""
        player = self.reg_system.current_player

        print("\n" + "=" * 60)
        self.print_slow("Дорогой друг, за этой дверью тебе откроется волшебный мир!")
        self.print_slow("Ты сможешь отдохнуть, восстановить свои силы и восполнить потери,")
        self.print_slow("но помни, у любого волшебства есть свои правила.")
        self.print_slow("Ты можешь войти в эту комнату всего лишь раз,")
        self.print_slow("подумай, может стоит приберечь эту возможность...")
        print("=" * 60)

        print("\nТвои действия:")
        print("1. Войти в тайную комнату")
        print("2. Вернуться в коридор")
        print("=" * 60)

        choice = input("Что выбираешь? (1-2): ")

        if choice == "2":
            print("\nТы решил не рисковать и вернулся в коридор...")
            return

        # Проверяем, был ли игрок уже в секретной комнате
        if player.secret_room_visited:
            print("\n" + "=" * 60)
            self.print_slow("Упсс, комната закрыта, видимо хозяева на парах,")
            self.print_slow("приходи в следующий раз!")
            print("=" * 60)
            input("\nНажми Enter чтобы вернуться в коридор...")
            return

        # Игрок впервые в секретной комнате
        print("\n" + "=" * 60)
        self.print_slow("Битва с тараканами может заурядно измучить,")
        self.print_slow("поэтому в общаге есть 'та самая' комната, где твориться магия.")
        self.print_slow("Ты заходишь, а вместо стен здесь живописные долины")
        self.print_slow("с водопадами и джунглями, здесь можно услышать как поют птицы,")
        self.print_slow("а в воздухе всегда можно уловить нежный запах манго-маракуйи.")
        self.print_slow("Тебя встречает хозяин комнаты - Богдан,")
        self.print_slow("а также его друзья Ника и Андрей.")
        self.print_slow("Ты не успеешь моргнуть глазом, как на столе уже появилось")
        self.print_slow("волшебное зелье 'Деревенька', которое заставит твоё сердце")
        self.print_slow("биться снова и придаст тебе сил для дальнейших сражений.")
        self.print_slow("Пей до дна, дорогой друг, и не пророни ни капли")
        self.print_slow("этого животворящего снадобья...")
        print("=" * 60)
        input("\nНажми Enter чтобы выпить зелье...")

        # Восстанавливаем силы игрока
        player.hp = 200  # Максимальное HP
        player.energy = 200  # Максимальная энергия

        print(f"\nТвои силы восстановлены!")
        print(f"HP: {player.hp}/200")
        print(f"Энергия: {player.energy}/200")

        # Отмечаем, что игрок посетил секретную комнату
        player.secret_room_visited = True

        # Сохраняем игру
        self.reg_system.save_game()

        print("\nТы чувствуешь прилив сил и готов к новым подвигам!")
        input("\nНажми Enter чтобы вернуться в коридор...")

    def mark_story_completed(self, story_name):
        """Отмечает сюжет как пройденный и добавляет прогресс"""
        player = self.reg_system.current_player

        if story_name not in player.completed_stories:
            player.completed_stories.append(story_name)
            player.progress += 33
            print(f"\nПрогресс: {player.progress}%")

            # Сохраняем игру после прохождения сюжета
            self.reg_system.save_game()

    def coworking_story(self):
        player = self.reg_system.current_player
        print("\n" + "=" * 60)
        self.print_slow("Самое время пойти позаниматься в коворкинг,")
        self.print_slow("ведь ученье - свет, а неученье - чуть свет и на работу!")
        self.print_slow("Коворкинг Икара - необычное место,")
        self.print_slow("только там можно встретить самое редкое явление МАИ - занимающихся учёбой ребят!")
        print()
        self.print_slow("Наверное по пути в это чудное или чудесное место")
        self.print_slow("ты слышал как на весь коридор матом кричал студент по имени Барисбий,")
        self.print_slow("оооох ну это неспроста, ведь в коворкинге тот обнаружил...")
        print()
        input("Нажми Enter чтобы продолжить...")

        print("\n" + "=" * 60)
        self.print_slow("ТАРАКАНА")
        self.print_slow("Как ты уже понял, этот коворкинг - уникальное место,")
        self.print_slow("поэтому и тараканы тут уникальные, точнее таракан,")
        self.print_slow("потому что он тут один, но зато какой...")
        self.print_slow("Это таракан-интеллектуал, чтобы с ним сразиться")
        self.print_slow("ты должен быть необычайно умён и остроумен.")
        self.print_slow("Удачи, дорогой друг!")
        print("=" * 60)
        input("\nНажми Enter чтобы начать интеллектуальную дуэль...")

        # Интеллектуальная битва
        cockroach = CockroachIntellectual()
        player_score = 3

        print("\n" + "=" * 60)
        print("ТАРАКАН-ИНТЕЛЛЕКТУАЛ ПРИВЕТСТВУЕТ ТЕБЯ!")
        print("=" * 60)

        for i in range(3):
            question, correct_answer = cockroach.questions[i]
            print(f"\nВопрос {i + 1}: {question}")
            answer = input("Твой ответ: ")

            if answer.strip().lower() == correct_answer.lower():
                print("Правильно! Таракан теряет силы!")
                cockroach.hp -= 25
                print(f"У таракана осталось {cockroach.hp} HP")
            else:
                print(f"Неправильно! Правильный ответ: {correct_answer}")
                player_score -= 1
                print(f"У тебя осталось {player_score} попыток")

            if cockroach.hp <= 0:
                break

        if cockroach.hp <= 0:
            print("\n" + "=" * 60)
            self.print_slow("Огого, друг, да ты чёртов гений!")
            self.print_slow("Наконец хоть кто-то смог одолеть этого таракана!")
            input("\nНажми Enter чтобы продолжить...")

            print("\n" + "=" * 60)
            self.print_slow("Покидая коворкинг, ты встречаешь Барисбия,")
            self.print_slow("который благодарит тебя за освобождение коворкинга")
            self.print_slow("и в качестве вознаграждения дарит тебе свой тапок!")
            print("=" * 60)

            # Получаем артефакт
            artifact = self.vault.get_artifact_by_name("Тапок Барисбия")
            if artifact:
                player.artifacts.append(artifact)
                print(f"\nТы получил артефакт: {artifact}")

            # Отмечаем сюжет как пройденный
            self.mark_story_completed("коворкинг")

        else:
            print("\n" + "=" * 60)
            self.print_slow("Таракан оказался умнее... Возвращайся, когда подучишься!")
            print("=" * 60)

        input("\nНажми Enter чтобы вернуться в коридор...")

    def tea_party_story(self):
        player = self.reg_system.current_player
        print("\n" + "=" * 60)
        self.print_slow("В общаге Икар много удивительных комнат,")
        self.print_slow("где творятся разные чудеса,")
        self.print_slow("но ни в одной ты не попробуешь такого великолепного чая,")
        self.print_slow("как в комнате 2205!")
        self.print_slow("Тут можно найти чай на любой вкус и цвет,")
        self.print_slow("например, весь второй этаж знает про их успакоительный чай,")
        self.print_slow("три кружечки - и ты в зюзю!")
        self.print_slow("Ну ладно, не раскрываю всех тайн! 2205 ждёт!")
        print("=" * 60)
        input("\nНажми Enter чтобы отправиться на второй этаж...")

        # Встреча с Анастасией Потоцкой
        print("\n" + "=" * 60)
        self.print_slow("По пути на второй этаж ты встречаешь")
        self.print_slow("ночного коменданта - Анастасию Потоцкую.")
        print("\nТвои действия:")
        print("1. Вежливо поздороваться")
        print("2. Пройти мимо, делая вид, что не заметил")
        print("=" * 60)

        choice = input("Что делаешь? (1-2): ")

        if choice == "1":
            self.print_slow("\nАнастасия улыбается: 'Привет, студент! Не шуми на этаже.'")
        else:
            self.print_slow("\nАнастасия хмурится: 'Молодой человек, вы что, не видите меня?'")
            player.hp -= 25
            print(f"Ты теряешь 25 HP. Теперь у тебя {player.hp} HP")

        input("\nНажми Enter чтобы продолжить путь в 2205...")

        print("\n" + "=" * 60)
        self.print_slow("Ты стоишь на пороге легендарной 2205.")
        self.print_slow("Тебя встречает Лиза с улыбкой и чайником в руках.")
        print("\nТвои действия:")
        print("1. Послушать сплетни за чаем")
        print("2. Предложить помочь - пойти набрать воды в чайник")
        print("=" * 60)

        choice = input("Что выбираешь? (1-2): ")

        if choice == "1":
            print("\n" + "=" * 60)
            self.print_slow("Лиза начала свой рассказ:")
            self.print_slow('"Вот представляете, мне недавно Настя из 2209 рассказала,')
            self.print_slow('что Клим из 2524 зашёл в душ к девочкам!')
            self.print_slow('В женской душевой был ремонт и все купались в мужской душевой,')
            self.print_slow('для мальчиков одно время, для девочек другое.')
            self.print_slow('Воот, и Клим или случайно, или специально перепутал')
            self.print_slow('и пришёл в женское время...я в шоке..."')
            print("=" * 60)

            # Дарим кружку 2205
            artifact = self.vault.get_artifact_by_name("Кружка 2205")
            if artifact:
                player.artifacts.append(artifact)
                print(f"\nЛиза дарит тебе на память кружку 2205!")
                print(f"Ты получил артефакт: {artifact}")

            # Отмечаем сюжет как пройденный
            self.mark_story_completed("чай_2205")
            input("\nНажми Enter чтобы вернуться в коридор...")

        else:
            print("\n" + "=" * 60)
            self.print_slow("Ты берёшь чайник и идешь на кухню...")
            self.print_slow("Но кажется, ты не один на кухне...")
            input("\nНажми Enter чтобы посмотреть вокруг...")

            print("\n" + "=" * 60)
            self.print_slow("ТАРАКАНЫ!")
            self.print_slow("На кухне целая армия тараканов!")
            print("=" * 60)

            # Битва 1 на 1 на кухне
            player_student = Student(player.username, "Студент", player.hp, player.energy)
            player_student.artifacts = player.artifacts.copy()

            cockroach = Cockroach("Таракан-кухонный", 80)

            battle_result = self.battle_system.one_on_one_battle(player_student, cockroach)

            # Обновляем состояние игрока
            player.hp = player_student.hp
            player.energy = player_student.energy
            player.artifacts = player_student.artifacts

            if battle_result:
                print("\n" + "=" * 60)
                print("После битвы у тебя есть выбор:")
                print("1. Вернуться в 2205 пить чай и слушать сплетни")
                print("2. Пойти пригласить на чаепитие Александра из 2202")
                print("=" * 60)

                choice = input("Что делаешь? (1-2): ")

                if choice == "1":
                    print("\n" + "=" * 60)
                    self.print_slow("Лиза начала свой рассказ:")
                    self.print_slow('"Вот представляете, мне недавно Настя из 2209 рассказала...')
                    print("=" * 60)

                    # Дарим кружку
                    artifact = self.vault.get_artifact_by_name("Кружка 2205")
                    if artifact:
                        player.artifacts.append(artifact)
                        print(f"\nЛиза дарит тебе на память кружку 2205!")
                        print(f"Ты получил артефакт: {artifact}")

                    # Отмечаем сюжет как пройденный
                    self.mark_story_completed("чай_2205")

                else:
                    self.invite_alexander()
            else:
                print("\nТы проиграл битву... возвращаешься в коридор.")

        input("\nНажми Enter чтобы вернуться в коридор...")

    def invite_alexander(self):
        player = self.reg_system.current_player
        print("\n" + "=" * 60)
        self.print_slow("Залог хорошего вечера - это хорошие люди вокруг,")
        self.print_slow("особенно когда мы говорим про Александра из 2202 - легенда Инноватики")
        print("=" * 60)
        input("\nНажми Enter чтобы продолжить...")

        print("\n" + "=" * 60)
        self.print_slow("В весьма необычной комнате 2202 ты находишь Александра и его соседа Андрея,")
        self.print_slow("вы уже уходите, в мыслях уже один чай и вкусные сплетни...")
        self.print_slow("как вдруг ты замечаешь их...")
        self.print_slow("ТАРАКАНЫ")
        print("=" * 60)
        input("\nНажми Enter чтобы начать битву...")

        # Битва 3 на 3: Игрок + Александр + Андрей vs 3 таракана
        player_student = Student(player.username, "Студент", player.hp, player.energy)
        player_student.artifacts = player.artifacts.copy()

        alexander = Alexander()
        andrey = Andrey()

        students = [player_student, alexander, andrey]

        cockroaches = [
            Cockroach("Таракан-солдат", 70),
            Cockroach("Таракан-разведчик", 60),
            Cockroach("Таракан-мутант", 80)
        ]

        battle_result = self.battle_system.simple_battle_3v3(students, cockroaches)

        # Обновляем состояние игрока
        player.hp = player_student.hp
        player.energy = player_student.energy
        player.artifacts = player_student.artifacts

        if battle_result:
            print("\n" + "=" * 60)
            self.print_slow("Это была сложная битва, но ты справился!")
            self.print_slow(f"Трипещите тараканы, {player.username} покажет вам, где раки зимуют!!!")
            print("=" * 60)
            input("\nНажми Enter чтобы продолжить...")

            print("\n" + "=" * 60)
            self.print_slow("После сложной битвы, сидеть и пить чай в 2205 было ой как приятно,")
            self.print_slow("особенно под интересные истории, ведь где ещё можно узнать,")
            self.print_slow("что на прошлой неделе мальчик по имени Клим заходил в женский душ,")
            self.print_slow("137 группа завалила контрольную по мат.анализу и то,")
            self.print_slow(
                "что самолёт летает потому что молекулы воздуха толкают крылышки самолёта и тот не падает...")
            print("=" * 60)

            # Дарим кружку
            artifact = self.vault.get_artifact_by_name("Кружка 2205")
            if artifact:
                player.artifacts.append(artifact)
                print(f"\nЛиза дарит тебе на память кружку 2205!")
                print(f"Ты получил артефакт: {artifact}")

            # Отмечаем сюжет как пройденный
            self.mark_story_completed("чай_2205")
        else:
            print("\nБитва проиграна... возвращаешься в коридор.")

        input("\nНажми Enter чтобы вернуться в коридор...")

    def room_2209_story(self):
        player = self.reg_system.current_player
        print("\n" + "=" * 60)
        self.print_slow("После долгой дороги с Оршанки до нашей общаги ты вероятно устал,")
        self.print_slow("поэтому тебя всегда ждёт самая гостеприимная комната в Икаре - 2209.")
        self.print_slow("Здесь тебя всегда угостят тёплым чаем со всякими вкусностями,")
        self.print_slow("расскажут незабываемые истории и разрешат остаться на ночь.")
        self.print_slow(
            "По пути на второй этаж ты проходишь мимо комнаты с главным комендантом Икара - Ольга Васильевна")
        print("=" * 60)

        print("\nТвои действия:")
        print("1. Заколотиться поздороваться с Ольгой Васильевной")
        print("2. Пройти мимо")
        print("=" * 60)

        choice = input("Что делаешь? (1-2): ")

        if choice == "1":
            artifact = self.vault.get_artifact_by_name("Милость Ольги Васильевны")
            if artifact:
                player.artifacts.append(artifact)
                print(f"\nОльга Васильевна улыбается и дарит тебе свою милость!")
                print(f"Ты получил артефакт: {artifact}")
        else:
            print("\nТы проходишь мимо... Ольга Васильевна смотрит тебе вслед.")

        input("\nНажми Enter чтобы продолжить путь в 2209...")

        print("\n" + "=" * 60)
        self.print_slow("Наконец ты добрался до комнаты, где тебя встречают самые красивые девушки МАИ.")
        self.print_slow("Но вот незадача, как только ты переступил порог 2209,")
        self.print_slow("ты увидел, как те самые красивые девушки МАИ - Ника, Настя и Маша - очень напуганы.")
        self.print_slow("Оказывается их комнату оккупировали тараканы.")
        self.print_slow("Вместе вы должны победить их!")
        print("=" * 60)
        input("\nНажми Enter чтобы начать битву...")

        # Битва 4 на 3: Игрок + 3 девушки vs 3 таракана
        player_student = Student(player.username, "Студент", player.hp, player.energy)
        player_student.artifacts = player.artifacts.copy()

        nika = Nika()
        nastya = Nastya()
        masha = Masha()

        students = [player_student, nika, nastya, masha]

        cockroaches = [
            Cockroach("Таракан-захватчик", 70),
            Cockroach("Таракан-шпион", 60),
            Cockroach("Таракан-гигант", 90)
        ]

        battle_result = self.battle_system.simple_battle_3v3(students, cockroaches)

        # Обновляем состояние игрока
        player.hp = player_student.hp
        player.energy = player_student.energy
        player.artifacts = player_student.artifacts

        if battle_result:
            print("\n" + "=" * 60)
            self.print_slow("Тараканы отступили! Тебе удалось победить тараканов и освободить 2209.")
            self.print_slow("Да ты достойный маёвец, дорогой друг!")
            print("=" * 60)

            # Дарим артефакт
            artifact = self.vault.get_artifact_by_name("Теннисная ракетка Маши")
            if artifact:
                player.artifacts.append(artifact)
                print(f"\nМаша дарит тебе свою теннисную ракетку в благодарность!")
                print(f"Ты получил артефакт: {artifact}")

            # Отмечаем сюжет как пройденный
            self.mark_story_completed("комната_2209")
        else:
            print("\nБитва проиграна... возвращаешься в коридор.")

        input("\nНажми Enter чтобы вернуться в коридор...")

    def final_battle(self):
        player = self.reg_system.current_player

        print("\n" + "=" * 60)
        self.print_slow("Стрелки часов лениво ползли вверх по циферблату,")
        self.print_slow("а это лишь означало, что дело идёт к ночи")
        self.print_slow("и все студенты возвращаются в общагу.")
        self.print_slow("Вот и твои друзья уже вернулись к себе в комнату,")
        self.print_slow("самое время их навестить!")
        print("=" * 60)
        input("\nНажми Enter чтобы подняться на 5-й этаж...")

        print("\n" + "=" * 60)
        self.print_slow("Ты поднимаешься на 5-й этаж...")
        self.print_slow("Тебя сразу встречает гостеприимная дверь 2519,")
        self.print_slow("которая сама открывается, как бы приветствуя 'своих'.")
        self.print_slow("Тебя встречают обитатели этой просторной комнаты:")
        self.print_slow("будущее российской науки, обладатель звания")
        self.print_slow("'Мистер Флэт Уайт МАИ', да и просто хороший человек - Захар;")
        self.print_slow("звезда модельной индустрии, амбассадор роскошной жизни - Тимур;")
        self.print_slow("ииии красивый Барисбий!!!")
        self.print_slow("Вместе вы садитесь пить ромашковый чай!")
        print("=" * 60)
        input("\nНажми Enter чтобы продолжить...")

        # Загадка от Тимура
        print("\n" + "=" * 60)
        self.print_slow("Тимур улыбается и говорит:")
        self.print_slow("'Дорогой друг, прежде чем мы продолжим,")
        self.print_slow("отгадай-ка загадку: Летит - гудит, сядет - замолчит.'")
        print("=" * 60)

        answer = input("Твой ответ: ").strip().lower()

        if answer == "самолёт":
            print("\nТимур хлопает в ладоши: 'Верно! Ты заслужил награду!'")

            # Получаем артефакт "Браслет Тимура"
            artifact = self.vault.get_artifact_by_name("Браслет Тимура")
            if artifact:
                player.artifacts.append(artifact)
                print(f"\nТимур снимает с руки браслет и дарит тебе!")
                print(f"Ты получил артефакт: {artifact}")
                print("Этот браслет защитит тебя от атак тараканов!")
        else:
            print(f"\nТимур смеётся: '{answer}? Интересно, но нет. Правильный ответ: самолёт.'")
            print("Впрочем, это не главное. Продолжим...")

        input("\nНажми Enter чтобы продолжить...")

        print("\n" + "=" * 60)
        self.print_slow("Захар серьёзно смотрит на тебя и говорит:")
        self.print_slow("'Друг, пока мы тут чай пьём, у меня есть важные новости.'")
        self.print_slow("'В общаге появилась страшная угроза -")
        self.print_slow("Королева Тараканов обосновалась на кухне 5-го этажа,'")
        self.print_slow("'в той горе посуды, которая никогда не убирается.'")
        self.print_slow("'Она уже успела собрать целую армию тараканов.'")
        self.print_slow("'Если мы не остановим её сейчас, вся общага будет захвачена!'")
        print("=" * 60)

        print("\nБарисбий встаёт и говорит:")
        print("'Что ж, пора действовать! Пойдём, покажем этой королеве,'")
        print("'кто в общаге хозяин!'")
        print("=" * 60)

        input("\nНажми Enter чтобы отправиться на финальную битву...")

        print("\n" + "=" * 60)
        self.print_slow("КУХНЯ 5-ГО ЭТАЖА")
        self.print_slow("Перед тобой гора грязной посуды, а из-под неё...")
        self.print_slow("появляется ОНА - КОРОЛЕВА ТАРАКАНОВ!")
        print("=" * 60)
        input("\nНажми Enter чтобы начать финальную битву...")

        # Финальная битва 4 на 1: Игрок + Захар + Тимур + Барисбий vs Королева
        player_student = Student(player.username, "Студент", player.hp, player.energy)
        player_student.artifacts = player.artifacts.copy()

        zakhar = Zakhar()
        timur = Timur()
        barisbiy = Barisbiy()

        students = [player_student, zakhar, timur, barisbiy]
        boss = CockroachQueen()

        battle_result = self.battle_system.boss_battle(students, boss)

        # Обновляем состояние игрока
        player.hp = player_student.hp
        player.energy = player_student.energy
        player.artifacts = player_student.artifacts

        if battle_result:
            print("\n" + "=" * 60)
            self.print_slow("КОРОЛЕВА ТАРАКАНОВ ПОВЕРЖЕНА!")
            self.print_slow("Общага 'Икар' спасена!")
            self.print_slow("Ты стал легендой МАИ!")
            print("=" * 60)

            player.progress = 100
            self.story_completed = True

            # Показываем финальную надпись и завершаем игру
            self.show_ending()
        else:
            print("\n" + "=" * 60)
            self.print_slow("Королева победила... нужно больше силы.")
            self.print_slow("Вернись, когда соберёшь больше артефактов.")
            print("=" * 60)

            # Даже при поражении показываем финальную надпись
            self.show_ending()

    def exit_option(self):
        player = self.reg_system.current_player
        print("\n" + "=" * 60)
        print("Ты стоишь у выхода из общаги...")
        print("1. Сохранить игру и выйти")
        print("2. Выйти без сохранения")
        print("=" * 60)

        choice = input("Что выбираешь? (1-2): ")

        if choice == "1":
            self.reg_system.save_game()
            print("\nИгра сохранена. Возвращайся в Икар!")
        else:
            print("\nТы выходишь из общаги... прогресс потерян.")

        # Всегда показываем финальную надпись при выходе
        self.show_ending()


# ==================== ЗАПУСК ИГРЫ ====================
if __name__ == "__main__":
    # Проверяем папку для сохранений
    if not os.path.exists("saves"):
        os.makedirs("saves")

    # Создаём и запускаем игру
    game = IkarGame()
    game.show_intro()
    game.main_menu()