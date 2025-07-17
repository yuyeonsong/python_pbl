import requests

APP_ID = "a8414e0ad4fe40d1a664e4c57bb091b6"
CURRENCIES = ['USD', 'KRW', 'JPY', 'EUR', 'CNY', 'GBP', 'CAD', 'AUD', 'CHF', 'SGD']

def get_rates(app_id):
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']
    
    except requests.exceptions.RequestException:
        return None

def show_currencies(rates, target_currencies):
    print("=" * 60)
    print("선택 가능한 통화 리스트")
    for code in target_currencies:
        if code in rates:
            print(f"- {code}")
        else:
            print(f"- {code} 입력하신 통화의 정보를 찾을 수 없습니다.")
    print("=" * 60)

def get_input(message, options=None):
    while True:
        user_input = input(message).upper()
        if options:
            if user_input in options:
                return user_input
            else:
                print("해당 통화는 지원되지 않습니다. 목록에서 골라주세요.")

        else:
            if user_input:
                return user_input
            else:
                print("입력되지않았습니다. 다시 입력해주세요.")

def calc_money(amount, from_rate, to_rate):
    amount_in_usd = amount / from_rate
    exchanged = amount_in_usd * to_rate
    
    return exchanged

def main():

    print("="*20, "환율 계산기 프로그램", "=" * 20)

    rates_data = get_rates(APP_ID)
    show_currencies(rates_data, CURRENCIES)

    while True:
        from_money = get_input("변환할 통화를 입력해주세요: ", CURRENCIES)
        to_money = get_input("목표 통화를 입력해주세요: ", CURRENCIES)

        if from_money not in rates_data or to_money not in rates_data:
            print("선택하신 통화 중 일부가 유효하지 않습니다. 다시 시도해주세요.")
        else:
            try:
                amount_to_exchange = int(input(f"{from_money}로 환전할 금액을 입력해주세요: "))
                if amount_to_exchange <= 0:
                    print("금액을 0보다 크게 입력해주세요.")
                else:
                    from_rate = rates_data[from_money]
                    to_rate = rates_data[to_money]

                    result_amount = calc_money(amount_to_exchange, from_rate, to_rate)

                    print("="*20, "환전 결과", "="*20)
                    print(f"{from_money} {amount_to_exchange:,.0f}은 약 {to_money} {result_amount:,.0f} 정도입니다.")
                    print("환율 계산기를 이용해주셔서 감사합니다.")
                    print("프로그램을 종료합니다.")
                    print("="*52)

            except ValueError:
                print("유효한 숫자를 입력해주세요.")

            break

if __name__ == "__main__":
    main()
