import random

def number_game():
    number = random.randint(1, 100)
    guess = 0
    attempts = 0

    print("---")
    print("1부터 100까지의 숫자 중 제가 생각한 숫자를 맞춰보세요!")
    print("---")

    while guess != number:
        try:
            guess = int(input("어떤 숫자일까요? 숫자를 입력해주세요: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("숫자는 1부터 100까지만 입력할 수 있습니다. 다시 시도해주세요!")
            elif guess < number:
                print(f"{guess}은 생각한 숫자보다 작습니다. 좀 더 큰 수를 입력해주세요!")
            elif guess > number:
                print(f"{guess}은 생각한 숫자보다 큽니다. 좀 더 작은 수를 입력해주세요!")
            else:
                print(f"정답입니다! {attempts}번 시도 끝에 성공하셨습니다! 생각한 숫자는 바로 {number}이었습니다!")

        except ValueError:
            print("숫자만 입력할 수 있어요! 다시 시도해주세요.")
        print("---")

# 게임 시작
number_game()