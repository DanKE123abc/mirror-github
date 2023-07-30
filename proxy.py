import re
from mitmproxy import http


class RedirectAddon:
    def __init__(self):
        self.redirect_mappings = {
            "github.com": "github.dkdk.eu.org",
            "api.github.com": "api.github.dkdk.eu.org",
            # "raw.githubusercontent.com": "raw.githubusercontent.dkdk.eu.org",
            "github.githubassets.com": "github.githubassets.dkdk.eu.org",
            "avatars.githubusercontent.com": "avatars.githubusercontent.dkdk.eu.org",
            "alive.github.com": "alive.github.dkdk.eu.org"
        }

    def redirect_host(self, flow: http.HTTPFlow) -> None:
        host = flow.request.pretty_host
        if host in self.redirect_mappings:
            new_host = self.redirect_mappings[host]
            flow.request.host = new_host
            flow.request.headers["Host"] = new_host
            if "Referer" in flow.request.headers:
                flow.request.headers["Referer"] = re.sub(
                    f"https://{host}", f"https://{new_host}", flow.request.headers["Referer"]
                )
            print(f"Redirected host: {host} -> {new_host}")

    def redirect_location(self, flow: http.HTTPFlow) -> None:
        host = flow.request.pretty_host
        if host in self.redirect_mappings:
            new_host = self.redirect_mappings[host]
            flow.response.headers["Location"] = re.sub(
                f"https://{host}", f"https://{new_host}", flow.response.headers["Location"]
            )
            print(f"Redirected location: {flow.response.headers['Location']}")

    def request(self, flow: http.HTTPFlow) -> None:
        if flow.request.pretty_host in self.redirect_mappings:
            self.redirect_host(flow)

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.request.pretty_host in self.redirect_mappings:
            self.redirect_location(flow)


addons = [
    RedirectAddon()
]
