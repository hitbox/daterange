import contextlib
import io
import sys
import unittest

from datetime import date
from datetime import timedelta

from daterange import daterange
from daterange import main

class TestDaterange(unittest.TestCase):

    def test_daterange_errors(self):
        # no arguments raises
        with self.assertRaises(TypeError):
            daterange()
        # must consume generator below here
        # extra arguments raises
        with self.assertRaises(TypeError):
            list(daterange(date(2021,1,24), date(2021,1,30), 1, 'extra', 'args'))
        # invalid types
        with self.assertRaises(TypeError):
            list(daterange(date(2021,1,24), date(2021,1,30), '1'))
        with self.assertRaises(TypeError):
            list(daterange('2021-01-24', date(2021,1,30), '1'))

    def test_daterange_stop_from_today(self):
        today = date.today()
        oneday = timedelta(days=1)
        a = list(daterange(today + oneday * 4))
        b = [today + oneday * i for i in range(4)]
        self.assertListEqual(a, b)

    def test_daterange_start_stop(self):
        a = list(daterange(date(2021,1,25), date(2021,1,28)))
        b = [date(2021,1,25), date(2021,1,26), date(2021,1,27)]
        self.assertListEqual(a, b)

    def test_daterange_start_stop_step(self):
        g = daterange(date(2021,1,25), date(2021,1,31), 3)
        a = list(g)
        b = [date(2021,1,25), date(2021,1,28)]
        self.assertListEqual(a, b)

    def test_daterange_start_after_stop_yield_nothing(self):
        g = daterange(date(2021,1,31), date(2021,1,24))
        a = list(g)
        b = []
        self.assertListEqual(a, b)

    def test_main_normal(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main(['2021-01-24', '2021-01-28'])
        a = output.getvalue()
        b = '2021-01-24\n2021-01-25\n2021-01-26\n2021-01-27'
        self.assertEqual(a, b)

    def test_main_separator(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main(['2021-01-24', '2021-01-28', '-z'])
        a = output.getvalue()
        b = '\0'.join(['2021-01-24', '2021-01-25', '2021-01-26', '2021-01-27'])
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
