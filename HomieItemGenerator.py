
class HomieProperty:

    def __init__(self, property_name, property_type, settable=False, readable=True):
        self.property_name = property_name
        self.property_type = property_type
        self.settable = settable
        self.readable = readable
        pass


class HomieItem:

    def __init__(self, base_topic, device_id):
        self.base_topic = base_topic
        self.device_id = device_id
        pass


class HomieItemGenerator:

    def __init__(self):
        pass



item = HomieItem("Test1/Test2/")

print(item)

