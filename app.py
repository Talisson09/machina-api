from flask import Flask, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "ok": True,
        "mensagem": "Machina API funcionando"
    })

@app.route("/brasileirao")
def brasileirao():
    try:
        resultado = subprocess.run(
            [
                "sports-skills",
                "football",
                "get_season_standings",
                "--season_id=serie-a-brazil-2026",
                "--json"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if resultado.returncode != 0:
            return jsonify({
                "ok": False,
                "erro": resultado.stderr
            }), 500

        return jsonify(json.loads(resultado.stdout))

    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": str(e)
        }), 500
