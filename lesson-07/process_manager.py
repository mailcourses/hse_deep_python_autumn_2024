import multiprocessing as mp


class Person:
    def __init__(self, name):
        self.name = name


def update(data: dict):
    print("update start", data)

    data[(1, "to_up")] = "updated"
    data["value"] = 42
    data["steve"] = Person("Steve")

    print("update finish", data)


if __name__ == "__main__":
    data = {(1, "to_up"): "initial"}
    print("data before update:", data)

    pr = mp.Process(target=update, args=(data,))
    pr.start()
    pr.join()

    print("data after update:", data)
    print("\n---------\n")

    with mp.Manager() as manager:
        data = manager.dict()
        data[(1, "to_up")] = "initial"

        print("data before update:", data)

        pr = mp.Process(target=update, args=(data,))
        pr.start()
        pr.join()

        print("data after update:", data)

