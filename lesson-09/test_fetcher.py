import asyncio
from functools import partial
import time
import unittest
from unittest import mock

import fetcher as ft


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    # async def asyncSetUp(self):
    #     print("asyncSetUp")
    #
    # async def asyncTearDown(self):
    #     print("asyncTearDown")

    async def test_fetch_url(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as cl_mock:
            text_mock = mock.AsyncMock(return_value="orig_resp")
            resp_mock = mock.AsyncMock(text=text_mock)
            cl_mock.return_value.__aenter__.return_value = resp_mock

            result = await ft.fetch_url("fake_url")

            self.assertEqual("orig_resp", result)

            expected_calls = [
                mock.call("fake_url"),
                mock.call().__aenter__(),
                mock.call().__aenter__().text(),
                mock.call().__aexit__(None, None, None),
            ]
            self.assertEqual(expected_calls, cl_mock.mock_calls)

    async def test_fetch_url_with_error(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as cl_mock:
            cl_mock.side_effect = ValueError("Connection lost")

            with self.assertRaises(ValueError) as err:
                await ft.fetch_url("fake_url")

            expected_calls = [
                mock.call("fake_url"),
            ]
            self.assertEqual(expected_calls, cl_mock.mock_calls)

    async def test_fetch_batch_urls(self):
        urls = ["url1", "url2", "url3"]

        with mock.patch("fetcher.aiohttp.ClientSession.get") as cl_mock:
            text_mock = mock.AsyncMock(side_effect=[f"resp_{url}" for url in urls])
            resp_mock = mock.AsyncMock(text=text_mock)
            cl_mock.return_value.__aenter__.return_value = resp_mock

            result = await ft.fetch_batch_urls(urls)

            self.assertEqual(["resp_url1", "resp_url2", "resp_url3"], result)

            expected_calls = []
            for url in urls:
                expected_calls.extend(
                    [
                        mock.call(url),
                        mock.call().__aenter__(),
                        mock.call().__aenter__().text(),
                        mock.call().__aexit__(None, None, None),
                    ]
                )

            self.assertEqual(expected_calls, cl_mock.mock_calls)

    async def get_fetch_batch_time(self, urls, delay_time):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as cl_mock:
            text_mock = mock.AsyncMock(
                side_effect=partial(asyncio.sleep, delay_time)
            )
            resp_mock = mock.AsyncMock(text=text_mock)
            cl_mock.return_value.__aenter__.return_value = resp_mock

            tstart = time.time()
            await ft.fetch_batch_urls(urls)
            tfin = time.time()

            cl_mock.assert_has_calls(
                [mock.call(url) for url in urls],
                any_order=True,
            )
            self.assertLess(tstart, tfin)

            return tfin - tstart

    async def test_fetch_batch_timing(self):
        delay_time = 1.0
        total_times = []

        for n in (1, 3, 10, 100):
            urls = [f"url{k}" for k in range(n)]
            tt = await self.get_fetch_batch_time(urls, delay_time)
            total_times.append(tt)

        for tt in total_times:
            self.assertLess(delay_time, tt)
            self.assertLess(tt, delay_time * 2)


if __name__ == "__main__":
    unittest.main()
