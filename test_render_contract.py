import unittest

from pydantic import ValidationError

from render_contract import OutputFormat, RenderRequest


class RenderContractTest(unittest.TestCase):
    def test_url_image_request_is_supported(self):
        request = RenderRequest.model_validate(
            {
                "url": "https://example.com",
                "output": "png",
                "viewport": {
                    "width": 1280,
                    "height": 720,
                    "device_scale_factor": 1,
                },
            }
        )
        self.assertEqual(request.output, OutputFormat.PNG)

    def test_non_url_source_is_rejected(self):
        with self.assertRaises(ValidationError):
            RenderRequest.model_validate(
                {
                    "html": "<p>x</p>",
                    "output": "png",
                }
            )


if __name__ == "__main__":
    unittest.main()
