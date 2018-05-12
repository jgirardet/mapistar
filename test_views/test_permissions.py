import pytest
import json


class TestIsAuthenticated:

    @pytest.mark.pony
    def test_no_header(self, cli_anonymous, app):
        r = cli_anonymous.get(app.reverse_url("patients:liste"))
        assert r.status_code == 401
        assert r.json() == "Authorization header is missing."

    @pytest.mark.pony
    def test_bad_jwt(self, cli, app):
        head = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLmIq4o8Q"}
        r = cli.get(app.reverse_url("patients:liste"), headers=head)
        assert r.json() == "Incorrect authentication credentials."

    @pytest.mark.pony
    def test_pass(self, cli, app, user):
        r = cli.post(
            app.reverse_url("users:login"),
            data=json.dumps({"username": user.username, "password": "j"}),
        )
        token = r.content.decode()
        head = {"Authorization": f"Bearer {token}"}
        r = cli.get(app.reverse_url("patients:liste"), headers=head)
        assert r.status_code == 200
