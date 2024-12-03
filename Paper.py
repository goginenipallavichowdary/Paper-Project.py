import time
import random
import matplotlib.pyplot as plt

def is_prime_trial_div(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    divisor = 5
    while divisor * divisor <= n:
        if n % divisor == 0 or n % (divisor + 2) == 0:
            return False
        divisor += 6
    return True

def generate_primes_eratosthenes(limit):
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    current = 2
    while current * current <= limit:
        if sieve[current]:
            for multiple in range(current * current, limit + 1, current):
                sieve[multiple] = False
        current += 1
    return [idx for idx, is_prime in enumerate(sieve) if is_prime]

def is_prime_fermat_test(value, iterations=7):
    if value <= 1:
        return False
    if value <= 3:
        return True
    for _ in range(iterations):
        base = random.randint(2, value - 2)
        if pow(base, value - 1, value) != 1:
            return False
    return True

def is_prime_miller_rabin_test(num, rounds=7):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0:
        return False

    def miller_trial(d, num):
        base = random.randint(2, num - 2)
        x = pow(base, d, num)
        if x == 1 or x == num - 1:
            return True
        while d != num - 1:
            x = (x * x) % num
            d *= 2
            if x == 1:
                return False
            if x == num - 1:
                return True
        return False

    d = num - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(rounds):
        if not miller_trial(d, num):
            return False
    return True

def time_algorithm(func, test_input):
    start = time.time()
    try:
        result = func(test_input)
    except Exception:
        result = None
    elapsed = time.time() - start
    return result, elapsed

if __name__ == "__main__":
    test_value = 10**5 + 1
    test_runs = 15

    print(f"Performance comparison of primality testing algorithms over {test_runs} runs for number {test_value}:")

    methods = [
        ("Trial Division", is_prime_trial_div),
        ("Sieve of Eratosthenes", lambda x: test_value in generate_primes_eratosthenes(x)),
        ("Fermat's Primality Test", is_prime_fermat_test),
        ("Miller-Rabin Test", is_prime_miller_rabin_test)
    ]

    avg_times = []
    for method_name, method in methods:
        cumulative_time = 0
        for _ in range(test_runs):
            _, duration = time_algorithm(method, test_value)
            cumulative_time += duration
        mean_time = cumulative_time / test_runs
        print(f"{method_name}: Average Execution Time = {mean_time:.6f} seconds")
        avg_times.append(mean_time)

    
    plt.figure(figsize=(10, 6))
    plt.bar([name for name, _ in methods], avg_times, color='coral')
    plt.xlabel('Algorithms for Primality Testing')
    plt.ylabel('Mean Execution Time (seconds)')
    plt.title(f'Performance of Primality Testing Algorithms ({test_runs} runs, value = {test_value})')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('primality_testing_comparison_updated.png')  
    plt.show()
