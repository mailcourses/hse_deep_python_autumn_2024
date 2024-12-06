import unittest

import capi_fibs


class TestCApiFibs(unittest.TestCase):
    def test_rec_fib(self):
        self.assertEqual(1, capi_fibs.fib_rec_api(1))
        self.assertEqual(1, capi_fibs.fib_rec_api(2))
        self.assertEqual(2, capi_fibs.fib_rec_api(3))
        self.assertEqual(3, capi_fibs.fib_rec_api(4))
        self.assertEqual(6765, capi_fibs.fib_rec_api(20))

    def test_rec_iter(self):
        self.assertEqual(1, capi_fibs.fib_iter_api(1))
        self.assertEqual(1, capi_fibs.fib_iter_api(2))
        self.assertEqual(2, capi_fibs.fib_iter_api(3))
        self.assertEqual(3, capi_fibs.fib_iter_api(4))
        self.assertEqual(6765, capi_fibs.fib_iter_api(20))
