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
                "--season_id=serie-a-brazil-2026"
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

@app.route("/time/<nome>")
def time_recente(nome):
    try:
        resultado = subprocess.run(
            [
                "sports-skills",
                "football",
                "get_season_standings",
                "--season_id=serie-a-brazil-2026"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if resultado.returncode != 0:
            return jsonify({
                "ok": False,
                "erro": resultado.stderr
            }), 500

        dados = json.loads(resultado.stdout)

        entries = (
            dados
            .get("data", {})
            .get("standings", [{}])[0]
            .get("entries", [])
        )

        nome_busca = nome.lower()

        for item in entries:
            time = item.get("team", {})

            if nome_busca in time.get("name", "").lower():
                return jsonify({
                    "ok": True,
                    "time": time
                })

        return jsonify({
            "ok": False,
            "erro": "Time não encontrado"
        }), 404

    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": str(e)
        }), 500

@app.route("/jogos/<nome>")
def jogos_time(nome):
    try:
        resultado = subprocess.run(
            [
                "sports-skills",
                "football",
                "get_team_schedule",
    "--team_id=2029",
    "--season_id=serie-a-brazil-2026"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if resultado.returncode != 0:
            return jsonify({
                "ok": False,
                "erro": resultado.stderr
            }), 500

        dados = json.loads(resultado.stdout)

        return jsonify(dados)

    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": str(e)
        }), 500
