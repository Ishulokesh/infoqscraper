# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, Clément MATHIEU
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import shutil
import tempfile

from infoqscraper import cache

from infoqscraper.test.compat import unittest


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = cache.XDGCache()
        self.cache.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.cache.dir)

    def test_no_found_test(self):
        not_in_cache = "http://example.com/foo"
        self.assertIsNone(self.cache.get_path(not_in_cache))
        self.assertIsNone(self.cache.get_content(not_in_cache))

    def test_simple_content_add(self):
        url = "http://example.com/foo"
        content = b"content"
        self.assertIsNone(self.cache.get_path(url))
        self.cache.put_content(url, content)
        self.assertEqual(self.cache.get_content(url), content)
        with open(self.cache.get_path(url), 'rb') as f:
            self.assertEqual(f.read(), content)

    def test_simple_path_add(self):
        url = "http://example.com/foo"
        content = b"content"
        tmp = tempfile.mktemp()
        with open(tmp, 'wb') as f:
            f.write(content)

        self.assertIsNone(self.cache.get_path(url))
        self.cache.put_path(url, tmp)
        self.assertEqual(self.cache.get_content(url), content)
        with open(self.cache.get_path(url), 'rb') as f:
            self.assertEqual(f.read(), content)
        os.unlink(tmp)

    def test_update(self):
        url = "http://example.com/foo"
        content = b"V1"
        self.cache.put_content(url, content)
        self.assertEqual(self.cache.get_content(url), content)
        content = b"V2"
        self.cache.put_content(url, content)
        self.assertEqual(self.cache.get_content(url), content)
        content = b"V3"
        tmp = tempfile.mktemp()
        with open(tmp, 'wb') as f:
            f.write(content)
        self.cache.put_path(url, tmp)
        self.assertEqual(self.cache.get_content(url), content)

    def test_clear(self):
        url = "http://example.com/foo"
        content = b"V1"
        self.cache.put_content(url, content)
        self.assertEqual(self.cache.get_content(url), content)
        self.cache.clear()
        self.assertIsNone(self.cache.get_content(url))
        self.cache.put_content(url, content)
        self.assertEqual(self.cache.get_content(url), content)

    def test_size(self):
        url = "http://example.com/foo"
        content = b"x" * 1026
        self.cache.put_content(url, content)
        size = self.cache.size
        self.assertEqual(size, 1026)


