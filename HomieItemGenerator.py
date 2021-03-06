
HOMIE_PROPERTIES = [
    {
        "property_name": "name",
        "property_path": "$name",
        "value_type": "String",
        "display_text": "Device Name [%s]",
        "icon": "keyring",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "mac",
        "property_path": "$mac",
        "value_type": "String",
        "display_text": "MAC [%s]",
        "icon": "text",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "ip",
        "property_path": "$localip",
        "value_type": "String",
        "display_text": "IP [%s]",
        "icon": "text",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "signal",
        "property_path": "$stats/signal",
        "value_type": "Number",
        "display_text": "Signal [%.1f%%]",
        "icon": "network",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "uptime",
        "property_path": "$stats/uptime",
        "value_type": "Number",
        "display_text": "Uptime [JS(uptime.js):%s]",
        "icon": "time",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "fw_name",
        "property_path": "$fw/name",
        "value_type": "String",
        "display_text": "FW Name [%s]",
        "icon": "text",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "fw_version",
        "property_path": "$fw/version",
        "value_type": "String",
        "display_text": "FW Version [%s]",
        "icon": "text",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "current_config",
        "property_path": "$implementation/config",
        "value_type": "String",
        "display_text": "Config JSON [%s]",
        "icon": "settings",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "ota_enabled",
        "property_path": "$implementation/ota/enabled",
        "value_type": "String",
        "display_text": "OTA Enabled [%s]",
        "icon": "wind",
        "transform": "default",
        "sitemap_type": "Text"
    },
    {
        "property_name": "state",
        "property_path": "$state",
        "value_type": "String",
        "display_text": "State [%s]",
        "icon": "poweroutlet_us",
        "transform": "default",
        "sitemap_type": "Text"
    }
]

PROPERTIES_SITEMAPPING = {
    "Device Details": [
        "name",
        "state",
        "uptime",
        "fw_name",
        "fw_version",
        "ota_enabled",
        "current_config"
    ],
    "Network": [
        "ip",
        "signal",
        "mac"
    ]
}


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


def build_out_header(header):
    header_length = 120
    current_header_length = len(header)
    if current_header_length >= header_length:
        return header
    for _ in range(header_length - current_header_length):
        header += "-"
    return header


class HomieHabProperty:

    def __init__(self, property_name, root_name, property_path, root_path, value_type, display_text,
                 additional_groups=None, icon="none", transform="default", sitemap_type="Text", sitemap_properties="",
                 settable=False, readable=True):
        if additional_groups is None:
            additional_groups = []
        self.property_name = property_name
        self.root_name = root_path
        self.name = build_name(root_name, property_name)
        self.property_path = property_path
        self.root_path = root_path
        self.value_type = value_type
        self.display_text = display_text
        self.additional_groups = additional_groups
        self.icon = icon
        self.transform = transform
        self.sitemap_type = sitemap_type
        self.sitemap_properties = sitemap_properties
        self.settable = settable
        self.readable = readable
        self.path = build_mqtt_path(root_path, property_path)


class HomieHabNode:

    def __init__(self, node_name, root_name, node_path, root_path, node_group_name):
        self.node_name = node_name
        self.root_name = root_name
        self.name = build_name(root_name, node_name)
        self.node_path = node_path
        self.root_path = root_path
        self.node_group_name = node_group_name
        self.group_name = build_name(node_group_name, node_name)
        self.path = build_mqtt_path(root_path, node_path)
        self.node_properties = []

    def add_property(self, **kwargs):
        homie_property = HomieHabProperty(
            **kwargs, root_name=self.name, root_path=self.path)
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


