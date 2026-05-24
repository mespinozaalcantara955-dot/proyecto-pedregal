from flask import Flask, render_template_string, url_for

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Barrio Pedregal - Ruta de Recolección</title>

    <style>
        * {
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #050505;
            color: white;
            overflow-x: hidden;
        }

        /* PORTADA CON PLANETA DE FONDO */
        .portada {
            min-height: 100vh;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: #000;
        }

         .video-fondo {
           position: absolute;
           top: 0;
           left: -8%;
           width: 116%;
           height: 100%;
           object-fit: cover;
           z-index: 1;
           opacity: 1;
           filter: brightness(1.35) contrast(1.25) saturate(1.25);
         }

        .capa-oscura {
            position: absolute;
            inset: 0;
            background: rgba(0, 0, 0, 0.10);
            z-index: 2;
        }

        .contenido-portada {
            position: relative;
            z-index: 3;
            width: 90%;
            max-width: 900px;
            text-align: center;
            padding: 40px;
            border-radius: 25px;
            background: rgba(0, 0, 0, 0.35);
            box-shadow: 0 0 45px rgba(0, 255, 150, 0.25);
        }

        .contenido-portada h1 {
            font-size: 52px;
            margin-bottom: 15px;
            text-shadow: 0 0 18px #00ff99;
        }

        .contenido-portada p {
            font-size: 23px;
            color: #d8f7ff;
            margin-bottom: 35px;
        }

        .panel-busqueda {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 22px;
        }

        .titulo-buscar {
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .input-barrio {
            width: 360px;
            max-width: 90%;
            padding: 18px 25px;
            border: 2px solid #00ff99;
            outline: none;
            border-radius: 18px;
            font-size: 26px;
            text-align: center;
            background: rgba(220, 225, 245, 0.92);
            color: #111;
            box-shadow: 0 0 30px rgba(0, 255, 200, 0.65);
        }

        .boton {
            width: 360px;
            max-width: 90%;
            min-height: 90px;
            background: #8fd2a4;
            border: none;
            border-radius: 0 0 25px 0;
            color: white;
            font-size: 34px;
            font-weight: bold;
            line-height: 0.95;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(0, 255, 120, 0.35);
            transition: 0.3s;
        }

        .boton:hover {
            transform: scale(1.04);
            background: #00c853;
        }

        .mensaje {
            color: #ffdddd;
            font-size: 18px;
            margin-top: 15px;
            display: none;
        }

        /* MAPA OCULTO AL INICIO */
        .zona-mapa {
            display: none;
            min-height: 100vh;
            background: radial-gradient(circle at center, #082018, #030303);
            padding: 45px 20px;
            text-align: center;
        }

        .zona-mapa h2 {
            font-size: 38px;
            margin-bottom: 8px;
            text-shadow: 0 0 12px #00ff99;
        }

        .zona-mapa p {
            font-size: 21px;
            color: #d8d8d8;
        }

        .contenedor-mapa {
            position: relative;
            width: 760px;
            max-width: 95%;
            margin: 25px auto;
        }

        .mapa {
            width: 100%;
            border-radius: 8px;
            border: 3px solid #00c853;
            box-shadow: 0 0 35px rgba(0, 255, 120, 0.35);
            display: block;
        }

        .ruta-svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: visible;
            pointer-events: none;
            z-index: 10;
        }

        .panel-info {
            margin: 30px auto 0;
            max-width: 900px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }

        .info {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(0,255,120,0.45);
            border-radius: 12px;
            padding: 13px;
            text-align: center;
            font-size: 15px;
        }

        .volver {
            margin-top: 30px;
            display: inline-block;
            background: #00c853;
            color: white;
            padding: 14px 28px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
        }

        @media (max-width: 800px) {
            .contenido-portada h1 {
                font-size: 36px;
            }

            .contenido-portada p {
                font-size: 18px;
            }

            .panel-info {
                grid-template-columns: 1fr;
            }

            .input-barrio,
            .boton {
                width: 100%;
            }
        }
    </style>
</head>

<body>

    <!-- PRIMERA PARTE: SOLO PLANETA + BUSCADOR -->
    <section class="portada" id="inicio">
        <video class="video-fondo" autoplay loop muted playsinline>
            <source src="{{ url_for('static', filename='planeta.mp4') }}" type="video/mp4">
        </video>

        <div class="capa-oscura"></div>

        <div class="contenido-portada">
            <h1>Ruta de Recolección de Residuos</h1>

            <div class="panel-busqueda">
                <div class="titulo-buscar">BUSCAR BARRIO:</div>

                <input 
                    type="text" 
                    id="busqueda" 
                    class="input-barrio" 
                    placeholder=""
                >

                <button class="boton" onclick="mostrarMapa()">
                    INICIAR<br>RECORRIDO
                </button>

                <div class="mensaje" id="mensaje">
                    Escribe “Pedregal” para iniciar el recorrido.
                </div>
            </div>
        </div>
    </section>

    <!-- SEGUNDA PARTE: MAPA OCULTO HASTA PRESIONAR EL BOTÓN -->
    <section class="zona-mapa" id="mapa">
        <h2>Ruta de Recolección - Barrio Pedregal</h2>
        <p>Recorrido aproximado: <strong>2,1 km</strong></p>

        <div class="contenedor-mapa">
            <img src="{{ url_for('static', filename='mapa.jpg') }}" class="mapa" alt="Mapa Barrio Pedregal">

            <svg class="ruta-svg" viewBox="0 0 100 100" preserveAspectRatio="none">

                <path id="rutaCamion"
                      d="M 88 8
                         L 88 30
                         L 88 50
                         L 88 78
                         L 72 78
                         L 72 92
                         L 55 92
                         L 35 92
                         L 10 92
                         L 10 74
                         L 30 74
                         L 30 58
                         L 48 58
                         L 48 42
                         L 66 42
                         L 66 14
                         L 54 14"
                      fill="none"
                      stroke="transparent"
                      stroke-width="0"/>

                <image href="{{ url_for('static', filename='camion.png') }}"
                       x="-8"
                       y="-5"
                       width="16"
                       height="9">
                    <animateMotion dur="22s" repeatCount="indefinite" rotate="0">
                        <mpath href="#rutaCamion"/>
                    </animateMotion>
                </image>

            </svg>
        </div>

        <div class="panel-info">
            <div class="info">🟢 Ruta del camión</div>
            <div class="info">🗑️ Tachos = nodos</div>
            <div class="info">🛣️ Calles = aristas</div>
            <div class="info">📏 Distancia: 2,1 km</div>
        </div>

        <a href="#inicio" class="volver">VOLVER AL INICIO</a>
    </section>

    <script>
        function mostrarMapa() {
            const texto = document.getElementById("busqueda").value.toLowerCase().trim();
            const mapa = document.getElementById("mapa");
            const mensaje = document.getElementById("mensaje");

            if (texto.includes("pedregal")) {
                mensaje.style.display = "none";
                mapa.style.display = "block";

                setTimeout(() => {
                    mapa.scrollIntoView({ behavior: "smooth" });
                }, 100);
            } else {
                mensaje.style.display = "block";
            }
        }
    </script>

</body>
</html>
""")


if __name__ == "__main__":
    app.run(debug=True)