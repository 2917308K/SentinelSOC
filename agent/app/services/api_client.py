import requests

from app.config import API_URL, AGENT_API_KEY


class SentinelAPIClient:
    def __init__(self):
        self.base_url = API_URL.rstrip("/")

        self.headers = {
            "Content-Type": "application/json",
        }

        if AGENT_API_KEY:
            self.headers["X-Agent-Key"] = AGENT_API_KEY

    def send_event(self, event: dict) -> bool:
        

        try:
            response = requests.post(
                f"{self.base_url}/events/",
                json=event,
                headers=self.headers,
                timeout=10,
            )

            response.raise_for_status()

            return True

        except requests.RequestException as exc:
            print(
                f"Failed to send event to SentinelSOC: {exc}"
            )

            return False

    def register_endpoint(
        self,
        endpoint: dict,
    ) -> bool:
        

        try:
            response = requests.post(
                f"{self.base_url}/endpoints/register",
                json=endpoint,
                headers=self.headers,
                timeout=10,
            )

            response.raise_for_status()

            return True

        except requests.RequestException as exc:
            print(
                f"Failed to register endpoint: {exc}"
            )

            return False

    def send_events(self, events: list[dict]) -> bool:

        if not events:
            return True

        try:
            response = requests.post(
                f"{self.base_url}/events/batch",
                json=events,
                headers=self.headers,
                timeout=10,
            )

            response.raise_for_status()

            return True

        except requests.RequestException as exc:
            print(
                f"Failed to send event batch to SentinelSOC: {exc}"
            )

            return False