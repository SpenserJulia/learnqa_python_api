import requests
import pytest
import json

class TestUserAgentCheck:
    data = [
        (
            "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')",
            "Mobile",
            "No",
            "Android"
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            "Mobile",
            "Chrome",
            "iOS"
        ),
        (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Googlebot",
            "Unknown",
            "Unknown"
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "Web",
            "Chrome",
            "No"
        ),
        (
            "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "Mobile",
            "No",
            "iPhone"
        )
    ]

    @pytest.mark.parametrize('ua, platform, browser, device', data)
    def test_user_agent_check(self, ua, platform, browser, device):
        url = "https://playground.learnqa.ru/api/user_agent_check"

        response = requests.get(url, headers={"User-Agent": ua})

        print(f"{response.json()}")

        obj = json.loads(response.text)

        platform_from_response = obj.get("platform")
        browser_from_response = obj.get("browser")
        device_from_response = obj.get("device")

        assert platform_from_response == platform, f"Platform from response '{platform_from_response}' 'is not equal '{platform}'"
        assert browser_from_response == browser, f"Browser from response '{browser_from_response}' is not equal '{browser}'"
        assert device_from_response == device, f"Platform from response '{device_from_response}' is not equal '{device}'"

        # AssertionError: Browser from response 'No' is not equal 'Chrome'
        # AssertionError: Platform from response 'Unknown' 'is not equal 'Googlebot'
        # AssertionError: Platform from response 'Unknown' is not equal 'iPhone'
