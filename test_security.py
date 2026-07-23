import socket
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from render_contract import RenderRequest
from render_engine import (
    RenderLimits,
    ensure_dimensions,
    is_public_http_url,
    routed_headers,
)
from render_errors import RenderError


class SsrfTests(unittest.IsolatedAsyncioTestCase):
    @patch("render_engine.socket.getaddrinfo")
    async def test_private_address_is_blocked(self, getaddrinfo):
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))
        ]
        self.assertFalse(await is_public_http_url("https://example.com"))

    @patch("render_engine.socket.getaddrinfo")
    async def test_public_address_is_allowed(self, getaddrinfo):
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        ]
        self.assertTrue(await is_public_http_url("https://example.com"))

    @patch("render_engine.socket.getaddrinfo")
    async def test_mixed_dns_result_is_blocked(self, getaddrinfo):
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.1", 443)),
        ]
        self.assertFalse(await is_public_http_url("https://example.com"))


class HeaderRoutingTests(unittest.TestCase):
    def test_custom_headers_reach_same_origin(self):
        result = routed_headers(
            "https://example.com/page",
            "https://example.com",
            {"Accept": "text/html", "Authorization": "browser"},
            {"Authorization": "custom"},
        )
        self.assertEqual(result["Authorization"], "custom")
        self.assertEqual(result["Accept"], "text/html")

    def test_custom_headers_do_not_follow_cross_origin(self):
        result = routed_headers(
            "https://cdn.example.net/asset",
            "https://example.com",
            {"Accept": "image/*", "Authorization": "browser"},
            {"Authorization": "custom"},
        )
        self.assertNotIn("Authorization", result)
        self.assertEqual(result["Accept"], "image/*")


class ValidationTests(unittest.TestCase):
    def test_selector_requires_viewport_capture(self):
        with self.assertRaises(ValidationError):
            RenderRequest(url="https://example.com", selector="main")

    def test_managed_header_is_rejected(self):
        with self.assertRaises(ValidationError):
            RenderRequest(url="https://example.com", headers={"Host": "internal"})

    def test_valid_request(self):
        request = RenderRequest(
            url="https://example.com", full_page=False, selector="main"
        )
        self.assertEqual(request.source_type, "url")


class DimensionTests(unittest.TestCase):
    def test_dimensions_within_limits(self):
        ensure_dimensions(1280, 720, 1, RenderLimits())

    def test_dimension_limit_is_enforced(self):
        with self.assertRaisesRegex(RenderError, "output_dimensions_exceeded"):
            ensure_dimensions(
                2001, 1000, 1, RenderLimits(max_width=2000, max_height=1000)
            )

    def test_pixel_limit_is_enforced(self):
        with self.assertRaisesRegex(RenderError, "pixel_limit_exceeded"):
            ensure_dimensions(100, 100, 1, RenderLimits(max_pixels=9999))


if __name__ == "__main__":
    unittest.main()
