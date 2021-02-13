def win_print(msg):
    print(f"{msg}".encode('cp932', 'ignore').decode('cp932'), flush=True)
