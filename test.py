
def my_help():
    print("Help")

requests = {
    'help': my_help
}

if __name__ == "__main__":
    requests['help']()