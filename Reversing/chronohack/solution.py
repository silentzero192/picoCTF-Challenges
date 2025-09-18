import socket
import time
import random
import sys


def get_random(length, seed):
    """Generate a random token with the given seed and length."""
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(seed)
    return "".join(random.choice(alphabet) for _ in range(length))


def connect_and_guess(
    start_seed_index, seeds, offsets, Ts, host, port, token_length, max_attempts
):
    """Connect to the server and attempt to guess the token starting from start_seed_index."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        response = client_socket.recv(4096).decode("utf-8")
        print("Server response:")
        print(response)
        T_welcome = int(time.time() * 1000)

        if start_seed_index == 0:
            dummy_guess = "dummy"
            T_send = int(time.time() * 1000)
            client_socket.send((dummy_guess + "\n").encode("utf-8"))
            reply = client_socket.recv(4096).decode("utf-8")
            T_receive = int(time.time() * 1000)
            print("Dummy guess reply:")
            print(reply)
            RTT = T_receive - T_send
            one_way_delay = RTT / 2
            Ts[0] = T_welcome - one_way_delay
            print(f"Estimated Ts: {Ts[0]}, RTT: {RTT}, Delay: {one_way_delay}")
        else:

            Ts[0] = T_welcome
            print(f"Reconnection Ts: {Ts[0]}")

        print(f"Testing seeds around Ts={Ts[0]} ms")
        print(f"Total seeds to try: {len(seeds)}")
        print(f"Starting at offset: {offsets[start_seed_index]} ms")
        print(f"Starting at seed: {seeds[start_seed_index]}")

        attempts_made = 0
        for i in range(start_seed_index, len(seeds)):
            if attempts_made >= max_attempts - (1 if start_seed_index == 0 else 0):
                print("Reached 50 attempt limit. Will reconnect.")
                return i

            seed = seeds[i]
            offset = offsets[i]
            guess = get_random(token_length, seed)
            print(f"Attempt {attempts_made + 1}: Trying {guess} (Offset: {offset} ms)")
            client_socket.send((guess + "\n").encode("utf-8"))
            reply = client_socket.recv(4096).decode("utf-8")
            print("Server reply:")
            print(reply)
            attempts_made += 1

            if "Congratulations" in reply or "flag" in reply.lower():
                print("Success! The correct token was:", guess)
                client_socket.close()
                print("Connection closed")
                sys.exit(0)

        return len(seeds)

    except Exception as e:
        print(f"An error occurred: {e}")
        return start_seed_index

    finally:
        client_socket.close()
        print("Connection closed")


def main():
    # Server details
    HOST = "verbal-sleep.picoctf.net"
    PORT = 51348  # Change the port HERE
    token_length = 20
    max_attempts = 50
    range_start_ms = -50  # Start at Ts - 50 ms
    range_end_ms = 1000  # End at Ts + 1000 ms

    Ts = [0]

    offsets = list(range(range_start_ms, range_end_ms + 1))
    seeds = [0] * len(offsets)
    print(f"Total seeds to try: {len(seeds)}")

    start_seed_index = 0
    while start_seed_index < len(seeds):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST, PORT))
            response = client_socket.recv(4096).decode("utf-8")
            T_welcome = int(time.time() * 1000)
            client_socket.close()

            Ts[0] = T_welcome
            seeds = [int(T_welcome + offset) for offset in offsets]
            print(f"Initial Ts for connection: {Ts[0]}")

            result = connect_and_guess(
                start_seed_index,
                seeds,
                offsets,
                Ts,
                HOST,
                PORT,
                token_length,
                max_attempts,
            )
            if result == -1:
                break
            start_seed_index = result
            if start_seed_index < len(seeds):
                print(
                    f"Reinitiating connection to try seeds starting from index {start_seed_index} (Offset: {offsets[start_seed_index]} ms)"
                )
                time.sleep(1)

        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(1)

    if start_seed_index >= len(seeds):
        print("Exhausted all seeds without finding the correct token.")


if __name__ == "__main__":
    main()
