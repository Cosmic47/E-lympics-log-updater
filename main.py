from datetime import datetime

log_filename = "E-lympics.txt"
leaderboard_header = \
    """===== Leaderboard =====
Member: gold medals/silver medals/bronze medals
"""


def leaderboard_to_string(board):
    """
    :param board: literally just leaderboard but pycharm bitched about variable names shadowing
    :return: leaderboard ready to be written to file
    """
    max_str_len = 0
    for name, score in board.items():
        board[name] = '/'.join(map(str, score))  # mb actually do not do this
        entry_len = len(name) + len(board[name])
        if max_str_len < entry_len:
            max_str_len = entry_len

    output = ""
    for name, data in board.items():
        offset_length = max_str_len - (len(name) + len(data))
        output += name + ": " + ' ' * offset_length + data + '\n'
    return output


def create_log_string(first, second, third):
    """
    :param first: the first E-er
    :param second: the second E-er
    :param third: take a guess
    :return: new log entry with date and information about who won in what order
    """
    date_string = datetime.now().strftime("%d.%m.%Y")
    return f"{date_string}: {first} won a gold medal, {second} won a silver medal and {third} won a bronze medal."


def extract_data():
    """
    :return: leaderboard dict and log string
    """
    with open(log_filename, 'r') as file:
        file.readline()  # skip first two lines
        file.readline()

        leaderboard_data = {}
        while (line := file.readline()) != '\n':
            username, score_data = line.split()
            username = username[:-1]  # to remove : at the end
            score_array = list(map(int, score_data.split('/')))
            leaderboard_data[username] = score_array

        tours_data = file.read()[:-1]  # -1 to delete \n char at the end

    return leaderboard_data, tours_data


def update_winner(board, user, place):
    """
    :param board: leaderboard dictionary
    :param user: username that won some place
    :param place: what place did user take, int from 1 to 3
    :return: nothing, it literally just updates user place
    """
    if user not in board:
        board[user] = [0, 0, 0]
    board[user][place - 1] += 1


if __name__ == "__main__":
    leaderboard, tours = extract_data()

    name1 = input("Input the name of the first E-er: ")
    name2 = input("Input the name of the second E-er: ")
    name3 = input("Input the name of the third E-er: ")

    leaderboard[name1][0] += 1
    leaderboard[name2][1] += 1
    leaderboard[name3][2] += 1

    leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda i: i[1], reverse=True)}  # sort leaderboard

    new_leaderboard_string = leaderboard_to_string(leaderboard)
    new_log_string = create_log_string(name1, name2, name3)

    with open(log_filename, 'w') as log:
        log.write(leaderboard_header)
        log.write(new_leaderboard_string)
        log.write('\n')
        log.write(tours)
        log.write(new_log_string)
