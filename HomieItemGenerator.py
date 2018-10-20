
HOMIE_PROPERTIES = [
    {"property_name": "name",                "property_path": "$name",                            "value_type": "String",        "display_text": "Device Name [%s]",                 "icon": "keyring",              "transform": "default"},
    {"property_name": "mac",                 "property_path": "$mac",                             "value_type": "String",        "display_text": "MAC [%s]",                         "icon": "text",                 "transform": "default"},
    {"property_name": "ip",                  "property_path": "$localip",                         "value_type": "String",        "display_text": "IP [%s]",                          "icon": "text",                 "transform": "default"},
    {"property_name": "signal",              "property_path": "$signal",                          "value_type": "Number",        "display_text": "Signal [%.1f%%]",                  "icon": "network",              "transform": "default"},
    {"property_name": "uptime",              "property_path": "$uptime",                          "value_type": "Number",        "display_text": "Uptime [JS(uptime.js):%s]",        "icon": "time",                 "transform": "default"},
    {"property_name": "fw_name",             "property_path": "$fw/name",                         "value_type": "String",        "display_text": "FW Name [%s]",                     "icon": "text",                 "transform": "default"},
    {"property_name": "fw_version",          "property_path": "$fw/version",                      "value_type": "String",        "display_text": "FW Version [%s]",                  "icon": "text",                 "transform": "default"},
    {"property_name": "current_config",      "property_path": "$implementation/config",           "value_type": "String",        "display_text": "Config JSON [%s]",                 "icon": "settings",             "transform": "default"},
    {"property_name": "ota_enabled",         "property_path": "$implementation/ota/enabled",      "value_type": "String",        "display_text": "OTA Enabled [%s]",                 "icon": "wind",                 "transform": "default"},
    {"property_name": "online",              "property_path": "$online",                          "value_type": "String",        "display_text": "Online [%s]",                      "icon": "poweroutlet_us",       "transform": "default"}
]


def build_mqtt_path(*elements):
    mqtt_path = ""
    element_length = len(elements) - 1
    for index, element in enumerate(elements):
        mqtt_path += element
        if index < element_length and not element.endswith('/'):
            mqtt_path += "/"
    return mqtt_path


def build_name(*elements):
    return "_".join(elements)


class HomieishProperty:

    def __init__(self, property_name, root_name, property_path, root_path, value_type,
                 group_name, display_text, icon, transform="default", settable=False, readable=True):
        self.property_name = property_name
        self.root_name = root_path
        self.name = build_name(root_name, property_name)
        self.property_path = property_path
        self.root_path = root_path
        self.value_type = value_type
        self.group_name = group_name
        self.display_text = display_text
        self.icon = icon
        self.transform = transform
        self.settable = settable
        self.readable = readable
        self.path = build_mqtt_path(root_path, property_path)


class HomieishNode:

    def __init__(self, node_name, root_name, node_path, root_path, node_group_name):
        self.node_name = node_name
        self.root_name = root_name
        self.name = build_name(root_name, node_name)
        self.node_path = node_path
        self.root_path = root_path
        self.group_name = node_group_name
        self.group_name = build_name(node_group_name, node_name, "Node")
        self.path = build_mqtt_path(root_path, node_path)
        self.node_properties = []

    def add_property(self, **kwargs):
        homie_property = HomieishProperty(
            **kwargs, root_name=self.name, root_path=self.path, group_name=self.group_name)
        self.node_properties.append(homie_property)
        return homie_property

    def add_properties(self, *properties):
        for homie_property in properties:
            self.add_property(**homie_property)
        return self.node_properties

    def node_property(self, property_name):
        for homie_property in self.node_properties:
            if homie_property.property_name == property_name:
                return homie_property


class HomieishItem:

    def __init__(self, name, root_path, device_id):
        self.name = name
        self.group_name = "g" + name
        self.settings_group_name = build_name(self.group_name, "Item", "Properties")
        self.base_path = root_path
        self.device_id = device_id
        self.path = build_mqtt_path(root_path, device_id)
        self.item_nodes = []
        self._generate_device_properties()

    def _generate_device_properties(self):
        self.item_properties = []
        for property_dict in HOMIE_PROPERTIES.copy():
            self.item_properties.append(HomieishProperty(
                **property_dict, root_name=self.name, root_path=self.path, group_name=self.settings_group_name))

    def add_node(self, **kwargs):
        homie_node = HomieishNode(
            **kwargs, root_name=self.name, root_path=self.path, node_group_name=self.group_name)
        self.item_nodes.append(homie_node)
        return homie_node

    def item_node(self, name):
        for node in self.item_nodes:
            if node.node_name == name:
                return node

    def item_property(self, name):
        for item_property in self.item_properties:
            if item_property.property_name == name:
                return item_property


class HomieOpenhabItemGenerator:

    def __init__(self, broker_name):
        self.broker_name = broker_name
        self.homie_items = []

    def add_item(self, **kwargs):
        homie_item = HomieishItem(**kwargs)
        self.homie_items.append(homie_item)
        return homie_item

    def homie_item(self, name):
        for homie_item in self.homie_items:
            if homie_item.name == name:
                return homie_item


item = HomieishItem("CoolItem", "Test1/Test2/", "me")
item.add_node(node_name="nodeName", node_path="nodePath").add_properties(
    {"property_name": "newProperty", "property_path": "$propertyPath", "value_type": "StringType", "display_text": "testTest", "icon": "temperatore"},
    {"property_name": "newPropertyTwo", "property_path": "propertyPathTwo", "value_type": "StringTypeTwo", "display_text": "testTest", "icon": "temperatore"},
)

print(item.item_node("nodeName").node_property("newProperty").icon)
print(item.item_property("signal").name)

