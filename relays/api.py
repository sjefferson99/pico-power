from webserver import website
from hardware import relay_board
from json import dumps

class relayapi:
    """
    Creates a pico webserver ready for modules
    """  
    def __init__(self, coresite: website) -> None:
        """
        Tinyweb server API definitions for the relay board to extend the webserver passed.
        """
        # Relay API page
        @coresite.app.route('/relay/api')
        async def api(request, response):
            # Start HTTP response with content-type text/html
            await response.start_html()
            # Send actual HTML page
            html = """
            <html>
                <body>
                    <h1>Relay control API definition</h1>                
                    <p>
                    Use the following endpoints to drive the pico relays with appropriate data:
                    <ul>
                    <li>List relays and names - GET /relay/api/relays/</li>
                    <li>Switch or toggle relay - PUT /relay/api/relays/{relay number (1-4)}</li>
                    </ul>
                    Data:
                    <ul>
                    <li>type="switch"/"toggle" (Switch=Switch to given value, toggle=Switch intiial value and switch to opposite value after 500ms)</li>
                    <li>value="0"/"1" (0=Common connected to NC, 1=Common connected to NO)</li>
                    </ul>
                    </p>
                </body>
            </html>\n
            """
            await response.send(html)

        coresite.app.add_resource(relaylist, '/relay/api/relays')
        coresite.app.add_resource(relay, '/relay/api/relays/<relayid>')

class relaylist():

    def get(self, data):
        """Return list of all relays"""
        hardware = relay_board()
        return dumps(hardware.list_relays())

class relay():
    def put(self, data, relayid):
        """Switch relay"""
        value = data["value"]
        type = data["type"]
        print("Received API call - relayid {}, type: {}, value: {}".format(relayid, type, value))
        hardware = relay_board()
        if type == "switch":
            print("API call to switch")
            hardware.relay_switch(int(relayid), int(value))
            # Return message AND set HTTP response code to "200"
            return {'message': 'Switched'}, 200
        elif type == "toggle":
            print("API call to toggle")
            hardware.relay_toggle(int(relayid), 500, int(value))
            # Return message AND set HTTP response code to "200"
            return {'message': 'Toggled'}, 200
        else:
            print("Incorrect data provided to relays API")
            # Return message AND set HTTP response code to "200"
            return {'message': 'Error'}, 500
