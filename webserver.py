from tinyweb import webserver
import uasyncio

class website:
    """
    Creates a pico webserver ready for modules
    """    
    def __init__(self) -> None:
        self.app = webserver()

        # Index page
        @self.app.route('/')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """<!DOCTYPE html>
            <html>
                <head> <title>Pico-Power</title> </head>
                <body> <h1>Pico-Power: Relay control of 4 circuits up to 240v AC or 30v DC</h1>
                    <p>
            Use the following URL suffixes to drive functions on this Pico:
            <ul>
            <li>Relay control - <a href="relay">/relay</a></li>
            </p>
                </body>
            </html>\n
            """
            await response.send(html)

    def run(self) -> uasyncio.Loop:
        loop = self.app.run(host='0.0.0.0', port=80, loop_forever=False)
        return loop