class HomieHabItem:

    def __init__(self, location_name, device_id, root_path="homie"):
        self.location_name = location_name
        self.device_id = device_id
        self.name = build_name(location_name, device_id)
        self.location_group_name = build_name("g", location_name)
        self.group_name = build_name(self.location_group_name, device_id)
        self.settings_group_name = build_name(self.group_name, "properties")
        self.root_path = root_path
        self.path = build_mqtt_path(root_path, location_name, device_id.lower())
        self.item_nodes = []
        self._generate_device_properties()

    def _generate_device_properties(self):
        self.item_properties = []
        for property_dict in HOMIE_PROPERTIES.copy():
            self.item_properties.append(HomieHabProperty(
                **property_dict, root_name=self.name, root_path=self.path))

    def add_node(self, **kwargs):
        homie_node = HomieHabNode(
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


class HomieHabItemGenerator:

    LOCATIONS_FILE = "Homie_Locations.items"

    def __init__(self, broker_name, homie_items):
        self.broker_name = broker_name
        self.homie_items = homie_items
        self.generated_homie_items = None

    def generate_items(self):
        self.generated_homie_items = []
        for homie_item in self.homie_items:
            self.generated_homie_items.append({
                "item": homie_item,
                "item_header": self.generate_item_header(homie_item),
                "item_groups_header": self.generate_groups_header(homie_item),
                "item_groups": self.generate_item_groups(homie_item),
                "item_properties_header": self.generate_item_properties_header(homie_item),
                "item_properties": self.generate_item_properties(homie_item),
                "item_nodes": self.generate_item_nodes(homie_item)
            })
        return self.generated_homie_items

    def generate_item_groups(self, homie_item):
        groups = list()
        main_group_string = self.generate_item_group(homie_item.group_name)
        main_group_string += " (%s)" % homie_item.location_group_name
        groups.append(main_group_string)
        groups.append(self.generate_item_group(homie_item.settings_group_name))
        for node in homie_item.item_nodes:
            groups.append(self.generate_item_group(node.group_name))
        return groups

    def generate_item_properties(self, homie_item):
        item_properties = []
        for item_property in homie_item.item_properties:
            item_properties.append(
                self.generate_item(item_property, homie_item.group_name, homie_item.settings_group_name))
        return item_properties

    def generate_item_nodes(self, homie_item):
        item_properties = []
        for item_node in homie_item.item_nodes:
            item_property = dict()
            item_property["node_header"] = self.generate_node_header(item_node)
            item_property["node_properties"] = []
            for node_property in item_node.node_properties:
                item_property["node_properties"].append(
                    self.generate_item(node_property, homie_item.group_name, item_node.group_name))
            item_properties.append(item_property)
        return item_properties

    def generate_item_group(self, name):
        return "Group " + name

    def generate_item(self, item_property, *groups):
        property_data = list()
        property_data.append(item_property.value_type)
        property_data.append(item_property.name)
        property_data.append("\"" + item_property.display_text + "\"")
        property_data.append("<" + item_property.icon + ">")
        property_data.append("(" + ", ".join(list(groups) + item_property.additional_groups) + ")")
        mqtt_string = "{ autoupdate=\"false\", mqtt=\""
        mqtt_parts = []
        if item_property.readable:
            mqtt_parts.append("<[%s:%s:state:%s]" % (self.broker_name, item_property.path, item_property.transform))
        if item_property.settable:
            mqtt_parts.append(">[%s:%s:command:*:%s]" % (
                self.broker_name, item_property.path + "/set", item_property.transform))
        mqtt_string += ", ".join(mqtt_parts)
        mqtt_string += "\" }"
        property_data.append(mqtt_string)
        return " ".join(property_data)

    def generate_node_header(self, item_node):
        top_string = "// ---- Node Properties ----"
        top_string = build_out_header(top_string)
        bottom_string = "// ---- Node: %s --- Path: %s ----" % (
            item_node.node_name, item_node.node_path)
        bottom_string = build_out_header(bottom_string)
        return "\n".join(["", top_string, bottom_string])

    def generate_groups_header(self, _):
        groups_header = "// ---- Group Definitions ----"
        groups_header = build_out_header(groups_header)
        return "\n\n" + groups_header

    def generate_item_properties_header(self, _):
        property_item_header = "// ---- Item Properties ----"
        property_item_header = build_out_header(property_item_header)
        return "\n\n" + property_item_header

    def generate_item_header(self, homie_item):
        top_string = "// ---- AUTOGENERATED HOMIE ITEM MAP FILE ----"
        top_string = build_out_header(top_string)
        middle_string = "// ---- Broker: %s --- Location: %s ----" % (self.broker_name, homie_item.location_name)
        middle_string = build_out_header(middle_string)
        bottom_string = "// ---- DeviceID: %s ----" % homie_item.device_id
        bottom_string = build_out_header(bottom_string)
        item_header = "\n".join([top_string, middle_string, bottom_string])
        return item_header

    def save_item_locations_file(self):
        found_locations = []
        for homie_item in self.homie_items:
            if homie_item.location_group_name not in found_locations:
                found_locations.append(homie_item.location_group_name)
        with open(HomieHabItemGenerator.LOCATIONS_FILE, "w") as file:
            file.write("// ---- AUTOGENERATED HOMIE LOCATIONS --------\n\n")
            for found_location in found_locations:
                file.write("Group " + found_location + "\n")
            file.write("\n")

    def save_item_files(self):
        for generated_item in self.generated_homie_items:
            file_lines = list()
            file_lines.append(generated_item["item_header"])
            file_lines.append(generated_item["item_groups_header"])
            for group in generated_item["item_groups"]:
                file_lines.append(group)
            file_lines.append(generated_item["item_properties_header"])
            for item_property in generated_item["item_properties"]:
                file_lines.append(item_property)
            for item_node in generated_item["item_nodes"]:
                file_lines.append(item_node["node_header"])
                for node_property in item_node["node_properties"]:
                    file_lines.append(node_property)
            with open(generated_item["item"].name + ".items", "w") as file:
                file.write("\n".join(file_lines))
                file.write("\n")

    def save_items(self):
        self.save_item_locations_file()
        self.save_item_files()


class HomieHabSitemapGenerator:

    def __init__(self, broker_name, homie_items):
        self.broker_name = broker_name
        self.homie_items = homie_items
        self.generated_homie_sitemaps = None

    def generate_sitemaps(self):
        self.generated_homie_sitemaps = []
        for homie_item in self.homie_items:
            self.generated_homie_sitemaps.append({
                "item": homie_item,
                "sitemap_header": self.generate_sitemap_header(homie_item),
                "sitemap_open": self.generate_sitemap_open(homie_item),
                "sitemap_properties_header": self.generate_sitemap_properties_header(homie_item),
                "sitemap_properties": self.generate_sitemap_properties(homie_item),
                "sitemap_nodes": self.generate_sitemap_nodes(homie_item),
                "sitemap_close": self.generate_sitemap_close(homie_item)
            })
        return self.generated_homie_sitemaps

    def generate_sitemap_header(self, homie_item):
        top_string = "// ---- AUTOGENERATED HOMIE SITEMAP FILE ----"
        top_string = build_out_header(top_string)
        middle_string = "// ---- Broker: %s --- Location: %s ----" % (self.broker_name, homie_item.location_name)
        middle_string = build_out_header(middle_string)
        bottom_string = "// ---- DeviceID: %s ----" % homie_item.device_id
        bottom_string = build_out_header(bottom_string)
        item_header = "\n".join([top_string, middle_string, bottom_string])
        return item_header

    def generate_sitemap_open(self, homie_item):
        return "sitemap %s label=\"%s\" {" % (
            homie_item.name,
            "%s %s Item" % (homie_item.location_name, homie_item.device_id))

    def generate_sitemap_close(self, _):
        return "}"

    def generate_sitemap_properties_header(self, _):
        property_item_header = "\t// ---- Item Properties ----"
        property_item_header = build_out_header(property_item_header)
        return property_item_header

    def generate_frame_open(self, name):
        return "\tFrame label=\"%s\" {" % name

    def generate_frame_close(self):
        return "\t}"

    def generate_item_map(self, homie_property):
        return "\t\t%s item=%s %s" % (
            homie_property.sitemap_type, homie_property.name, homie_property.sitemap_properties)

    def generate_sitemap_properties(self, homie_item):
        item_properties = []
        for frame, property_names in PROPERTIES_SITEMAPPING.items():
            property_sitemap = dict()
            property_sitemap["frame_open"] = self.generate_frame_open(frame)
            property_sitemap["properties"] = []
            property_sitemap["frame_close"] = self.generate_frame_close()
            for property_name in property_names:
                property_sitemap["properties"].append(
                    self.generate_item_map(homie_item.item_property(property_name)))
            item_properties.append(property_sitemap)
        return item_properties

    def generate_node_header(self, item_node):
        string = "\t// ---- Node: %s --- Path: %s ----" % (item_node.node_name, item_node.node_path)
        return build_out_header(string)

    def generate_sitemap_nodes(self, homie_item):
        item_properties = []
        for item_node in homie_item.item_nodes:
            item_property = dict()
            item_property["node_header"] = self.generate_node_header(item_node)
            item_property["node_frame_open"] = self.generate_frame_open(item_node.node_name)
            item_property["node_properties"] = []
            item_property["node_frame_close"] = self.generate_frame_close()
            for node_property in item_node.node_properties:
                item_property["node_properties"].append(
                    self.generate_item_map(node_property))
            item_properties.append(item_property)
        return item_properties

    def save_sitemaps(self):
        for generated_sitemap in self.generated_homie_sitemaps:
            file_lines = list()
            file_lines.append(generated_sitemap["sitemap_header"])
            file_lines.append(generated_sitemap["sitemap_open"])
            file_lines.append(generated_sitemap["sitemap_properties_header"])
            for item_frame in generated_sitemap["sitemap_properties"]:
                file_lines.append(item_frame["frame_open"])
                for item_property in item_frame["properties"]:
                    file_lines.append(item_property)
                file_lines.append(item_frame["frame_close"])
            for node_frame in generated_sitemap["sitemap_nodes"]:
                file_lines.append(node_frame["node_header"])
                file_lines.append(node_frame["node_frame_open"])
                for node_property in node_frame["node_properties"]:
                    file_lines.append(node_property)
                file_lines.append(node_frame["node_frame_close"])
            file_lines.append(generated_sitemap["sitemap_close"])
            with open(generated_sitemap["item"].name + ".sitemap", "w") as file:
                file.write("\n".join(file_lines))
                file.write("\n")


class HomieHabGenerator:

    def __init__(self, broker_name):
        self.broker_name = broker_name
        self.homie_items = []

    def add_item(self, **kwargs):
        homie_item = HomieHabItem(**kwargs)
        self.homie_items.append(homie_item)
        return homie_item

    def homie_item(self, name):
        for homie_item in self.homie_items:
            if homie_item.device_id == name:
                return homie_item

    def generate_items(self):
        item_generator = HomieHabItemGenerator(self.broker_name, self.homie_items)
        item_generator.generate_items()
        item_generator.save_items()

    def generate_sitemaps(self):
        sitemap_generator = HomieHabSitemapGenerator(self.broker_name, self.homie_items)
        sitemap_generator.generate_sitemaps()
        sitemap_generator.save_sitemaps()
