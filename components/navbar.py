import streamlit as st
import streamlit.components.v1 as components

def navbar():
    # HTML + CSS + JS
    navbar_html = """
    <style>
        /* --- Conteneur principal --- */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #262730;
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.4);
        }

        /* --- Liens de navigation --- */
        .nav-links {
            display: flex;
            gap: 25px;
        }
        .nav-links a {
            text-decoration: none;
            color: white;
            font-weight: 500;
            font-size: 16px;
            transition: color 0.2s ease-in-out;
        }
        .nav-links a:hover {
            color: #00c3ff;
        }

        /* --- Horloge --- */
        .clock {
            font-size: 18px;
            font-weight: bold;
            color: white;
        }

        /* --- Décalage du contenu Streamlit sous la navbar --- */
        .stApp {
            margin-top: 70px;
        }
    </style>

    <div class="navbar">
        <div class="clock">🕒 <span id="clock">00:00:00</span></div>
        <div class="nav-links">
            <a href="?page=home">Accueil</a>
            <a href="?page=admin">Admin</a>
            <a href="?page=user">Utilisateur</a>
            <a href="?page=login">Connexion</a>
            <a href="?page=register">Inscription</a>
        </div>
    </div>

    <script>
        function updateClock() {
            var now = new Date();
            var h = now.getHours().toString().padStart(2, '0');
            var m = now.getMinutes().toString().padStart(2, '0');
            var s = now.getSeconds().toString().padStart(2, '0');
            document.getElementById("clock").innerText = h + ":" + m + ":" + s;
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """

    components.html(navbar_html, height=80)
