
from HomieItemGenerator import *

generator = HomieHabItemGenerator("AutomationServer")

#####################
#  Sandy DHT1 Item  #
#####################
sandy_dht1 = generator.add_item(
    location_name="Sandy",
    device_id="DHT1"
)
sandy_dht1_dht_node = sandy_dht1.add_node(
    node_name="DHT",
    node_path="sensor/dht"
)
sandy_dht1_dht_node.add_properties(
    {
        "property_name": "Humidity",
        "property_path": "humidity",
        "value_type": "Number",
        "display_text": "Humidity [%.1f%%]",
        "icon": "humidity"
    },
    {
        "property_name": "Temperature_F",
        "property_path": "temperature_f",
        "value_type": "Number",
        "display_text": "Temperature [%.1f °F]",
        "icon": "temperature"
    },
    {
        "property_name": "Temperature_F",
        "property_path": "temperature_f",
        "value_type": "Number",
        "display_text": "Temperature [%.1f °F]",
        "icon": "temperature"
    }
)


generator.generate_items()
generator.save_files()

