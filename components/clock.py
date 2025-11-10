import streamlit.components.v1 as components

def display_clock(color="white", size="22px", show_seconds=True, format_24h=True):
    clock_html = f"""
    <div style="font-size:{size}; font-weight:bold; color:{color}; margin-bottom:10px;">
        🕒 <span id="clock">00:00:00</span>
    </div>
    <script>
        function updateClock() {{
            var now = new Date();
            var h = now.getHours();
            var m = now.getMinutes();
            var s = now.getSeconds();

            if (!{str(format_24h).lower()}) {{
                var suffix = h >= 12 ? " PM" : " AM";
                h = h % 12 || 12;
            }} else {{
                var suffix = "";
            }}

            h = h.toString().padStart(2,'0');
            m = m.toString().padStart(2,'0');
            s = s.toString().padStart(2,'0');
            var time = h + ":" + m + ({'":" + s' if show_seconds else '""'}) + suffix;
            document.getElementById("clock").innerText = time;
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """
    components.html(clock_html, height=50)
