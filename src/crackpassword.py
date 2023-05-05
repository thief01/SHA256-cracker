import itertools
import string
import hashlib
import threading
import time
from multiprocessing import Process
from multiprocessing import Pool
# SuperFastPython.com
import math
from concurrent.futures import ProcessPoolExecutor


class Cracker:

    def __init__(self, password_hash, password_count, characters_at_end, using_letters_set):
        self.password_hash = password_hash
        self.password_count = password_count
        self.using_letters_set = string.ascii_letters.strip()
        self.using_letters_set = string.ascii_lowercase.strip()
        self.characters_counts = len(self.using_letters_set)
        self.combinations = self.characters_counts ** password_count
        self.characters_at_end = characters_at_end
        self.stop_all_threads = False
        self.checked_passwords = 0
        self.cracked_password = ""
        self.done = False

        self.dividers_for_rests = [0] * self.password_count
        for i in range(0, self.password_count):
            self.dividers_for_rests[i] = self.characters_counts ** (i + 1)

    def start_cracking_normal(self):
        self.cracking_loop()

    def start_cracking_by_multi_tasking(self, threads):

        thread = threading.Thread(target=self.log_loop)
        thread.start()
        ths = []

        for i in range(0, threads):
            params = self.generate_starting_parameters(i, threads)
            self.prints_stating_positions(params, i)
            temp_thread = threading.Thread(target=self.cracking_loop, args=(params,))
            temp_thread.start()
            ths.append(temp_thread)

        thread.join()

    def start_simple_task(self):
        self.cracking_loop([0] * self.password_count)

    def test_pool(self, thread_id, threads):
        args = self.generate_starting_parameters(thread_id, threads)
        self.cracking_loop(args)

    def cracking_loop(self, starting_parameters: []):
        password_ids = starting_parameters
        rounds = 0

        for i in range(0, self.combinations):
            self.compare_password(self.get_passwords(password_ids))
            if self.cracked_password:
                break

            rounds += 1
            self.checked_passwords += 1
            password_ids[0] += 1
            password = ""
            for j in range(0, len(password_ids)):
                if password_ids[j] >= len(self.using_letters_set):
                    password_ids[j] = 0
                    if j + 1 < len(password_ids):
                        password_ids[j + 1] += 1

    def start_really_multi_thread(self, params: []):
        if __name__ == '__main__':
            # report a message
            print('Starting task...')
            # create the process pool
            with ProcessPoolExecutor(8) as exe:
                # perform calculations
                exe.map(cracker.compare_password, range(1, self.combinations))
            # report a message
            print('Done ALL COMBOSES.')

    def log_loop(self):
        previous_time = time.perf_counter()
        while True:
            current_time = time.perf_counter()
            execution_time = current_time - previous_time
            if execution_time > 1:
                print(f"Combinations {self.checked_passwords}/{self.combinations} Progress:",
                      str(self.checked_passwords / self.combinations * 100) + "%")
                previous_time = time.perf_counter()
            if self.cracked_password:
                break

    def test_loop(self):
        previous_time = time.perf_counter()
        id = 0
        while True:
            current_time = time.perf_counter()
            execution_time = current_time - previous_time
            if execution_time > 0.00001:
                id += 1
                self.compare_password_with_new_rule(id)
                previous_time = time.perf_counter()
            if self.cracked_password:
                break

    def get_passwords(self, generated_parameters):
        text = ""
        for i in range(0, self.password_count):
            text += self.using_letters_set[generated_parameters[i]]
        return text

    def compare_password_with_new_rule(self, combinationId):
        rests = [0] * self.password_count
        dividers = [0] * self.password_count
        to_divide = [0] * self.password_count

        previousRest = combinationId
        for i in reversed(range(0, len(self.dividers_for_rests))):
            rests[i] = previousRest % self.dividers_for_rests[i]
            dividers[i] = previousRest / self.dividers_for_rests[i]
            if i + 1 < len(self.dividers_for_rests):
                if dividers[i] > 1:
                    dividers[i + 1] = int(dividers[i])
                else:
                    dividers[i + 1] = 0
            if i == 0:
                dividers[i] = rests[i]
            previousRest = rests[i]
        # print(combinationId)
        # print(self.dividers_for_rests)
        # print(rests)
        # print(dividers)
        print(self.get_passwords(dividers))
        # self.crackedPassword = "XD"
        # self.done = False

    def compare_password(self, generated_password) -> bool:
        generated_password += self.characters_at_end
        hash_object2 = hashlib.sha256(generated_password.encode())
        new_hash = hash_object2.hexdigest()

        if new_hash == self.password_hash:
            self.stop_all_threads = True
            self.cracked_password = generated_password
            print("Password got breaked:", generated_password)
            return True
        return False

    def compare_password_with_current(self, generatedPassword):
        generatedPassword += self.characters_at_end
        hash_object2 = hashlib.sha256(generatedPassword.encode())
        new_hash = hash_object2.hexdigest()
        print(new_hash)
        print(new_hash == self.password_hash)

    def generate_starting_parameters(self, thread_id, max_threads) -> []:
        if thread_id == 0:
            params = [0] * self.password_count
            return params
        params = [0] * (self.password_count - 1)
        every_thread = self.characters_counts / max_threads
        every_thread = int(every_thread)
        last_param = thread_id * every_thread
        if thread_id * every_thread >= self.characters_counts:
            last_param = self.characters_counts - 1
        params.append(last_param)
        return params

    def prints_stating_positions(self, params, id):
        text = ""
        for i in range(0, len(params)):
            text += self.using_letters_set[params[i]]
        print("Started with:", text, "at thread ID:", id)


# cracker = Cracker("08cf04af4d3b7e903cb15582d02b7fce682f867f04e9b9a82ea719f6e7ecad63", 3, "")
cracker = Cracker("8338482d1dc4f7d3447b41fa646b354c2dce447c3028d087561d856a2b99d47b", 6, "ia!")
# cracker.ComparePasswordWithCurrent("xdd")

cracker.start_cracking_by_multi_tasking(10)
