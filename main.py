from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello():
	return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Something wonderful begins here</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, #111827, #312e81);
            color: #f8fafc;
            font-family: system-ui, sans-serif;
        }
        main {
            margin: 24px;
            padding: clamp(24px, 6vw, 64px);
            max-width: 640px;
            text-align: center;
            border: 1px solid #ffffff30;
            border-radius: 24px;
            background: #ffffff0d;
            box-shadow: 0 24px 80px #00000040;
        }
        .eyebrow { color: #c4b5fd; letter-spacing: 0.2em; text-transform: uppercase; }
        h1 { font-size: clamp(2rem, 6vw, 3.5rem); line-height: 1.1; }
        .subtitle { color: #cbd5e1; font-size: 1.15rem; line-height: 1.7; }
    </style>
</head>
<body>
    <main>
        <p class="eyebrow">Welcome to your next chapter</p>
        <h1>Something wonderful begins here.</h1>
        <p class="subtitle">Big ideas start with a simple hello. Let's build something extraordinary.</p>
    </main>
</body>
</html>
"""


if __name__ == "__main__":
	app.run()
