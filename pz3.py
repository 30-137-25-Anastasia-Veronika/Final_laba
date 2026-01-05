class Descriptor:

    def __init__(self, cipher_type, shift=3):
        self.cipher_type = cipher_type
        self.shift = shift

    def __get__(self, obj, objtype):
        return self

    def shrift_1(self, text, mode='encrypt'):
        """Шифр Цезаря: сдвиг каждой буквы на заданное количество позиций."""
        result = ""

        for char in text:
            if char.isalpha():
                if char.isupper():
                    base = ord('A')
                else:
                    base = ord('a')

                char_index = ord(char) - base

                if mode == 'encrypt':
                    new_index = (char_index + self.shift) % 26
                else:
                    new_index = (char_index - self.shift) % 26
                new_char = chr(base + new_index)
                result += new_char
            else:
                result += char

        return result

    def atbash_cipher(self, text, mode='encrypt'):
        """Шифр Атбаш: замена каждой буквы на противоположную в алфавите."""
        result = ""

        for char in text:
            if char.isalpha():  # Если символ - буква
                if char.isupper():
                    # Для больших букв: A->Z, B->Y и т.д.
                    # ord('A') = 65, ord('Z') = 90
                    # Противоположная буква: (90 - (код_буквы - 65))
                    new_char = chr(ord('Z') - (ord(char) - ord('A')))
                else:
                    # Для маленьких букв: a->z, b->y и т.д.
                    # ord('a') = 97, ord('z') = 122
                    new_char = chr(ord('z') - (ord(char) - ord('a')))
                result += new_char
            else:
                # Если не буква, оставляем как есть
                result += char

        return result

    def encrypt(self, text):
        """Шифрование текста."""
        if self.cipher_type == 'caesar':
            return self.shrift_1(text, 'encrypt')
        elif self.cipher_type == 'atbash':
            return self.atbash_cipher(text, 'encrypt')

    def decrypt(self, text):
        """Дешифрование текста."""
        if self.cipher_type == 'caesar':
            return self.shrift_1(text, 'decrypt')
        elif self.cipher_type == 'atbash':
            return self.atbash_cipher(text, 'decrypt')


class EncryptionSystem:
    """Класс для работы с шифрами."""

    # Создаем дескрипторы для каждого шифра
    caesar = Descriptor('caesar', shift=3)  # Цезарь со сдвигом 3
    atbash = Descriptor('atbash')  # Атбаш (сдвиг не нужен)


# Демонстрация работы
def main():
    # Создаем объект для работы с шифрами
    cipher_system = EncryptionSystem()

    # Тестовый текст
    test_text = "Hello World! 2025"
    print(f"Исходный текст: {test_text}")
    print()

    # Шифр Цезаря
    print("=== Шифр Цезаря (сдвиг 3) ===")
    encrypted_caesar = cipher_system.caesar.encrypt(test_text)
    print(f"Зашифрованный: {encrypted_caesar}")

    decrypted_caesar = cipher_system.caesar.decrypt(encrypted_caesar)
    print(f"Расшифрованный: {decrypted_caesar}")
    print()

    # Шифр Атбаш
    print("=== Шифр Атбаш ===")
    encrypted_atbash = cipher_system.atbash.encrypt(test_text)
    print(f"Зашифрованный: {encrypted_atbash}")

    decrypted_atbash = cipher_system.atbash.decrypt(encrypted_atbash)
    print(f"Расшифрованный: {decrypted_atbash}")
    print()

    # Пример с другим текстом
    print("=== Еще примеры ===")
    another_text = "Python Programming"
    print(f"Исходный: {another_text}")
    print(f"Цезарь зашифрованный: {cipher_system.caesar.encrypt(another_text)}")
    print(f"Атбаш зашифрованный: {cipher_system.atbash.encrypt(another_text)}")


if __name__ == "__main__":
    main()