def dp_change(money, coins):
    min_num_coins = [0 for i in range(0, money + 1)]
    for m in range(1, money + 1):
        min_num_coins[m] = 99999999999999
        for i in range(0, len(coins)):
            coin = coins[i]
            if m >= coin:
                if min_num_coins[m - coin] + 1 < min_num_coins[m]:
                    min_num_coins[m] = min_num_coins[m - coin] + 1
    return max(min_num_coins)


if __name__ == "__main__":
    data = "".join(open('change_problem.txt')).split()
    money = int(data[0])
    coins = list(map(int, data[1].split(',')))
    print(dp_change(money, coins))
