from chacha_with_viz import encrypt as viz_encrypt
from chacha import encrypt
import os


def main():
    key = get_bytes_from_file('chacha_secret.txt')
    nonce = get_bytes_from_file('chacha_nonce.txt')
    iv = 0

    visualize = input("If you want to watch the algorithm, enter YES: ")
    viz_speed = 0 if visualize.lower() != 'yes' else float(input("How many frames per second? 0.1 is fast, 1 is slow. "))

    done = False
    while not done:
        plaintext = input("Enter text to encrypt (or 'quit' to end): ")
        if plaintext.lower() == 'quit':
            print("Thanks for encrypting with ChaCha20!")
            done = True
        else:
            try:
                plaintext = plaintext.encode('UTF-8')
                if visualize.lower() == 'yes':
                    result = viz_encrypt(key, nonce, plaintext, viz_speed, iv)
                else:
                    result = encrypt(key, nonce, plaintext, iv)
                decrypted_plaintext = encrypt(key, nonce, result, iv)
                print()
                print("The encrypted result is...")
                print(result)
                print("This result was decrypted back to...")
                print(decrypted_plaintext)
            except ValueError as err:
                print(err)
        print()


def get_bytes_from_file(filename):
    try:
        if not os.path.exists(filename):
            raise Exception(filename + " does not exist")
        if os.path.isdir(filename):
            raise Exception(filename + " is a directory")

        input_file = open(filename, 'r')

        file_data = input_file.readline()
        file_data = file_data.rstrip('\n')

        input_file.close()

        return file_data.encode('UTF-8')
    except PermissionError:
        print("You do not have sufficient permissions to open", filename)
    except OSError:
        print("An unexpected error occurred while attempting to open", filename)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
