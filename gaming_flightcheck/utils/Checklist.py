import os


class Checklist:

    def __init__(self):
        self.available_items_list = self._build_checklist_items_list()
        self.current_items_list = {}

    def add_item(self, item_level, item_name):

        assert item_level in self.available_items_list.keys()
        assert item_name in self.available_items_list[item_level]

        if item_level not in self.current_items_list.keys():
            self.current_items_list[item_level] = []

        self.current_items_list[item_level].append(item_name)

    def get_checklist_items_data(self):

        checklist_items_data = []

        for item_level in self.current_items_list.keys():
            for item_name in self.current_items_list[item_level]:

                item_title = self._get_item_title(item_level, item_name)

                checklist_items_data.append((item_level, item_title))

        return checklist_items_data

    @staticmethod
    def _build_checklist_items_list():

        available_items_list = {}

        checklist_pages_folder_path = Checklist._get_checklist_pages_folder_path()

        for item_level in ["INFO", "OK", "WARNING", "CRITICAL"]:

            available_items_list[item_level] = []

            level_folder_path = os.path.join(checklist_pages_folder_path, item_level)

            if not os.path.isdir(level_folder_path):
                continue

            for item_name in os.listdir(level_folder_path):
                available_items_list[item_level].append(item_name)

        return available_items_list

    @staticmethod
    def _get_checklist_pages_folder_path():
        root_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        checklist_pages_folder_path = os.path.join(root_folder_path, "data", "checklist_items_pages")
        return checklist_pages_folder_path

    @staticmethod
    def _get_item_title(item_level, item_name):

        checklist_pages_folder_path = Checklist._get_checklist_pages_folder_path()
        item_path = os.path.join(checklist_pages_folder_path, item_level, item_name)
        title_path = os.path.join(item_path, "title.txt")

        with open(title_path, "r") as f:
            title = f.read().strip()

        return title
