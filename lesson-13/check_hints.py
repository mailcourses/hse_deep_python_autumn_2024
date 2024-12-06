from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import (
    Any,
    Generator,
    Iterable,
    NewType,
    Protocol,
    runtime_checkable,
    Sequence,
    TypeVar,
)


DEBUG = True


@dataclass
class User:
    user_id: str
    age: int
    name: str

    def __bool__(self) -> bool:
        return self.user_id in {"123", "77", "789"}


@dataclass
class Person(User):
    pass


type UserData = dict[str, str | int]
type OptUserData = UserData | None  # Optional[UserData]


def fetch_url(url: str) -> UserData:
    return {
        "user_id": "123",
        "name": "Steve",
        "age": 77,
    }


def get_user_data(user: User) -> OptUserData:
    if not user:
        return None

    if DEBUG:
        url = f"https://python.org/555"
    else:
        url = f"https://python.org/{user.user_id}"

    data = fetch_url(url)

    return data


def run_get_user_data() -> None:
    user1 = User("123", 77, "Steve")
    data1: OptUserData = get_user_data(user1)
    print(f"{user1=} got data: {data1=}")

    user2 = Person("789", 55, "NotSteve")
    data2 = get_user_data(user2)
    print(f"{user2=} got data: {data2=}")

    user3 = User("42", 177, "Steve42")
    data3: OptUserData = get_user_data(user3)
    print(f"{user3=} got data: {data3=}")


Celsius = NewType("Celsius", float)
Fareng = NewType("Fareng", float)


def convert_c_to_f(temp: Celsius) -> Fareng:
    return Fareng(temp * 9 / 5 + 32)


def get_max_temp(temps: Iterable[Celsius]) -> Celsius | None:
    if not temps:
        return None

    return max(temps)


T = TypeVar("T")

def get_first_temp_generic(temps: Sequence[T]) -> T | None:
    if not temps:
        return None

    return temps[0]


def get_first_temp(temps: Sequence[Celsius]) -> Celsius | None:
    if not temps:
        return None

    return temps[0]


def create_gen_temps(start: Celsius) -> Generator[Celsius, None, str]:
    tmp = yield start
    yield Celsius(start + 10.0)
    yield Celsius(start + 5.0)

    return "finished"  # StopIteration("finished")


def run_temperatures() -> None:
    temp_c1 = Celsius(36.6)
    print(f"\nis Celsius: {Celsius is float=}, {type(temp_c1)}, {temp_c1 + 0.1=}")

    temp_f1 = convert_c_to_f(temp_c1)
    print(f"temperatures: {temp_c1=}, {temp_f1=}")

    temp_c2 = Celsius(-40)
    temp_f2 = convert_c_to_f(temp_c2)
    print(f"temperatures: {temp_c2=}, {temp_f2=}")

    temps_f = [Fareng(10.0), Fareng(20.0), Fareng(15.0)]
    max_temp_f: Fareng | None = get_first_temp_generic(temps_f)
    print(f"\nfirst temp faren: {max_temp_f=} of {temps_f=}")

    temps_s = ("sdf", "qwe", "rty")
    max_temp_s = get_first_temp_generic(temps_s)
    print(f"\nfirst temp str: {max_temp_s=} of {temps_s=}")

    temps1 = [Celsius(10.0), Celsius(20.0), Celsius(15.0)]
    max_temp1 = get_max_temp(temps1)
    print(f"\nmax temp: {max_temp1=} of {temps1=}")

    temps2 = (Celsius(10.0), Celsius(20.0), Celsius(30.0))
    max_temp2 = get_max_temp(temps2)
    print(f"\nmax temp: {max_temp2=} of {temps2=}")

    temps3 = create_gen_temps(Celsius(10.0))
    max_temp3 = get_max_temp(temps3)
    print(f"\nmax temp: {max_temp3=} of {temps3=}")

    temps4: list[Celsius] = []
    max_temp4 = get_max_temp(temps4)
    print(f"\nmax temp: {max_temp4=} of {temps4=}")

    tpl: tuple[int, int, str] = (1, 2, "123")

    first_temp1 = get_first_temp(temps1)
    print(f"\nfirst temp: {first_temp1=} of {temps1=}")

    first_temp2 = get_first_temp(temps2)
    print(f"\nfirst temp: {first_temp2=} of {temps2=}")

    # first_temp3 = get_first_temp(temps3)
    # print(f"\nfirst temp: {first_temp3=} of {temps3=}")

    first_temp4 = get_first_temp(temps4)
    print(f"\nfirst temp: {first_temp4=} of {temps4=}")


def deco_common(fn: Callable[..., T]) -> Callable[..., T]:
    def inner(*args: Any, **kwargs: Any) -> T:
        return fn(*args, **kwargs)
    return inner


def deco(fn: Callable[..., T]) -> Callable[..., T]:
    @wraps(fn)
    def inner(a: T, b: T) -> T:
        return fn(a, b)
    return inner


@deco
def add_int(a: int, b: int) -> int:
    return a + b


@deco
def add_str(a: str, b: str) -> str:
    return a + b


def run_functions() -> None:
    r1 = add_int(1, 2)
    print(f"\n{r1=}")

    r2 = add_str(1, 2)
    print(f"\n{r2=}")


@runtime_checkable
class Predictable(Protocol):
    def predict(self) -> float:
        ...


def calc_predict(model: Predictable) -> float:
    # return model.predict()
    return 0.1


class RandomForest:
    def predict(self) -> float:
        return 0.999


def run_protocol() -> None:
    forest = RandomForest()
    score = calc_predict(forest)
    print(f"\n{score=}")

    user = User("123", 55, "wqr")
    score_user = calc_predict(user)
    print(f"\n{score_user=}")

    print(f"{isinstance(forest, Predictable)=}, {isinstance(user, Predictable)=}")



if __name__ == "__main__":
    run_get_user_data()
    run_temperatures()
    run_functions()
    run_protocol()
