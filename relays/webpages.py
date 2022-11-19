from webserver import website

class relaysite:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, coresite: website) -> None:
        """
        Tinyweb server definitions for the relay board to extend the webserver passed.
        """
        # Relay page
        @coresite.app.route('/relay')
        async def index(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>Relay control</h1>                
                    <p>
                    There is not currently a web form feature available. Please refer to the <a href="/relay/api">API reference</a> for interacting with the rest API.
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)