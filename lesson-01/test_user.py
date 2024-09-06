import unittest
from unittest import mock

from user import User


class TestUser(unittest.TestCase):

    def test_init(self):
        user = User("login", 42)

        self.assertEqual("login", user.name)
        self.assertEqual(42, user.age)

    def test_greetings(self):
        user = User("login", 42)

        self.assertEqual("login", user.name)
        self.assertEqual("Hello, login!", user.greetings())

    def test_birthday(self):
        user = User("login", 42)

        self.assertEqual(42, user.age)
        self.assertEqual(43, user.birthday())

        self.assertEqual(43, user.age)

    def test_get_friends_not_work(self):
        user = User("login", 42)

        with self.assertRaises(NotImplementedError):
            user.get_friends()

    def test_get_friends_empty(self):
        user = User("login", 42)

        with mock.patch("user.fetch_vk_api") as mock_fetch:
            mock_fetch.return_value = []

            self.assertEqual([], user.get_friends())
            self.assertEqual(
                [mock.call("/friends", "login", part=None)],
                mock_fetch.mock_calls,
            )

            self.assertEqual([], user.get_friends("some"))
            self.assertEqual(
                [
                    mock.call("/friends", "login", part=None),
                    mock.call("/friends", "login", part="SOME"),
                ],
                mock_fetch.mock_calls,
            )

    def test_get_friends_single(self):
        user = User("login", 42)

        with mock.patch("user.fetch_vk_api") as mock_fetch:
            mock_fetch.return_value = ["password"]

            self.assertEqual(["password"], user.get_friends())
            self.assertEqual(
                [mock.call("/friends", "login", part=None)],
                mock_fetch.mock_calls,
            )

            self.assertEqual([], user.get_friends("some"))
            self.assertEqual(
                [
                    mock.call("/friends", "login", part=None),
                    mock.call("/friends", "login", part="SOME"),
                ],
                mock_fetch.mock_calls,
            )

            self.assertEqual(["password"], user.get_friends("pass"))
            self.assertEqual(
                [
                    mock.call("/friends", "login", part=None),
                    mock.call("/friends", "login", part="SOME"),
                    mock.call("/friends", "login", part="PASS"),
                ],
                mock_fetch.mock_calls,
            )

    def test_get_friends_many(self):
        user = User("login", 42)

        with mock.patch("user.fetch_vk_api") as mock_fetch:
            mock_fetch.side_effect = [
                ["password", "qwerty"],
                ["password", "asdf"],
                ["qwerty", "asdf"],
            ]

            self.assertEqual(["password", "qwerty"], user.get_friends())
            self.assertEqual(
                [mock.call("/friends", "login", part=None)],
                mock_fetch.mock_calls,
            )

            self.assertEqual(["password", "asdf"], user.get_friends("a"))
            self.assertEqual(
                [
                    mock.call("/friends", "login", part=None),
                    mock.call("/friends", "login", part="A"),
                ],
                mock_fetch.mock_calls,
            )

            self.assertEqual(["qwerty", "asdf"], user.get_friends())
            self.assertEqual(
                [
                    mock.call("/friends", "login", part=None),
                    mock.call("/friends", "login", part="A"),
                    mock.call("/friends", "login", part=None),
                ],
                mock_fetch.mock_calls,
            )

    @mock.patch("user.fetch_vk_api")
    def test_get_friends_with_error(self, mock_fetch):
        user = User("login", 42)

        mock_fetch.return_value = ["password"]

        self.assertEqual(["password"], user.get_friends())
        self.assertEqual(
            [mock.call("/friends", "login", part=None)],
            mock_fetch.mock_calls,
        )

        mock_fetch.side_effect = Exception("wrong")

        with self.assertRaises(Exception) as err:
            user.get_friends("some")

        self.assertEqual("wrong", str(err.exception))
        self.assertEqual(
            [
                mock.call("/friends", "login", part=None),
                mock.call("/friends", "login", part="SOME"),
            ],
            mock_fetch.mock_calls,
        )

    @mock.patch("user.fetch_vk_api")
    def test_get_friends_with_lambda(self, mock_fetch):
        user = User("login", 42)

        mock_fetch.side_effect = lambda *a, **k: ["password"]

        self.assertEqual(["password"], user.get_friends())
        self.assertEqual(
            [
                mock.call("/friends", "login", part=None),
            ],
            mock_fetch.mock_calls,
        )

        self.assertEqual(["password"], user.get_friends("pass"))
        self.assertEqual(
            [
                mock.call("/friends", "login", part=None),
                mock.call("/friends", "login", part="PASS"),
            ],
            mock_fetch.mock_calls,
        )

        self.assertEqual([], user.get_friends("err"))
        self.assertEqual(
            [
                mock.call("/friends", "login", part=None),
                mock.call("/friends", "login", part="PASS"),
                mock.call("/friends", "login", part="ERR"),
            ],
            mock_fetch.mock_calls,
        )
