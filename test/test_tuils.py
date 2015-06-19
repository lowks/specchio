#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from specchio.utils import get_re_from_single_line


class GetReFromSingleLineTest(TestCase):

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_from_blank_line(self, _fnmatch):
        result = get_re_from_single_line(" ")
        self.assertEqual(result, (0, None))
        self.assertEqual(_fnmatch.translate.call_count, 0)

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_from_comment_line(self, _fnmatch):
        result = get_re_from_single_line("# too simple")
        self.assertEqual(result, (0, None))
        self.assertEqual(_fnmatch.translate.call_count, 0)

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_from_hash_line(self, _fnmatch):
        result = get_re_from_single_line("\\#2A00BF")
        self.assertEqual(result, (1, "2A00BF"))
        self.assertEqual(_fnmatch.translate.call_count, 0)

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_from_simple_line(self, _fnmatch):
        result = get_re_from_single_line("excited/*.*")
        self.assertEqual(result[0], 3)
        _fnmatch.translate.assert_called_with("excited/*.*")

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_with_negate_pattern(self, _fnmatch):
        result = get_re_from_single_line("!too_simple.py")
        self.assertEqual(result[0], 2)
        _fnmatch.translate.assert_called_with("too_simple.py")

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_with_double_asterisk(self, _fnmatch):
        result = get_re_from_single_line("young/**/simple/**/naive")
        self.assertEqual(result[0], 3)
        _fnmatch.translate.assert_called_with("young/*/simple/*/naive")

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_with_space(self, _fnmatch):
        result = get_re_from_single_line("too\\ young.py")
        self.assertEqual(result[0], 3)
        _fnmatch.translate.assert_called_with("too young.py")

    @mock.patch("specchio.utils.fnmatch")
    def test_get_re_with_head_slash(self, _fnmatch):
        result = get_re_from_single_line("/too_young.py")
        self.assertEqual(result[0], 3)
        _fnmatch.translate.assert_called_with("too_young.py")
