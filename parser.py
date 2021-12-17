def parse_file(filename):
    with open(filename) as file:
        data = file.read().split("\n")

    data = [i.replace("(1-t)^3", "")
                .replace("t(1-t)^2", "")
                .replace("t^2(1-t)", "")
                .replace("t^3", "")
                .replace("(1-t)", "")
                .replace("t", "")
                .replace(" + ", " ")
                .replace(" - ", " -")
                .replace("(", "")
                .replace(")", "")
                .split(", ") for i in data]

    x_s = []
    y_s = []

    for row in data:
        x_k = [float(i) for i in row[0].split()]
        y_k = [float(i) for i in row[1].split()]
        for t in range(100):
            x = 0
            for i in range(len(x_k))[::-1]:
                x += x_k[i] * (t / 100) ** i * (1 - t / 100) ** (len(y_k) - 1 - i)
            y = 0
            for i in range(len(y_k))[::-1]:
                y += y_k[i] * (t / 100) ** i * (1 - t / 100) ** (len(y_k) - 1 - i)
            x_s.append(x)
            y_s.append(y)

    return x_s, y_s

