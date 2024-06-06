from flask import Flask, request, redirect, session, jsonify, url_for
import requests
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "your_secret_key"

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
OPENAI_API_KEY = ""

openai.api_key = OPENAI_API_KEY


@app.route("/login")
def login():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}"
    )
    print(f"Redirecting to GitHub OAuth URL: {github_auth_url}")
    return redirect(github_auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        print("No code parameter in the callback URL")
        return jsonify({"error": "No code parameter in the callback URL"}), 400

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )

    if token_response.status_code != 200:
        print(
            f"Failed to get access token from GitHub, status code: {token_response.status_code}"
        )
        return jsonify({"error": "Failed to get access token from GitHub"}), 400

    token_json = token_response.json()
    if "access_token" not in token_json:
        print("No access_token in the response from GitHub")
        return jsonify({"error": "No access_token in the response from GitHub"}), 400

    session["github_token"] = token_json["access_token"]
    print("GitHub access token received and stored in session")
    return redirect("http://localhost:3000/repositories")


@app.route("/repositories")
def repositories():
    if "github_token" not in session:
        print("User not authenticated")
        return jsonify({"error": "User not authenticated"}), 401

    headers = {"Authorization": f'token {session["github_token"]}'}
    repos_response = requests.get("https://api.github.com/user/repos", headers=headers)

    if repos_response.status_code != 200:
        print(
            f"Failed to fetch repositories from GitHub, status code: {repos_response.status_code}"
        )
        return jsonify({"error": "Failed to fetch repositories from GitHub"}), 400

    return jsonify(repos_response.json())


@app.route("/create-webhook", methods=["POST"])
def create_webhook():
    if "github_token" not in session:
        print("User not authenticated")
        return jsonify({"error": "User not authenticated"}), 401

    repo = request.json["repo"]
    webhook_url = "https://8722-2405-201-2000-d8a5-dc35-255-4597-2511.ngrok-free.app/webhook"  # Make sure this URL is correctly set
    headers = {"Authorization": f'token {session["github_token"]}'}
    data = {
        "name": "web",
        "active": True,
        "events": ["push"],
        "config": {"url": webhook_url, "content_type": "json"},
    }
    print(f"Creating webhook for repo: {repo} with data: {data}")
    response = requests.post(
        f"https://api.github.com/repos/{repo}/hooks", json=data, headers=headers
    )

    if response.status_code != 201:
        print(
            f"Failed to create webhook, status code: {response.status_code}, response: {response.json()}"
        )
        return jsonify({"error": "Failed to create webhook"}), 400

    return jsonify(response.json())


@app.route("/abc", methods=["POST"])
def abc():
    print("Hello")


@app.route("/webhook", methods=["POST"])
def webhook():
    print(request.json)
    # payload = request.json
    # commits = payload["commits"]
    # for commit in commits:
    #     review_code(commit["modified"])
    return "", 204


def review_code(files):
    for file in files:
        # Fetch the file content from GitHub and review it
        pass


if __name__ == "__main__":
    app.run(port=5000)
